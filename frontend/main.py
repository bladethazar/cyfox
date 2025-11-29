import pygame
import os

class CyfoxFrontend:
    def __init__(self, backend):
        self.backend = backend
        pygame.init()
        self.screen = pygame.display.set_mode((128, 128))
        pygame.display.set_caption("Cyfox Buddy")
        self.clock = pygame.time.Clock()

        # load sprite(s)
        self.idle_img = pygame.image.load(
            os.path.join(os.path.dirname(__file__), "assets/cyfox.png")
        )
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # black background

            # show idle sprite if backend says idle
            if self.backend.get_state() == "idle":
                self.screen.blit(self.idle_img, (0, 0))

            pygame.display.flip()
            self.clock.tick(30)  # 30 FPS

        pygame.quit()
