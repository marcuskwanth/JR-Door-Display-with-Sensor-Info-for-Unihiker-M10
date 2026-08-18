# DEVICE: UNIHIKER M10
# REFERENCE: https://www.unihiker.com.cn/wiki/m10/unihiker_python_lib_1

import time
import cv2
import requests
import random
from datetime import datetime
from PIL import Image
from unihiker import GUI
from pinpong.board import Board, Pin, I2C
from pinpong.extension.unihiker import light, buzzer, button_a, button_b

from stop_list import jp_y, kana_y, en_y, stations
from openweather_info import opw_url    # Add openweather_info.py separately and add the OpenWeather API key in there
from weather_codes import weather_codes
from ani_quotes import quotes

Board().begin()
gui = GUI()
width, height = 240, 320

# Camera capture for camera overlay
def camera_init():
    global camera_capture
    camera_capture = cv2.VideoCapture(0)
    camera_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

camera_init()
camera_view = None
middle_panel_height = 200
middle_panel_y = 70

# Initialize I2C
i2c = I2C(bus_num=0) 
SHT4X_ADDR = 0x44

# Configurations
BG_COLOR = "#1F1F30"
LINE_COLOR = "#9BCB45" # Yamanote Green
CAR_NO = "8"

# Global Variables
middle_panel_objects = []
last_weather_update = 0
last_sensor_update = 0
cur_weather_cond = ["---", "---"]
cur_sensor_temp = 0.0
cur_sensor_humi = 0.0
station_index = 0                   # Current station index in the stations list
station_display_index = 0           # Current display layout index (0, 1, or 2)
dest_index = 0
last_station_change = time.time()
display_version = 0                 # Display version counter to track changes and trigger updates
button_a_pressed = False            # Flag to indicate if the button A is toggled (panel 3 or 4)
button_b_pressed = False            # Flag to indicate if the button B is toggled (camera overlay)

# ===== 1. Header Panel ===== 
# Top bar
gui.fill_rect(x=0, y=0, w=width, h=70, color=BG_COLOR)
gui.fill_rect(x=80, y=2, w=13, h=65, color=LINE_COLOR)

# Left side
destination_en1 = gui.draw_text(x=5, y=22, text="---", color="white", font_size=6)
destination_en2 = gui.draw_text(x=5, y=21, text="---", color="white", font_size=8)
destination_jp1 = gui.draw_text(x=5, y=16, text="", color="white", font_size=10)
destination_jp2 = gui.draw_text(x=52, y=22, text="", color="white", font_size=8)
#line_type = gui.draw_text(x=10, y=25, text="LOCAL 各駅", color="yellow", font_size=10)

# Right side
# Top section
next_station = gui.draw_text(x=98, y=3, text="---", color="white", font_size=8)
time_text = gui.draw_text(x=160, y=2, text="00:00", color="white", font_size=10)
car_no = gui.draw_text(x=227, y=0, text=CAR_NO, color="white", font_size=12)
car_no_jp = gui.draw_text(x=225, y=20, text="", color="white", font_size=5)
car_no_en = gui.draw_text(x=206, y=4, text="", color="white", font_size=4)

# Station's Acronym and JY Number Box
next_station_acy = gui.draw_text(x=115, y=24, text="---", color="white", font_size=7, origin="top")
gui.fill_rect(x=102, y=40, w=25, h=25, color="white")
gui.draw_rect(x=102, y=40, w=25, h=25, color=LINE_COLOR, width=3)
gui.draw_text(x=110, y=42, text="JY", color="black", font_size=6)
station_jy = gui.draw_text(x=108, y=48, text="--", color="black", font_size=9)

# Station Name Text
station_jp = gui.draw_text(x=140, y=jp_y, text="--", color="white", font_size=25, origin="left")
station_kana = gui.draw_text(x=140, y=kana_y, text="--", color="white", font_size=12, origin="left")
station_en = gui.draw_text(x=140, y=en_y, text="--", color="white", font_size=12, origin="left")

# ===== 2. Footer Panel ===== 
gui.draw_line(x0=0, y0=270, x1=250, y1=270, color="gray", width=1)

