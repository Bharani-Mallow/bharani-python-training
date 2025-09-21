def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        tasks = list(map(int, input().split()))

        # Calculate prefix sums for processor 1
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + tasks[i]

        # Calculate suffix sums for processor 2
        suffix_sum = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suffix_sum[i] = suffix_sum[i + 1] + tasks[i]

        # Find minimum time by checking all possible split points
        min_time = float("inf")
        for i in range(n + 1):
            # Processor 1 gets tasks 0 to i-1 (prefix_sum[i])
            # Processor 2 gets tasks i to n-1 (suffix_sum[i])
            time1 = prefix_sum[i]
            time2 = suffix_sum[i]
            max_time = max(time1, time2)
            min_time = min(min_time, max_time)

        print(min_time)


if __name__ == "__main__":
    solve()
