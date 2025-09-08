def find_longest_consecutive_substring(string: str) -> str:

    max_length = 0
    current_length = 1

    for i in range(1, len(string)):
        if string[i] == string[i - 1]:
            current_length += 1
        else:
            if current_length > max_length:
                max_length = current_length

            current_length = 1

    if current_length > max_length:
        max_length = current_length

    return max_length


no_of_case = int(input("Enter no of cases: "))
result_set = []
for iteration in range(no_of_case):
    str_length, no_of_append = map(
        int, input("Enter str_length, no_of_append: ").split()
    )
    string_1 = input("Enter String: ")

    str_list = [string_1]

    for i in range(no_of_append):

        char_to_append = input()
        string_1 = string_1 + char_to_append
        str_list.append(string_1)

    results = []
    for i in range(len(str_list)):
        result = find_longest_consecutive_substring(str_list[i])
        results.append(result)

    result_set.append(results)

for res in result_set:
    print(*res)
