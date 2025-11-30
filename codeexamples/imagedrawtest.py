import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Load PNG Example")

# Load original image
original_image = pygame.image.load("assets/Graphics/Aseprite/debug32x32.png").convert()

# create font
font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()
angle = 45

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 150, 255))

    # Always rotate the ORIGINAL image
    rotated = pygame.transform.rotate(original_image, angle)
    angle += 45   # 1 degree per frame


    # To keep it centered at (100, 100)
    rect = rotated.get_rect(center=(100, 100))     
    rect3 = rotated.get_rect(topleft=(100, 100))

    size1 = rect.size
 
    


    print(rect)
    print(rect3)
    print(size1)
 

    """
    Rect(78, 78, 45, 45)
    Rect(0, 0, 45, 45)
    Rect(100, 100, 45, 45)
    (45, 45)
    """
    
    # draw text
    #text = font.render(rect, True, (255, 255, 255))

    #screen.blit(text, (50, 50))
    screen.blit(rotated, (100, 100)) # if a rect is used, it uses the topleft corner

    pygame.display.flip()
    clock.tick(1)
