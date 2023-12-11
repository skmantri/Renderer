import numpy as np
import pygame
#creates screen
class Screen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Window")

    def ratio(self):
        return self.width / self.height

    def draw(self, buffer: np.ndarray):
        if buffer.shape != (self.width, self.height, 3):
            raise Exception("Buffer and screen must not the same size")

        buffer = np.fliplr(buffer)

        pygame.pixelcopy.array_to_surface(self.screen, buffer)
        pygame.display.flip()
    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()

    def screen_to_pixel(self, x, z):
        return np.array([int((x+1) * self.width / 2), int((z+1) * self.height / 2)])

    def pixel_to_screen(self, x, y):
        return np.array([(2 * (x+0.5) / self.width) - 1.0, 0.0, (2 * (y + 0.5) / self.height) - 1.0])
