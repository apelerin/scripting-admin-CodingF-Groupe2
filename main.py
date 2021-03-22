# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from functions import *


def convert_string_to_b64(value):
    splitted_list = string_to_list(value)
    ascii_list = char_list_to_ascii_list(splitted_list)
    binary_list = ascii_list_to_binary_list(ascii_list)
    binary_list = add_0_to_beginning_of_non_8_long_binaries(binary_list)
    string_binary = string_list_to_string(binary_list)
    list_block = split_binary_to_block(string_binary)
    list_block = format_missing_zeros(list_block)
    decimal_list = binary_list_to_decimal_list(list_block)
    b64 = transform_base64(decimal_list)
    b64_string = string_list_to_string(b64)
    print(multiple_of_four(b64_string))
    return b64_string


def convert_b64_to_string(value):
    characters = split_string_and_remove_equal_sign(value)
    # ascii_list = char_list_to_ascii_list(characters)
    # print(ascii_list)
    # binaries = ascii_list_to_binary_list(ascii_list)
    # print(binaries)
    return value


if __name__ == '__main__':
    original_string = input("Enter a string: ")
    b64_value = convert_string_to_b64(original_string)
    original_string = convert_b64_to_string(b64_value)
