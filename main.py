import pygetwindow as gw
import time
import random

class CatBrain:
    def __init__(self):
        self.roasts = [
            "Meow-nimum effort detected. Get back to work!",
            "I've seen yarn balls with better logic than this code.",
            "Are you coding or just taking a digital cat nap?",
            "If I had nine lives, I'd spend zero of them watching you slack.",
            "That bug isn't going to fix itself, human."
        ]
        
        self.compliments = [
            "Purr-fect indentation! 🐾",
            "You're the cat's pajamas at debugging.",
            "Keep going, human. I might actually feed myself at this rate.",
            "Sharp logic! Almost as sharp as my claws.",
            "Deploying to production? Brave kitty."
        ]

    def get_cat_reaction(self, state):
        if state == "Slacking":
            return "😾", random.choice(self.roasts)
        elif state == "Working":
            return "😺", random.choice(self.compliments)
        else:
            return "🐱", "I'm judging your cursor movements..."

class ShellShockBrain:
    def __init__(self):
        # --- PERSONALIZED CONTEXT ---
        # 1. Dev Tools (General)
        self.dev_tools = ["Visual Studio Code", "IntelliJ", "Eclipse", "Terminal", "PowerShell", "Command Prompt", "Git", "Postman"]
        
        # 2. Specific Projects (Your Real Work)
        self.projects = ["aegis", "verifier", "blockchain", "spring", "java", "maven", "docker"]
        
        # 3. Learning/Docs
        self.learning = ["stackoverflow", "documentation", "localhost", "w3schools", "geeksforgeeks"]

        # 4. Distractions
        self.chaos_apps = ["youtube", "netflix", "facebook", "instagram", "discord", "reddit", "twitter", "steam"]

    def analyze_activity(self):
        try:
            active_window = gw.getActiveWindowTitle()
            if not active_window:
                return "NEUTRAL", "Where did you go?"

            active_window = active_window.lower()

            # CHECK: Are you slacking?
            if any(app in active_window for app in self.chaos_apps):
                return "ANGRY", "SLACKING DETECTED"
            
            # CHECK: Are you doing Deep Work (Project Specific)?
            elif any(proj in active_window for proj in self.projects):
                # Custom compliment for your specific tech stack
                return "HAPPY", "Deep work detected! The blockchain thanks you. 🔗"
            
            # CHECK: General Dev Work
            elif any(tool.lower() in active_window for tool in self.dev_tools):
                return "HAPPY", "Good code flow. Keep those commits coming."
            
            # CHECK: Learning
            elif any(doc in active_window for doc in self.learning):
                return "HAPPY", "Learning new tricks? Acceptable."

            else:
                return "NEUTRAL", "Watching..."
        except:
            return "NEUTRAL", "System glitch. Stay focused."

if __name__ == "__main__":
    # Test the brain independently
    brain = ShellShockBrain()
    while True:
        mood, msg = brain.analyze_activity()
        print(f"Mood: {mood} | Msg: {msg}")
        time.sleep(1)