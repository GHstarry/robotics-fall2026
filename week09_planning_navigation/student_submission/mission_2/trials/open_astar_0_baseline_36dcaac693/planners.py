"""Mission 1: BFS, DFS, IDDFS and A* on a four-connected occupancy grid.

How the pieces fit together
---------------------------
Every planner receives ``ctx`` (a SearchContext). The grid is never turned into
an explicit graph. Instead the graph is *implicit*:

* a node is a free cell ``(row, column)``
* its edges lead to the free neighbours returned by ``ctx.expand(cell, n)``
* every edge costs 1 (one grid step)

``ctx.expand(cell, frontier_size)`` does three jobs at once:
  1. returns the legal neighbours in a fixed order (right, up, left, down),
  2. counts one expansion for the metrics table,
  3. records the frontier size so the guide can report the peak frontier.
It raises TimeoutError when the expansion budget runs out. We deliberately do
NOT catch that, so the runner can honestly report ``resource_limit``.

Shared conventions used by all four functions
---------------------------------------------
* Goal test happens when a cell is *removed* from the frontier, before it is
  expanded. Reaching the goal therefore never costs an extra expansion.
* ``frontier_size`` passed to ctx.expand is ``len(frontier) + 1``: the cells
  still waiting, plus the current cell we just removed. This matches the hint
  in the starter BFS docstring and the guide's teaching animations.
* Paths are rebuilt by following ``parent`` links backwards from the goal
  (``reconstruct``), or, for IDDFS, carried along with each stack entry.
* If the start or goal is occupied there is no legal path, so we return [].
  If the start already is the goal we return ``[start]`` with zero moves and
  no expansion.
"""
from collections import deque
from heapq import heappush, heappop
from planning.core import reconstruct


def _is_free(grid, cell):
    """True if ``cell`` is inside the grid and not an obstacle (0 = free)."""
    r, c = cell
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and not grid[r][c]


def _trivial_result(ctx):
    """Handle the two special cases every planner shares.

    Returns a finished answer (a list) when the search does not need to run,
    or None when the caller should go ahead and search.
    """
    if not _is_free(ctx.grid, ctx.start) or not _is_free(ctx.grid, ctx.goal):
        return []                 # an occupied endpoint can never be on a path
    if ctx.start == ctx.goal:
        return [ctx.start]        # already there: one cell, zero moves
    return None


# ---------------------------------------------------------------------------
# Breadth-first search
# ---------------------------------------------------------------------------
def bfs(ctx):
    """Explore in rings of increasing step count using a FIFO queue.

    Because every edge costs 1 and the queue is first-in-first-out, all cells
    that are k steps from the start are removed before any cell that is k+1
    steps away. The first time the goal is removed, it was reached by a path
    with the fewest possible steps, so BFS is optimal on this unit-cost grid.

    ``parent`` does double duty: it stores how we reached each cell (for path
    reconstruction) and it is the "discovered" set. A cell is marked the moment
    it is *enqueued*, so it can never be added to the queue twice.
    """
    done = _trivial_result(ctx)
    if done is not None:
        return done

    frontier = deque([ctx.start])          # FIFO queue of cells to visit
    parent = {ctx.start: None}             # discovered cells -> predecessor

    while frontier:
        current = frontier.popleft()       # oldest cell = fewest steps
        if current == ctx.goal:
            return reconstruct(parent, current)

        # +1 counts the current cell, which we just removed from the queue.
        for nxt in ctx.expand(current, len(frontier) + 1):
            if nxt not in parent:          # first discovery is the shortest
                parent[nxt] = current
                frontier.append(nxt)

    return []                              # queue empty: goal unreachable


# ---------------------------------------------------------------------------
# Depth-first search
# ---------------------------------------------------------------------------
def dfs(ctx):
    """Dive down one branch as far as possible using a LIFO stack.

    The only structural change from BFS is ``pop()`` from the end of a list
    instead of ``popleft()``: the newest cell is explored next, so the search
    keeps going deeper before it backtracks.

    Neighbours are pushed in *reverse* order so that the first neighbour the
    context supplies ends up on top of the stack and is explored first. That
    keeps the supplied neighbour order (right, up, left, down).

    Cells are marked as discovered when pushed (via ``parent``), which stops
    cycles and duplicate stack entries. The price is that DFS returns *a*
    valid path, usually not the shortest one: the first route that reaches a
    cell claims it, even if a shorter route to that cell exists.
    """
    done = _trivial_result(ctx)
    if done is not None:
        return done

    frontier = [ctx.start]                 # Python list used as a LIFO stack
    parent = {ctx.start: None}

    while frontier:
        current = frontier.pop()           # newest cell = deepest branch
        if current == ctx.goal:
            return reconstruct(parent, current)

        neighbours = ctx.expand(current, len(frontier) + 1)
        for nxt in reversed(neighbours):   # reversed so neighbours[0] is on top
            if nxt not in parent:
                parent[nxt] = current
                frontier.append(nxt)

    return []


