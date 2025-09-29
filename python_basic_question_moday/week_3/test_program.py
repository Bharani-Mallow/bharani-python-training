import sys
import traceback
import time

# Import the solve_problem function from main.py
try:
    from main import solve_problem
except ImportError:
    print("Error: Could not import solve_problem from main.py")
    print("Make sure main.py exists and contains the solve_problem function")
    sys.exit(1)


class TestCase:
    """Represents a single test case for Roman to Integer problem"""

    def __init__(self, roman_numeral: str, expected_output: int, description: str = ""):
        self.roman_numeral = roman_numeral
        self.expected_output = expected_output
        self.description = description


class TestRunner:
    """Runs and manages test cases for Roman to Integer problem"""

    def __init__(self):
        self.test_cases = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def add_test_case(
        self, roman_numeral: str, expected_output: int, description: str = ""
    ):
        """Add a test case to the test suite"""
        self.test_cases.append(TestCase(roman_numeral, expected_output, description))

    def run_single_test(
        self, test_case: TestCase, test_number: int, show_details: bool = False
    ):
        """Run a single test case"""
        try:
            start_time = time.time()
            result = solve_problem(test_case.roman_numeral)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

            if result == test_case.expected_output:
                self.passed += 1
                if show_details:
                    print(f"✅ Test {test_number} ({execution_time:.2f}ms)")
                    print(f"  Input: {test_case.roman_numeral}")
                    print(f"  Expected: {test_case.expected_output}, Got: {result}")
            else:
                self.failed += 1
                print(f"❌ Test {test_number} ({execution_time:.2f}ms)")
                if test_case.description:
                    print(f"  Description: {test_case.description}")
                print(f"  Input: {test_case.roman_numeral}")
                print(f"  Expected: {test_case.expected_output}, Got: {result}")

        except Exception as e:
            self.errors += 1
            print(f"⚠️ Test {test_number} ERROR")
            if test_case.description:
                print(f"  Description: {test_case.description}")
            print(f"  Input: {test_case.roman_numeral}")
            print(f"  Error: {str(e)}")
            if show_details:
                print(f"  Traceback: {traceback.format_exc()}")

    def run_all_tests(self, show_details: bool = False, show_summary: bool = True):
        """Run all test cases"""
        print("Roman to Integer - Test Suite")
        print("=" * 50)

        if not self.test_cases:
            print("No test cases found!")
            return

        for i, test_case in enumerate(self.test_cases, 1):
            self.run_single_test(test_case, i, show_details)
            if i < len(self.test_cases):
                print()

        if show_summary:
            self.print_summary()

    def print_summary(self):
        """Print test execution summary"""
        total = len(self.test_cases)
        print("=" * 50)
        print("TEST SUMMARY")
        print("-" * 50)
        print(
            f"Total: {total} | Passed: {self.passed} | Failed: {self.failed} | Errors: {self.errors}"
        )

        if self.passed == total:
            print("✅ ALL TESTS PASSED!")
        elif self.failed > 0:
            print("❌ Some tests failed.")
        if self.errors > 0:
            print("⚠️ Some tests had errors.")

        print("=" * 50)


