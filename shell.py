import tkinter as tk
import pyautogui
import threading
import time
import math
import random
import subprocess
import sys
from PIL import Image, ImageTk
from pynput import mouse, keyboard  # MUST HAVE: pip install pynput

class ShellShockUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg="white")

        # --- WINDOW SIZE & POSITION ---
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.curr_x = self.screen_w - 360
        self.curr_y = self.screen_h - 250
        self.root.geometry(f"350x200+{self.curr_x}+{self.curr_y}")

        # --- THE FACE (Emoji Only) ---
        self.pet_label = tk.Label(self.root, text="🐱", font=("Segoe UI Emoji", 60), bg="white")
        self.pet_label.place(relx=0.8, rely=0.5, anchor="center")

        # --- SPEECH BUBBLE ---
        self.speech_bubble = tk.Label(
            self.root, text="", font=("Verdana", 9, "italic"),
            bg="#2C3E50", fg="#ECF0F1", 
            wraplength=190,
            padx=12, pady=8, justify="left"
        )
        self.speech_bubble.place(x=10, rely=0.35)
        self.speech_bubble.lower()

        # --- SMART ACTIVITY TRACKING ---
        self.last_activity_time = time.time()
        self.is_distracted = False 
        self.angle = 0.0

        # Start Input Listeners (Scroll, Key, Click, Move)
        self.start_input_listeners()
        
        self.setup_interactions()
        
        # Start Threads
        threading.Thread(target=self.idle_monitor, daemon=True).start()
        self.float_animation()

    def reset_timer(self, *args):
        """Resets the idle timer whenever you do ANYTHING."""
        self.last_activity_time = time.time()

    def start_input_listeners(self):
        """Listens for ANY user activity (Scroll, Type, Click)."""
        # Mouse Listener (Moves, Clicks, Scrolls)
        self.mouse_listener = mouse.Listener(
            on_move=self.reset_timer,
            on_click=self.reset_timer,
            on_scroll=self.reset_timer  # <--- This fixes the scrolling issue
        )
        
        # Keyboard Listener (Any key press)
        self.key_listener = keyboard.Listener(
            on_press=self.reset_timer
        )

        self.mouse_listener.start()
        self.key_listener.start()

    def update_face(self, emoji, message):
        """Called by the Brain to update the face and text."""
        if self.is_distracted: return 
        
        self.pet_label.config(text=emoji)
        
        if message:
            self.speech_bubble.config(text=message)
            self.speech_bubble.lift()
            # Bubble stays for 5 seconds
            self.root.after(5000, lambda: self.speech_bubble.lower())

    def trigger_punishment(self):
        """Hides the face and launches Flappy Bird."""
        if self.is_distracted: return
        self.is_distracted = True
        
        self.pet_label.config(text="🚀")
        self.speech_bubble.config(text="Bye bye! See you after the break.")
        self.root.update()
        time.sleep(1)
        
        self.root.withdraw() 
        
        try:
            # Launch Flappy Bird 
            subprocess.run([sys.executable, "flappy-bird-main/main.py"])
        except Exception as e:
            print(f"Game Error: {e}")

        self.root.deiconify() 
        self.is_distracted = False
        self.last_activity_time = time.time() 
        self.update_face("🐱", "Hope that reset your brain.")

    def idle_monitor(self):
        """Checks if user has been 100% idle for 20s."""
        while True:
            time.sleep(1)
            if self.is_distracted: continue

            # Check time elapsed since last activity
            idle_duration = time.time() - self.last_activity_time

            if idle_duration >= 60:
                self.pet_label.config(text="😴")
                # Trigger shake every 5 seconds if still idle
                if int(idle_duration) % 5 == 0: 
                    self.shake_effect() 

    def shake_effect(self):
        """Captures the screen and shakes it."""
        try:
            screenshot = pyautogui.screenshot()
            w, h = screenshot.size
            screenshot_tk = ImageTk.PhotoImage(screenshot)

            top = tk.Toplevel(self.root)
            top.overrideredirect(True)
            top.attributes("-topmost", True)
            top.geometry(f"{w}x{h}+0+0")
            
            label = tk.Label(top, image=screenshot_tk, borderwidth=0)
            label.pack()
            label.image = screenshot_tk 
            
            # Shake Loop
            for _ in range(20):
                dx = random.randint(-15, 15)
                dy = random.randint(-15, 15)
                top.geometry(f"+{dx}+{dy}") 
                top.update()
                time.sleep(0.02)
                
            top.destroy()
        except Exception as e:
            print(f"Shake failed: {e}")

    def float_animation(self):
        self.angle += 0.08
        offset = int(12 * math.sin(self.angle))
        self.root.geometry(f"+{self.curr_x}+{self.curr_y + offset}")
        self.root.after(40, self.float_animation)

    def setup_interactions(self):
        self.pet_label.bind("<Button-3>", lambda e: self.root.destroy())
        def start_drag(e): self.root.x, self.root.y = e.x, e.y
        def do_drag(e):
            self.curr_x = self.root.winfo_pointerx() - self.root.x
            self.curr_y = self.root.winfo_pointery() - self.root.y
            self.root.geometry(f"+{self.curr_x}+{self.curr_y}")
        self.pet_label.bind("<ButtonPress-1>", start_drag)
        self.pet_label.bind("<B1-Motion>", do_drag)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ShellShockUI().run()