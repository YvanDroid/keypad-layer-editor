import json, sys

from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode
#from adafruit_hid.gamepad import Gamepad
from adafruit_hid.mouse import Mouse

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Setting up input functionality
keyboard = Keyboard()
layout = KeyboardLayoutUS(keyboard)


def remove_lessons(lesson_number: int):
    lesson_text = f"L{lesson_number}"
    key_list = []
    key_list.append(Keycode.F2)
    key_list = key_list + [Keycode.BACKSPACE for x in enumerate(lesson_text)]

    return tuple(key_list)


def current_lesson(lesson_number: int):
    lesson_text = f"L{lesson_number}"
    key_list = []
    key_list.append(Keycode.F2)
    key_list = key_list + [layout.keycodes(x) for x in lesson_text]
    key_list = key_list + [
        (Keycode.LEFT_ARROW, Keycode.SHIFT) for x in enumerate(lesson_text)
    ]

    return tuple(key_list)

# Keypad with Commas and Tab
data_numpad= {
    9: {
        "codes": Keycode.ONE,
        "title": "1",
        "device": "keyboard",
        },
    10: {
        "codes": Keycode.TWO,
        "title": "2",
        "device": "keyboard",
        },
    11: {
        "codes": Keycode.THREE,
        "title": "3",
        "device": "keyboard",
        },
    14: {
        "codes": Keycode.COMMA,
        "title": ",",
        "device": "keyboard",
        },
    5: {
        "codes": Keycode.FOUR,
        "title": "4",
        "device": "keyboard",
        },
    6: {
        "codes": Keycode.FIVE,
        "title": "5",
        "device": "keyboard",
        },
    7: {
        "codes": Keycode.SIX,
        "title": "6",
        "device": "keyboard",
        },
    1: {
        "codes": Keycode.SEVEN,
        "title": "7",
        "device": "keyboard",
        },
    2: {
        "codes": Keycode.EIGHT,
        "title": "8",
        "device": "keyboard",
        },
    3: {
        "codes": Keycode.NINE,
        "title": "9",
        "device": "keyboard",
        },
    13: {
        "codes": Keycode.ZERO,
        "title": "0",
        "device": "keyboard",
        },
    15: {
        "codes": Keycode.BACKSPACE,
        "title": "Backspace",
        "device": "keyboard",
        },
    4: {
        "codes": Keycode.TAB,
        "title": "Tab",
        "device": "keyboard",
        },
    8: {
        "codes": Keycode.SPACE,
        "title": "Space",
        "device": "keyboard",
        },
    12: {
        "codes": Keycode.ENTER,
        "title": "Enter",
        "device": "keyboard",
        },
}
# VLC and OBS keybinds
vlc_obs = {
    1: {
        "codes": ConsumerControlCode.VOLUME_DECREMENT,
        "title": "Vol -",
        "device": "consumer_control",
        "colours": (255, 255, 0),
    },
    2: {
        "codes": ConsumerControlCode.MUTE,
        "title": "Mute Volume",
        "device": "consumer_control",
        "colours": (255, 255, 0),
    },
    3: {
        "codes": ConsumerControlCode.VOLUME_INCREMENT,
        "title": "Vol +",
        "device": "consumer_control",
        "colours": (255, 255, 0),
    },
    4: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.P},
        "title": "VLC: Play/ Pause",
        "device": "keyboard",
        "colours": (255, 140, 15),
    },
    5: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.ZERO},
        "title": "VLC: Mute",
        "colours": (255, 140, 15),
        "device": "keyboard",
    },
    6: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.LEFT_ARROW},
        "title": "VLC: Prev Chapter",
        "colours": (255, 140, 15),
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.RIGHT_ARROW},
        "title": "VLC: Next Chapter",
        "colours": (255, 140, 15),
        "device": "keyboard",
    },
    8: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.ONE},
        "title": "OBS: Scene 1",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.TWO},
        "title": "OBS: Scene 2",
        "device": "keyboard",
    },
    10: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.THREE},
        "title": "OBS: Scene 3",
        "device": "keyboard",
    },
    11: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.T},
        "title": "OBS: Transition",
        "device": "keyboard",
    },
    12: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.FOUR},
        "title": "OBS: Scene 4",
        "device": "keyboard",
    },
    13: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.FIVE},
        "title": "OBS: Scene 5",
        "device": "keyboard",
    },
    14: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.SIX},
        "title": "OBS: Scene 6",
        "device": "keyboard",
    },
    15: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.B},
        "title": "OBS: Fade-black",
        "device": "keyboard",
    },
}

