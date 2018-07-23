'''
五子棋
作者：赵丽丽

'''
import pygame,sys,random
from chessboardsize import ChessBoard
class wzqGame(object):
    '''第一区域：属性初始化'''
    def __init__(self):
        """ 1.1 棋盘，棋子设置 """
        # 设置棋盘格子数量
        self.gridNum = 24
        # 设置一个格子的大小
        self.gridSize = 30
        # Num=16==>size=45,24==>30,32==>23
        # 设置预留边缘大小 实际只要设置一边即可，为了方便后期更新设置，分别设置
        self.edgeleft = 16
        self.edgeright = 16
        self.edgeup = 16
        self.edgedown = 16
        # 计算棋盘大小 不包含边缘
        self.chessBoardSize = self.gridNum * self.gridSize

        #当前格子的位置
        self.top_th = 10000
        self.left_th = 10000

        """1.2 窗口背景图片设置"""
        # 设置窗口
        self.screen = pygame.display.set_mode((self.chessBoardSize + 2 * self.edgeup,
                                               self.chessBoardSize + 2 * self.edgeleft),0,0)
                # 实例化棋盘对象
        chessBoardObject = ChessBoard(self.gridSize,self.gridNum,self.edgeup,self.edgeleft)
        # 获得棋盘图片
        self.background = chessBoardObject.chessboardImg
        # 获得空白网格图片
        self.chessNullImg = chessBoardObject.chessNullImg
		
        #导入黑白棋图片并且更改大小
        self.black = pygame.image.load("img/1.png")
        self.white = pygame.image.load("img/2.png")
        # 调整大小 下标0是偶数，对应黑色
        self.chessPic =[ pygame.transform.scale(self.black, (self.gridSize, self.gridSize)),
                         pygame.transform.scale(self.white, (self.gridSize, self.gridSize))]

        # 设置格子,-1表示空，1表示白棋，0表示黑棋
        self.grids=[]
        for _ in range(self.gridNum+1):
            line = []
            for _ in range(self.gridNum+1):
                line.append(-1)
            self.grids.append(line)

        """1.3 设置字体"""
        pygame.font.init()
        self.fontsize = 1.5
        self.ft = pygame.font.Font("xixinkaijian.ttf", int(1.5 * self.gridSize))

        """1.4 设置业务逻辑涉及的参数"""
        #记所下的棋子数
        self.count = -1
        # 设置允许下的棋子数，大于该棋子数，则和棋
        self.MAXCOUNT = 10 * 10
        # 根据self.count奇偶获得当前用户,偶数是黑色
        # 1表示白棋，0表示黑棋
        self.Name = ["black","white"]
        self.renew = False
        self.stop = False

    '''第二区域：开始游戏前，初始化界面及其游戏设置'''
    # 2.1 开始游戏主函数
    def inGame(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # 按钮enter,退出初始动作
                if event.key == pygame.K_RETURN:
                    # 返回True，表示退出初始界面
                    return True
                # 按钮0, 16*16 格棋盘
                if event.key == pygame.K_0:
                    self.change(16,45)
                # 按钮1, 24*24 格棋盘
                if event.key == pygame.K_1:
                    self.change(24,30)
                # 按钮2, 32*32 格棋盘
                if event.key == pygame.K_2:
                    self.fontsize = 3
                    self.change(32,23)
            # 2.1.1 初始化界面
            self.initPaint()
            # 没有选择enter键，返回False继续等待用户设置，进入游戏
            return False

    # 2.1.1 改变游戏设置，修改游戏属性
    def change(self,gridNum,gridSize):
        self.gridSize = gridSize
        self.gridNum = gridNum
        self.chessPic = [pygame.transform.scale(self.black, (self.gridSize, self.gridSize)),
                         pygame.transform.scale(self.white, (self.gridSize, self.gridSize))]
        chessboard = ChessBoard(self.gridSize, self.gridNum,self.edgeup, self.edgeleft)
        self.background = chessboard.chessboardImg
        self.chessNullImg = chessboard.chessNullImg
						
        # 设置格子,-1表示空，1表示白棋，0表示黑棋
        self.grids=[]
        for _ in range(self.gridNum+1):
            line = []
            for _ in range(self.gridNum+1):
                line.append(-1)
            self.grids.append(line)

    # 2.1.2 初始化界面
    def initPaint(self):
        self.screen.blit(self.background,(0,0))
        bw4 = self.ft.render("当前格子"+str(self.gridNum)+"*"+str(self.gridNum),
                             True,(100,100,100))
        bw0 = self.ft.render("按钮0==>16*16",True,(100,100,100))
        bw1 = self.ft.render("按钮1==>24*24",True,(100,100,100))
        bw2 = self.ft.render("按钮2==>32*32",True,(100,100,100))
        bw = self.ft.render("点击Enter进入游戏，r悔棋一步", True, (100, 100, 100))
        self.screen.blit(bw4, (self.chessBoardSize // 2 - 150,
                              self.chessBoardSize // 2-100 ))
        self.screen.blit(bw0, (self.chessBoardSize // 2 - 150,
                              self.chessBoardSize // 2-50 ))
        self.screen.blit(bw1, (self.chessBoardSize // 2 - 150,
                              self.chessBoardSize // 2 ))
        self.screen.blit(bw2, (self.chessBoardSize // 2 - 150,
                              self.chessBoardSize // 2+50 ))

        self.screen.blit(bw, (self.chessBoardSize // 2 - 300,
                               self.chessBoardSize // 2 + 150))


    '''第三区域: 进入游戏中；业务逻辑函数及其绘制界面'''
    # 3. 业务逻辑主函数
    def action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # 按钮enter,退出初始动作
                if event.key == pygame.K_r and self.count>-1 and self.rebackFlag == False:
                    self.reback()
                    # return 退出action()函数
                    return True

            # 根据结束条件，绘制结束图片，做出相应动作
            if self.stop == True:
                if self.renew == True:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            wzq = wzqGame()
                            wzq.main()
                    else:
                        self.endPaint()
                        return True
                self.renew = True
                return True





            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标信息
                mouseLeft, mouseTop = pygame.mouse.get_pos()

                # 获取鼠标点击
                leftFlag = pygame.mouse.get_pressed()[0]
                # 判断鼠标是否左击，以及击中的位置是否在棋盘范围内
                if leftFlag and self.edgeleft-self.gridSize//2< mouseLeft< self.chessBoardSize+self.left_th+self.gridSize//2 \
                        and self.edgeup-self.gridSize//2 < mouseTop< self.chessBoardSize+self.top_th+self.gridSize//2:
                    # 根据鼠标点击的具体位置获取在棋盘的位置

                    # 更新当前棋子在棋盘的位置
                    self.top_th = (mouseTop-self.edgeup-self.gridSize//2)//self.gridSize+1
                    self.left_th = (mouseLeft-self.edgeleft-self.gridSize//2)//self.gridSize+1
                    print(self.top_th,self.left_th)
                    # 如果该位置棋子的标志是-1，表示该位置为空
                    if self.grids[self.top_th][self.left_th] == -1:
                        '''
                        游戏开始时候,self.count=-1,
                        当落下一个棋子时候，self.count=0为偶数，第一个是黑棋子落下
                         '''
                        # 该位置合法，棋子数量增加
                        self.count += 1

                        #已经下了新棋子，悔棋标志改为False
                        self.rebackFlag = False

                        # 更新棋盘列表，黑棋为0，白棋为1
                        self.grids[self.top_th][self.left_th] = self.count%2
                        self.paintChess()
                    self.judegWin()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # 根据结束条件，绘制结束图片，做出相应动作
            if self.stop == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        wzq = wzqGame()
                        wzq.main()
                else:
                    self.endPaint()
                    return True
                #self.renew = True
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标信息
                mouseLeft, mouseTop = pygame.mouse.get_pos()

                # 获取鼠标左击事件
                leftFlag = pygame.mouse.get_pressed()[0]
                # 判断鼠标是否左击，以及击中的位置是否在棋盘范围内
                if leftFlag and self.edgeleft-self.gridSize//2< mouseLeft< self.chessBoardSize+self.left_th+self.gridSize//2 \
                        and self.edgeup-self.gridSize//2 < mouseTop< self.chessBoardSize+self.top_th+self.gridSize//2:
                    # 根据鼠标点击的具体位置获取在棋盘的位置

                    # 更新当前棋子在棋盘的位置
                    self.top_th = (mouseTop-self.edgeup-self.gridSize//2)//self.gridSize+1
                    self.left_th = (mouseLeft-self.edgeleft-self.gridSize//2)//self.gridSize+1

                    # 如果该位置棋子的标志是-1，表示该位置为空
                    if self.grids[self.top_th][self.left_th] == -1:
                        '''
                        游戏开始时候,self.count=-1,
                        当落下一个棋子时候，self.count=0为偶数，第一个是黑棋子落下
                         '''
                        # 该位置合法，棋子数量增加
                        self.count += 1

                        # 更新棋盘列表，黑棋为0，白棋为1
                        self.grids[self.top_th][self.left_th] = self.count%2
                        self.paintChess()
                    self.judegWin()

    # 3.1 绘制棋子图片
    def paintChess(self):
        self.screen.blit(self.chessPic[self.count%2],
                         (self.left_th*self.gridSize+self.edgeup-self.gridSize//2,
                         self.top_th * self.gridSize + self.edgeleft-self.gridSize//2)
                         )
        self.music()


    def music(self):  # Add music
        pygame.mixer.init()
        pygame.mixer.music.load('hit.mp3')
        # 1 表示播放1次 0.0音乐开始位置
        pygame.mixer.music.play(1, 0.0)

        # 3.3 悔棋逻辑 用空白网格图片覆盖当前棋子的位置，修改相关变量
    def reback(self):
        # 用空白网格图片覆盖当前棋子的位置，
        self.screen.blit(self.chessNullImg,
                         (self.left_th * self.gridSize + self.edgeup - self.gridSize // 2,
                          self.top_th * self.gridSize + self.edgeleft - self.gridSize // 2)
                         )
        # 悔棋，则落子的数量减1
        self.count -= 1
        # 将该位子棋子的标志重新设置为0
        self.grids [self.top_th][self.left_th] = -1
        return True
	
	
    # 3.2 判断是否获胜
    def judegWin(self):
        # 判断上下，水平，两条斜边线上是否存在五子连续
        if self.judgeWinVertical() or self.judgeWinLevel()\
            or self.judgeWinDiagonalLeft() or self.judgeWinDiagonalRight():
            return True

    # 3.2.1 判断垂直线上是否存在5子连续
    def judgeWinVertical(self):
        #获得当前位置标志
        flag = self.grids[self.top_th][self.left_th]

        #判断竖直线上开头和结束位置，即9子的开头和结尾（如果靠近边界，可能不到9子）
        start_top = self.top_th-4
        if start_top<0:
            start_top=0
        end_top = self.top_th+4
        if end_top>self.gridNum:
            end_top = self.gridNum

        # 初始化num,记录连续棋子数量
        num = 0
        for top_th in range(start_top,end_top+1):
            if self.grids[top_th][self.left_th]==flag:
                num += 1
            else:
                num = 0
            if num == 5:
                self.stop = True
                return True
        return False

    # 3.2.2 判断水平线上是否存在5子连续
    def judgeWinLevel(self):
        # 获得当前位置标志
        flag = self.grids[self.top_th][self.left_th]

        # 判断水平线上开头和结束位置，即9子的开头和结尾（如果靠近边界，可能不到9子）
        start_left = self.left_th - 4
        if start_left < 0:
            start_left = 0
        end_left = self.left_th + 4
        if end_left > self.gridNum:
            end_left = self.gridNum


        # 初始化num,记录连续棋子数量
        num = 0
        for left_th in range(start_left, end_left+1):
            if self.grids[self.top_th][left_th] == flag:
                num += 1
            else:
                num = 0
            if num == 5:
                self.stop = True
                return True

        return False

    # 3.2.3 判断垂直线上是否存在5子连续
    def judgeWinDiagonalLeft(self):
        # 获得当前位置标志
        flag = self.grids[self.top_th][self.left_th]

        # 判断斜线上开头和结束位置，即9子的开头和结尾（如果靠近边界，可能不到9子）
        start_left = self.left_th - 4
        start_top = self.top_th - 4
        end_left = self.left_th + 4
        end_top = self.top_th + 4

        if start_left<0 or start_top<0:
            while True:
                start_top += 1
                start_left += 1
                if start_left >= 0 and start_top >= 0:
                    break
        if end_left>self.gridNum or end_top>self.gridNum:
            while True:
                end_top -= 1
                end_left -= 1
                if end_left <= self.gridNum and end_top <= self.gridNum:
                    break

        # 初始化num,记录连续棋子数量
        num = 0
        left_th = start_left
        top_th = start_top
        while left_th <= end_left and top_th <= end_top:
            if self.grids[top_th][left_th] == flag:
                num += 1
            else:
                num = 0

            if num == 5:
                self.stop = True
                return True

            left_th += 1
            top_th += 1
        return False

    # 3.2.4 判断垂直线上是否存在5子连续
    def judgeWinDiagonalRight(self):
        # 获得当前位置标志
        flag = self.grids[self.top_th][self.left_th]

        # 判断斜线上开头和结束位置，即9子的开头和结尾（如果靠近边界，可能不到9子）
        start_left = self.left_th + 4
        start_top = self.top_th - 4
        end_left = self.left_th - 4
        end_top = self.top_th + 4

        if start_left>self.gridNum or start_top<0:
            while True:
                start_top += 1
                start_left -= 1
                if start_left <= self.gridNum and start_top >= 0:
                    break
        if end_left < 0 or end_top>self.gridNum:
            while True:
                end_top -= 1
                end_left += 1
                if end_left >= 0 and end_top <= self.gridNum:
                    break

        # 初始化num,记录连续棋子数量
        num = 0
        left_th = start_left
        top_th = start_top
        while left_th >= 0 and top_th <= end_top:

            if self.grids[top_th][left_th] == flag:
                num += 1
            else:
                num = 0

            if num == 5:
                self.stop = True
                return True

            left_th -= 1
            top_th += 1
        return False

    # 3.3 绘制游戏结束图片
    def endPaint(self):
        if self.count >= self.MAXCOUNT:
            bw1 = self.ft.render("厉害了，旗鼓相当！", True, (100, 100, 100))
        else:
            # 偶数self.count是黑棋子（第一次下self.count=1)
            bw1 = self.ft.render("恭喜"+self.Name[self.count%2]+"获胜！", True, (100, 100, 100))
        bw2 = self.ft.render("输入enter,重新开始游戏", True, (100, 100, 100))
        self.screen.blit(bw1, (self.chessBoardSize // 2 - 200, self.chessBoardSize // 2 - 100))
        self.screen.blit(bw2, (self.chessBoardSize // 2 - 200, self.chessBoardSize // 2-50 ))

    '''第四区域，游戏主函数'''
    def main(self):
        # 设置标题
        pygame.display.set_caption("五子棋")
        self.screen.blit(self.background, (0, 0))

        # 是否进入游戏操作
        while True:
            if self.inGame():
                self.screen.blit(self.background, (0,0))
                break
            pygame.display.update()


        # 进入游戏中
        while True:
            # 调用业务执行函数
            self.action()
            # 刷新函数
            pygame.display.update()

if __name__ == '__main__':
    wzq = wzqGame()
    wzq.main()
