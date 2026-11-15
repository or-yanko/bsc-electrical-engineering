# author: or yanko
question = input("Enter question number: ")
if question == "1":
    # taking inputs and declaring variables
    kaprekar_list = []
    number = input("Enter a four-digit number: ")

    # do the calculate 3 times
    while number != "6174":
        # add the number to the list
        kaprekar_list.append(number)

        # sort from largest to smallest with buuble sort :)
        help_list = list(number)
        for i in range(len(help_list) - 1):
            for j in range(len(help_list) - 1 - i):
                if help_list[j] < help_list[j + 1]:
                    help_list[j], help_list[j + 1] = help_list[j + 1], help_list[j]
        # .join()
        largest_number = ""
        for i in help_list:
            largest_number += i

        # sort from smallest to largest with buuble sort :)
        smallest_number = largest_number[::-1]

        # divide the numberst and fill zeros to
        int_number = int(largest_number) - int(smallest_number)
        number = ""
        for i in range(len(help_list) - len(str(int_number))):
            number += "0"
        number += str(int_number)

    # add the last one and print the numbers list
    kaprekar_list.append(number)
    print(kaprekar_list)

elif question == "2":
    first_string = ""
    second_string = ""
    # deals with input
    while True:
        plus_count = 0
        flag = False
        full_strings = input("Enter two words separated by '+': ")
        # checking every char and count +
        for char in full_strings.lower():
            if char == "+":
                plus_count += 1
            # check for invalid chars
            elif "a" <= char <= "z" or char == " ":
                pass
            else:
                flag = True

        # deals with no '+'
        if plus_count == 0:
            print("Only one word was received. Please try again.")
            continue

        # deals with multiple '+' or invalid characters
        if flag or plus_count > 1:
            print("Char not in alphabet. Please try again.")
            continue

        # cut the full string to 2 seperate strings and format it without spaces
        plus_index = full_strings.find("+")
        first_string = full_strings[:plus_index].lower().replace(" ", "")
        second_string = full_strings[plus_index + 1 :].lower().replace(" ", "")
        break

    # mirroring the first string
    help_string = first_string
    first_string = ""
    for char in help_string:
        first_string += chr(219 - ord(char))

    # check if anagram
    ## check if the strings havr different length
    if len(first_string) != len(second_string):
        print(False)
    else:
        # sorting first
        help_list = list(first_string)
        for i in range(len(help_list) - 1):
            for j in range(len(help_list) - 1 - i):
                if help_list[j] < help_list[j + 1]:
                    help_list[j], help_list[j + 1] = help_list[j + 1], help_list[j]
        ## joining
        first_string = ""
        for i in help_list:
            first_string += i

        # sorting second
        help_list = list(second_string)
        for i in range(len(help_list) - 1):
            for j in range(len(help_list) - 1 - i):
                if help_list[j] < help_list[j + 1]:
                    help_list[j], help_list[j + 1] = help_list[j + 1], help_list[j]
        ## joining
        second_string = ""
        for i in help_list:
            second_string += i

        # final check if they are anagram
        if first_string == second_string:
            print(True)
        else:
            print(False)

elif question == "3":
    # variable declaration
    original_string = input("Enter text: ")
    largest_balanced_string = ""
    largest_balanced_string_length = 0
    largest_balanced_string_index = 0
    largest_balanced_string_end_index = 0

    # goes over the sections contained in the string, first for (i) is to decide the first index of slicing
    for i in range(len(original_string) - 1):
        # check  if the first letter is valid
        if ("a" <= original_string[i] <= "z") or ("A" <= original_string[i] <= "Z"):
            pass
        else:
            continue
        # second for (j) is to decide the last index of slicing
        for j in range(i + 2, len(original_string) + 1):
            # slicing if the string is balanced
            sliced_string = original_string[i:j]
            # counting uppers and lowers letters
            upper_count = 0
            lower_count = 0
            for k in sliced_string:
                if "a" <= k <= "z":
                    lower_count += 1
                elif "A" <= k <= "Z":
                    upper_count += 1
            # checking if balanced, and if it is balance updating the varibles
            if (
                upper_count == lower_count
                and upper_count + lower_count > largest_balanced_string_length
            ):
                largest_balanced_string = sliced_string
                largest_balanced_string_length = upper_count + lower_count
                largest_balanced_string_index = i
                largest_balanced_string_end_index = j
    print(
        f"Result: "
        + original_string[:largest_balanced_string_index]
        + "{"
        + largest_balanced_string
        + "}"
        + original_string[largest_balanced_string_end_index:]
    )
else:
    print("Error")
