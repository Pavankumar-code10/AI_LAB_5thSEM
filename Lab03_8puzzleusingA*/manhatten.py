
import heapq

start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


# Manhattan Distance heuristic
def h(state):
    distance = 0

    for i in range(9):
        tile = state[i]

        if tile != 0:
            goal_index = goal.index(tile)

            row = i // 3
            col = i % 3
            goal_row = goal_index // 3
            goal_col = goal_index % 3

            distance += abs(row - goal_row)
            distance += abs(col - goal_col)

    return distance


# Print the puzzle board
def show(state):
    for i in range(0, 9, 3):
        print(" ".join("_" if x == 0 else str(x)
                       for x in state[i:i + 3]))


# Generate valid successor states
def successors(state):
    zero = state.index(0)
    result = []

    moves = [
        (zero - 3, "UP"),
        (zero + 3, "DOWN"),
        (zero - 1, "LEFT"),
        (zero + 1, "RIGHT")
    ]

    for new, move in moves:
        if not 0 <= new < 9:
            continue

        # Prevent left-right wrapping
        if abs(new - zero) == 1 and zero // 3 != new // 3:
            continue

        s = list(state)
        s[zero], s[new] = s[new], s[zero]
        result.append((tuple(s), move))

    return result


# A* search algorithm
def astar(start, goal):
    # Entries: (f, g, state)
    open_list = [(h(start), 0, start)]
    parent = {start: None}
    cost = {start: 0}
    closed = set()
    step = 0

    while open_list:
        f, g, state = heapq.heappop(open_list)

        if state in closed:
            continue

        step += 1
        closed.add(state)

        print("\n" + "=" * 35)
        print("EXPANDED NODE", step)
        show(state)
        print("g(n) =", g)
        print("h(n) =", h(state))
        print("f(n) =", g + h(state))

        # Goal test
        if state == goal:
            print("\nGOAL FOUND!")

            path = []
            current = state

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()

            print("\nSOLUTION PATH:")

            for i, board in enumerate(path):
                print("\nStep", i)
                show(board)
                print("g(n) =", i)
                print("h(n) =", h(board))
                print("f(n) =", i + h(board))

            print("\nTotal moves =", len(path) - 1)
            return

        # Display and process successors
        print("\nSUCCESSORS:")

        for nxt, move in successors(state):
            new_g = g + 1
            new_h = h(nxt)
            new_f = new_g + new_h

            print("\nMove blank", move)
            show(nxt)
            print("g(n) =", new_g,
                  "h(n) =", new_h,
                  "f(n) =", new_f)

            if nxt not in cost or new_g < cost[nxt]:
                cost[nxt] = new_g
                parent[nxt] = state
                heapq.heappush(
                    open_list, (new_f, new_g, nxt)
                )

    print("No solution found.")


astar(start, goal)
