Help on module find_string:

NAME
    find_string

DESCRIPTION
    # Extends pyautogui and pytesseract to find and click string locations on screen.
    # Works by analyzing a screenshot.
    # Not guaranteed to find all strings in input.
    # Made by Daniel Enesi. August 15-16, 2024. All rights reserved.

FUNCTIONS
    clickString(string, **args)
        Function to click a string on the screen.

        Raises RuntimeError if text not found on screen.

    clickStrings(strings, **args)
        Click strings provided in the order listed by pytesseract
        Accepts **args to apply pyautogui-provided behaviour for clicks.

    findString(string)
        Function to get a location of a particular string.

        Returns None if string is  found.
        Returns a tuple (x, y) of a position of the string.
        if string as multiple location, returns the first one listed by pytesseract

    findStrings(strings)
        Function to get the center location of text boxes in a page.
        Works by taking a screenshot and using a pytesseract function
        to get the bounds as a DataFrame.
        Case sensitive. Matches whole string not substrings.

        Passing a string will find locations of that string.
        Passing a list of strings will find locations of the strings.

        Returns None if none of the strings are found.

        Returns a DataFrame object containing bounds and mid-points ("x", "y") of texts provided in
        argument <strings>.

VERSION
    1.0.0