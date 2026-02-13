import time
from shell import DesktopPet
from main import ShellShockBrain
import threading

def run_logic(pet, brain):
    while True:
        # 1. Brain analyzes the screen
        mood, message = brain.analyze_activity()
        
        # 2. Shell updates the UI
        pet.update_text(message)
        
        # 3. Handle specific triggers (like shaking) later
        time.sleep(2)

# Start UI and Logic at the same time
pet = DesktopPet()
brain = ShellShockBrain()

# We run the logic in a separate 'thread' so the UI doesn't freeze
logic_thread = threading.Thread(target=run_logic, args=(pet, brain), daemon=True)
logic_thread.start()

pet.run()