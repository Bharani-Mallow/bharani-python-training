import sys
import traceback
import time
from typing import Any, List


try:
    from main import solve_problem
except ImportError:
    print("Error: Could not import solve_problem from main.py")
    print("Make sure main.py exists and contains the solve_problem function")
    sys.exit(1)


class TestCase:
    """Represents a single test case for Shortest Path in Binary Matrix problem"""
    def __init__(self, grid: List[List[int]], expected_output: int, description: str = ""):
        self.grid = grid
        self.expected_output = expected_output
        self.description = description


class TestRunner:
    """Runs and manages test cases for Shortest Path in Binary Matrix problem"""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.passed = 0
        self.failed = 0
        self.errors = 0
    
    def add_test_case(self, grid: List[List[int]], expected_output: int, description: str = ""):
        """Add a test case to the test suite"""
        self.test_cases.append(TestCase(grid, expected_output, description))
    
    def run_single_test(self, test_case: TestCase, test_number: int, show_details: bool = False):
        """Run a single test case"""
        try:
            start_time = time.time()
            result = solve_problem([row[:] for row in test_case.grid])  # deep copy to avoid mutation
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            
            if result == test_case.expected_output:
                self.passed += 1
                status = "PASS"
                if show_details:
                    print(f"✓ Test {test_number}: {status} ({execution_time:.2f}ms)")
                    if test_case.description:
                        print(f"  Description: {test_case.description}")
                    print(f"  Input: {test_case.grid}")
                    print(f"  Expected: {test_case.expected_output}")
                    print(f"  Got: {result}")
            else:
                self.failed += 1
                status = "FAIL"
                print(f"✗ Test {test_number}: {status} ({execution_time:.2f}ms)")
                if test_case.description:
                    print(f"  Description: {test_case.description}")
                print(f"  Input: {test_case.grid}")
                print(f"  Expected: {test_case.expected_output}")
                print(f"  Got: {result}")
                
        except Exception as e:
            self.errors += 1
            print(f"✗ Test {test_number}: ERROR ({type(e).__name__})")
            if test_case.description:
                print(f"  Description: {test_case.description}")
            print(f"  Input: {test_case.grid}")
            print(f"  Error: {str(e)}")
            if show_details:
                print(f"  Traceback: {traceback.format_exc()}")
    
    def run_all_tests(self, show_details: bool = False, show_summary: bool = True):
        """Run all test cases"""
        print("🟩 Shortest Path in Binary Matrix - Comprehensive Test Suite")
        print("=" * 70)
        
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
        print("=" * 70)
        print("TEST SUMMARY")
        print("-" * 70)
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed} ({(self.passed/total)*100:.1f}%)")
        print(f"Failed: {self.failed} ({(self.failed/total)*100:.1f}%)")
        print(f"Errors: {self.errors} ({(self.errors/total)*100:.1f}%)")
        print("=" * 70)
        
        if self.passed == total:
            print("🎉 ALL TESTS PASSED! Your solution handles all cases correctly!")
        elif self.failed > 0:
            print("❌ Some tests failed. Double-check BFS/edge conditions.")
        if self.errors > 0:
            print("⚠️  Some tests had runtime errors. Check your implementation.")


def create_test_cases() -> TestRunner:
    """
    Create comprehensive test cases for Shortest Path in Binary Matrix problem.
    Includes edge cases, performance tests, and tricky scenarios.
    """
    test_runner = TestRunner()
    
    # Basic cases
    test_runner.add_test_case([[0]], 1, "Single open cell")
    test_runner.add_test_case([[1]], -1, "Single blocked cell")
    test_runner.add_test_case([[0,1],[1,0]], 2, "Smallest valid path")
    
    # Edge conditions
    test_runner.add_test_case([[1,0],[0,0]], -1, "Start blocked")
    test_runner.add_test_case([[0,0],[0,1]], -1, "End blocked")
    
    # Simple paths
    test_runner.add_test_case([[0,0],[0,0]], 2, "Fully open 2x2")
    test_runner.add_test_case([[0,0,0],[1,1,0],[1,1,0]], 4, "Straight path in 3x3")
    test_runner.add_test_case([[0,1,1],[1,0,1],[1,1,0]], 3, "Diagonal path 3x3")
    
    # Complex paths
    test_runner.add_test_case(
        [[0,1,0],[0,1,0],[0,0,0]],
        4,
        "Zigzag path around obstacles (diagonal allowed)"
    )
    test_runner.add_test_case(
        [[0,0,0],[1,1,1],[0,0,0]], 
        -1, 
        "No path due to full blocked row"
    )
    
    # Performance cases
    test_runner.add_test_case([[0]*10 for _ in range(10)], 10, "10x10 all open")
    test_runner.add_test_case([[0 if i==j else 1 for j in range(20)] for i in range(20)], 20, "20x20 diagonal only")
    
    return test_runner


def main():
    """Main function to run the comprehensive test suite"""
    print("🚀 Shortest Path in Binary Matrix - Testing System")
    print()
    
    test_runner = create_test_cases()
    test_runner.run_all_tests(show_details=False, show_summary=True)


if __name__ == "__main__":
    main()
