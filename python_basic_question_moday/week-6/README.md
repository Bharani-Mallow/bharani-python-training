
# Median of Two Sorted Arrays

## Problem Statement

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.

The overall run time complexity should be $O(\log(m+n))$.

### Examples

**Example 1:**

Input: `nums1 = [1,3]`, `nums2 = [2]`
Output: `2.00000`
Explanation: Merged array = `[1,2,3]` and median is `2`.

**Example 2:**

Input: `nums1 = [1,2]`, `nums2 = [3,4]`
Output: `2.50000`
Explanation: Merged array = `[1,2,3,4]` and median is `(2 + 3) / 2 = 2.5`.

### Constraints

- `nums1.length == m`
- `nums2.length == n`
- $0 \leq m \leq 1000$
- $0 \leq n \leq 1000$
- $1 \leq m + n \leq 2000$
- $-10^6 \leq nums1[i], nums2[i] \leq 10^6$

---

## How to run

1. Run the main program:
   ```sh
   python main.py
   ```
2. Run tests:
   ```sh
   python test_program.py
   ```
3. Run tests with details:
   ```sh
   python test_program.py -d
   ```

## Check your solution on LeetCode

For more corner cases and to verify your time complexity, you can run your solution on LeetCode:

- [Median of Two Sorted Arrays on LeetCode](https://leetcode.com/problems/median-of-two-sorted-arrays?envType=problem-list-v2&envId=array)

LeetCode provides a large set of test cases and performance analysis. Paste your function there to validate your approach!
