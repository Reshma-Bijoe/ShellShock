import tkinter as tk
from tkinter import simpledialog, messagebox 
import pyautogui
import threading
import time
import math
import random
import subprocess
import sys
import os 
from pynput import mouse, keyboard
from PIL import Image, ImageTk

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

        # --- QUIT BUTTON ---
        self.quit_btn = tk.Button(
            self.root, text="X", font=("Arial", 8, "bold"), 
            bg="black", fg="white", bd=0, padx=5, pady=0, cursor="hand2",
            activebackground="#333333", activeforeground="white",
            command=self.quit_program
        )
        self.quit_btn.place(relx=0.98, rely=0.02, anchor="ne")
        self.quit_btn.lift()

        # --- THE TIMER LABEL ---
        self.timer_label = tk.Label(
            self.root, text="00:00", font=("Consolas", 16, "bold"), 
            fg="red", bg="white"
        )
        self.timer_label.place(relx=0.8, rely=0.85, anchor="center")

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
        self.mouse_listener = None
        self.key_listener = None
        
        # --- POMODORO VARIABLES ---
        self.is_focus_mode = True
        self.focus_duration = 25 * 60 
        self.break_duration = 5 * 60  
        self.current_timer = self.focus_duration
        self.timer_running = False

        self.start_input_listeners()
        self.setup_interactions()
        
        # Start Background Threads
        threading.Thread(target=self.idle_monitor, daemon=True).start()
        self.float_animation()
        
        # --- STARTUP SEQUENCE ---
        self.root.after(100, self.setup_pomodoro)

    def setup_pomodoro(self):
        """Asks user for Focus and Break times, then starts the timer."""
        self.root.withdraw()
        
        f_min = simpledialog.askinteger("Pomodoro Setup", "Enter Focus Time (minutes):", 
                                       parent=self.root, minvalue=1, maxvalue=120, initialvalue=25)
        b_min = simpledialog.askinteger("Pomodoro Setup", "Enter Break Time (minutes):", 
                                       parent=self.root, minvalue=1, maxvalue=60, initialvalue=5)
        
        self.root.deiconify()
        
        if f_min: self.focus_duration = f_min * 60
        if b_min: self.break_duration = b_min * 60
        
        self.current_timer = self.focus_duration
        self.is_focus_mode = True
        self.timer_running = True
        
        self.update_face("😺", f"Let's focus for {f_min} mins!")
        self.run_timer_tick()

    def run_timer_tick(self):
        """Main timer loop handling Focus/Break logic."""
        if not self.timer_running: return

        # Update Display
        mins, secs = divmod(self.current_timer, 60)
        self.timer_label.config(text=f"{mins:02}:{secs:02}")
        
        # Color Logic: Red for Focus, Green for Break
        color = "red" if self.is_focus_mode else "green"
        self.timer_label.config(fg=color)

        if self.current_timer > 0:
            self.current_timer -= 1
            self.root.after(1000, self.run_timer_tick)
        else:
            self.switch_mode()

    def switch_mode(self):
        """Switches between Focus and Break modes."""
        if self.is_focus_mode:
            # Focus Just Ended -> ASK THE USER WHAT TO DO
            self.timer_running = False # Pause timer while asking
            self.show_break_options()
        else:
            # Break Just Ended -> Auto-switch to Focus
            self.start_focus_mode()

    def show_break_options(self):
        """Shows a custom dialog for Break Options: Rest, Play, or Continue."""
        self.is_distracted = True # Pause idle checks
        
        # Create a custom popup window
        popup = tk.Toplevel(self.root)
        popup.title("Time's Up!")
        popup.geometry("300x180")
        
        # Center the popup on screen
        x = (self.screen_w // 2) - 150
        y = (self.screen_h // 2) - 90
        popup.geometry(f"+{x}+{y}")
        popup.attributes("-topmost", True)
        popup.grab_set() # Make modal (disable main window interaction)

        label = tk.Label(popup, text="Good Job! Focus Session Complete.\nWhat would you like to do?", 
                        font=("Arial", 10), pady=10)
        label.pack()

        # Option 1: Take a Rest (Start Break Timer)
        def on_rest():
            popup.destroy()
            self.is_distracted = False
            self.start_break_mode()
        
        # Option 2: Play Game (Launch Flappy Bird)
        def on_play():
            popup.destroy()
            # Launch game, then go back to Focus (Game acts as the break)
            self.manual_game_launch(next_mode="focus") 

        # Option 3: Continue (Skip Break)
        def on_continue():
            popup.destroy()
            self.is_distracted = False
            self.start_focus_mode()

        btn_rest = tk.Button(popup, text="☕ Take a Rest", command=on_rest, width=20, bg="#ddffdd")
        btn_rest.pack(pady=5)

        btn_play = tk.Button(popup, text="🎮 Wanna Play?", command=on_play, width=20, bg="#ddddff")
        btn_play.pack(pady=5)

        btn_cont = tk.Button(popup, text="⏩ Continue Working", command=on_continue, width=20)
        btn_cont.pack(pady=5)

        # Handle window close (X button) same as Continue
        popup.protocol("WM_DELETE_WINDOW", on_continue)

    def start_break_mode(self):
        self.is_focus_mode = False
        self.current_timer = self.break_duration
        self.timer_running = True
        self.update_face("😎", "Time for a break!")
        self.run_timer_tick()

    def start_focus_mode(self):
        self.is_focus_mode = True
        self.current_timer = self.focus_duration
        self.timer_running = True
        self.update_face("😺", "Back to work!")
        self.run_timer_tick()

    def quit_program(self):
        """Safely stops listeners and force-kills the app."""
        print("Exiting ShellShock...")
        try:
            if self.mouse_listener: self.mouse_listener.stop()
            if self.key_listener: self.key_listener.stop()
        except: pass
        self.root.destroy()
        os._exit(0)

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
        try:
            self.pet_label.config(text=emoji)
            if message:
                self.speech_bubble.config(text=message)
                self.speech_bubble.lift()
                self.root.after(5000, lambda: self.speech_bubble.lower())
        except: pass

    def manual_game_launch(self, next_mode=None):
        """Launches the game. 
        Args:
            next_mode (str): 'focus' to start focus timer after game, None to stay idle.
        """
        self.trigger_punishment(manual=True, next_mode=next_mode)

    def trigger_punishment(self, manual=False, next_mode=None):
        if self.is_distracted and not manual: return 
        self.is_distracted = True
        
        # --- MANUAL GAME ---
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
                
                # --- EXE FIX: Determine which python to use ---
                if getattr(sys, 'frozen', False):
                    # If we are running as an .exe, use system python
                    python_executable = "python"
                else:
                    # If running from code, use the current interpreter
                    python_executable = sys.executable

                # Run the game
                subprocess.run([python_executable, "main.py"], cwd=game_folder, check=True)
                
                self.root.deiconify() 
                self.update_face("😹", "Game Over!")
                time.sleep(1)
            except Exception as e:
                self.root.deiconify()
                self.update_face("😿", f"Error: {str(e)[:20]}...")

        self.is_distracted = False
        self.last_activity_time = time.time() 
        
        if next_mode == "focus":
            self.start_focus_mode()
        elif self.is_focus_mode:
            self.update_face("😺", "Okay, back to work.")
        else:
            self.update_face("😎", "Chilling...")
    def idle_monitor(self):
        """Monitors for lack of mouse/keyboard activity."""
        while True:
            time.sleep(1)
            if self.is_distracted: continue
            idle_duration = time.time() - self.last_activity_time
            
            # If idle for > 60s during FOCUS mode, get angry/shake
            if idle_duration >= 60 and self.is_focus_mode:
                try:
                    self.pet_label.config(text="😴")
                    if int(idle_duration) % 5 == 0: 
                        self.root.after(0, self.shake_effect)
                except: pass

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
        except Exception as e:
            print(f"Shake error: {e}")

    def float_animation(self):
        try:
            self.angle += 0.08
            offset = int(12 * math.sin(self.angle))
            self.root.geometry(f"+{self.curr_x}+{self.curr_y + offset}")
            self.root.after(40, self.float_animation)
        except: pass

    def setup_interactions(self):
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