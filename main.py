from ChessBoard import ChessBoard
import pygame 
pygame.init()

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

gameDisplay = pygame.display.set_mode((800,800))

CB=ChessBoard()
CB.drawBoard(gameDisplay=gameDisplay)
CB.loadPieces(gameDisplay=gameDisplay)


running =True
piece_selected=False
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONUP:
            if not piece_selected:
                cur = list(pygame.mouse.get_pos())
                cur[0]=cur[0]//100
                cur[1]=cur[1]//100
                print("current", cur)
                if(CB.Board[cur[1]][cur[0]]!='-'):
                    piece_selected=True
            else:
                nxt=list(pygame.mouse.get_pos())
                nxt[0]=nxt[0]//100
                nxt[1]=nxt[1]//100
                if(CB.Board[nxt[1]][nxt[0]]!='-' and CB.Board[nxt[1]][nxt[0]]==CB.Board[cur[1]][cur[0]]):
                    cur[0]=nxt[0]
                    cur[1]=nxt[1]
                    print("current", cur)
                    continue
                print("next",nxt)
                if(CB.move(CB.Board[cur[1]][cur[0]],cur,nxt)==True):
                    print("true")
                    if((cur[1]+cur[0])%2==0):
                        color=(144,238,144)
                    else:
                        color=(50,205,50)
                    
                    #vacanting the current place
                    pygame.draw.rect(gameDisplay, color,
                            pygame.Rect(100*cur[0], 100*cur[1], 100, 100))
                    #print(100*cur[1],100*cur[0])
                    image = pygame.image.load('Chess_Pieces\\'+CB.Board[cur[1]][cur[0]][0:2]+".png")
                    image = pygame.transform.scale(image, (100,100))
                    # putting our image surface on display
                    # surface
                    print("put on",nxt)
                    gameDisplay.blit(image,(100*nxt[0],100*nxt[1]))
                    temp=CB.Board[cur[1]][cur[0]]
                    CB.Board[cur[1]][cur[0]]=CB.Board[nxt[1]][nxt[0]]
                    CB.Board[nxt[1]][nxt[0]]=temp     
                piece_selected=False
            #highlight_selected_square(get_square_for_position(pos))
        elif event.type == QUIT:
            running = False
    pygame.display.flip()
