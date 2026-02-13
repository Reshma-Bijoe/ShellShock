import tkinter as tk
import pyautogui
import threading
import time
import random
import pygetwindow as gw
import game  # Integrates the 60s break game built by Partner A

# -------------------------
# PERSONALITY ENGINE
# -------------------------
def get_roast(category):
    """Returns a random roast or compliment based on activity."""
    roasts = {
        "slacking": [
            "Watching YouTube instead of coding? Groundbreaking.",
            "Is this what 'productivity' looks like to you?",
            "Your compiler is lonely. Get back to work.",
            "I'm not mad, just disappointed. Okay, I'm a little mad."
        ],
        "working": [
            "Finally, some actual code. Don't stop now.",
            "Wow, you actually remember how to use an IDE.",
            "Keep going, human. Those bugs won't write themselves.",
            "Terminal warrior detected. Respect +1."
        ]
    }
    return random.choice(roasts[category])

# -------------------------
# WINDOW SETUP
# -------------------------
mood = "happy"
root = tk.Tk()
root.overrideredirect(True)  # Makes window borderless
root.attributes("-topmost", True)  # Keeps pet always on top
root.config(bg="white")
root.attributes("-transparentcolor", "white")  # Creates the 'ghost' effect

window_width, window_height = 200, 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Initial position: bottom right
root.geometry(f"{window_width}x{window_height}+{screen_width-250}+{screen_height-300}")

pet_label = tk.Label(root, text="👁️", font=("Arial", 60), bg="white")
pet_label.pack(expand=True)

speech = tk.Label(root, text="", font=("Arial", 10), bg="yellow", wraplength=180)
speech.place(x=10, y=10)
speech.lower()

def show_speech(text):
    """Displays the speech bubble with roasts."""
    speech.config(text=text)
    speech.lift()
    root.after(4000, lambda: speech.lower())

def shake_window():
    """Intervention for 'The Stare-Down' analysis paralysis."""
    original_x = root.winfo_x()
    original_y = root.winfo_y()
    for _ in range(20):
        dx, dy = random.randint(-10, 10), random.randint(-10, 10)
        root.geometry(f"+{original_x + dx}+{original_y + dy}")
        root.update()
        time.sleep(0.02)
    root.geometry(f"+{original_x}+{original_y}")

# -------------------------
# INTEGRATED LOGIC LOOPS
# -------------------------
def active_monitor():
    """Tracks windows to roast slacking or trigger the break game."""
    global mood
    while True:
        try:
            title = gw.getActiveWindowTitle()
            if title:
                # Detection for "Social Media Rabbit Hole"
                if any(x in title for x in ["YouTube", "Chrome", "Reddit"]):
                    mood = "angry"
                    show_speech(get_roast("slacking"))
                    time.sleep(2)
                    root.withdraw()  # Hide pet during the game
                    game.start_break_game()  # Launches the 60s game
                    root.deiconify()  # Reappear after game force-closes
                    show_speech("Break over. Back to work!")
                
                # Detection for "Deep Work"
                elif any(x in title for x in ["Code", "Visual Studio", "Terminal"]):
                    mood = "happy"
                    if random.random() > 0.8:
                        show_speech(get_roast("working"))
            
            pet_label.config(text="👁️" if mood == "happy" else "😠")
            time.sleep(8)
        except: 
            pass

def idle_checker():
    """Detects inactivity to trigger the 'Shock' intervention."""
    last_pos = pyautogui.position()
    idle_time = 0
    while True:
        time.sleep(1)
        curr_pos = pyautogui.position()
        if curr_pos == last_pos:
            idle_time += 1
        else:
            idle_time = 0
            mood = "happy"
        last_pos = curr_pos

        if idle_time >= 15:  # Intervenes after 15 seconds of no mouse movement
            mood = "angry"
            shake_window()
            show_speech("Stop staring! Do something!")
            idle_time = 0

# -------------------------
# INTERACTION & START
# -------------------------
def start_drag(e): root.x, root.y = e.x, e.y
def do_drag(e): root.geometry(f"+{root.winfo_pointerx()-root.x}+{root.winfo_pointery()-root.y}")

pet_label.bind("<ButtonPress-1>", start_drag)  # Drag pet around screen
pet_label.bind("<B1-Motion>", do_drag)
root.bind("<Button-3>", lambda e: root.destroy())  # Right-click kill switch

# Run threads for constant monitoring
threading.Thread(target=active_monitor, daemon=True).start()
threading.Thread(target=idle_checker, daemon=True).start()

root.mainloop()