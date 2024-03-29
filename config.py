# InsomniaDriver Configuration File

# -- DROWSY THRESHOLDS

ear_threshold = 0.18
wait_time_threshold = 1.0

# -- FONT

# 'sys' (system font) or 'file' (eg. ttf file)
# any other value = default font
font_type = "file"
font_size = 24
font_antialias = True
font = "assets/CozetteVector.ttf"

# -- COLORS

red = (255, 50, 50)
green = (100, 255, 100)
blue = (80, 80, 255)
lightblue = (100, 100, 255)
lightred = (255, 100, 100)

white = (250, 250, 250)
gray = (100, 100, 100)
shadow = (10, 10, 10)
black = (0, 0, 0)

# -- USER INPUT MODE

# 'keyboard' = get user input from the keyboard
#   - X to disable alarm
#   - Q to quit application

# 'rpi' = get user input from RPi's GPIO pins
#   - button press on selected pin to disable alarm

input_mode = "keyboard"
input_pin = 21

# -- ALARM

ALARMTYPE_SOUND = 0
ALARMTYPE_LED = 1

alarm_mode = ALARMTYPE_LED
alarm_sound = "assets/alarm.ogg"
alarm_led_pin = 20

# -- VIDEO MODES

# first is the highest priority, last is the lowest
# if no mode from this list maches, first is the default
supported_video_modes = [
    (1280, 720),
    (800, 480)
]