# Webex Keybinds
webex = {
    4: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.D},
        "title": "Share Content",
        "device": "keyboard",
    },
    5: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.H},
        "title": "Toggle Menu Bar",
        "device": "keyboard",
    },
    6: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.L},
        "title": "Toggle Meeting Lock",
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.U},
        "title": "Mute all",
        "device": "keyboard",
    },
    8: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.Z},
        "title": "Stop Sharing",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.M},
        "title": "Music Mode",
        "device": "keyboard",
    },
    10: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.S},
        "title": "Pause/Resume Sharing",
        "device": "keyboard",
    },
    11: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.Y},
        "title": "Fullscreen",
        "device": "keyboard",
    },
    12: {
        "codes": {Keycode.CONTROL, Keycode.M},
        "title": "Mute/Unmute",
        "device": "keyboard",
    },
    13: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.V},
        "title": "Video on/off",
        "device": "keyboard",
    },
    14: {
        "codes": {Keycode.CONTROL, Keycode.SHIFT, Keycode.R},
        "title": "Raise/Lower Hand",
        "device": "keyboard",
    },
    15: {
        "codes": {Keycode.CONTROL, Keycode.Q},
        "title": "Quit Meeting",
        "device": "keyboard",
    },
}

# All media keys
media_keys = {
    12: {
        "codes": ConsumerControlCode.VOLUME_DECREMENT,
        "title": "Vol -",
        "device": "consumer_control",
    },
    8: {
        "codes": ConsumerControlCode.SCAN_PREVIOUS_TRACK,
        "title": "Prev Track",
        "device": "consumer_control",
    },
    4: {
        "codes": ConsumerControlCode.MUTE,
        "title": "Output Mute",
        "device": "consumer_control",
    },
    5: {"codes": Keycode.F20,
        "title": "Mic Mute (Linux)",
        "device": "keyboard"
        },
    9: {
        "codes": ConsumerControlCode.PLAY_PAUSE,
        "title": "Play/Pause",
        "device": "consumer_control",
    },
    13: {
        "codes": ConsumerControlCode.VOLUME_INCREMENT,
        "title": "Vol +",
        "device": "consumer_control",
    },
    11: {
        "codes": ConsumerControlCode.SCAN_NEXT_TRACK,
        "title": "Next Track",
        "device": "consumer_control",
    },
    6: {
        "codes": ConsumerControlCode.REWIND,
        "title": "Rewind",
        "device": "consumer_control",
    },
    7: {
        "codes": ConsumerControlCode.FAST_FORWARD,
        "title": "Fast Forward",
        "device": "consumer_control",
    },
    10: {
        "codes": ConsumerControlCode.STOP,
        "title": "Stop",
        "device": "consumer_control",
    },
}