# ---------------------------------------------------------------------------
# Iterative deepening depth-first search
# ---------------------------------------------------------------------------
def iddfs(ctx):
    """Repeat a depth-limited DFS with limits 0, 1, 2, ... until success.

    Idea: DFS uses little memory but is not optimal. BFS is optimal but keeps a
    large frontier. IDDFS gets BFS's shortest-step guarantee with DFS-sized
    memory by running DFS that is *not allowed* to go deeper than ``limit``
    steps, and raising the limit by one each round. The first round that finds
    the goal finds it at the smallest possible depth.

    Rules from the assignment, and how they are met:
    * No global visited set across rounds. Each round starts fresh, and inside
      a round we only refuse to revisit cells that are on the *current path*
      (``nxt not in path``). That prevents walking in circles while still
      allowing a cell to be reached by a different branch later.
    * Expansions are counted again every round, because the work really is
      repeated. That is why IDDFS's expansion count is much larger than BFS's.
    * Exhaustive failure: if a whole round finishes without ever being stopped
      by the depth limit (``cutoff`` stays False), then every reachable path
      was explored completely. A larger limit cannot find anything new, so we
      return [] instead of looping forever.
    * Budget exceptions from ctx.expand are not caught.
    """
    done = _trivial_result(ctx)
    if done is not None:
        return done

    limit = 0
    while True:
        # Each stack entry: (cell, path from start to that cell, steps left).
        # Carrying the path lets us check for cycles and return it directly.
        stack = [(ctx.start, (ctx.start,), limit)]
        cutoff = False                     # did the limit stop any branch?

        while stack:
            current, path, steps_left = stack.pop()
            if current == ctx.goal:
                return list(path)

            # Neighbours not already on this path (cycle prevention).
            successors = [p for p in ctx.expand(current, len(stack) + 1)
                          if p not in path]

            if steps_left > 0:
                # Reverse so the first supplied neighbour is popped first.
                for nxt in reversed(successors):
                    stack.append((nxt, path + (nxt,), steps_left - 1))
            elif successors:
                # We are at the depth limit but could have gone further.
                # A deeper round might still reach the goal.
                cutoff = True

        if not cutoff:
            return []                      # explored everything: unreachable
        limit += 1


# ---------------------------------------------------------------------------
# A* search
# ---------------------------------------------------------------------------
def astar(ctx):
    """Best-first search ordered by f = g + h.

    * g(n): exact steps taken from the start to n so far.
    * h(n): ``ctx.heuristic(n)``, the Manhattan distance |dr| + |dc| to the
      goal. On a 4-connected grid with unit steps it never overestimates the
      true remaining cost (admissible) and never drops by more than 1 per step
      (consistent). Those properties guarantee the first time the goal is
      removed from the heap, its g is the shortest possible path length.

    Compared with BFS, A* still finds a shortest path, but the heuristic pulls
    the search toward the goal, so it usually expands far fewer cells.

    Python's heapq cannot lower the priority of an item already in the heap.
    Instead, when we find a cheaper route to a cell we push a *new* entry and
    leave the old one behind. When an old (outdated) entry is popped later, its
    g no longer matches ``best_g`` and it is skipped. ``in_frontier`` tracks
    which cells have a live entry, so the frontier size we report counts real
    waiting cells, not stale heap entries.
    """
    done = _trivial_result(ctx)
    if done is not None:
        return done

    start, goal = ctx.start, ctx.goal
    best_g = {start: 0}                    # cheapest known steps to each cell
    parent = {start: None}
    closed = set()                         # cells already expanded
    in_frontier = {start}                  # cells with a live heap entry
    counter = 0                            # tie-breaker: first pushed wins
    # Heap entries: (f, g, counter, cell). Ties on f prefer smaller g, then
    # insertion order, so the result is deterministic.
    heap = [(ctx.heuristic(start), 0, counter, start)]

    while heap:
        _, g, _, current = heappop(heap)
        if current in closed or g != best_g[current]:
            continue                       # outdated entry: a better one won
        in_frontier.discard(current)

        if current == goal:                # stop when the goal is *removed*
            return reconstruct(parent, current)
        closed.add(current)

        for nxt in ctx.expand(current, len(in_frontier) + 1):
            candidate = g + 1              # every edge costs 1
            if candidate < best_g.get(nxt, float('inf')):
                best_g[nxt] = candidate
                parent[nxt] = current
                counter += 1
                heappush(heap, (candidate + ctx.heuristic(nxt), candidate,
                                counter, nxt))
                in_frontier.add(nxt)

    return []
