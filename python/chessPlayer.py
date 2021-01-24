import math
import pygame
import random
import os

if __name__ == "__main__":
    main()

def main():
    game = chessBoard()
    game.init_Board()
    game.update_All()
    game.after_Update()
    ###################
    mPos = (0,0)
    mOffset = (0,0)
    screenSize = (360,360)
    display = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    ###################
    runGame = True
    time = 0
    pieceInHand = None
    print(game)
    while(runGame):
        blackMove = False
        mPos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                runGame = False
            
            if(game.winner == -1):
                if game.currentTeam:
                    pass
                else:
                    if(event.type == 5):
                        #Mouse click
                        i1 = game.getPieceAt((int(mPos[0]/45),int(mPos[1]/45)))
                        if(i1 and i1.color == game.currentTeam):
                            mOffset = (int(mPos[0]%45),int(mPos[1]%45))
                            if(pieceInHand):
                                pieceInHand.canRender = True
                            i1.canRender = False
                            pieceInHand = i1
                            pieceInHand.update()
                        

            if(event.type == 6):
                #Drag release
                if(pieceInHand and not game.currentTeam):
                    if(game.move(pieceInHand.pos,(int(mPos[0]/45),int(mPos[1]/45)))):
                        print(game)
                        print("Current player: {}".format("black" if game.currentTeam else "white"))
                        print('--- MOVING BLACK ---')
                        game.computerMove()
                        chessGame.currentTeam = (game.currentTeam + 1) %2

                        print()
                        print("Current player: {}".format("black" if game.currentTeam else "white"))

                    pieceInHand.canRender = True
                    pieceInHand = None

                    
        display.fill((0,0,0))




boardfix = [
    ["┌","┬","┐"],
    ["├","┼","┤"],
    ["└","┴","┘"],
]
def pos2index(pos):
    return pos[0]+pos[1]*8

class piece:
    loc = (0,0)
    board = None
    color = -1
    spritesheet = (pygame.image.load("chesspieces.png"),45)
    spriteIndex = (0,0)

    canRender = True
    hadLastMove = False
    hasMoved = False

    validMoves = []
    threat = []
    semiThreat = []
    char = ["?"]

    def __init__(self,board,loc,color):
        self.loc = loc
        self.color = color
        self.board = board
        self.canRender = True
        self.hasMoved = False
        self.hadLastMove = False
        self.threat = []
        self.validMoves = []
        self.semiThreat = []

    def moveTo(self,loc):
        if(self.canMoveTo(loc)):
            self.hasMoved = True
            destPiece = self.board.getPieceAt(loc)
            self.board.setPieceAt(loc,self)
            self.board.setPieceAt(self.loc,None)
            self.loc = loc
            if(destPiece): #kills opponent
                destPiece.kill()
                return True,True
            return True,False
        return False,False

    def canMoveTo(self,loc):
        return loc in self.validMoves
    
    def render(self,surface):
        if(self.canRender):
            s = self.spritesheet
            surface.blit(s[0],(self.loc[0]*s[1],self.loc[1]*s[1]),((self.spriteIndex[self.color]%6)*s[1],math.floor(self.spriteIndex[self.color]/6)*s[1],s[1],s[1]))
            
    def kill(self):
        pass

class King(piece):
    spriteInd = (0,6)

    def render(self,surface):
        if self.board.isThreatend(self.pos, self.color):
            pygame.draw.rect(surface,(255,100,0),(self.pos[0]*45,self.pos[1]*45,45,45))
        super(King,self).render(surface)
    
class Rook(piece):
    char = ["R","r"]

class Knight(piece):
    char = ["N","n"]

class Bishop(piece):
    char = ["B","b"]

