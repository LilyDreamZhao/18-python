
import pygame
class ChessBoard(object):
    def __init__(self,gridSize,gridNum,edgeup,edgeleft):
        self.gridSize = gridSize
        self.gridNum = gridNum
        self.edgeup = edgeup,
        self.edgeleft = edgeleft
        self.chessboardSize = self.gridSize*self.gridNum
        # self.chessboardImg = pygame.Surface((gridSize*gridNum+edgeup*2,gridSize*gridNum+edgeleft*2))
        self.chessboardImg = pygame.Surface((self.chessboardSize+2*edgeup,self.chessboardSize+2*edgeleft))
        self.chessboardImg.fill((237,145,33))

        # 剪切棋盘的空白（没有棋子的网点）网点
        self.chessNullImg = pygame.Surface((gridSize,gridSize))
        self.chessNullImg.fill((237,145,33))
        pygame.draw.line(self.chessNullImg,(0,0,0),(gridSize//2,0),(gridSize//2,gridSize),2)
        pygame.draw.line(self.chessNullImg,(0,0,0),(0,gridSize//2),(gridSize,gridSize//2),2)

        # 绘制线条
        for i in range(gridNum+1):
            pygame.draw.line(self.chessboardImg,(0,0,0),(edgeleft+gridSize*i,edgeup),
                             (edgeleft+gridSize*i,edgeup+self.chessboardSize),2)
            pygame.draw.line(self.chessboardImg, (0, 0, 0), (edgeleft, edgeup+gridSize*i), (self.chessboardSize+edgeleft,edgeup+gridSize*i),2)
        #pygame.draw.line(chessboardImg,(0,0,0),(self.edgeup,self.edgeleft),(self.edgeup+self.gridSize,self.edgeleft+self.gridSize))


# 测试本类
'''
import sys
pygame.init()
chess = ChessBoard(30,16,16,16)
screen= pygame.display.set_mode((30*16+16*2,30*16+16*2))
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(chess.chessNullImg, (0, 0))
    # screen.blit(chess.chessboardImg, (0,0))
    pygame.display.update()
'''
