import pygetwindow as gw
import time
import game  
import random

def brain_loop():
    print("ShellShock is watching...")
    
    while True:
        title = gw.getActiveWindowTitle()
        
        # Logic: If user is on a "Slacking" site, trigger a prompt
        if title and "YouTube" in title:
            print("ALERT: Slacking detected! Would you like a 60s break instead?")
            # For now, we trigger it automatically for testing
            time.sleep(1)
            game.start_break_game()
            print("Break over. Monitoring resumed.")
            
        time.sleep(2)
class CatBrain:
    def __init__(self):
        # Cat-themed Roasts for slacking
        self.roasts = [
            "Meow-nimum effort detected. Get back to work!",
            "I've seen yarn balls with better logic than this code.",
            "Are you coding or just taking a digital cat nap?",
            "If I had nine lives, I'd spend zero of them watching you slack."
        ]
        
        # Cat-themed Compliments for working
        self.compliments = [
            "Purr-fect indentation! 🐾",
            "You're the cat's pajamas at debugging.",
            "Keep going, human. I might actually feed myself at this rate.",
            "Sharp logic! Almost as sharp as my claws."
        ]

    def get_cat_reaction(self, state):
        if state == "Slacking":
            return "Angry", random.choice(self.roasts)
        elif state == "Working":
            return "Happy", random.choice(self.compliments)
        else:
            return "Neutral", "I'm judging your cursor movements..."
class ShellShockBrain:
    def __init__(self):
        # Add everything you use for work here
        self.focus_apps = ["Code", "Studio", "Terminal", "PowerShell", "Stack Overflow", "Docs"]
        # Add your distractions here
        self.chaos_apps = ["YouTube", "Netflix", "Facebook", "Instagram", "Discord", "Reddit"]

    def analyze_activity(self):
        try:
            active_window = gw.getActiveWindowTitle()
            if not active_window:
                return "NEUTRAL", "Where did you go, Reshma?"

            # Check for Focus
            if any(word.lower() in active_window.lower() for word in self.focus_apps):
                return "HAPPY", "Productive cat is pleased. Keep coding! 🐾"
            
            # Check for Chaos
            elif any(word.lower() in active_window.lower() for word in self.chaos_apps):
                return "ANGRY", "Is that a cat video? Get back to the shell! 💀"
            
            else:
                return "CURIOUS", "I'm watching... don't get distracted."
        except:
            return "NEUTRAL", "System glitch. Stay focused anyway."

if __name__ == "__main__":
    brain_loop()