weather_text = gui.draw_text(x=10, y=274, text="---", color="blue", font_size=11)
humidity_text = gui.draw_text(x=230, y=274, text="---", color="green", font_size=11, origin="top_right")
g_force_text = gui.draw_text(x=10, y=298, text="---", color="orange", font_size=10)
weather_cond = gui.draw_text(x=230, y=298, text="---", color="#AC41CC", font_size=10, origin="top_right")

# ===== 3. Middle Information Panels ===== 
# Clear the middle panel using object list
def clear_middle_panel():
    global middle_panel_objects, camera_view
    for obj in middle_panel_objects:
        gui.remove(obj)
    middle_panel_objects.clear()
    camera_view = None

# Panel 1
def draw_layout_one(station):
    clear_middle_panel()
    border_x = 8
    border_y = 134
    border_w = 224
    border_h = 46
    
    # From top left box -> clockwise -> left vertical line
    obj = gui.fill_rect(x=border_x + 8, y=border_y + 8, w=10, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + 14, y=border_y + 2, w=border_w - 28, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + border_w - 18, y=border_y + 8, w=10, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + border_w - 14, y=border_y + 14, w=10, h=border_h - 26, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + border_w - 18, y=border_y + border_h - 17, w=10, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + 14, y=border_y + border_h - 12, w=border_w - 28, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + 8, y=border_y + border_h - 16, w=10, h=10, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.fill_rect(x=border_x + 4, y=border_y + 14, w=10, h=border_h - 26, color=LINE_COLOR)
    middle_panel_objects.append(obj)

    # Manually select 20 stations to display, with the index = JY - 1
    included_stations = [0,1,2,4,6,7,8,10,12,14,16,17,18,19,21,23,24,26,27,28] 
    
    # Calculating the white/yellow dots positions
    offsets = [
        (200, 36),
        (200, 4), (180, 4), (160, 4), (140, 4), (120, 4), (100, 4), (80, 4), (60, 4), (40, 4), (20, 4),
        (20, 36), (40, 36), (60, 36), (80, 36), (100, 36), (120, 36), (140, 36), (160, 36), (180, 36)
    ]
    dot_coords = [(border_x + dx, border_y + dy) for dx, dy in offsets]

    for i, station_idx in enumerate(included_stations):
        dot_x, dot_y = dot_coords[i]
        station_entry = station[station_idx]

        # For current station, mark the dot yellow
        is_current = (station_idx == station_index)
        obj = gui.fill_circle(x=dot_x+3, y=dot_y+3, r=3, color="yellow" if is_current else "white")
        middle_panel_objects.append(obj)

        # Deciding whether the position of station texts based on dots' positions
        if dot_y == border_y + 4: 
            text_y = dot_y - 6
            origin = "top_left"
        else:
            text_y = dot_y + 12
            origin = "top_right"

        obj = gui.draw_text(x=dot_x - 4, y=text_y, text=station_entry["kanji"], color="black", font_size=7, angle=90, origin=origin)
        middle_panel_objects.append(obj)

    obj = gui.draw_text(x=5, y=134 + 110, 
                        text="のりかえ、待合せ時間は含まれません。\n電車により多少時間が異なります。", color="black", font_size=5)
    middle_panel_objects.append(obj)

# Panel 2
def draw_layout_two(station):
    clear_middle_panel()
    line1_start_x, line1_start_y = 0, 88
    line1_end_x, line1_end_y = 50, 88
    line2_start_x, line2_start_y = line1_end_x, line1_end_y
    line2_end_x, line2_end_y = 150, 210
    line3_start_x, line3_start_y = line2_end_x, line2_end_y
    line3_end_x, line3_end_y = line2_end_x, 270
    line_w = 30

    # Diagonal line (from bottom to top)
    obj = gui.draw_line(x0=line1_start_x, y0=line1_start_y, x1=line1_end_x, y1=line1_end_y, color=LINE_COLOR, width=line_w)
    middle_panel_objects.append(obj)
    obj = gui.draw_line(x0=line2_start_x, y0=line2_start_y, x1=line2_end_x, y1=line2_end_y, color=LINE_COLOR, width=line_w)
    middle_panel_objects.append(obj)
    obj = gui.fill_circle(x=line1_end_x, y=line1_end_y, r=15, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    obj = gui.draw_line(x0=line3_start_x, y0=line3_start_y, x1=line3_end_x, y1=line3_end_y, color=LINE_COLOR, width=line_w)
    middle_panel_objects.append(obj)
    obj = gui.fill_circle(x=line2_end_x, y=line2_end_y, r=14, color=LINE_COLOR)
    middle_panel_objects.append(obj)
    
    dot_positions = [(150, 238), (135, 191), (100, 149), (65, 106), (18, 88)]
    for i, (dot_x, dot_y) in enumerate(dot_positions):
        obj = gui.fill_circle(x=dot_x, y=dot_y, r=12, color="yellow" if i == 0 else "white")
        middle_panel_objects.append(obj)
        
        # Decide the target station
        station_entry = station[(station_index + i) % len(station)]
        
        if i == 0:
            label_x = dot_x + 22
        elif i == 1:
            label_x = dot_x + 34
        else:
            label_x = dot_x + 36
        label_y = dot_y

        #obj = gui.draw_text(x=label_x, y=label_y - 8, text=f"{station_entry['jy']}", color="black", font_size=8, origin="top_left")
        #middle_panel_objects.append(obj)
        
        # Estimated time in second
        obj = gui.draw_text(x=dot_x, y=dot_y, text=f"{(i+1)*2}", color="black", font_size=10, origin="center")
        middle_panel_objects.append(obj)
        
        # Not to write station name for the last dot
        if i == len(dot_positions)-1:
            break
        
        obj = gui.draw_text(x=label_x, y=label_y - 16, text=f"{station_entry['kanji']}", color="black", font_size=9, origin="top_left")
        middle_panel_objects.append(obj)
        obj = gui.draw_text(x=label_x, y=label_y + 0, text=f"{station_entry['en']}", color="black", font_size=7, origin="top_left")
        middle_panel_objects.append(obj)

    obj = gui.draw_line(x0=line3_start_x-15, y0=263, x1=line3_start_x, y1=253, color="red", width=4)
    middle_panel_objects.append(obj)
    obj = gui.draw_line(x0=line3_start_x+14, y0=263, x1=line3_start_x, y1=253, color="red", width=4)
    middle_panel_objects.append(obj)
        
    obj = gui.draw_text(x=5, y=134 + 110, 
                        text="のりかえ、待合せ時間は含まれません。\n電車により多少時間が異なります。", color="black", font_size=5)
    middle_panel_objects.append(obj)
        
# Panel 3 (Default) and Panel 4 (after button toggle)
def draw_layout_three(quotes):
    clear_middle_panel()
    selected_quote = random.choice(quotes) # Draw random quote
    text_x = 12
    separator_x0 = 25
    separator_x1 = 215

    obj = gui.draw_text(x=120, y=83, text="Random Quote from Anime", color="red", font_size=10, origin="top")
    middle_panel_objects.append(obj)
    obj = gui.draw_line(x0=separator_x0, y0=105, x1=separator_x1, y1=105, color="red", width=1)
    middle_panel_objects.append(obj)
    obj = gui.draw_text(x=120, y=162, w=width-text_x-15, text=selected_quote["quote"], color="#0A3D0A", font_size=10, origin="center")
    middle_panel_objects.append(obj)
    obj = gui.draw_line(x0=separator_x0, y0=218, x1=separator_x1, y1=218, color="#C4C4C4", width=1)
    middle_panel_objects.append(obj)
    obj = gui.draw_text(x=120, y=223, w=width-text_x-15, text=selected_quote["name"], color="#0A3D0A", font_size=10, origin="top")
    middle_panel_objects.append(obj)
    
    # Alert box
    obj = gui.draw_rect(x=2, y=73, w=width-5, h=195, width=5, color="red")
    middle_panel_objects.append(obj)
    
def draw_camera_frame():
    global camera_view
    if camera_view is not None:
        return
    clear_middle_panel()

    placeholder = Image.new("RGB", (width, middle_panel_height), BG_COLOR)
    camera_view = gui.draw_image(x=0, y=middle_panel_y, w=width, h=middle_panel_height, image=placeholder)
    middle_panel_objects.append(camera_view)

def update_camera_frame():
    global camera_view
    if camera_view is None or not camera_capture.isOpened():
        camera_init()
        return

    ret, frame = camera_capture.read()
    if not ret:
        camera_init()
        return

    h, w, _ = frame.shape
    target_w = width
    target_h = middle_panel_height
    crop_w = min(w, h * target_w // target_h)
    if crop_w <= 0:
        return

    x1 = max(0, (w - crop_w) // 2)
    frame = frame[:, x1:x1 + crop_w]
    frame = cv2.resize(frame, (target_w, target_h))
    frame = cv2.convertScaleAbs(frame, alpha=1.0, beta=50)
    frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    camera_view.config(image=frame)

def draw_middle_display(station, quotes):
    if station_display_index == 0:
        draw_layout_one(station)
    elif station_display_index == 1:
        draw_layout_two(station)
    else:
        draw_layout_three(quotes)

# ===== Multi-threading Functions ===== 
def light_update():
    while True:
        try:
            g_force_text.config(text=f"{jp_or_en('光強度', 'Light')}: {light.read()}")
        except Exception:
            pass
        time.sleep(0.1)

def station_cycle_update():
    global station_index, station_display_index, last_station_change, display_version
    while True:
        # Check whether display cycles based on button b presses and time elapsed
        if not button_b_pressed and time.time() - last_station_change > 7:
            station_display_index = (station_display_index + 1) % 3
            if station_display_index == 0:
                station_index = (station_index + 1) % len(stations)
            display_version += 1
            last_station_change = time.time()
        time.sleep(0.1)

def update_station_display_thread():
    seen_version = -1
    while True:
        if display_version != seen_version:
            update_station_display(stations[station_index])
            seen_version = display_version
        time.sleep(0.1)

def update_destination_display_thread():
    seen_version = -1
    while True:
        if display_version != seen_version:
            update_destination_display(station_index)
            seen_version = display_version
        time.sleep(0.1)

def draw_middle_display_thread():
    seen_version = -1
    while True:
        # Camera overlay takes priority and stays visible on top of all panels.
        if button_a_pressed:
            if camera_view is None:
                draw_camera_frame()
            update_camera_frame()
            time.sleep(0.03)
            continue

        if display_version != seen_version:
            draw_middle_display(stations, quotes)
            seen_version = display_version
        time.sleep(0.1)
        
# ===== Weather / Sensor Functions ===== 
def update_weather_cond():
    global cur_weather_cond
    
    # Open Weather for condition
    try:
        response = requests.get(opw_url, timeout=10)
        data = response.json()
        cur_weather_cond = weather_codes.get(data['weather'][0]['id'], ['不明な天気', 'Unknown Weather'])
    except Exception as e:
        print("Error fetching weather condition:", e)

def update_sht4x_data():
    global cur_sensor_temp, cur_sensor_humi

    try:
        i2c.writeto(SHT4X_ADDR, [0xFD])
        time.sleep(0.02)

        data = i2c.readfrom(SHT4X_ADDR, 6)
        if len(data) != 6:
            raise ValueError("Incomplete data frame received")

        raw_temp = (data[0] << 8) | data[1]
        raw_hum = (data[3] << 8) | data[4]
        cur_sensor_temp = round(-45.0 + 175.0 * (raw_temp / 65535.0), 1)
        cur_sensor_humi = round(-6.0 + 125.0 * (raw_hum / 65535.0), 1)

    except Exception as e:
        print(f"SHT4X Read Error: {e}")
        cur_sensor_temp = 99.9
        cur_sensor_humi = 0

# ===== Helper Functions ===== 
def jp_or_en(jp_txt, en_txt):
    return jp_txt if station_display_index == 0 or station_display_index == 1 else en_txt

def update_station_display(station):
    next_station_acy.config(text=station["acy"] if "acy" in station else "")
    
    if station_display_index == 0:
        station_jp.config(text=station["kanji"], font_size=station["kanji_font"], y=station["kanji_y"] if "kanji_y" in station else jp_y)
        station_kana.config(text="")
        station_en.config(text="")
        next_station.config(text="つぎは")
        car_no_jp.config(text="号車")
        car_no_en.config(text="")
    elif station_display_index == 1:
        station_jp.config(text="")
        station_kana.config(text=station["kana"], font_size=station["kana_font"], y=station["kana_y"] if "kana_y" in station else kana_y)
        station_en.config(text="")
        next_station.config(text="つぎは")
        car_no_jp.config(text="号車")
        car_no_en.config(text="")
    else:
        station_jp.config(text="")
        station_kana.config(text="")
        station_en.config(text=station["en"], font_size=station["en_font"], y=station["en_y"] if "en_y" in station else en_y)
        next_station.config(text=" Next")
        car_no_jp.config(text="")
        car_no_en.config(text="Car No.")
    
    station_jy.config(text=station["jy"])
    
def update_destination_display(station_idx):
    if station_idx+1 in range(2,6):
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n上野・池袋")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nUeno & \nIkebukuro")
    elif station_idx+1 in range(6,14):
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n池袋・新宿")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nIkebukuro & \nShinjuku")
    elif station_idx+1 in range(14,18):
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n新宿・渋谷")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nShinjuku & \nShibuya")
    elif station_idx+1 in range(18,21):
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n渋谷・品川")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nShibuya & \nShinagawa")
    elif station_idx+1 in range(21,26):
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n品川・東京")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nShinagawa & \nTōkyō")
    else:
        if station_display_index == 0 or station_display_index == 1:
            destination_jp1.config(text="\n東京・上野")
            destination_jp2.config(text="\n\n方面")
            destination_en1.config(text="")
            destination_en2.config(text="")
        else:
            destination_jp1.config(text="")
            destination_jp2.config(text="")
            destination_en1.config(text="Bound for")
            destination_en2.config(text="\nTōkyō & \nUeno")

