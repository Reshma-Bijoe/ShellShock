import time
import threading
from shell import ShellShockUI
from main import ShellShockBrain, CatBrain

def run_logic(pet, brain, cat_personality):
    print("🧠 Brain Module Started...")
    
    # --- 1. WELCOME MESSAGE ---
    # Show this immediately when the app starts
    pet.update_face("👋", "Welcome back, Reshma! I'm watching you...")
    time.sleep(5) # Keep the welcome message for 5 seconds

    # Timers to control frequency
    last_compliment_time = 0
    COMPLIMENT_GAP = 100  # <--- CHANGED: Compliments appear every 100 seconds (approx 1.5 mins)

    while True:
        # --- 2. ANALYZE ACTIVITY ---
        mood_code, activity_msg = brain.analyze_activity() 
        current_time = time.time()
        
        # --- 3. DECIDE REACTION ---
        
        # CASE A: DISTRACTION (Immediate Reaction)
        if mood_code == "ANGRY":
            pet.trigger_punishment()
            time.sleep(2) # Wait a bit after punishment before checking again
            
        # CASE B: WORKING (Delayed Reaction)
        elif mood_code == "HAPPY":
            # Only compliment if enough time has passed (The "Gap")
            if current_time - last_compliment_time > COMPLIMENT_GAP:
                emoji = "😺" 
                # Use the Face (Emoji)
                _, message = cat_personality.get_cat_reaction("Working")
                pet.update_face(emoji, message)
                last_compliment_time = current_time
            else:
                # If working but in the "gap", show Happy Face with NO text
                pet.update_face("😺", "") 
                
        # CASE C: IDLE/NEUTRAL
        else:
            pet.update_face("🧐", "") # Just watching, no text
            
        # Check every 2 seconds (Fast enough to catch YouTube)
        time.sleep(2) 

if __name__ == "__main__":
    # Initialize Components
    pet = ShellShockUI()
    brain = ShellShockBrain()
    cat = CatBrain()

    # Run the Logic in a separate thread
    logic_thread = threading.Thread(target=run_logic, args=(pet, brain, cat), daemon=True)
    logic_thread.start()

    # Start the UI
    pet.run()