# OLD FILE

import time
import requests
from datetime import datetime
from unihiker import GUI
from pinpong.board import Board, Pin
from pinpong.extension.unihiker import accelerometer

# Initialize PinPong board for onboard sensors
Board().begin()

# Initialize Unihiker GUI (Default portrait 240x320)
gui = GUI()

# --- Configurations ---
LINE_COLOR = "#76B82A" # Yamanote Green
LATITUDE = 35.6762      # Change to your local latitude
LONGITUDE = 139.6503    # Change to your local longitude

# --- UI Layout Drawing (Portrait 240x320) ---

# 1. Header (0 to 50px)
gui.fill_rect(x=0, y=0, w=240, h=50, color=LINE_COLOR)
line_title = gui.draw_text(x=10, y=5, text="YAMANOTE LINE", color="white", font_size=11)
line_title_jp = gui.draw_text(x=10, y=25, text="山手線  LOCAL 各駅", color="yellow", font_size=11)

# 2. Main Body (Next Station Info - 55 to 240px)
next_label = gui.draw_text(x=10, y=60, text="NEXT", color="#FF5555", font_size=11)

# Next Station Kanji (Larger size works great on vertical screen)
station_jp = gui.draw_text(x=10, y=80, text="渋 谷", color="white", font_size=38)
station_kana = gui.draw_text(x=10, y=135, text="（しぶや）", color="gray", font_size=14)

# Next Station English & Destination
station_en = gui.draw_text(x=10, y=165, text="SHIBUYA", color="white", font_size=22)
destination_en = gui.draw_text(x=10, y=200, text="for Shinjuku & Ikebukuro", color="#A0A0A0", font_size=10)
destination_jp = gui.draw_text(x=10, y=218, text="新宿・池袋 方面", color="#A0A0A0", font_size=10)

# Divider line
gui.draw_line(x0=10, y0=242, x1=230, y1=242, color="gray", width=1)

# 3. Footer Area (245 to 320px - split into clean rows)
# Row 1: Time & Weather
time_text = gui.draw_text(x=10, y=250, text="00:00:00", color="white", font_size=13)
weather_text = gui.draw_text(x=125, y=251, text="Temp: --°C", color="cyan", font_size=11)

# Row 2: Tilt / G-Force Sensor Status
g_force_text = gui.draw_text(x=10, y=274, text="Tilt X: 0.00G", color="orange", font_size=11)

# Row 3: Running Status Ticker
status_scroller = gui.draw_text(x=10, y=298, text="運行情報: 平常運転 (Normal)", color="#55FF55", font_size=10)


# --- Helper Functions ---
def get_weather():
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        response = requests.get(url, timeout=3).json()
        temp = response['current_weather']['temperature']
        return f"OUT: {temp}°C"
    except Exception:
        return "OUT: Offline"

# Local station rotation database (To simulate train movement)
stations = [
    {"kanji": "渋 谷", "kana": "（しぶや）", "en": "SHIBUYA"},
    {"kanji": "原 宿", "kana": "（はらじゅく）", "en": "HARAJUKU"},
    {"kanji": "代々木", "kana": "（よよぎ）", "en": "YOYOGI"},
    {"kanji": "新 宿", "kana": "（しんじゅく）", "en": "SHINJUKU"}
]

# --- Main Program Loop ---
last_weather_update = 0
station_index = 0
last_station_change = time.time()

while True:
    # 1. Update Clock
    current_time = datetime.now().strftime("%H:%M:%S")
    time_text.config(text=current_time)
    
    # 2. Update Weather via API every 10 minutes (600 seconds)
    if time.time() - last_weather_update > 600:
        weather_info = get_weather()
        weather_text.config(text=weather_info)
        last_weather_update = time.time()
        
    # 3. Read Internal Accelerometer (Simulates Train "leaning/tilting")
    try:
        ax = accelerometer.get_x()
        g_force_text.config(text=f"Tilt X: {ax:.2f}G")
    except Exception:
        pass
        
    # 4. Simulate Train Moving to Next Station every 15 seconds
    if time.time() - last_station_change > 15:
        station_index = (station_index + 1) % len(stations)
        curr = stations[station_index]
        
        # Flash the "NEXT" label to simulate arriving/departing
        next_label.config(color="yellow")
        time.sleep(0.5)
        next_label.config(color="#FF5555")
        
        # Update UI texts
        station_jp.config(text=curr["kanji"])
        station_kana.config(text=curr["kana"])
        station_en.config(text=curr["en"])
        
        last_station_change = time.time()

    time.sleep(0.2) # Update interval
