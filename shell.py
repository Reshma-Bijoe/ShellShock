import tkinter as tk
import pyautogui
import threading
import time
import random

# -------------------------
# WINDOW SETUP
# -------------------------
mood = "happy"
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.config(bg="white")
root.attributes("-transparentcolor", "white")

window_width = 200
window_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = screen_width - window_width - 50
y = screen_height - window_height - 100

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# -------------------------
# PET BODY
# -------------------------

pet_label = tk.Label(root, text="👁️", font=("Arial", 60), bg="white")
pet_label.pack(expand=True)

# -------------------------
# SPEECH BUBBLE
# -------------------------

speech = tk.Label(
    root,
    text="",
    font=("Arial", 10),
    bg="yellow",
    wraplength=180,
    justify="center"
)
speech.place(x=10, y=10)
speech.lower()


def show_speech(text):
    speech.config(text=text)
    speech.lift()
    root.after(3000, lambda: speech.lower())


# -------------------------
# SHAKE FUNCTION
# -------------------------

def shake_window():
    original_x = root.winfo_x()
    original_y = root.winfo_y()

    for _ in range(20):
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        root.geometry(f"+{original_x + dx}+{original_y + dy}")
        root.update()
        time.sleep(0.02)

    root.geometry(f"+{original_x}+{original_y}")


# -------------------------
# IDLE DETECTION
# -------------------------

def idle_checker():
    global mood
    last_position = pyautogui.position()
    idle_time = 0

    while True:
        time.sleep(1)
        current_position = pyautogui.position()

        if current_position == last_position:
            idle_time += 1
        else:
            idle_time = 0
            mood = "happy"

        last_position = current_position

        if idle_time >= 10:
            mood = "angry"
            show_speech("Stop staring at the screen. Move.")
            shake_window()

        if idle_time >= 20:
            mood = "sleepy"
            show_speech("I'm bored... 😴")

        update_mood()

# -------------------------
# FLOATING ANIMATION
# -------------------------

def float_animation():
    direction = 1
    while True:
        for _ in range(10):
            current_y = root.winfo_y()
            root.geometry(f"+{root.winfo_x()}+{current_y + direction}")
            time.sleep(0.05)
        direction *= -1


# -------------------------
# DRAG MOVEMENT
# -------------------------

def start_drag(event):
    root.x = event.x
    root.y = event.y


def do_drag(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")


pet_label.bind("<ButtonPress-1>", start_drag)
pet_label.bind("<B1-Motion>", do_drag)


# -------------------------
# HIDDEN CLOSE
# -------------------------

def check_close(event):
    if event.x > window_width - 20 and event.y < 20:
        root.destroy()


root.bind("<Button-1>", check_close)

# -------------------------
# BLINK ANIMATION
# -------------------------

def blink_animation():
    while True:
        time.sleep(random.randint(3, 7))
        pet_label.config(text="😑")
        time.sleep(0.2)
        pet_label.config(text="👁️")


def update_mood():
    if mood == "happy":
        pet_label.config(text="👁️")
    elif mood == "angry":
        pet_label.config(text="😠")
    elif mood == "sleepy":
        pet_label.config(text="😴")

import pygetwindow as gw

def check_active_window():
    global mood
    while True:
        try:
            window = gw.getActiveWindowTitle()

            if window:
                if "Code" in window:
                    mood = "happy"
                    show_speech("Good. Keep coding.")
                elif "Chrome" in window:
                    mood = "angry"
                    show_speech("Why are you in Chrome?")
                elif "Command Prompt" in window or "Terminal" in window:
                    mood = "happy"
                    show_speech("Terminal warrior detected.")
            
            update_mood()
            time.sleep(8)

        except:
            pass

# -------------------------
# START THREADS
# -------------------------

idle_thread = threading.Thread(target=idle_checker, daemon=True)
idle_thread.start()

float_thread = threading.Thread(target=float_animation, daemon=True)
float_thread.start()

blink_thread = threading.Thread(target=blink_animation, daemon=True)
blink_thread.start()

window_thread = threading.Thread(target=check_active_window, daemon=True)
window_thread.start()



# -------------------------
# RUN
# -------------------------

root.mainloop()
