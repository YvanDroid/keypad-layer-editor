import json
import sys
import ast

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.mouse import Mouse

import dearpygui.dearpygui as dpg

# Getting keyboard constants consistent with circuitpython's definitions
# Try to modify keyboard class to be a virtual keyboard
keyboard = Keyboard()
layout = KeyboardLayoutUS(keyboard)

layer_details = {}
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

    # Macros
    if isinstance(codes, tuple):
#         print("Is Macro")
        for i, v in enumerate(codes):
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
    for key in layerdetails.keys():
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

def output_to_json(sender, app_data, user_data):
    global layer_details
    with open(app_data['file_path_name'],"w+") as json_file:
        json_file.write(json_serialise(layer_details))

def load_json_file(sender, app_data, user_data):
    with open(app_data['file_path_name'],"rb") as json_data:
        # Strip whitespace
        json_string = json_data.read().strip()
        # print(json_string)
        global layer_details
        layer_details = json_deserialise(json_string)
        layer_titles = get_dict(layer_details, "layer_title") # Use in dropdown menu

        # Make a new list from 1 to 15 and add titles if they exist
        layer_selector = [i for i in range(1,15,1)]

        print(layer_titles)
        dpg.add_combo(items=layer_selector, label="Layer", tag="layer_select",
                        callback=layer_display, parent="Primary Window")

def change_key_title(sender, app_data, user_data):
    new_title = dpg.get_value("key_title_input")
    global layer_details
    layer_details[user_data[0]]['layer_data'][user_data[1]]['title'] = new_title

def change_key_color(sender, app_data, user_data):
    # user_data : (layer_number, text_label_tag)
    global layer_details
    color = ast.literal_eval(dpg.get_value(user_data[2]))
    color = [int(i) for i in color]
    print(color)
    layer_details[user_data[0]]['layer_colour'][user_data[1]]['colours'] = color

def assign_new_value(sender, app_data, user_data):
    # Give a key to a value and its corresponding new value
    pass

def new_key(key_number, layer_data):
    layer_data.setdefault(key_number, {'title': "", 'colours': (0,0,0), 'device':"keyboard", 'codes':()})

def key_display(sender, app_data, user_data):
    # Key index should be given in app_data
    # user_data is the current layer
    global layer_details
    current_layer = user_data
    current_key = int(app_data)
    layer_data = layer_details[current_layer]['layer_data']
    # Check if key exists
    try:
        key_title = layer_data[current_key]['title']
    except KeyError:
        new_key(current_key, layer_data)
        key_title = layer_data[current_key]['title']
    with dpg.group(parent="layer_display", tag="key_display"):
        # Key Title
        with dpg.group(horizontal=True):
            dpg.add_input_text(label="Layer Title", default_value=key_title, tag="key_title_input")
            dpg.add_button(label="Submit New Title", callback=change_key_title, user_data=(current_layer, current_key))
        # Key Colour
        with dpg.group():
            dpg.add_text(default_value=str(layer_data[current_key]['colours']), tag="current_key_color")
            dpg.add_color_edit(label="Layer Color", tag="key_color_input", callback=change_color_text, user_data="current_key_color")
            dpg.add_button(label="Submit New Color", tag="key_color_button", callback=change_key_color, user_data=(current_layer, current_key, "current_color"))

        # Key Device
        device_list = ["keyboard", "mouse", "midi", "consumer_control"]
        dpg.add_combo(items=device_list, label="Device", tag="device_select", user_data=(current_layer, current_key))
        # TODO: Add UI for each device type



def change_layer_title(sender, app_data, user_data):
    print(app_data, user_data)
    new_title = dpg.get_value("layer_title_input")
    global layer_details
    layer_details[app_data]['layer_title'] = new_title

def change_layer_color(sender, app_data, user_data):
    # user_data : (layer_number, text_label_tag)
    print(app_data, user_data)
    global layer_details
    color = ast.literal_eval(dpg.get_value(user_data[1]))
    color = [int(i) for i in color]
    print(color)
    layer_details[user_data[0]]['layer_colour'] = color
def change_color_text(sender, app_data, user_data):
    color = dpg.get_value(sender)
    dpg.set_value(user_data, color[0:3])

def new_layer(layer_key):
    # Initialise a new layer 
    global layer_details
    layer_details.setdefault(layer_key, {'layer_title': "", 'layer_colour': (0,0,0), 'layer_data':{}})

def layer_display(sender, app_data, user_data):
    global layer_details
    print(app_data) # Selected layer
    try:
        selected_layer = layer_details[int(app_data)]
    except KeyError: # Create an empty layer
        new_layer(int(app_data))
        selected_layer = layer_details[int(app_data)]
    current_layer = int(app_data)
    with dpg.group(parent="Primary Window", tag="layer_display"):
        key_selector = [i for i in range(1,15,1)]
        # Might have empty layers:
        try:
            layer_title = selected_layer['layer_title']
        except KeyError:
            layer_title = ""
        
        # Layer Title
        with dpg.group(horizontal=True):
            dpg.add_input_text(label="Layer Title", default_value=layer_title, tag="layer_title_input")
            dpg.add_button(label="Submit New Title", callback=change_layer_title, user_data=current_layer)
        # Layer Colors
        with dpg.group():
            dpg.add_text(default_value=str(selected_layer['layer_colour']), tag="current_color")
            dpg.add_color_edit(label="Layer Color", tag="layer_color_input", callback=change_color_text, user_data="current_color")
            dpg.add_button(label="Submit New Color", tag="layer_color_button", callback=change_layer_color, user_data=(current_layer, "current_color"))

        # Layer Keys
        dpg.add_combo(items=key_selector, label="Key", tag="key_select", user_data=current_layer, callback=key_display)

        # print(layers, colours)



dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# input_file = input("")
with dpg.window(label="Main Window", tag="Primary Window"):
    with dpg.file_dialog(directory_selector=False,
                            show=True,
                            callback=load_json_file,
                            tag="file_load_dialog",
                            width=700,
                            height=400,
                            default_filename='layout'):
        dpg.add_file_extension(".json", color=(255,0,255,255))
    with dpg.file_dialog(directory_selector=False,
                            show=False,
                            callback=output_to_json,
                            tag="file_save_dialog",
                            width=700,
                            height=400,
                            default_filename='layout'):
        dpg.add_file_extension(".json", color=(255,0,255,255))
    dpg.add_button(label="Save to json file", callback=lambda:dpg.show_item("file_save_dialog"))


dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
