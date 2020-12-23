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
    screenSize = (360,360)
    display = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("Chess")
    ###################
    runGame = True
    time = 0
    clock = pygame.time.Clock()
    pieceInHand = None
    mPos = (0,0)
    mOffset = (0,0)
    print(game)
    ###################
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
                        if(i1 and i1.team == game.currentTeam):
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
    pos = (0,0)
    board = None
    team = -1
    spritesheet = (pygame.image.load("chesspieces.png"),45)
    spriteIndex = (0,0)

    canRender = True
    hadLastMove = False
    hasMoved = False

    validMoves = []
    threat = []
    semiThreat = []
    char = ["?"]

    def __init__(self,board,pos,team):
        self.pos = pos
        self.team = team
        self.board = board
        self.canRender = True
        self.hasMoved = False
        self.hadLastMove = False
        self.threat = []
        self.validMoves = []
        self.semiThreat = []

    def moveTo(self,pos):
        if(self.canMoveTo(pos)):
            self.hasMoved = True
            pos2 = self.board.getPieceAt(pos)
            self.board.setPieceAt(pos,self)
            self.board.setPieceAt(self.pos,None)
            self.pos = pos
            if(pos2):
                pos2.kill()
                return True,True
            return True,False
        return False,False

    def canMoveTo(self,pos):
        return pos in self.validMoves
    
    def render(self,surface):
        if(self.canRender):
            s = self.spritesheet
            surface.blit(s[0],(self.pos[0]*s[1],self.pos[1]*s[1]),((self.spriteIndex[self.team]%6)*s[1],math.floor(self.spriteIndex[self.team]/6)*s[1],s[1],s[1]))
            
    def kill(self):
        pass

class King(piece):
    spriteInd = (0,6)

    def render(self,surface):
        if self.board.isThreatend(self.pos, self.team):
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
        
    def update_All(self):
        for i in self.board:
            if(i): i.update()
    
    def after_Update(self):
        for i in self.board:
            if(i): i.afterUpdate()
                
    def init_Board(self):
        self.board[0:7] = [Rook(self,(0,0),0),Knight(self,(1,0),0),Bishop(self,(2,0),0),Queen(self,(3,0),0),King(self,(4,0),0),Bishop(self,(5,0),0),Knight(self,(6,0),0),Rook(self,(7,0),0)]
        self.board[8:15] = [Pawn(self,(i,1),0) for i in range(8)]
        self.board[pos2index((0,7))-1 : pos2index((7,7))-1] = [Rook(self,(0,7),1),Knight(self,(1,7),1),Bishop(self,(2,7),1),Queen(self,(3,7),1),King(self,(4,7),1),Bishop(self,(5,7),1),Knight(self,(6,7),1),Rook(self,(7,7),1)]
        self.board[pos2index((0,6)) : pos2index((7,6))] = [Pawn(self,(i,6),1) for i in range(8)]
        


    def getPiecesAt(self,pos):
        return self.board[pos2index(pos)]
    
    def setPieceAt(self,pos,piece):
        self.board[pos2index(pos)] = piece



        
        

        
