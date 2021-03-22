# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.

def string_to_list(string):
    """

    :param string:
    :return:
    """
    splitted_list = []
    splitted_list[:0] = string
    return splitted_list


def char_list_to_ascii_list(char_list):
    """

    :param char_list:
    :return:
    """
    for i, char in enumerate(char_list):
        char_list[i] = ord(char)
    return char_list


def ascii_list_to_binary_list(ascii_list):
    """

    :param ascii_list:
    :return:
    """
    for i, char in enumerate(ascii_list):
        ascii_list[i] = bin(char).replace('b', '')
    return ascii_list


def string_list_to_string(string):
    """

    :param string:
    :return:
    """
    return ''.join(string)


def split_binary_to_block(string):
    """

    :param string:
    :return:
    """
    list_block = []
    i = 0
    block = ''
    for char in string:
        if i % 6 == 0 and i != 0:
            list_block.append(block)
            block = ''
        block += char
        i += 1
    if block != '':
        list_block.append(block)
    return list_block


if __name__ == '__main__':
    original_string = "ABCDE"
    splitted_list = string_to_list(original_string)
    ascii_list = char_list_to_ascii_list(splitted_list)
    binary_list = ascii_list_to_binary_list(ascii_list)
    string_binary = string_list_to_string(binary_list)
    print(string_binary)
    list_block = split_binary_to_block(string_binary)
    print(list_block)
