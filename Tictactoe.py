#tic tac toe game
class Tictactoe:
    def __init__(self):
        self.playingField = ['1','2','3','4','5','6','7','8','9']
        self.board = ""

    def showBoard(self):
        self.board = ""
        for i in range(0,9):
            self.board += self.playingField[i]
            self.board += " "
            if i!=2 and i!=5 and i!=8:
                self.board += '| '
            if i==2 or i==5:
                self.board += '\n'
        return self.board

    def move(self, player, move):
        for i in range(0,9):
            if move == self.playingField[i]:
                self.playingField[i] = player
                print(self.playingField)
        win = self.checkWin(player)
        return win

    def checkWin(self, player):
        win = False
        ID = player
        if self.playingField[0]==ID and self.playingField[1]==ID and self.playingField[2]==ID:
            win = True
        if self.playingField[3]==ID and self.playingField[4]==ID and self.playingField[5]==ID:
            win = True
        if self.playingField[6]==ID and self.playingField[7]==ID and self.playingField[8]==ID:
            win = True
        if self.playingField[0]==ID and self.playingField[3]==ID and self.playingField[6]==ID:
            win = True
        if self.playingField[1]==ID and self.playingField[4]==ID and self.playingField[7]==ID:
            win = True
        if self.playingField[2]==ID and self.playingField[5]==ID and self.playingField[8]==ID:
            win = True
        if self.playingField[0]==ID and self.playingField[4]==ID and self.playingField[8]==ID:
            win = True
        if self.playingField[2]==ID and self.playingField[4]==ID and self.playingField[6]==ID:
            win = True
        return win
# showBoard()
#
# Player1 = 'X'
# Player2 = 'O'
# win1 = False; win2 = False
# while win1 == False and win2 == False:
#     win1 = move(Player1)
#     if win1 == False:
#         win2 = move(Player2)

