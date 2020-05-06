import math
import pygame
import random
import os


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

class chessBoard:
    board = [None]*(8*8)
    currentTeam = 0

    def getPiecesAt(self,pos):
        return self.board[pos2index(pos)]
    
    def setPieceAt(self,pos,piece):
        self.board[pos2index(pos)] = piece



        
        

        
