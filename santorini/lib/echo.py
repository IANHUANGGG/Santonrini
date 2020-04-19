#!/usr/bin/python3
""" Echos JSON as array with reverse index """

import sys
import json
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def json_echo(string):
    """ Echos JSON as array with reverse index

        json_echo takes in a string that contains multiple valid JSON data
        and returns a string that outputs all the JSON values, each on a
        separated line, embedded in a JSON array that indicates its reverse
        position.

        :param str string: Input string to parse JSON from
        :raises json.decoder.JSONDecodeError if string contains invalid JSON
        :return JSON as array with reverse index
        :rtype: str
    """
    output = []

    decoder = json.JSONDecoder()

    next_string = string.lstrip()

    while next_string != "":
        parsed_line, index = decoder.raw_decode(next_string)
        next_string = next_string[index:].lstrip()
        output.append(parsed_line)

    return output


def main():
    """ Main function that reads from stdin and prints to stdout """
    try:
        print(json_echo(sys.stdin.read()))
    except json.decoder.JSONDecodeError:
        print("Invalid JSON")


if __name__ == "__main__":
    main()
