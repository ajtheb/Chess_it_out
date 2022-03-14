from ChessBoard import ChessDisplay
import pygame
import warnings

pygame.display.init()
pygame.font.init()
# pygame.mixer.init()  # disable sound

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


warnings.filterwarnings("ignore")


class Game:
    def __init__(self) -> None:
        self.gameDisplay = pygame.display.set_mode((800, 800))
        self.CB = ChessDisplay(self.gameDisplay)
        self.CB.draw()
        print(self.CB.board)
        return

    def _parser(self, pos):
        pos = [x // 100 for x in pos]
        return pos

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                # print(event)
                if event.type == QUIT:
                    exit(0)
                elif event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    _board_pos = self._parser(pos)
                    self.CB.select_or_move(_board_pos)
            pygame.display.flip()


g = Game()
g.run()


# while running:
#     for event in pygame.event.get():
#         if event.type == KEYDOWN:
#             if event.key == K_ESCAPE:
#                 running = False
#         if event.type == MOUSEBUTTONUP:
#             # no piece selected at the moment
#             if not piece_selected:
#                 cur = list(pygame.mouse.get_pos())
#                 cur[0]=cur[0]//100
#                 cur[1]=cur[1]//100
#                 print("current", cur)
#                 if(CB.Board[cur[1]][cur[0]]!='-'):
#                     piece_selected=True
#             else:
#                 nxt=list(pygame.mouse.get_pos())
#                 nxt[0]=nxt[0]//100
#                 nxt[1]=nxt[1]//100
#                 # next piece is not empty and it is equal to itself
#                 if(CB.Board[nxt[1]][nxt[0]]!='-' and CB.Board[nxt[1]][nxt[0]]==CB.Board[cur[1]][cur[0]]):
#                     # selection of piece to move is changed
#                     cur[0]=nxt[0]
#                     cur[1]=nxt[1]
#                     print("current", cur)
#                     continue
#                 print("next",nxt)

#                 # check if move is allowed
#                 if(CB.move(CB.Board[cur[1]][cur[0]],cur,nxt)==True):
#                     print("true")
#                     color=CB.which_color(cur[1],cur[0])
#                     #vacanting the current place
#                     pygame.draw.rect(gameDisplay, color,
#                             pygame.Rect(100*cur[0], 100*cur[1], 100, 100))
#                     #print(100*cur[1],100*cur[0])
#                     image = pygame.image.load('Chess_Pieces\\'+CB.Board[cur[1]][cur[0]][0:2]+".png")
#                     image = pygame.transform.scale(image, (100,100))

#                     print("put on",nxt)
#                     color=CB.which_color(nxt[1],nxt[0])
#                     print(color)
#                     pygame.draw.rect(gameDisplay, color,
#                             pygame.Rect(100*nxt[0], 100*nxt[1], 100, 100))
#                     gameDisplay.blit(image,(100*nxt[0],100*nxt[1]))
#                     temp=CB.Board[cur[1]][cur[0]]
#                     CB.Board[cur[1]][cur[0]]=CB.Board[nxt[1]][nxt[0]]
#                     CB.Board[nxt[1]][nxt[0]]=temp
#                 piece_selected=False
#             #highlight_selected_square(get_square_for_position(pos))
#         elif event.type == QUIT:
#             running = False
#     pygame.display.flip()
