from ChessBoard import ChessBoard
import pygame
import numpy as np

pygame.init()

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

gameDisplay = pygame.display.set_mode((800, 800))

CB = ChessBoard()
CB.drawBoard(gameDisplay=gameDisplay)
CB.loadPieces(gameDisplay=gameDisplay)


running = True
piece_selected = False
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == MOUSEBUTTONUP:
            # no piece selected at the moment
            if not piece_selected:

                cur = list(pygame.mouse.get_pos())
                cur[0] = cur[0] // 100
                cur[1] = cur[1] // 100
                print("current", cur)
                if (CB.color_check(CB.Board[cur[1]][cur[0]]) and CB.white_turn) or (
                    not CB.color_check(CB.Board[cur[1]][cur[0]]) and CB.black_turn
                ):
                    if CB.Board[cur[1]][cur[0]] != "-":
                        piece_selected = True
            else:
                nxt = list(pygame.mouse.get_pos())
                nxt[0] = nxt[0] // 100
                nxt[1] = nxt[1] // 100
                castle=False
                if(CB.Board[cur[1]][cur[0]][1]!="-" and CB.Board[cur[1]][cur[0]][1]=='K' and CB.Board[nxt[1]][nxt[0]] !="-" and CB.Board[nxt[1]][nxt[0]][1]=='R'):
                    castle=True
                # next piece is not empty and piece colour is same
                if CB.Board[nxt[1]][nxt[0]] != "-" and CB.color_check(CB.Board[nxt[1]][nxt[0]]) == CB.color_check(CB.Board[cur[1]][cur[0]]) and not castle:
                    # selection of moving piece is changed
                    print("selection of moving piece is changed")
                    cur[0] = nxt[0]
                    cur[1] = nxt[1]
                    print("current", cur)
                    continue
                print("next", nxt)

                # check if move is allowed
                if CB.move(CB.Board[cur[1]][cur[0]], cur, nxt) == True:
                    print("true")
                    color = CB.which_color(cur[1], cur[0])
                    # vacanting the current place
                    pygame.draw.rect(
                        gameDisplay,
                        color,
                        pygame.Rect(100 * cur[0], 100 * cur[1], 100, 100),
                    )
                    image = pygame.image.load(CB._path / f"{CB.Board[cur[1]][cur[0]][0:2]}.png")
                    image = pygame.transform.scale(image, (100, 100))

                    if castle==True :
                        if((nxt[0]-cur[0])>0):
                            inc_horizontal=1
                        else:
                            inc_horizontal=-1
                        # vacanting place for king
                        color = CB.which_color(cur[1], cur[0]+2)
                        print(color)
                        print(nxt)
                        pygame.draw.rect(
                            gameDisplay,
                            color,
                            pygame.Rect(100 * (cur[0]+2*inc_horizontal), 100 * cur[1], 100, 100),
                        )
                        # putting king
                        gameDisplay.blit(image, (100 *(cur[0]+2*inc_horizontal), 100 * cur[1]))
                        
                        #vacanting the current place of rook
                        color = CB.which_color(nxt[1], nxt[0])
                        print(color)
                        print(nxt)
                        pygame.draw.rect(
                            gameDisplay,
                            color,
                            pygame.Rect(100 * (nxt[0]), 100 * nxt[1], 100, 100)
                        )

                        # vacanting place for rook
                        color = CB.which_color(cur[1], cur[0]+inc_horizontal)
                        print(color)
                        print(nxt)
                        pygame.draw.rect(
                            gameDisplay,
                            color,
                            pygame.Rect(100 * (cur[0]+inc_horizontal), 100 * cur[1], 100, 100)
                        )

                        #putting rook
                        image_rook = pygame.image.load(CB._path / f"{CB.Board[nxt[1]][nxt[0]][0:2]}.png")
                        image_rook = pygame.transform.scale(image_rook, (100, 100))
                        gameDisplay.blit(image_rook, (100 *(cur[0]+inc_horizontal), 100 * cur[1]))

                        # updating places in array
                        # king
                        temp = CB.Board[cur[1]][cur[0]+2*inc_horizontal]
                        CB.Board[cur[1]][cur[0]+2*inc_horizontal] = CB.Board[cur[1]][cur[0]]
                        CB.Board[cur[1]][cur[0]] = temp

                        # rook

                        temp = CB.Board[cur[1]][cur[0]+inc_horizontal]
                        CB.Board[cur[1]][cur[0]+inc_horizontal] = CB.Board[nxt[1]][nxt[0]]
                        CB.Board[nxt[1]][nxt[0]] = temp


                    else:    
                        
                        # print(100*cur[1],100*cur[0])
                        
                        print("put on", nxt)
                        color = CB.which_color(nxt[1], nxt[0])
                        print(color)
                        pygame.draw.rect(
                            gameDisplay,
                            color,
                            pygame.Rect(100 * nxt[0], 100 * nxt[1], 100, 100),
                        )
                        gameDisplay.blit(image, (100 * nxt[0], 100 * nxt[1]))
                        CB.Board[nxt[1]][nxt[0]] = CB.Board[cur[1]][cur[0]]
                        CB.Board[cur[1]][cur[0]] = "-"
                    CB.black_turn = not CB.black_turn
                    CB.white_turn = not CB.white_turn

                piece_selected = False
            # highlight_selected_square(get_square_for_position(pos))
            print(np.array(CB.Board))
        elif event.type == QUIT:
            running = False
        
    
    pygame.display.flip()