class Pawn(piece):
    char = ["P","p"]
    doubleMovesDone = False

    def __init__(self, board, loc, color):
        self.validMoves = []
        self.threat = []
        self.doubleMovesDone = False
        piece.__init__(self,  board, loc, color,color)

    def move(self, loc):
        xDiff = loc[0] - self.loc[0]
        yDiff = loc[1] - self.loc[1]
        empty, kill = super(Pawn, self).moveTo(loc)
        self.doubleMovesDone = abs(yDiff)>1 and empty

        if (empty):
            #en passant condition(enemy pawns right next to each other) = enemy can kill as if pawn moved 1 step forwrad instead of 2 
            if (not kill and abs(yDiff)==1 and abs(xDiff)==1): 
                opponentPos = (loc[0], loc[1] + (self.color*2-1))
                opponentPiece = self.board.getPiecesAt(opponentPos)
                self.board.setPieceAt((opponentPos,None)) #removes the enemy next to it but still moves to its normal destination (diagonaly)
                opponentPiece.kill()
            
            #pawn reaches end of board(transfroms)
            if (loc[1]+1)%8 == self.color:
                while(True): 
                    try:
                        if self.color == 1:
                            self.board.setPieceAt(loc, Queen(self.board,loc,self.color))
                        inp = int(input("Change pawn to 1: queen, 2: knight, 3: bishop, 4: rook: "))
                        if(inp == 1):
                            obj = Queen(self.board,loc,self.color)
                        if(inp == 2):
                            obj = Knight(self.board,loc,self.color)
                        if(inp == 3):
                            obj = Bishop(self.board,loc,self.color)
                        if(inp == 4):
                            obj = Rook(self.board,loc,self.color)
                        self.board.setPieceAt(loc,obj)
                        break
                    except Exception: 
                        pass
        return empty, kill

        def update(self):
            pos = self.pos
            self.threat = [(pos[0]-1,pos[1]-(self.color*2 - 1)),(pos[0]+1,pos[1]-(self.color*2 - 1))]

            ###########Update Valid moves############
            self.validMoves = []
            for i in self.threat:
                piece = self.board.getPieceAt(i)
                if(piece):
                    if(piece.team != self.team): #check if enemy
                        self.validMoves += [i] #can eat
            
            '''
            p1 = (pos[0],self.pos[1]-(self.team*2 - 1))
            p2 = (pos[0],self.pos[1]-(self.team*2 - 1)*2)
            
            if(not self.board.getPieceAt(p1)):
                self.validMoves += [p1]
            if(not self.hasMoved):
                if(not self.board.firstEncounter(pos,p2)):
                    self.validMoves += [p2]
            
            p3 = (pos[0]-1,pos[1])
            p4 = (pos[0]+1,pos[1])
            i3 = self.board.getPieceAt(p3)
            i4 = self.board.getPieceAt(p4)
            
            if(i3 and i3.hadLastMove and isinstance(i3,Pawn) and i3.movedTwice and i3.team != self.team):
                self.validMoves += [(pos[0]-1,pos[1]-(self.team*2 - 1))]
            elif(i4 and i4.hadLastMove and isinstance(i4,Pawn) and i4.movedTwice and i4.team != self.team):
                self.validMoves += [(pos[0]+1,pos[1]-(self.team*2 - 1))]'''



        

class Queen(rook,bishop):
    char = ["Q","q"]


class chessBoard:
    board = [None]*(8*8)
    currentTeam = 0
    winner = -1
    lastPiece = None

    def __init__(self):
        self.board = [None]*(8*8)
        self.winner = -1
        self.lastPiece = None
        self.currentTeam = 0  

    def set_Board(self, board):
        for loc,piece in enumerate(board):
            board[loc] = piece

    def get_Piece(self,loc):
        return self.board[pos2index(loc)]
        

    def set_Piece(self, loc, piece):
        self.board[pos2index(loc)] = piece
        
    def update_All(self):
        for i in self.board:
            if(i): i.update()
    
    def after_Update(self):
        for i in self.board:
            if(i): i.afterUpdate()

    def swap(self,loc1,loc2):
        temp = self.board[pos2index(loc1)]
        self.board[pos2index(loc1)] = self.board[pos2index(loc2)]
        self.board[pos2index(loc2)] = self.board[pos2index(loc1)]
                
    def init_Board(self):
        self.board[0:7] = [Rook(self,(0,0),0),Knight(self,(1,0),0),Bishop(self,(2,0),0),Queen(self,(3,0),0),King(self,(4,0),0),Bishop(self,(5,0),0),Knight(self,(6,0),0),Rook(self,(7,0),0)]
        self.board[8:15] = [Pawn(self,(i,1),0) for i in range(8)]
        self.board[pos2index((0,7))-1 : pos2index((7,7))-1] = [Rook(self,(0,7),1),Knight(self,(1,7),1),Bishop(self,(2,7),1),Queen(self,(3,7),1),King(self,(4,7),1),Bishop(self,(5,7),1),Knight(self,(6,7),1),Rook(self,(7,7),1)]
        self.board[pos2index((0,6)) : pos2index((7,6))] = [Pawn(self,(i,6),1) for i in range(8)]
        
    def first_Encounter(self, loc1, loc2, maxx = 1):
        diffX = -loc1[0]+loc2[0]
        diffY = -loc1[1]+loc2[1]
        cPos = loc1
        first = True
        for i in self.raycast(loc1,loc2,maxx):
            if(self.get_Piece(i)):
                return i




        
        

        
