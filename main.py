import layer_handler as lh
import dearpygui.dearpygui as dpg

# Getting keyboard constants consistent with circuitpython's definitions
# Try to modify keyboard class to be a virtual keyboard
keyboard = Keyboard()
layout = KeyboardLayoutUS(keyboard)

layer_details = {}
# For transition of layouts to JSON format, only use for serialisation since it will change the data
# Serialise sets into lists, returns json string

def output_to_json(sender, app_data, user_data):
    global layer_details
    with open(app_data['file_path_name'],"w+") as json_file:
        json_file.write(lh.json_serialise(layer_details))

def load_json_file(sender, app_data, user_data):
    with open(app_data['file_path_name'],"rb") as json_data:
        # Strip whitespace
        json_string = json_data.read().strip()
        # print(json_string)
        global layer_details
        layer_details = lh.json_deserialise(json_string)
        layer_titles = lh.get_dict(layer_details, "layer_title") # Use in dropdown menu

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

def keyboard_record(sender, app_data, user_data):
    dpg.set_value("input_text", app_data)

def record_activate(sender, app_data, user_data):
    dpg.show_item("input_handler")

def device_selection(sender, app_data, user_data):
    with dpg.group(parent="key_display", tag="device_display"):
        if app_data == "keyboard":
            dpg.add_text(default_value='', tag="input_text")
            dpg.add_button(label="Record Keyboard", callback=record_activate, tag="key_rec_button", user_data="input_handler")
        if app_data == "mouse":
            pass
        if app_data == "midi":
            pass
        if app_data == "consumer_control":
            pass
            # dpg.add_combo(items=)

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
        dpg.add_combo(items=device_list, label="Device", tag="device_select", user_data=(current_layer, current_key), callback=device_selection)
        # TODO: Add UI for each device type



def change_layer_title(sender, app_data, user_data):
    print(app_data, user_data)
    new_title = dpg.get_value("layer_title_input")
    global layer_details
    layer_details[user_data]['layer_title'] = new_title
    print(layer_titles)

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
        key_selector = [str(i) for i in range(1,15,1)]
        dpg.add_combo(items=key_selector, label="Key", tag="key_select", user_data=current_layer, callback=key_display)

        # print(layers, colours)



dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# input_file = input("")
with dpg.handler_registry(tag="input_handler",show=False):
    dpg.add_key_press_handler(callback=keyboard_record)

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
