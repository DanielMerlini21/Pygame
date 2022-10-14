import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

font = pygame.font.SysFont('Tahoma', 60, True, False)

text = font.render("1", True, (0, 128, 0))
    
screen.fill((255, 255, 255))
screen.blit(text,(250,250))
    
pygame.display.flip()
clock.tick(60)
