"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
The overall run time complexity should be O(log (m+n)).
"""


def findMedianSortedArrays(nums1, nums2):
    sorted_array = sorted(nums1 + nums2)

    array_length = len(sorted_array)

    if len(sorted_array) % 2 == 0:
        center_index = len(sorted_array) // 2

        return (sorted_array[center_index] + sorted_array[center_index - 1]) / 2
    else:
        return sorted_array[array_length // 2]


def main():
    print("Hello from findMedianSortedArrays!")


def run_sample_tests():
    # Sample Test Case 1
    sample_input_1 = ([1, 3], [2])
    expected_output_1 = 2
    try:
        result_1 = findMedianSortedArrays(*sample_input_1)
        print("Your output: ", result_1)
        print("Expected output: ", expected_output_1)
        print("✅" if result_1 == expected_output_1 else "❌")
    except Exception as e:
        print("⚠️", e)

    # Sample Test Case 2
    sample_input_2 = ([1, 2], [3, 4])
    expected_output_2 = 2.5
    try:
        result_2 = findMedianSortedArrays(*sample_input_2)
        print("Your output: ", result_2)
        print("Expected output: ", expected_output_2)
        print("✅" if result_2 == expected_output_2 else "❌")
    except Exception as e:
        print("⚠️", e)


if __name__ == "__main__":
    main()
    run_sample_tests()
