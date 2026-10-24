
import heapq

# Initial and goal states
start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)


# Misplaced Tiles heuristic
def misplaced(state):
    return sum(1 for i in range(9)
               if state[i] != 0 and state[i] != goal[i])


# Generate valid next states
def successors(state):
    zero = state.index(0)
    moves = []

    for new in [zero - 3, zero + 3, zero - 1, zero + 1]:
        if 0 <= new < 9:
            if abs(new - zero) == 1 and zero // 3 != new // 3:
                continue

            s = list(state)
            s[zero], s[new] = s[new], s[zero]
            moves.append(tuple(s))

    return moves


# A* search algorithm
def astar(start, goal):
    open_list = [(misplaced(start), 0, start)]
    parent = {start: None}
    cost = {start: 0}
    closed = set()

    while open_list:
        f, g, state = heapq.heappop(open_list)

        if state in closed:
            continue

        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]

            return path[::-1]

        closed.add(state)

        for next_state in successors(state):
            new_g = g + 1

            if next_state not in cost or new_g < cost[next_state]:
                cost[next_state] = new_g
                parent[next_state] = state
                new_f = new_g + misplaced(next_state)

                heapq.heappush(
                    open_list, (new_f, new_g, next_state)
                )

    return None


# Display solution
path = astar(start, goal)

if path:
    print("Solution found!")
    print("Number of moves:", len(path) - 1)

    for step, state in enumerate(path):
        print("\nStep", step)
        for i in range(0, 9, 3):
            print(state[i:i + 3])
else:
    print("No solution found.")