# Other Keybinds
miscellaneous = {
    4: {
        "codes": {Keycode.WINDOWS, Keycode.SHIFT, Keycode.C},
        "title": "Color Picker",
        "device": "keyboard",
    },
    5: {
        "codes": {Keycode.WINDOWS, Keycode.SHIFT, Keycode.S},
        "title": "Snip and Sketch",
        "device": "keyboard",
    },
    6: {
        "codes": {Keycode.WINDOWS, Keycode.SHIFT, Keycode.T},
        "title": "Text Extractor",
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.WINDOWS, Keycode.CONTROL, Keycode.T},
        "title": "Always on Top",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.WINDOWS, Keycode.SHIFT, Keycode.M},
        "title": "Screen Ruler",
        "device": "keyboard",
    },
    8: {"codes": {Keycode.CONTROL, Keycode.Y}, "title": "Redo", "device": "keyboard"},
    10: {
        "codes": {Keycode.CONTROL, Keycode.KEYPAD_FOUR},
        "title": "RTSS Overlay Toggle",
        "device": "keyboard",
    },
    12: {"codes": {Keycode.CONTROL, Keycode.Z}, "title": "Undo", "device": "keyboard"},
    13: {"codes": {Keycode.CONTROL, Keycode.X}, "title": "Cut", "device": "keyboard"},
    14: {"codes": {Keycode.CONTROL, Keycode.C}, "title": "Copy", "device": "keyboard"},
    15: {"codes": {Keycode.CONTROL, Keycode.V}, "title": "Paste", "device": "keyboard"},
}
# Excel Keybinds
excel = {
    10: {
        "codes": (
            # {Keycode.CONTROL, Keycode.B},
            Keycode.ALT,
            Keycode.H,
            Keycode.F,
            Keycode.C,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.DOWN_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Change to red",  # and bold",
        "device": "keyboard",
    },
    11: {
        "codes": remove_lessons,
        "title": "Remove Lesson Count",
        "device": "keyboard",
    },
    12: {"codes": (), "title": "Reset Lesson Count", "device": "keyboard"},
    13: {"codes": (), "title": "Decrement Lesson Count", "device": "keyboard"},
    14: {"codes": current_lesson, "title": "Print Lesson Count", "device": "keyboard"},
    15: {"codes": (), "title": "Increment Lesson Count", "device": "keyboard"},
    9: {
        "codes": (
            {Keycode.CONTROL, Keycode.ONE},
            {Keycode.ALT, Keycode.B},
            Keycode.ENTER,
        ),
        "title": "Change Format",
        "device": "keyboard",
    },
    1: {
        "codes": (Keycode.ALT, Keycode.H, Keycode.J, Keycode.HOME, Keycode.ENTER),
        "title": "Absent",
        "colours": (218, 150, 148),
        "device": "keyboard",
    },
    2: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Attended",
        "colours": (196, 215, 155),
        "device": "keyboard",
    },
    3: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Committee Prayer 1",
        "colours": (0, 176, 240),
        "device": "keyboard",
    },
    4: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Committee Prayer 2",
        "colours": (255, 192, 0),
        "device": "keyboard",
    },
    5: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Attended (Other)",
        "colours": (177, 160, 199),
        "device": "keyboard",
    },
    6: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "Sign Forgor",
        "colours": (149, 179, 215),
        "device": "keyboard",
    },
    7: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.DOWN_ARROW,
            Keycode.ENTER,
        ),
        "title": "No Report",
        "colours": (255, 255, 255),
        "device": "keyboard",
    },
    8: {
        "codes": (
            Keycode.ALT,
            Keycode.H,
            Keycode.J,
            Keycode.HOME,
            Keycode.DOWN_ARROW,
            Keycode.RIGHT_ARROW,
            Keycode.ENTER,
        ),
        "title": "R1_07",
        "colours": (250, 191, 143),
        "device": "keyboard",
    },
}

# Pure OBS
pure_obs = {
    1: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.KEYPAD_FIVE},
        "title": "OBS: Save Replay",
        "device": "keyboard",
    },
    2: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.KEYPAD_SIX},
        "title": "OBS: Start Replay",
        "device": "keyboard",
    },
    3: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.KEYPAD_SEVEN},
        "title": "OBS: Start Record",
        "device": "keyboard",
    },
    4: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.ONE},
        "title": "OBS: Scene 1",
        "device": "keyboard",
    },
    5: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.TWO},
        "title": "OBS: Scene 2",
        "device": "keyboard",
    },
    6: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.THREE},
        "title": "OBS: Scene 3",
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.FOUR},
        "title": "OBS: Scene 4",
        "device": "keyboard",
    },
    8: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.FIVE},
        "title": "OBS: Scene 5",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.SIX},
        "title": "OBS: Scene 6",
        "device": "keyboard",
    },
    10: {
        "codes": (
            {Keycode.CONTROL, Keycode.KEYPAD_PLUS},
            {Keycode.CONTROL, Keycode.KEYPAD_NINE},
        ),
        "title": "Capture Foreground",
        "device": "keyboard",
    },
    11: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.T},
        "title": "OBS: Transition",
        "device": "keyboard",
    },
    12: {
        "codes": {Keycode.CONTROL, Keycode.KEYPAD_ZERO},
        "title": "Mute Desktop Audio",
        "device": "keyboard",
    },
    13: {
        "codes": {Keycode.CONTROL, Keycode.KEYPAD_PERIOD},
        "title": "Mute Game Audio",
        "device": "keyboard",
    },
}