# ===== 6. Main Program Loop===== 
# Initialize the displays
gui.start_thread(station_cycle_update)
gui.start_thread(update_station_display_thread)
gui.start_thread(update_destination_display_thread)
gui.start_thread(draw_middle_display_thread)
gui.start_thread(light_update)

# buzzer.play(buzzer.POWER_UP, buzzer.Once)

while True:
    # ===== a. Update Clock =====
    current_time = datetime.now().strftime("%H:%M")
    time_text.config(text=current_time)
    
    # ===== b-1. Read Weather Info every minute (60 seconds) =====
    if time.time() - last_weather_update > 60:
        update_weather_cond()
        last_weather_update = time.time()

    # ===== b-2. Read SHT4X temperature when enabled (1 second) =====
    if time.time() - last_sensor_update > 1:
        update_sht4x_data()
        last_sensor_update = time.time()
       
    # ===== c. Perform updates on car_no based on the button_press status =====
    if button_a_pressed and button_b_pressed:
        car_no.config(text="5")
    elif button_a_pressed:
        car_no.config(text="3")
    elif button_b_pressed:
        car_no.config(text="4")
    else:
        car_no.config(text="8")
    
    humidity_text.config(text=f"{jp_or_en('湿度', 'Humi')}: {cur_sensor_humi}%")
    weather_text.config(text=f"{jp_or_en('温度', 'Temp')}: {cur_sensor_temp}°C")
    weather_cond.config(text=f"{jp_or_en(cur_weather_cond[0], cur_weather_cond[1])}")

    # ===== d. Toggle button A to show/hide the camera overlay on top of everything =====
    if button_a.is_pressed() == True:
        button_a_pressed = not button_a_pressed
        if button_a_pressed:
            draw_camera_frame()
        else:
            display_version += 1
        time.sleep(0.2)
        
    # ===== e. Toggle button B to pause the middle panel cycle =====
    if button_b.is_pressed() == True:
        button_b_pressed = not button_b_pressed
        time.sleep(0.2)

    # ===== NOTE: Light reading, station cycles, updating station/destination/middle panel are done by threads! =====

    time.sleep(0.1)