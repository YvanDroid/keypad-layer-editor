import json
import sys
import ast
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

# Use this to get by for now. This should encode the given layers.py to a JSON file. Use to edit the keybinds before implementing the GUI.

# Getting keyboard constants consistent with circuitpython's definitions
# Try to modify keyboard class to be a virtual keyboard
keyboard = Keyboard()
layout = KeyboardLayoutUS(keyboard)

# For transition of layouts to JSON format, only use for serialisation since it will change the data
# Serialise sets into lists, returns json string


def get_dict(dictionary, selector_index):
    """Returns a separate dictionary from a given dictionary and index selector.
    Useful for if a dictionary has an array for each value."""
    return dict(
        [
            (key, value)
            for key, value in sorted(
                [(i, dictionary[i][selector_index]) for i in dictionary]
            )
        ]
    )


def serialise_codes(codes):
    #Input keycode list. It will be parsed to maintain the data
    #print("sending keyboard inputs")
    code_array = []
    # Singular keys, leave as int
    if isinstance(codes, int):
#         print("Is Single")
        return codes

    # Singular Combos
    if isinstance(codes, set):
#         print("Is Combo")
        code_array.extend(codes)
        code_array.append("combo")

    if isinstance(codes, str): #String value printed as is
        codes

    # Macros
    if isinstance(codes, tuple):
#         print("Is Macro")
        for i, v in enumerate(codes):
            if isinstance(v, str): # String is printed as is
                code_array.append(v)
            if isinstance(v, float): # Float signifies delay
                code_array.append(v)
            if isinstance(v, int):  # Single key, place in list
                code_array.append(v)
            if isinstance(v, set) or isinstance(v, tuple):  # Combo
                combo_array = []
                combo_array.extend(v)
                combo_array.append("combo")
                code_array.append(combo_array)
        code_array.append("macro")

    # Should be a parsed list of codes
#     print(code_array)
    return code_array

def deserialise_codes(codes):
    # Backwards operations from serialised lists

    # If single key, return already int
    if isinstance(codes, int):
#         print("Is Single")
        return codes

    # Single string
    if isinstance(codes, str):
        return codes

    # Combos and macros
    if isinstance(codes, list):
        # Weird empty lists from empty tuples
        if len(codes) == 0:
            return set(codes)

        # Singular combos
        if codes[-1] == "combo":
#             print("Is Combo")
            del codes[-1]
            codes = set(codes)
            return codes

        # Macros
        if codes[-1] == "macro":
#             print("Is Macro")
            del codes [-1]
            for i in range(len(codes)):
                # String
                if isinstance(codes[i], str):
                    continue
                # Delay
                if isinstance(codes[i], float):
                    continue
                # Single
                if isinstance(codes[i], int):
                    continue
                # Combo
                if isinstance(codes[i], list):
                    del codes[i][-1]
                    codes[i] = set(codes[i])
            codes = tuple(codes)
#     print(codes)
    return codes

def json_serialise(layerdetails):
    print( layerdetails.keys())
    for key in layerdetails.keys():
        print(key)
        # Iterate over items inside the keys
        for button in layerdetails[key]["layer_data"].keys():
            for item, value in layerdetails[key]["layer_data"][button].items():
                if item == "codes":
                    # print(value)
                    layerdetails[key]["layer_data"][button][item] = serialise_codes(value)
                    continue
                if isinstance(value, set):
                    layerdetails[key]["layer_data"][button][item] = list(layerdetails[key]["layer_data"][button][item])

    json_string = json.dumps(layerdetails, indent=4)
    # print(json_string)
    return json_string

def json_deserialise(jsonstr):
    # Decoded data is treated like a dict. Makes it easy to index if formatted correctly
    decoded_data = json.loads(jsonstr)
#     for key in decoded_data.keys():
#        for item in decoded_data[key].keys():
#            if isinstance(decoded_data[key][item], list):
#                # Check for "tuple" or "set"
#                decoded_data[key][item] = tuple(decoded_data[key][item])
#     print(decoded_data)
    for key, details in decoded_data.items():
        # Handle layer colours
        # Iterate over items inside the keys
        if isinstance(details["layer_colour"], list):
            details["layer_colour"] = tuple(details["layer_colour"])
        for button in details["layer_data"].keys():
            for item, value in details["layer_data"][button].items():
                if item == "codes":
#                     print(value)
                    details["layer_data"][button][item] = deserialise_codes(value)
                    continue
                if isinstance(value, list):
                    details["layer_data"][button][item] = tuple(details["layer_data"][button][item])

        details["layer_data"] = {int(key1): value1 for key1, value1 in details["layer_data"].items()}
    # Convert keys to integer keys
    decoded_data = {int(key): value for key, value in decoded_data.items()}
#     print(decoded_data)
    return decoded_data

def new_key(key_number, layer_data):
    layer_data.setdefault(key_number, {'title': "", 'colours': (0,0,0), 'device':"keyboard", 'codes':()})