# Google Meet Controls
google_meet = {
    12: {
        "codes": {Keycode.CONTROL, Keycode.D},
        "title": "Mute Microphone",
        "device": "keyboard",
    },
    13: {
        "codes": {Keycode.CONTROL, Keycode.E},
        "title": "Toggle Camera",
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.K},
        "title": "Increase Participants",
        "device": "keyboard",
    },
    11: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.J},
        "title": "Decrease Participants",
        "device": "keyboard",
    },
    14: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.H},
        "title": "Toggle Hand",
        "device": "keyboard",
    },
    8: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.C},
        "title": "Toggle Chat",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.P},
        "title": "Toggle Participants",
        "device": "keyboard",
    },
    10: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.M},
        "title": "Toggle Video Size",
        "device": "keyboard",
    },
}

# Obsidian Notes
obsidian = {
    12: {
        "codes": {Keycode.SHIFT, Keycode.FOUR},
        "title": "Latex Formatting",
        "device": "keyboard",
    },
    13: {
        "codes": {Keycode.CONTROL, Keycode.B},
        "title": "Toggle Bold",
        "device": "keyboard",
    },
    14: {
        "codes": {Keycode.CONTROL, Keycode.I},
        "title": "Toggle Italics",
        "device": "keyboard",
    },
    15: {
        "codes": {Keycode.CONTROL, Keycode.GRAVE_ACCENT},
        "title": "Toggle Blockquote",
        "device": "keyboard",
    },
    8: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.A},
        "title": "Latex: Align",
        "device": "keyboard",
    },
    9: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.C},
        "title": "Latex: Cases",
        "device": "keyboard",
    },
    10: {
        "codes": {Keycode.ALT, Keycode.SHIFT, Keycode.M},
        "title": "Latex: Matrix",
        "device": "keyboard",
    },
    11: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.T},
        "title": "Table of Contents",
        "device": "keyboard",
    },
    4: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.LEFT_ARROW},
        "title": "Navigate Back",
        "device": "keyboard",
    },
    5: {
        "codes": {Keycode.CONTROL, Keycode.ALT, Keycode.RIGHT_ARROW},
        "title": "Navigate Forward",
        "device": "keyboard",
    },
    7: {
        "codes": {Keycode.CONTROL, Keycode.PAGE_DOWN},
        "title": "Next Tab",
        "device": "keyboard",
    },
    6: {
        "codes": {Keycode.CONTROL, Keycode.PAGE_UP},
        "title": "Previous Tab",
        "device": "keyboard",
    },
}

mouse_functions = {
    # Adding mouse buttons in a combo requires the | operator
    # so that it will send all inputs at once
    1: {"buttons": Mouse.LEFT_BUTTON, "title": "Left Mouse", "device": "mouse"},
    3: {"buttons": Mouse.RIGHT_BUTTON, "title": "Right Mouse", "device": "mouse"},
    6: {"buttons": Mouse.MIDDLE_BUTTON, "title": "Middle Mouse", "device": "mouse"},
    2: {"y": -50, "title": "Move Up", "device": "mouse"},
    5: {"x": -50, "title": "Move Left", "device": "mouse"},
    7: {"x": 50, "title": "Move Right", "device": "mouse"},
    10: {"y": 50, "title": "Move Down", "device": "mouse"},
    4: {"wheel": 3, "title": "Scroll Up", "device": "mouse"},
    8: {"wheel": -3, "title": "Scroll Down", "device": "mouse"},
    12: {
        "code": Keycode.CONTROL,
        "title": "Shoot",
        "colours": (255, 255, 0),
        "device": "keyboard",
    },
    13: {
        "code": Keycode.W,
        "title": "Forward",
        "colours": (255,255,0),
        "device":"keyboard",
    }
}

non_standard_keys = {
    # Used for keys not typically present on a keyboard.
    4: {"codes": Keycode.F13, "title": "F13", "device": "keyboard"},
    5: {"codes": Keycode.F14, "title": "F14", "device": "keyboard"},
    6: {"codes": Keycode.F15, "title": "F15", "device": "keyboard"},
    7: {"codes": Keycode.F16, "title": "F16", "device": "keyboard"},
    8: {"codes": Keycode.F17, "title": "F17", "device": "keyboard"},
    9: {"codes": Keycode.F18, "title": "F18", "device": "keyboard"},
    10: {"codes": Keycode.F19, "title": "F19", "device": "keyboard"},
    11: {"codes": Keycode.F20, "title": "F20", "device": "keyboard"},
    12: {"codes": Keycode.F21, "title": "F21", "device": "keyboard"},
    13: {"codes": Keycode.F22, "title": "F22", "device": "keyboard"},
    14: {"codes": Keycode.F23, "title": "F23", "device": "keyboard"},
    15: {"codes": Keycode.F24, "title": "F24", "device": "keyboard"},
}

