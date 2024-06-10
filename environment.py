import pygame

# Opens the main focus window
def run():
    # Initialize all pygame modules
    if not pygame.get_init():
        pygame.init()
    
    screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
    pygame.display.set_caption("AI Galaga")

    running = True
    
    # Main loop to keep the window open and parse the event queue
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    
    pygame.quit()