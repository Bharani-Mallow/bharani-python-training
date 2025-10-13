import sys
import traceback
import time

try:
    from main import findMedianSortedArrays
except ImportError:
    print("Error: Could not import findMedianSortedArrays from main.py")
    print("Make sure main.py exists and contains the findMedianSortedArrays function")
    sys.exit(1)


class TestCase:
    def __init__(self, nums1, nums2, expected_output, description=""):
        self.nums1 = nums1
        self.nums2 = nums2
        self.expected_output = expected_output
        self.description = description


class TestRunner:
    def __init__(self):
        self.test_cases = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def add_test_case(self, nums1, nums2, expected_output, description=""):
        self.test_cases.append(TestCase(nums1, nums2, expected_output, description))

    def run_single_test(self, test_case, test_number, show_details=False):
        try:
            start_time = time.time()
            result = findMedianSortedArrays(test_case.nums1, test_case.nums2)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            if result == test_case.expected_output:
                self.passed += 1
                if show_details:
                    print(f"✅ Test {test_number} ({execution_time:.2f}ms)")
                    print(
                        f"  Input: nums1 = {test_case.nums1}, nums2 = {test_case.nums2}"
                    )
                    print(f"  Expected: {test_case.expected_output}, Got: {result}")
            else:
                self.failed += 1
                print(f"❌ Test {test_number} ({execution_time:.2f}ms)")
                if test_case.description:
                    print(f"  Description: {test_case.description}")
                print(f"  Input: nums1 = {test_case.nums1}, nums2 = {test_case.nums2}")
                print(f"  Expected: {test_case.expected_output}, Got: {result}")
        except Exception as e:
            self.errors += 1
            print(f"⚠️ Test {test_number} ERROR")
            if test_case.description:
                print(f"  Description: {test_case.description}")
            print(f"  Input: nums1 = {test_case.nums1}, nums2 = {test_case.nums2}")
            print(f"  Error: {str(e)}")
            if show_details:
                print(f"  Traceback: {traceback.format_exc()}")

    def run_all_tests(self, show_details=False, show_summary=True):
        print("Median of Two Sorted Arrays - Test Suite")
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
    test_runner = TestRunner()
    # Examples from problem statement
    test_runner.add_test_case([1, 3], [2], 2, "Example 1 from problem statement")
    test_runner.add_test_case([1, 2], [3, 4], 2.5, "Example 2 from problem statement")
    # Edge cases
    test_runner.add_test_case([], [1], 1, "Empty first array")
    test_runner.add_test_case([2], [], 2, "Empty second array")
    test_runner.add_test_case([1], [2], 1.5, "Both arrays single element")
    test_runner.add_test_case([1, 1, 1], [1, 1, 1], 1, "All elements same")
    test_runner.add_test_case([-5, -3, -1], [-2, 0, 2], -1.5, "Negative numbers")
    test_runner.add_test_case([1, 2, 3, 4, 5], [6], 3.5, "Different sizes")
    test_runner.add_test_case([1], [2, 3, 4, 5, 6], 3.5, "One large, one small")
    test_runner.add_test_case([-(10**6)], [10**6], 0, "Min/max values")
    test_runner.add_test_case([1, 4, 7], [2, 5, 8], 4.5, "Interleaved arrays")
    arr1 = list(range(1000))
    arr2 = list(range(1000, 2000))
    test_runner.add_test_case(arr1, arr2, 999.5, "Large arrays")
    return test_runner


def main():
    print("Median of Two Sorted Arrays Testing System")
    print()
    test_runner = create_test_cases()
    show_details = "--details" in sys.argv or "-d" in sys.argv
    test_runner.run_all_tests(show_details=show_details, show_summary=True)


if __name__ == "__main__":
    main()
