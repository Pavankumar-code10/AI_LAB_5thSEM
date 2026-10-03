def get_inversions(state):
    """Calculates the number of inversions in a state (ignoring blank space 0)."""
    tiles = [tile for tile in state if tile != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions


def is_solvable(start_state, goal_state):
    """
    Checks if moving from start_state to goal_state is solvable.
    For standard 3x3 8-puzzle, both states must have the same inversion parity (both even or both odd).
    """
    start_inversions = get_inversions(start_state)
    goal_inversions = get_inversions(goal_state)
    return (start_inversions % 2) == (goal_inversions % 2)


def get_neighbors(state):
    """Generates valid adjacent states by sliding the blank space (0)."""
    neighbors = []
    zero_idx = state.index(0)
    row, col = divmod(zero_idx, 3)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_zero_idx = r * 3 + c
            state_list = list(state)
            state_list[zero_idx], state_list[new_zero_idx] = (
                state_list[new_zero_idx],
                state_list[zero_idx],
            )
            neighbors.append(tuple(state_list))

    return neighbors


def solve_8_puzzle_dfs(start_state, goal_state, max_depth=30):
    """Solves the 8-puzzle using Depth-First Search with a depth limit."""
    stack = [(start_state, [start_state])]
    visited = {start_state}

    while stack:
        current, path = stack.pop()

        if current == goal_state:
            return path

        # Depth limit to prevent getting stuck in infinitely deep non-optimal paths
        if len(path) > max_depth:
            continue

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None


def get_user_state(state_name):
    """Prompts the user to enter a 3x3 board state."""
    print(f"\n--- Enter the {state_name.upper()} STATE ---")
    print("Use numbers 0-8 separated by spaces (0 represents the blank space):")

    board = []
    for i in range(3):
        while True:
            try:
                row_input = input(f"Enter Row {i+1} (3 numbers): ").strip().split()
                row_nums = [int(num) for num in row_input]
                if len(row_nums) != 3:
                    print("Error: Exactly 3 numbers required per row.")
                    continue
                board.extend(row_nums)
                break
            except ValueError:
                print("Error: Invalid input. Enter integers only.")

    if sorted(board) != list(range(9)):
        print("\nInvalid input! State must contain numbers 0 through 8 with no duplicates.")
        return None

    return tuple(board)


def print_board(state):
    """Prints a 3x3 grid cleanly."""
    for i in range(0, 9, 3):
        print(" ".join(str(x) if x != 0 else "_" for x in state[i:i+3]))
    print()


# Execution Block
if __name__ == "__main__":
    # Get Initial State from User
    start = get_user_state("initial")
    if start is None:
        exit()

    # Get Goal State from User
    goal = get_user_state("goal")
    if goal is None:
        exit()

    print("\n" + "=" * 40)
    print("INITIAL STATE:")
    print_board(start)

    print("GOAL STATE:")
    print_board(goal)
    print("=" * 40)

    # Check Solvability
    if not is_solvable(start, goal):
        print("Error: This goal state cannot be reached from the given initial state!")
        print("Reason: Mismatched inversion parity (one is even, the other is odd).")
    else:
        print("\nSearching for solution using Depth-First Search (DFS)...")
        path = solve_8_puzzle_dfs(start, goal)

        if path:
            print(f"\nGoal reached in {len(path) - 1} steps!\n")
            print("================ PATH TO GOAL ================\n")
            for step, state in enumerate(path):
                if step == 0:
                    print(f"Step {step} (Initial State):")
                elif step == len(path) - 1:
                    print(f"Step {step} (Goal State Reached):")
                else:
                    print(f"Step {step}:")
                print_board(state)
        else:
            print("\nNo solution found within the maximum depth limit.")
