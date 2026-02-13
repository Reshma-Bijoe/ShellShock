import time
import threading
from shell import ShellShockUI
from main import ShellShockBrain, CatBrain

def run_logic(pet, brain, cat_personality):
    print("🧠 Brain Module Started...")
    
    pet.update_face("👋", "Welcome back! Click me to play.")
    time.sleep(3) 
    
    # --- RESTORED: Personality Settings ---
    last_compliment_time = 0
    COMPLIMENT_GAP = 100 # Compliment every 100 seconds
    
    slack_start_time = None
    current_limit = 300 

    while True:
        mood_code, activity_msg = brain.analyze_activity() 
        current_time = time.time()
        
        # --- CASE A: DISTRACTION (YouTube/Reddit) ---
        if mood_code == "ANGRY":
            if slack_start_time is None:
                current_limit = pet.ask_slack_limit_safe()
                slack_start_time = time.time() 
            
            elapsed_slack = current_time - slack_start_time
            remaining_time = current_limit - elapsed_slack
            
            pet.update_stopwatch(remaining_time)
            
            # --- RESTORED: Insults while counting down ---
            # We don't spam it, just show the timer + angry face.
            # But we CAN send a roast if we want. For now, let's keep the timer clean
            # or send one roast at the start.
            if int(elapsed_slack) % 10 == 0: # Roast every 10 seconds of slacking
                 _, roast = cat_personality.get_cat_reaction("Slacking")
                 pet.update_face("😠", roast)
            else:
                 pet.update_face("😠", "")

            if remaining_time <= 0:
                pet.trigger_punishment()
                slack_start_time = None 
                time.sleep(2)

        # --- CASE B: WORKING ---
        elif mood_code == "HAPPY":
            if slack_start_time is not None:
                slack_start_time = None
                pet.hide_stopwatch()

            # --- RESTORED: Compliments! ---
            if current_time - last_compliment_time > COMPLIMENT_GAP:
                emoji = "😺" 
                _, message = cat_personality.get_cat_reaction("Working")
                pet.update_face(emoji, message)
                last_compliment_time = current_time
            else:
                # Working, but waiting for next compliment
                pet.update_face("😺", "") 
                
        # --- CASE C: IDLE/NEUTRAL ---
        else:
            if slack_start_time is not None:
                slack_start_time = None
                pet.hide_stopwatch()
            
            pet.update_face("🧐", "") 
            
        time.sleep(1) 

if __name__ == "__main__":
    pet = ShellShockUI()
    brain = ShellShockBrain()
    cat = CatBrain()

    logic_thread = threading.Thread(
        target=run_logic, 
        args=(pet, brain, cat), 
        daemon=True
    )
    logic_thread.start()

    pet.run()