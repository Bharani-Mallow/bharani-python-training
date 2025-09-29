def main():
    print("Hello from roman_to_integer!")


def solve_problem(s):
    """
    Roman to Integer Problem

    Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
    Symbol       Value
    I             1
    V             5
    X             10
    L             50
    C             100
    D             500
    M             1000

    Roman numerals are usually written largest to smallest from left to right.
    However, special cases exist where subtraction is used:
    - I can be placed before V (5) and X (10) to make 4 and 9.
    - X can be placed before L (50) and C (100) to make 40 and 90.
    - C can be placed before D (500) and M (1000) to make 400 and 900.

    Given a roman numeral, convert it to an integer.

    Args:
        s: str - A string representing the Roman numeral

    Returns:
        int - The integer value of the Roman numeral

    Examples:
        s = "III" -> 3
        s = "LVIII" -> 58
        s = "MCMXCIV" -> 1994
    """
    # ================================
    # WRITE YOUR SOLUTION CODE BELOW
    # ================================
    roman_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    result = 0
    i=0
    while i < len(s):
        print(s[i], " ==> ", roman_map[s[i]])

        if i + 1 < len(s) and roman_map[s[i]] < roman_map[s[i + 1]]:
            print(s[i + 1], " ==> ", roman_map[s[i + 1]])
            result -= roman_map[s[i]]
            print("Subtraction case: ",result)
        else:
            result += roman_map[s[i]]
            print("Addition case: ",result)
        i += 1
    return result
    # ================================
    # END OF SOLUTION CODE
    # ================================


def run_sample_tests():
    # Sample Test Case 1
    sample_input_1 = "III"
    expected_output_1 = 3

    try:
        result_1 = solve_problem(sample_input_1)
        print("Your output: ", result_1)
        print("Expected output: ", expected_output_1)
        print("✅" if result_1 == expected_output_1 else "❌")
    except Exception as e:
        print("⚠️", e)

    # Sample Test Case 2
    sample_input_2 = "LVIII"
    expected_output_2 = 58

    try:
        result_2 = solve_problem(sample_input_2)
        print("Your output: ", result_2)
        print("Expected output: ", expected_output_2)
        print("✅" if result_2 == expected_output_2 else "❌")
    except Exception as e:
        print("⚠️", e)

    # Sample Test Case 3
    sample_input_3 = "MCMXCIV"
    expected_output_3 = 1994

    try:
        result_3 = solve_problem(sample_input_3)
        print("Your output: ", result_3)
        print("Expected output: ", expected_output_3)
        print("✅" if result_3 == expected_output_3 else "❌")
    except Exception as e:
        print("⚠️", e)


if __name__ == "__main__":
    main()
    run_sample_tests()
