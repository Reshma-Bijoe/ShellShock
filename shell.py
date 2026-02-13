
import tkinter as tk
import pyautogui
import threading
import time
import math
import random
import pygetwindow as gw
import game  # Integrates Partner A's game

class ShellShockUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg="white")

        # Layout Settings
        self.window_w, self.window_h = 280, 180
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.curr_x = self.screen_w - 300
        self.curr_y = self.screen_h - 250
        self.root.geometry(f"{self.window_w}x{self.window_h}+{self.curr_x}+{self.curr_y}")

        # --- UI ELEMENTS ---
        # The Pet (Floating Character)
        self.pet_label = tk.Label(self.root, text="👁️", font=("Segoe UI Emoji", 60), bg="white")
        self.pet_label.place(relx=0.7, rely=0.5, anchor="center")

        # Modern Dark Speech Bubble
        self.speech_bubble = tk.Label(
            self.root, text="", font=("Verdana", 9, "italic"),
            bg="#2C3E50", fg="#ECF0F1", wraplength=140,
            padx=12, pady=8, justify="left"
        )
        self.speech_bubble.place(x=10, rely=0.4)
        self.speech_bubble.lower() # Start hidden

        # --- STATE ---
        self.angle = 0.0
        self.mood = "happy"
        self.setup_interactions()
        
        # Start Threads
        threading.Thread(target=self.logic_loop, daemon=True).start()
        self.float_animation()
        self.root.mainloop()

    def show_speech(self, text):
        self.speech_bubble.config(text=text)
        self.speech_bubble.lift()
        # Auto-hide after 4 seconds
        self.root.after(4000, lambda: self.speech_bubble.lower())

    def float_animation(self):
        """Creates a smooth 'breathing' effect using a Sine wave."""
        self.angle += 0.08
        # Formula: y = A * sin(B * t)
        offset = int(12 * math.sin(self.angle))
        self.root.geometry(f"+{self.curr_x}+{self.curr_y + offset}")
        self.root.after(40, self.float_animation)

    def shake_effect(self):
        """Aggressive shake for interventions."""
        for _ in range(15):
            dx, dy = random.randint(-8, 8), random.randint(-8, 8)
            self.root.geometry(f"+{self.curr_x + dx}+{self.curr_y + dy}")
            self.root.update()
            time.sleep(0.01)

    def logic_loop(self):
        last_mouse = pyautogui.position()
        idle_seconds = 0
        
        while True:
            time.sleep(1)
            # 1. Window Monitoring (The Rabbit Hole)
            try:
                active_title = gw.getActiveWindowTitle()
                if active_title and any(x in active_title for x in ["YouTube", "Chrome", "Reddit", "Twitter"]):
                    self.pet_label.config(text="😠")
                    self.show_speech("Distraction detected. Initiating circuit breaker...")
                    time.sleep(2)
                    self.root.withdraw() # Hide pet
                    game.start_break_game() # Launch Partner A's game
                    self.root.deiconify() # Reappear
                    self.show_speech("Focus restored. Get back to work!")
                elif active_title and any(x in active_title for x in ["Code", "Studio", "Terminal"]):
                    self.pet_label.config(text="👁️")
            except: pass

            # 2. Idle Monitoring (The Stare-Down)
            curr_mouse = pyautogui.position()
            if curr_mouse == last_mouse:
                idle_seconds += 1
            else:
                idle_seconds = 0
            last_mouse = curr_mouse

            if idle_seconds >= 15:
                self.pet_label.config(text="😴")
                self.show_speech("WAKE UP! You've been staring at the screen forever.")
                self.shake_effect()
                idle_seconds = 0

    def setup_interactions(self):
        """Right-click to exit, Left-click to drag."""
        self.pet_label.bind("<Button-3>", lambda e: self.root.destroy())
        def start_drag(e): self.root.x, self.root.y = e.x, e.y
        def do_drag(e):
            self.curr_x = self.root.winfo_pointerx() - self.root.x
            self.curr_y = self.root.winfo_pointery() - self.root.y
            self.root.geometry(f"+{self.curr_x}+{self.curr_y}")
        self.pet_label.bind("<ButtonPress-1>", start_drag)
        self.pet_label.bind("<B1-Motion>", do_drag)

if __name__ == "__main__":
    ShellShockUI()