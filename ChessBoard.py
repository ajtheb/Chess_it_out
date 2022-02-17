from importlib_metadata import flake8_bypass
import pygame

class ChessBoard:
    def __init__(self) -> None:
        self.Board=[
            ["BR1","BN1","BB1","BQ","BK","BB2","BN2","BR2"],
            ["BP1","BP2","BP3","BP4","BP5","BP6","BP7","BP8"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-"],
            ["WP1","WP2","WP3","WP4","WP5","WP6","WP7","WP8"],
            ["WR1","WN1","WB1","WQ","WK","WB2","WN2","WR2"] 
        ]
        self.black_turn=False
        self.white_turn=True
    
    def drawBoard(self,gameDisplay):
        i=0
        while(i<8):
            j=0
            while(j<8):
                if((i+j)%2==0):
                    color=	(144,238,144)
                else:
                    color=(50,205,50)
                    
                pygame.draw.rect(gameDisplay, color,
                        pygame.Rect(100*j, 100*i, 100, 100))
                #print(j)
                j+=1
            i+=1
    '''
    loads the pieces images on corresponding squares
    '''
    def loadPieces(self,gameDisplay):
        for i in [0,1,6,7]:
            for j in range(len(self.Board[0])):
                # Creating the image surface
                image = pygame.image.load('Chess_Pieces\\'+self.Board[i][j][0:2]+".png")
                image = pygame.transform.scale(image, (100,100))

                # putting our image surface on display
                # surface
                gameDisplay.blit(image,(100*j,100*i))
    '''
    returns true for white
    '''
    def color_check(self,piece_name):
        if(piece_name[0]=='W'):
            return True
        else:
            return False

    def move(self,piece_name,current,next):
        # move conditions for each peice
        allowed=False
        straight=False
        diagonal=False
        back=False
        left=False
        right=False
        x_change=next[0]-current[0]
        y_change=-1*(next[1]-current[1])
        if(abs(x_change)>0 and abs(y_change)>0):
            diagonal=True
        if(y_change>0 and x_change==0):
            straight=True
        if(y_change<0):
            back=True
        if((x_change>0 and y_change==0) ):
            right=True
        if(x_change<0 and y_change==0):
            left=True
        print(piece_name)
        
        if(piece_name[0:2]=="WP"):
            # stright movement
            #print(back,left,right,straight,x_change,y_change)
            if(not back and not right and not left and straight and y_change):
                if(current[1]==6 ):
                    if(y_change<=2):
                        allowed=True
                else:
                    if(y_change<=1):
                        allowed=True            
            if(not back and diagonal):
                if(self.Board[next[1]][next[0]]!='-' and y_change==1 and abs(x_change)==1):
                    allowed=True
        return allowed