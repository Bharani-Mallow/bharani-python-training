from collections import deque


def main():
    print("Hello from shortest_path_binary_matrix!")


def solve_problem(grid):
    """
    Shortest Path in Binary Matrix Problem

    Args:
        grid: List[List[int]] - binary matrix of 0s (open) and 1s (blocked)

    Returns:
        int - length of the shortest clear path, or -1 if no path exists
    """

    # ================================
    # WRITE YOUR SOLUTION CODE BELOW
    # ================================
    print("grid ====> ", grid)

    n = len(grid)
    m = len(grid[0])

    if grid[0][0] == 1:
        return -1
    if grid[n - 1][m - 1] == 1:
        return -1
    if n == 1 and m == 1:
        return 1

    step = 1
    current_position = [0, 0]
    destination = [n - 1, m - 1]
    print("current_position ====> ", current_position)
    i, j = 0, 0
    while current_position != destination:
        if i + 1 < n and j + 1 < m and grid[i + 1][j + 1] == 0:
            current_position = [i + 1, j + 1]
            i, j = i + 1, j + 1
            step += 1

        elif i < n and j + 1 < m and grid[i][j + 1] == 0:
            current_position = [i, j + 1]
            i, j = i, j + 1
            step += 1

        elif i + 1 < n and j < m and grid[i + 1][j] == 0:
            current_position = [i + 1, j]
            i, j = i + 1, j
            step += 1

        else:
            return -1

    return step

    # return step

    # ================================
    # END OF SOLUTION CODE
    # ================================


def run_sample_tests():
    print("Running Sample Test Cases...")
    print("=" * 60)

    test_cases = [
        ([[0, 1], [1, 0]], 2),
        ([[0, 0, 0], [1, 1, 0], [1, 1, 0]], 4),
        ([[1, 0, 0], [1, 1, 0], [1, 1, 0]], -1),
        ([[0]], 1),
        ([[1]], -1),
    ]

    for idx, (input_data, expected) in enumerate(test_cases, 1):
        try:
            print(f"Test {idx} ====>")
            result = solve_problem([row[:] for row in input_data])
            status = "✅" if result == expected else "❌"
            print(f"Result : {status} | Expected: {expected}, Got: {result}")
        except Exception as e:
            print(f"Test {idx}: ⚠️ Error occurred: {e}")

    print("=" * 60)


if __name__ == "__main__":
    main()
    print()
    run_sample_tests()
    print("\nTo run comprehensive tests, execute: python test_program.py")
