""" wrap.py
    demonstrate screen wrap boundaries
"""

import pygame
pygame.init()

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, background):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.background = background

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 255))
        pygame.draw.circle(self.image, (0, 0, 255), (15, 15), 15)
        self.rect = self.image.get_rect()

        self.rect.center = (320, 240)

        self.dx = 5
        self.dy = 5

    def update(self):
        oldCenter = self.rect.center
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        pygame.draw.line(self.background, (0, 0, 0), oldCenter, self.rect.center)

        self.checkBounds()

    def checkBounds(self):
        """ wrap around screen """

        if self.rect.centerx > self.screen.get_width():
            self.rect.centerx = 0
        if self.rect.centerx < 0:
            self.rect.centerx = self.screen.get_width()
        if self.rect.centery > self.screen.get_height():
            self.rect.centery = 0
        if self.rect.centery < 0:
            self.rect.centery = self.screen.get_height()

def main():
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Boundary-checking: wrap")

    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    ball = Ball(screen, background)
    allSprites = pygame.sprite.Group(ball)

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
