# Extends pyautogui and pytesseract to find and click string locations on screen.
# Requires Google Tesseract-OCR engine to be installed on system.
# Install pyautogui, pytesseract, pandas. Or pip install -r requirements.txt.
# Works by analyzing a screenshot.
# Not guaranteed to find all strings in input.

# Made by Daniel Enesi. August 15-16, 2024. All rights reserved.


import pyautogui
import pytesseract


__version__ = "1.0.0"


# Path to Google Tesseract engine. Edit to fit your specification.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"


def _getPoints(positions):
    """Returns x, y pairs for positions from findStrings / findString.

    Returns list of tuples.
    """
    return [
        (int(position["x"]), int(position["y"])) for position in positions.iloc
    ]


def findStrings(strings):
    """Function to get the center location of text boxes in a page.
    Works by taking a screenshot and using a pytesseract function
    to get the bounds as a DataFrame.
    Case sensitive. Matches whole string not substrings.

    Passing a string will find locations of that string.
    Passing a list of strings will find locations of the strings.

    Returns None if none of the strings are found.
    
    Returns a DataFrame object containing bounds and mid-points ("x", "y") of texts provided in 
    argument <strings>.
    """

    # Convert string to list of strings.
    if isinstance(strings, str):
        strings = [strings]
    # Convert common iterables to set for better searching (maybe not needed)
    strings = set(strings) if type(strings) in {tuple, list} else strings

    screen = pyautogui.screenshot()
    screen_data = pytesseract.image_to_data(screen, output_type="data.frame")

    positions = screen_data[screen_data["text"].isin(strings)]
    positions = positions[["text", "left", "top", "width", "height"]].copy()

    if positions.empty:
        return
    
    positions["x"] = positions["left"] + positions["width"] / 2
    positions["y"] = positions["top"] + positions["height"] / 2

    return positions


def findString(string):
    """Function to get a location of a particular string.

    Returns None if string is  found.
    Returns a tuple (x, y) of a position of the string.
    if string as multiple location, returns the first one listed by pytesseract
    """

    position = findStrings({string})
    if position is None or position.empty:
        return
    
    return _getPoints(position)[0]


def moveToString(string, **args):
    """Function to move to a string on the screen.
    DRYed clickString :)

    Raises RuntimeError if text not found on screen.
    """

    position = findString(string)
    if position is None:
        raise RuntimeError(f"String '{string}' not found on screen")
    
    x, y = position
    pyautogui.moveTo(x, y, **args)


def clickString(string, **args):
    """Function to click a string on the screen.

    Raises RuntimeError if text not found on screen.
    """

    position = findString(string)
    if position is None:
        raise RuntimeError(f"String '{string}' not found on screen")
    
    x, y = position
    pyautogui.click(x, y, **args)


def clickStrings(strings, **args):
    """Click strings provided in the order listed by pytesseract
    Accepts **args to apply pyautogui-provided behaviour for clicks.
    """

    positions = findStrings(strings)

    if positions is None:
        raise RuntimeError(f"None of '{strings}' found on screen")
    
    for position in _getPoints(positions):
        pyautogui.click(*position, **args)
