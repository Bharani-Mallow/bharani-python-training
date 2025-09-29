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
    print("n ====> ", n)
    print("m ====> ", m)
    if grid[0][0] == 1:
        return -1
    if grid[n - 1][m - 1] == 1:
        return -1
    if n == 1 and m == 1:
        return 1
    
    step = 0
    current_position = grid[0][0]
    for i in range(n):
        current_row = i
        if i == current_position[0]:
            for j in range(m):
                if j == current_position[1]:
                    current_column = j
                    current_position = grid[current_row][current_column]
                    if grid[current_row+1][current_column+1] == 0:
                        step += 1
                        current_position = grid[current_row+1][current_column+1]
                    if grid[current_row][current_column+1] == 0:
                        step += 1
                        current_position = grid[current_row][current_column+1]
                    if grid[current_row+1][current_column] == 0:
                        step += 1
                        current_position = grid[current_row+1][current_column]
                        step += 1
    return step
    
    

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
