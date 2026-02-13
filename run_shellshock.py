import time
import threading
from shell import ShellShockUI
from main import ShellShockBrain, CatBrain

def run_logic(pet, brain, cat_personality):
    print("🧠 Brain Module Started...")
    while True:
        # 1. Analyze the Screen
        mood_code, _ = brain.analyze_activity() # Returns "HAPPY", "ANGRY", "NEUTRAL"
        
        # 2. Decide on Action based on Mood
        if mood_code == "ANGRY":
            # SLACKING DETECTED -> Trigger Punishment
            pet.trigger_punishment()
            time.sleep(5) # Wait a bit before checking again
            
        elif mood_code == "HAPPY":
            # WORKING -> Send Compliment
            emoji = "😺" # Happy Cat
            _, message = cat_personality.get_cat_reaction("Working")
            pet.update_face(emoji, message)
            
        else:
            # NEUTRAL/CONFUSED -> Just Observe
            emoji = "🧐" # Monocle/Observing
            pet.update_face(emoji, "") # No text, just watching
            
        time.sleep(3) # Check window every 3 seconds

if __name__ == "__main__":
    # Initialize Components
    pet = ShellShockUI()
    brain = ShellShockBrain()
    cat = CatBrain()

    # Run the Logic in a separate thread so UI doesn't freeze
    logic_thread = threading.Thread(target=run_logic, args=(pet, brain, cat), daemon=True)
    logic_thread.start()

    # Start the UI
    pet.run()