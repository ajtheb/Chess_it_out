from ChessBoard import ChessBoard
import pygame 
pygame.init()

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

CB=ChessBoard()
gameDisplay = pygame.display.set_mode((800,800))
gameDisplay.fill((255,255,255))
running =True
# pygame.draw.rect(gameDisplay, (255,255,255),
#                   pygame.Rect(0, 0, 100, 100))

# pygame.draw.rect(gameDisplay, (255,255,255),
#                   pygame.Rect(200, 0, 100, 100))
i=0
while(i<8):
    j=0
    while(j<8):
        if(i%2==0):
            if( j%2==0):
                color=	(144,238,144)
            else:
                color=(50,205,50)
        else:
            if(j%2==0):
                color=(50,205,50)
            else:
                color=(144,238,144)
        
        pygame.draw.rect(gameDisplay, color,
                 pygame.Rect(100*j, 100*i, 100, 100))
        #print(j)
        j+=1
    i+=1

for i in [0,1,6,7]:
    for j in range(len(CB.Board[0])):
        # Creating the image surface
        image = pygame.image.load('Chess_Pieces\\'+CB.Board[i][j][0:2]+".png")
        image = pygame.transform.scale(image, (100,100))

        # putting our image surface on display
        # surface
        gameDisplay.blit(image,(100*j,100*i))


pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #highlight_selected_square(get_square_for_position(pos))
        elif event.type == QUIT:
            running = False
