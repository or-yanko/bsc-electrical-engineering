# my task 98/100
# Question 1
def clean_string(s, char):
    """Recursively removes all occurrences of a specific character from a string.

    Args:
        s (str): The source string to clean.
        char (str): The character to be removed.

    Returns:
        str: A new string containing all characters from s except 'char'"""

    def build_next_by_index(s, char, index=0):
        """Helper function that processes the string character by character using its index"""
        # base case: we reached the end of the string
        if index == len(s):
            return ""
        # if the character is different we add it, else we ignore it.
        if not s[index] == char:
            return s[index] + build_next_by_index(s, char, index + 1)
        return build_next_by_index(s, char, index + 1)

    return build_next_by_index(s, char)


# Question 2
def closest_power(base, num):
    """
    Finds the smallest non-negative integer exponent such that base^exponent is closest to num.
    If two exponents result in values equally close to num, the smaller exponent is returned.

    Args:
        base (int): A positive integer representing the base.
        num (int): A positive integer representing the target number].

    Returns:
        int: The exponent yielding the result closest to num.
    """
    if base == 1:
        return 0
    upper_exponent, lower_exponent = 0, 0
    # find the 2 exp that are the closest 2 to num
    for i in range(num + 1):
        # Iteratively search for the two exponents that bracket the target number 'num'
        if base**i > num:
            upper_exponent, lower_exponent = i, i - 1
            break
    # check with distance is amaller and retern the closest one
    if base**upper_exponent - num >= num - base**lower_exponent:
        return lower_exponent
    return upper_exponent


# Question 3
def skip_sum(lst):
    """
    Recursively calculates the sum of elements located at odd indices (1, 3, 5...).
    The implementation uses tail recursion to accumulate the sum.
        Args:
            lst (list): A list of numerical values.

        Returns:
            int/float: The sum of elements at indices 1, 3, 5, etc.
    """

    def skip_sum_by_index(sum_=0, index=1):
        """Recursive helper that carries the current sum and index forward"""
        # base case: we reached the end of the list
        if index >= len(lst):
            return sum_
        # add to the sum to continue the adding
        return skip_sum_by_index(sum_ + lst[index], index + 2)

    return skip_sum_by_index()


# Question 4
def deep_reverse(L):
    """
    Performs a deep recursive reversal of a list and all its sub-lists.

    Args:
        L (list): The list (potentially containing other lists) to reverse.

    Returns:
        list: A new list with all elements and sub-elements in reverse order.
    """
    # base case: if the element is not a list it got returned
    if type(L) != list:
        return L

    def get_reversed_list(index=0):
        # base case: the end of the list
        if index >= len(L):
            return []
        # add everyone, but starting from the last
        return get_reversed_list(index + 1) + [deep_reverse(L[index])]

    return get_reversed_list()


# Question 5
def is_constructable(word, word_bank):
    """
    Determines if target_word can be constructed by concatenating strings from word_bank.
    This implementation uses an iterative approach with a state-update list.

    Args:
        word (str): The target string to construct.
        word_bank (list): A list of available strings for construction.

    Returns:
        bool: True if the word can be successfully constructed, False otherwise.
    """
    # make a list that tells if we made same combination till that point
    is_buildable_bool_list = [True] + [False] * len(word)

    # doing the process max time  and on every index in word, not to miss any combinations
    for current_position in range(len(word) + 1):
        if is_buildable_bool_list[current_position]:
            # checking for something from the words bank that fits and update the boolian list
            for suspicious_sub_word in word_bank:
                if (
                    word[current_position : current_position + len(suspicious_sub_word)]
                    == suspicious_sub_word
                ):
                    if current_position + len(suspicious_sub_word) <= len(word):
                        is_buildable_bool_list[
                            current_position + len(suspicious_sub_word)
                        ] = True
    return is_buildable_bool_list[len(word)]


# Question 6
def can_frog_reach(board, k, m):
    """
    Checks if a frog can reach the bottom-right corner of the board from (0,0).
    The frog moves by jumping exactly k steps right or m steps down.

    Args:
        board (list): A list of strings representing the grid ('O' for allowed, 'X' for obstacles).
        k (int): Number of steps for a horizontal jump.
        m (int): Number of steps for a vertical jump.

    Returns:
        bool: True if a valid recursive path exists to the destination, False otherwise.
    """

    x_size = len(board[0])
    y_size = len(board)
    already_been_there_lst = []

    def is_jumpable(pos):
        """Checks if a landing position is within board limits and not an obstacle 'X'"""
        if pos[0] >= x_size:
            return False
        if pos[1] >= y_size:
            return False
        if board[pos[1]][pos[0]] == "O":
            return True
        return False

    def is_reach_endpoint(current_position):
        """bool: Recursive function that check every time if you can reach the point from the other posiible points."""
        if board[current_position[1]][current_position[0]] == "X":
            return False
        # base case: we reached the end of the board.
        if current_position[0] + 1 == x_size and current_position[1] + 1 == y_size:
            return True
        # cheching and activating next moves
        next_x_right_jump_pos = (current_position[0] + k, current_position[1])
        next_y_down_jump_pos = (current_position[0], current_position[1] + m)
        is_one_direction_reach_endpoint = False
        already_been_there_lst.append(current_position)
        if (
            is_jumpable(next_x_right_jump_pos)
            and k > 0
            and next_x_right_jump_pos not in already_been_there_lst
        ):
            is_one_direction_reach_endpoint = (
                is_one_direction_reach_endpoint
                or is_reach_endpoint(next_x_right_jump_pos)
            )
        if (
            is_jumpable(next_y_down_jump_pos)
            and m > 0
            and next_y_down_jump_pos not in already_been_there_lst
        ):
            is_one_direction_reach_endpoint = (
                is_one_direction_reach_endpoint
                or is_reach_endpoint(next_y_down_jump_pos)
            )
        return is_one_direction_reach_endpoint

    return is_reach_endpoint((0, 0))
