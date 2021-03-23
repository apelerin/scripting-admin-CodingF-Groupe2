from textwrap import wrap


def string_to_list(string):
    """
    Takes in a string, and return a list of characters of that string
    :param string:
    :return:
    """
    return [char for char in string]


def char_list_to_ascii_list(char_list):
    """
    Takes in a character list and return a list of ascii
    :param char_list:
    :return:
    """
    for i, char in enumerate(char_list):
        char_list[i] = ord(char)
    return char_list


def ascii_list_to_binary_list(ascii_list):
    """
    takes in a list of ascii values, and return a list of string binaries corresponding
    :param ascii_list:
    :return:
    """
    for i, char in enumerate(ascii_list):
        ascii_list[i] = bin(char).replace('0b', '')
    return ascii_list


def add_0_to_beginning_of_non_8_long_binaries(binaries):
    for i, binary in enumerate(binaries):
        binaries[i] = binary.zfill(8)
    return binaries


def string_list_to_string(string):
    """
    converts a string list to a string
    :param string:
    :return:
    """
    return ''.join(string)


def split_binary_to_block(binaries):
    """
    splits a binary string to a list of blocks of 6 characters when possible
    :param string:
    :return:
    """
    return wrap(binaries, 6)


def format_missing_zeros(list_binary):
    """
    formats the last element of a list of block binaries if there are less than 6 characters in it (filling with 0)
    :param list_binary:
    :return:
    """
    while len(list_binary[-1]) != 6:
        list_binary[-1] += '0'
    return list_binary


def binary_list_to_decimal_list(binary_list):
    """
    converts a binary list to a corresponding list of decimals
    :param binary_list:
    :return:
    """
    for index, value in enumerate(binary_list):
        binary_list[index] = int(value, 2)
    return binary_list


def transform_base64(splitedList):
    """
    convert a list in BASE64
    :param splitedList: a list of splited decimals
    :return:
    """
    chars = ""
    for i in range(len(splitedList)):
        chars = chars + chr(splitedList[i] + 65)
    return chars


def multiple_of_four(string):
    """
    check if a string has enough chars to be multipliable by 4 and adds '=' if it is not
    :param string: a string
    :return:
    """
    while (len(string) % 4 != 0):
        string = string + "="
    return string

def split_string_and_remove_equal_sign(value):
    value.replace('=', '')
    return string_to_list(value)
