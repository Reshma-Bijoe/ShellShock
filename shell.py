import pygame
import time
import sys

def start_break_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("ShellShock Break")
    
    start_time = time.time()
    font = pygame.font.SysFont("Arial", 24)

    # Updated time limit to 600 seconds (10 minutes)
    TIME_LIMIT = 600 

    running = True
    while running:
        # 1. Check the Kill-Switch
        elapsed = time.time() - start_time
        remaining = max(0, TIME_LIMIT - int(elapsed))
        
        if remaining <= 0:
            print("Time's up! Back to work.")
            running = False

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 3. Drawing the Game
        screen.fill((30, 30, 30))
        # Displays the updated countdown starting from 600s
        timer_text = font.render(f"Break ends in: {remaining}s", True, (255, 255, 255))
        screen.blit(timer_text, (100, 280))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    start_break_game()