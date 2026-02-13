import pygetwindow as gw
import time
import game  

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

if __name__ == "__main__":
    brain_loop()