import pygame
import time
import sys

def start_break_game():
    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption("ShellShock Break")
    
    start_time = time.time()
    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        # 1. Check the Kill-Switch (60 Seconds)
        elapsed = time.time() - start_time
        remaining = max(0, 60 - int(elapsed))
        
        if remaining <= 0:
            print("Time's up! Back to work.")
            running = False

        # 2. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 3. Drawing the "Mock" Game
        screen.fill((30, 30, 30))
        timer_text = font.render(f"Break ends in: {remaining}s", True, (255, 255, 255))
        screen.blit(timer_text, (100, 280))
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    start_break_game()