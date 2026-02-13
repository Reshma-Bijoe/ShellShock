import tkinter as tk
from tkinter import simpledialog, messagebox # <--- Added messagebox
import pyautogui
import threading
import time
import math
import random
import subprocess
import sys
import os 
from pynput import mouse, keyboard

class ShellShockUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "white")
        self.root.config(bg="white")

        # --- WINDOW SIZE ---
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.curr_x = self.screen_w - 360
        self.curr_y = self.screen_h - 250
        self.root.geometry(f"350x200+{self.curr_x}+{self.curr_y}")

        # --- THE FACE ---
        self.pet_label = tk.Label(self.root, text="😺", font=("Segoe UI Emoji", 60), bg="white")
        self.pet_label.place(relx=0.8, rely=0.5, anchor="center")
        self.pet_label.config(cursor="hand2") 

        # --- THE COUNTDOWN TIMER ---
        self.timer_label = tk.Label(
            self.root, text="00:00", font=("Consolas", 16, "bold"), 
            fg="red", bg="white"
        )
        self.timer_label.place(relx=0.8, rely=0.85, anchor="center")
        self.timer_label.place_forget() 

        # --- SPEECH BUBBLE ---
        self.speech_bubble = tk.Label(
            self.root, text="", font=("Verdana", 9, "italic"),
            bg="#2C3E50", fg="#ECF0F1", 
            wraplength=190,
            padx=12, pady=8, justify="left"
        )
        self.speech_bubble.place(x=10, rely=0.35)
        self.speech_bubble.lower()

        # --- STATE ---
        self.last_activity_time = time.time()
        self.is_distracted = False 
        self.angle = 0.0

        self.start_input_listeners()
        self.setup_interactions()
        
        threading.Thread(target=self.idle_monitor, daemon=True).start()
        self.float_animation()

    def ask_slack_limit_safe(self):
        self.popup_result = 300 
        self.popup_finished = threading.Event() 

        def show_popup_on_main_thread():
            self.root.withdraw() 
            minutes = simpledialog.askinteger(
                "YouTube Allowance", 
                "Distraction Detected!\nHow many minutes do you need?",
                parent=self.root,
                minvalue=1, maxvalue=120, initialvalue=5
            )
            self.root.deiconify() 
            if minutes:
                self.popup_result = minutes * 60
            self.popup_finished.set() 

        self.root.after(0, show_popup_on_main_thread)
        self.popup_finished.wait()
        return self.popup_result

    def reset_timer(self, *args):
        self.last_activity_time = time.time()

    def start_input_listeners(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.reset_timer, on_click=self.reset_timer, on_scroll=self.reset_timer 
        )
        self.key_listener = keyboard.Listener(on_press=self.reset_timer)
        self.mouse_listener.start()
        self.key_listener.start()

    def update_face(self, emoji, message):
        if self.is_distracted: return 
        self.pet_label.config(text=emoji)
        if message:
            self.speech_bubble.config(text=message)
            self.speech_bubble.lift()
            self.root.after(5000, lambda: self.speech_bubble.lower())

    def update_stopwatch(self, seconds_left):
        if seconds_left < 0: seconds_left = 0
        mins, secs = divmod(int(seconds_left), 60)
        time_str = f"{mins:02}:{secs:02}"
        self.timer_label.config(text=time_str)
        self.timer_label.place(relx=0.8, rely=0.85, anchor="center") 

    def hide_stopwatch(self):
        self.timer_label.place_forget()

    def manual_game_launch(self):
        # If user clicks, we play the GAME (Manual = True)
        self.trigger_punishment(manual=True)

    def trigger_punishment(self, manual=False):
        if self.is_distracted: return
        self.is_distracted = True
        self.hide_stopwatch() 
        
        # --- SCENARIO 1: MANUAL GAME (Clicking the Pet) ---
        if manual:
            self.pet_label.config(text="🎮")
            self.speech_bubble.config(text="Launching Game...")
            self.root.update()
            time.sleep(1)
            
            self.root.withdraw() 
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                game_folder = os.path.join(base_path, "flappy-bird-main")
                if not os.path.exists(game_folder): raise FileNotFoundError(f"Missing: {game_folder}")

                subprocess.run([sys.executable, "main.py"], cwd=game_folder, check=True)
                
                self.root.deiconify() 
                self.update_face("😹", "Game Over!")
                time.sleep(3) # Short wait for manual play
            except Exception as e:
                self.root.deiconify()
                self.update_face("😿", f"Error: {str(e)[:20]}...")

        # --- SCENARIO 2: AUTOMATIC PUNISHMENT (Time's Up) ---
        else:
            self.pet_label.config(text="🛑") # Stop Sign or Angry Face
            self.speech_bubble.config(text="Time's Up!")
            self.root.update()
            
            # --- THE POPUP (Instead of Game) ---
            messagebox.showwarning(
                "Time's Up!", 
                "You have exceeded your break limit.\nClose YouTube and get back to work!"
            )
            
        # Reset State
        self.is_distracted = False
        self.last_activity_time = time.time() 
        self.update_face("😺", "Okay, back to work.")

    def idle_monitor(self):
        while True:
            time.sleep(1)
            if self.is_distracted: continue
            idle_duration = time.time() - self.last_activity_time
            if idle_duration >= 60:
                self.pet_label.config(text="😴")
                if int(idle_duration) % 5 == 0: self.shake_effect() 

    def shake_effect(self):
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
            for _ in range(20):
                dx = random.randint(-15, 15)
                dy = random.randint(-15, 15)
                top.geometry(f"+{dx}+{dy}") 
                top.update()
                time.sleep(0.02)
            top.destroy()
        except: pass

    def float_animation(self):
        self.angle += 0.08
        offset = int(12 * math.sin(self.angle))
        self.root.geometry(f"+{self.curr_x}+{self.curr_y + offset}")
        self.root.after(40, self.float_animation)

    def setup_interactions(self):
        self.pet_label.bind("<Button-3>", lambda e: self.root.destroy())
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.has_moved = False

        def start_drag(e):
            self.drag_start_x = e.x_root
            self.drag_start_y = e.y_root
            self.has_moved = False
            self.root.x = e.x
            self.root.y = e.y

        def do_drag(e):
            if abs(e.x_root - self.drag_start_x) > 5 or abs(e.y_root - self.drag_start_y) > 5:
                self.has_moved = True
            self.curr_x = self.root.winfo_pointerx() - self.root.x
            self.curr_y = self.root.winfo_pointery() - self.root.y
            self.root.geometry(f"+{self.curr_x}+{self.curr_y}")

        def stop_drag(e):
            if not self.has_moved:
                self.manual_game_launch()

        self.pet_label.bind("<ButtonPress-1>", start_drag)
        self.pet_label.bind("<B1-Motion>", do_drag)
        self.pet_label.bind("<ButtonRelease-1>", stop_drag)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ShellShockUI().run()