def create_test_cases():
    """
    Create comprehensive test cases for Roman to Integer problem.
    """
    test_runner = TestRunner()

    # Basic Test Cases
    test_runner.add_test_case(
        roman_numeral="I", expected_output=1, description="Single symbol I"
    )

    test_runner.add_test_case(
        roman_numeral="V", expected_output=5, description="Single symbol V"
    )

    test_runner.add_test_case(
        roman_numeral="X", expected_output=10, description="Single symbol X"
    )

    test_runner.add_test_case(
        roman_numeral="L", expected_output=50, description="Single symbol L"
    )

    test_runner.add_test_case(
        roman_numeral="C", expected_output=100, description="Single symbol C"
    )

    test_runner.add_test_case(
        roman_numeral="D", expected_output=500, description="Single symbol D"
    )

    test_runner.add_test_case(
        roman_numeral="M", expected_output=1000, description="Single symbol M"
    )

    # Additive cases
    test_runner.add_test_case(
        roman_numeral="II", expected_output=2, description="Simple addition II"
    )

    test_runner.add_test_case(
        roman_numeral="XXX", expected_output=30, description="Simple addition XXX"
    )

    test_runner.add_test_case(
        roman_numeral="MDCLXVI",
        expected_output=1666,
        description="All symbols in descending order",
    )

    # Subtractive cases
    test_runner.add_test_case(
        roman_numeral="IV", expected_output=4, description="Subtractive case IV"
    )

    test_runner.add_test_case(
        roman_numeral="IX", expected_output=9, description="Subtractive case IX"
    )

    test_runner.add_test_case(
        roman_numeral="XL", expected_output=40, description="Subtractive case XL"
    )

    test_runner.add_test_case(
        roman_numeral="XC", expected_output=90, description="Subtractive case XC"
    )

    test_runner.add_test_case(
        roman_numeral="CD", expected_output=400, description="Subtractive case CD"
    )

    test_runner.add_test_case(
        roman_numeral="CM", expected_output=900, description="Subtractive case CM"
    )

    # Complex cases with multiple subtractive notations
    test_runner.add_test_case(
        roman_numeral="XLIX", expected_output=49, description="Complex number 49 (XLIX)"
    )

    test_runner.add_test_case(
        roman_numeral="XCIX", expected_output=99, description="Complex number 99 (XCIX)"
    )

    test_runner.add_test_case(
        roman_numeral="CMXCIX",
        expected_output=999,
        description="Complex number 999 (CMXCIX)",
    )

    # Edge cases
    test_runner.add_test_case(
        roman_numeral="MMMCMXCIX",
        expected_output=3999,
        description="Maximum valid Roman numeral (3999)",
    )

    # Examples from problem statement
    test_runner.add_test_case(
        roman_numeral="III",
        expected_output=3,
        description="Example 1 from problem statement",
    )

    test_runner.add_test_case(
        roman_numeral="LVIII",
        expected_output=58,
        description="Example 2 from problem statement",
    )

    test_runner.add_test_case(
        roman_numeral="MCMXCIV",
        expected_output=1994,
        description="Example 3 from problem statement",
    )

    # More complex test cases with mixed additive and subtractive notations
    test_runner.add_test_case(
        roman_numeral="MMCDXXI",
        expected_output=2421,
        description="Complex number 2421 (MMCDXXI)",
    )

    test_runner.add_test_case(
        roman_numeral="MCMXLIV",
        expected_output=1944,
        description="Complex number 1944 (MCMXLIV)",
    )

    test_runner.add_test_case(
        roman_numeral="MMCMXCIX",
        expected_output=2999,
        description="Complex number 2999 (MMCMXCIX)",
    )

    test_runner.add_test_case(
        roman_numeral="CDXLIV",
        expected_output=444,
        description="Complex number 444 (CDXLIV)",
    )

    test_runner.add_test_case(
        roman_numeral="CDXCIX",
        expected_output=499,
        description="Complex number 499 (CDXCIX)",
    )

    # Test cases with consecutive subtractive patterns
    test_runner.add_test_case(
        roman_numeral="MCMIV",
        expected_output=1904,
        description="Complex number 1904 with consecutive subtractive patterns (MCMIV)",
    )

    test_runner.add_test_case(
        roman_numeral="MMCMXCIV",
        expected_output=2994,
        description="Complex number 2994 with multiple subtractive patterns (MMCMXCIV)",
    )

    # Tests covering all digit positions
    test_runner.add_test_case(
        roman_numeral="MMMCDLXXVI",
        expected_output=3476,
        description="Complex number 3476 covering thousands, hundreds, tens, ones (MMMCDLXXVI)",
    )

    test_runner.add_test_case(
        roman_numeral="MMDCCLXXXIV",
        expected_output=2784,
        description="Complex number 2784 with no subtractive notation (MMDCCLXXXIV)",
    )

    # Years that might be commonly represented in Roman numerals
    test_runner.add_test_case(
        roman_numeral="MCMLXXXIV",
        expected_output=1984,
        description="Year 1984 (MCMLXXXIV)",
    )

    test_runner.add_test_case(
        roman_numeral="MMXXIII", expected_output=2023, description="Year 2023 (MMXXIII)"
    )

    # Test case with repeating patterns
    test_runner.add_test_case(
        roman_numeral="MXMIX",
        expected_output=1999,
        description="Complex number 1999 with repeating X-based patterns (MXMIX)",
    )

    return test_runner


def main():
    """Main function to run the comprehensive test suite"""
    print("Roman to Integer Testing System")
    print()

    # Create test cases
    test_runner = create_test_cases()

    # Parse command line arguments
    show_details = "--details" in sys.argv or "-d" in sys.argv

    # Run tests
    test_runner.run_all_tests(show_details=show_details, show_summary=True)


if __name__ == "__main__":
    main()