soundboard = {
    # Used in Resanance. To use, enable Midi Support in options
    # and use the CircuitPython Audio device as the midi input.
    # Afterwards, use the buttons to set your hotkeys.
    # Can use either codes or piano keys as string. It will decode it and send it.
    # Use single notes. Chords not supported yet.
    1: {"note": 1, "title": "Rizz Sounds", "device": "midi"},
    2: {"note": 2, "title": "Metal Pipe Sound", "device": "midi"},
    3: {"note": 3, "title": "Four Big Buys", "device": "midi"},
    4: {"note": 4, "title": "Fake Discord Ping", "device": "midi"},
    5: {"note": 5, "title": "Among Us Role Reveal", "device": "midi"},
    6: {"note": 6, "title": "Penguin0", "device": "midi"},
    11: {"note": 7, "title": "Spongebob Fail", "device": "midi"},
    8: {"note": 8, "title": "WTHOMG", "device": "midi"},
    9: {"note": 9, "title": "Goofy Ahh Car", "device": "midi"},
    10: {"note": 10, "title": "Fart Reverb", "device": "midi"},
    7: {"note": 11, "title": "Giga Chad Theme", "device": "midi"},
    12: {"note": 12, "title": "bruh", "device": "midi"},
    13: {"note": 13, "title": "Vine Boom", "device": "midi"},
    14: {"note": 14, "title": "Stop Playback", "device": "midi"},
    15: {"note": 15, "title": "(Un)Pause Playback", "device": "midi"},
}

google_sheets = {
    12: {"title":"Paste link in cell",
         "device":"keyboard",
         "codes":(Keycode.END,
                  {Keycode.SHIFT, Keycode.HOME},
                  {Keycode.CONTROL, Keycode.K},
                  {Keycode.CONTROL, Keycode.V},
                  0.5,
                  Keycode.ENTER,
                  ),

             },
    13: {"title":"Search Karaoke",
         "device":"keyboard",
         "codes":({Keycode.CONTROL, Keycode.A},
             {Keycode.CONTROL, Keycode.V},
                Keycode.SPACE,
                  "karaoke",
                Keycode.ENTER),
        },
    9: {"title":"Search Lyrics",
         "device":"keyboard",
         "codes":({Keycode.CONTROL, Keycode.A},
             {Keycode.CONTROL, Keycode.V},
                Keycode.SPACE,
                  "lyrics",
                Keycode.ENTER),
        },
    8: {"title": "Copy cell data",
        "device":"keyboard",
        "codes":(Keycode.HOME,
                  {Keycode.SHIFT, Keycode.END},
                  {Keycode.SHIFT, Keycode.RIGHT_ARROW},
                  {Keycode.SHIFT, Keycode.RIGHT_ARROW},
                  {Keycode.CONTROL, Keycode.C},
                  Keycode.RIGHT_ARROW,
                  Keycode.UP_ARROW,
                  ),},
    10: {"title": "Copy next cell data",
        "device":"keyboard",
        "codes":(Keycode.DOWN_ARROW,
                  Keycode.HOME,
                  {Keycode.SHIFT, Keycode.END},
                  {Keycode.SHIFT, Keycode.RIGHT_ARROW},
                  {Keycode.SHIFT, Keycode.RIGHT_ARROW},
                  {Keycode.CONTROL, Keycode.C},
                  Keycode.RIGHT_ARROW,
                  Keycode.UP_ARROW,
                  ),
        },
    14: {"title":"Paste, Select and Add Video",
         "device":"keyboard",
         "codes":(
             Keycode.TAB,
             Keycode.TAB,
             {Keycode.CONTROL, Keycode.V},
             Keycode.ENTER,
             1.5,
             Keycode.SPACE,
             Keycode.TAB,
             Keycode.TAB,
             Keycode.ENTER,
             )
         },
    15: {"title":"Semi Full Auto",
         "device":"keyboard",
         "codes":(
             Keycode.TAB,
             Keycode.TAB,
             {Keycode.CONTROL, Keycode.V},
             Keycode.ENTER,
             1.5,
             Keycode.SPACE,
             Keycode.TAB,
             Keycode.TAB,
             Keycode.ENTER,
             {Keycode.WINDOWS, Keycode.LEFT_ARROW},
             Keycode.END,
            {Keycode.SHIFT, Keycode.HOME},
            {Keycode.CONTROL, Keycode.K},
            {Keycode.CONTROL, Keycode.V},
            0.5,
            Keycode.ENTER,
            Keycode.DOWN_ARROW,
            Keycode.HOME,
            {Keycode.SHIFT, Keycode.END},
            {Keycode.SHIFT, Keycode.RIGHT_ARROW},
            {Keycode.SHIFT, Keycode.RIGHT_ARROW},
            {Keycode.CONTROL, Keycode.C},
            Keycode.RIGHT_ARROW,
            Keycode.UP_ARROW,
             )
         },
    2: {"title":"Niri: Move up",
        "device":"keyboard",
        "codes":(
            {Keycode.WINDOWS, Keycode.UP_ARROW},)},
    5: {"title":"Niri: Move left",
        "device":"keyboard",
        "codes":(
            {Keycode.WINDOWS, Keycode.LEFT_ARROW},)},
    6: {"title":"Niri: Move down",
        "device":"keyboard",
        "codes":(
            {Keycode.WINDOWS, Keycode.DOWN_ARROW},)},
    7: {"title":"Niri: Move right",
        "device":"keyboard",
        "codes":(
            {Keycode.WINDOWS, Keycode.RIGHT_ARROW},)},
    }

