import pathlib
import pygame

class ChessBoard:
    def __init__(self) -> None:
        self._path = pathlib.Path("Chess_Pieces")
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
    def loadPieces(self, gameDisplay):
        for i in [0,1,6,7]:
            for j in range(len(self.Board[0])):
                # Creating the image surface
                image = pygame.image.load(self._path / f"{self.Board[i][j][0:2]}.png")
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

    '''
    returns the color on the square with coordinates x and y
    '''
    def which_color(self,x,y):
        if((x+y)%2==0):
            color=(144,238,144)
        else:
            color=(50,205,50)
        return color


    '''
    returns true if the movement allowed according to piece
    '''
    def move(self,piece_name,current,next):
        # move conditions for each peice
        allowed=False
        straight=False
        diagonal=False
        back=False
        left=False # straight left
        right=False # straight right
        x_change=next[0]-current[0]
        y_change=-1*(next[1]-current[1])
        if(abs(x_change)>0 and abs(y_change)>0 and abs(x_change)==abs(y_change)):
            diagonal=True
        if(abs(y_change)>0 and x_change==0):
            straight=True
        if(y_change<0):
            back=True
        if((x_change>0 and y_change==0) ):
            right=True
        if(x_change<0 and y_change==0):
            left=True
        color=piece_name[0]
        
        if(color=='B'):
            back=not back
        
        print(piece_name)
        
        if(piece_name[1]=="P"):
            # stright movement
            print(back,left,right,straight,x_change,y_change)
            if(not back and not right and not left and straight and y_change):
                starting_row=6
                if(color=='B'):
                    starting_row=1
                if(current[1]==starting_row ):
                    if(abs(y_change)<=2):
                        allowed=True
                else:
                    if(abs(y_change)<=1):
                        allowed=True
                if(self.white_turn):
                    inc=-1
                else:
                    inc=1
                print(allowed)
                print(current[1]+inc)
                for i in range(current[1]+inc,next[1]+inc,inc):
                    print(i,current[0])
                    if(self.Board[i][current[0]]!='-'):
                        allowed=False
                print(allowed)

            if(not back and diagonal):
                # to capture diagonally
                if(self.Board[next[1]][next[0]]!='-' and abs(y_change)==1 and abs(x_change)==1 ):
                    if(self.color_check(self.Board[next[1]][next[0]])!=self.color_check(self.Board[current[1]][current[0]])):
                        allowed=True
            
        if(piece_name[1]=='N'):
            if((abs(x_change)==1 and abs(y_change)==2) or (abs(x_change)==2 and abs(y_change)==1)):
                allowed=True
        if(piece_name[1]=='B'):
            # only diagonal movement allowed
            if(diagonal==True and not straight ):
                allowed=True
            # Bishop is moving left or right
            if((next[0]-current[0])>0):
                inc_horizontal=1
            else:
                inc_horizontal=-1
            # bishop is moving up or down
            if(self.white_turn):
                inc_vertical=-1
            else:
                inc_vertical=1
            print(allowed)
            x_pos=current[0]+inc_horizontal
            y_pos=current[1]+inc_vertical
            print(x_pos,y_pos,next[0],next[1],inc_vertical,inc_horizontal)
            # go through the path and find if there is any obstacle
            while((inc_vertical==-1 and y_pos>next[1]) or (inc_vertical==1 and y_pos<next[1]) ) \
                and ((inc_horizontal==-1 and x_pos>next[0]) or (inc_horizontal==1 and x_pos<next[0])):
                print(x_pos,y_pos)
                if(self.Board[y_pos][x_pos]!='-'):
                    allowed=False
                x_pos+=inc_horizontal
                y_pos+=inc_vertical
            
            print(allowed)

            
        if(piece_name[1]=='R'):
            if(left==True or right==True or straight==True):
                allowed=True
            if((next[0]-current[0])>0):
                inc_horizontal=1
            else:
                inc_horizontal=-1
            # rook is moving up or down
            if(self.white_turn):
                inc_vertical=-1
            else:
                inc_vertical=1
            print(allowed)
            
            x_pos=current[0]
            y_pos=current[1]
            print(x_pos,y_pos)
            
            # go through the path and find if there is any obstacle

            if(abs(next[0]-current[0]) >0):
                x_pos=current[0]+inc_horizontal
                while((inc_horizontal==-1 and x_pos>next[0]) or (inc_horizontal==1 and x_pos<next[0])):
                    print(x_pos,y_pos)
                    if(self.Board[y_pos][x_pos]!='-'):
                        allowed=False
                    x_pos+=inc_horizontal
            
                    
            if(abs(next[1]-current[1]) >0):
                y_pos=current[1]+inc_vertical
                print(x_pos,y_pos)
                while((inc_vertical==-1 and y_pos>next[1]) or (inc_vertical==1 and y_pos<next[1]) ):
                    if(self.Board[y_pos][x_pos]!='-'):
                        allowed=False
                    y_pos+=inc_vertical 

            print(x_pos,y_pos,next[0],next[1],inc_vertical,inc_horizontal)
                      
        if(piece_name[1]=='K'):
            if(x_change<=1 and y_change<=1):
                allowed=True
            if(self.Board[next[1]][next[0]]!='-' and self.Board[next[1]][next[0]][1]=='R'):
                allowed=True
            x_pos=current[0]
            y_pos=current[1]
            if(self.Board[next[1]][next[0]]!='-' and self.Board[next[1]][next[0]][1]=='R'):
                # nothing in between
                # King side castle
                if((next[0]-current[0])>0):
                    inc_horizontal=1
                else:
                    inc_horizontal=-1
                print(y_pos,x_pos+inc_horizontal,y_pos,x_pos+2*inc_horizontal)
                print(self.Board)
                if(self.Board[y_pos][(x_pos+inc_horizontal)] !="-" or self.Board[y_pos][(x_pos+2*inc_horizontal)] !="-"):
                    allowed=False
            
                



        if(piece_name[1]=='Q'):
            if(diagonal  or right or straight or left):
                allowed=True
            if((next[0]-current[0])>0):
                inc_horizontal=1
            else:
                inc_horizontal=-1
            # bishop is moving up or down
            if(self.white_turn):
                inc_vertical=-1
            else:
                inc_vertical=1
            if(diagonal):
                x_pos=current[0]+inc_horizontal
                y_pos=current[1]+inc_vertical
                print(x_pos,y_pos,next[0],next[1],inc_vertical,inc_horizontal)
                # go through the path and find if there is any obstacle
                while((inc_vertical==-1 and y_pos>next[1]) or (inc_vertical==1 and y_pos<next[1]) ) \
                    and ((inc_horizontal==-1 and x_pos>next[0]) or (inc_horizontal==1 and x_pos<next[0])):
                    print(x_pos,y_pos)
                    if(self.Board[y_pos][x_pos]!='-'):
                        allowed=False
                    x_pos+=inc_horizontal
                    y_pos+=inc_vertical
            
            if(right or left or straight):
                x_pos=current[0]
                y_pos=current[1]
                print(x_pos,y_pos)
                
                # go through the path and find if there is any obstacle

                if(abs(next[0]-current[0]) >0):
                    x_pos=current[0]+inc_horizontal
                    while((inc_horizontal==-1 and x_pos>next[0]) or (inc_horizontal==1 and x_pos<next[0])):
                        print(x_pos,y_pos)
                        if(self.Board[y_pos][x_pos]!='-'):
                            allowed=False
                        x_pos+=inc_horizontal
                
                        
                if(abs(next[1]-current[1]) >0):
                    y_pos=current[1]+inc_vertical
                    print(x_pos,y_pos)
                    while((inc_vertical==-1 and y_pos>next[1]) or (inc_vertical==1 and y_pos<next[1]) ):
                        if(self.Board[y_pos][x_pos]!='-'):
                            allowed=False
                        y_pos+=inc_vertical 

        
        return allowed
    
    # def obstacle_check(self,piece_name,current,next):
    #     if(piece_name[1]=="P"):