# # Store all 3 above into one dict for easy management
layer_details = {
    1: {"layer_data":vlc_obs, "layer_colour":(255, 255, 255), "layer_title":"VLC & OBS"},
    2: {"layer_data":webex, "layer_colour":(0, 0, 255), "layer_title":"Webex Meetings"},
    3: {"layer_data":media_keys, "layer_colour":(255, 255, 0), "layer_title":"Media Keys"},
    4: {"layer_data":miscellaneous, "layer_colour":(232, 160, 152), "layer_title":"Misc. Functions"},
    5: {"layer_data":excel, "layer_colour":(0, 255, 0), "layer_title":"Excel Functions"},
    6: {"layer_data":pure_obs, "layer_colour":(255, 128, 255), "layer_title":"Pure OBS"},
    7: {"layer_data":google_meet, "layer_colour":(48, 168, 80), "layer_title":"Google Meet"},
    8: {"layer_data":obsidian, "layer_colour":(127, 106, 215), "layer_title":"Obsidian Notes"},
    9: {"layer_data":mouse_functions, "layer_colour":(59, 59, 59), "layer_title":"1$ Mouse"},
    10: {"layer_data":soundboard, "layer_colour":(0, 128, 0), "layer_title":"Meme Soundboard"},
    15: {"layer_data":non_standard_keys, "layer_colour":(255, 255, 0), "layer_title":"Extra Keys"},
    11: {"layer_data":data_numpad,"layer_colour":(100,119,141), "layer_title":"Data Numpad"},
    12: {"layer_data":google_sheets, "layer_colour":(0,0,255), "layer_title":"Google Sheets"},
}


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

# Function for choosing which color the keys will use. If there is a custom colour, it will take priority.
def key_colours(key, current_layer):
    """Returns a tuple of a given key's colour. Uses default layer colour but will also use custom colours if present."""
    try:
        return layers[current_layer][key]["colours"]
    except KeyError:
        return colours[current_layer] if key in layers[current_layer] else (0, 0, 0)


def current_layer_colours(current_layer, keys):
    """Returns the key colours for all keys in a current layer."""
    return [key_colours(k, current_layer) for k in keys]


def layer_key_descriptions(layer: int):
    """Returns the titles of the current layer's keys as a dict."""
    return get_dict(layers[layer], "title")
#
# with open('./layout.json',"rb") as json_data:
#     # Strip whitespace
#     layer_details = json_data.read().strip()
#     layer_details = json_deserialise(layer_details)

layers = get_dict(layer_details, "layer_data")

layer_titles = get_dict(layer_details, "layer_title")

colours = get_dict(layer_details, "layer_colour")

