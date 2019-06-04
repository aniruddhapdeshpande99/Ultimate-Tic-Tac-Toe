from time import time
import random
import signal
import copy
import sys


class Team52:
    def __init__(self):
        self.optimalMove = []

    def move(self, board, old_move, flag):
        TIME = 16
        signal.signal(signal.SIGALRM, handler)
        maxDepth = 5
        moveStore = []
        moved = False
        self.optimalMove = []
        signal.alarm(TIME)
        if old_move == (-1,-1):
            cells = board.find_valid_move_cells(old_move)
            return cells[random.randrange(len(cells))]

        for maxD in xrange(1,maxDepth+1):
            try:
                self.minimax(board, 0, maxD, old_move, flag, -sys.maxint - 1, sys.maxint)
                moveStore.append(self.optimalMove)
            except TimedOutExc:
                moved = True
                if(len(moveStore) == 0):
                    cells = board.find_valid_move_cells(old_move)
                    return cells[random.randrange(len(cells))]
                return moveStore[-1]

        if(moved == False):
            if(len(moveStore) == 0):
                cells = board.find_valid_move_cells(old_move)
                return cells[random.randrange(len(cells))]
            return moveStore[-1]

    def heuristic(self, board, old_move, flag):

        h = 0
        block_stat = board.block_status
        board_stat = board.board_status

        dia_1 = [(1,0),(0,1),(1,2),(2,1)]
        dia_2 = [(2,0),(1,1),(2,2),(3,1)]
        dia_3 = [(1,1),(0,2),(1,3),(2,2)]
        dia_4 = [(2,1),(1,2),(2,3),(3,2)]

        row_count_x = [0,0,0,0]
        index_row_count = 0
        col_count_x = [0,0,0,0]
        index_col_count = 0
        dia_count_x = [0,0,0,0]

        row_count_o = [0,0,0,0]
        index_row_count_o = 0
        col_count_o = [0,0,0,0]
        index_col_count_o = 0
        dia_count_o = [0,0,0,0]

        Brow_count_o = [0,0,0,0]
        index_Brow_count_o = 0
        Bcol_count_o = [0,0,0,0]
        index_Bcol_count_o = 0
        Bdia_count_o = [0,0,0,0]

        Brow_count_x = [0,0,0,0]
        index_Brow_count_x = 0
        Bcol_count_x = [0,0,0,0]
        index_Bcol_count_x = 0
        Bdia_count_x = [0,0,0,0]



        #If win then highest heuristic
        winDrawLose = board.find_terminal_state()

        if winDrawLose[1] == "WON":
            if winDrawLose[0] == flag:
                return 100000
            else:
                return -100000

        if winDrawLose == "DRAW":
            return 0

        curr_block = (old_move[0]%4, old_move[1]%4)




        #Counting Player in each diamond for both board and blocks
        for i in dia_1:
            if(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'x'):
                dia_count_x[0] = dia_count_x[0] + 1
            elif(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'o'):
                dia_count_o[0] = dia_count_o[0] + 1

            if(block_stat[i[0]][i[1]] == 'x'):
                Bdia_count_x[0] = Bdia_count_x[0] + 1
            elif(block_stat[i[0]][i[1]] == 'o'):
                Bdia_count_o[0] = Bdia_count_o[0] + 1

        for i in dia_2:
            if(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'x'):
                dia_count_x[1] = dia_count_x[1] + 1
            elif(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'o'):
                dia_count_o[1] = dia_count_o[1] + 1

            if(block_stat[i[0]][i[1]] == 'x'):
                Bdia_count_x[1] = Bdia_count_x[1] + 1
            elif(block_stat[i[0]][i[1]] == 'o'):
                Bdia_count_o[1] = Bdia_count_o[1] + 1

        for i in dia_3:
            if(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'x'):
                dia_count_x[2] = dia_count_x[2] + 1
            elif(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'o'):
                dia_count_o[2] = dia_count_o[2] + 1

            if(block_stat[i[0]][i[1]] == 'x'):
                Bdia_count_x[2] = Bdia_count_x[2] + 1
            elif(block_stat[i[0]][i[1]] == 'o'):
                Bdia_count_o[2] = Bdia_count_o[2] + 1

        for i in dia_4:
            if(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'x'):
                dia_count_x[3] = dia_count_x[3] + 1
            elif(board_stat[curr_block[0]*4 + i[0]][curr_block[1]*4 + i[1]] == 'o'):
                dia_count_o[3] = dia_count_o[3] + 1

            if(block_stat[i[0]][i[1]] == 'x'):
                Bdia_count_x[3] = Bdia_count_x[3] + 1
            elif(block_stat[i[0]][i[1]] == 'o'):
                Bdia_count_o[3] = Bdia_count_o[3] + 1


        #Counting Player in each row for both board and blocks
        for i in range(curr_block[0]*4, curr_block[0]*4 + 4):
            for j in range(curr_block[1]*4, curr_block[1]*4 + 4):
                if board_stat[i][j] == 'x':
                    row_count_x[index_row_count] = row_count_x[index_row_count] + 1
            index_row_count = index_row_count + 1

        for i in range(curr_block[0]*4, curr_block[0]*4 + 4):
            for j in range(curr_block[1]*4, curr_block[1]*4 + 4):
                if board_stat[i][j] == 'o':
                    row_count_o[index_row_count_o] = row_count_o[index_row_count_o] + 1
            index_row_count_o = index_row_count_o + 1

        for i in range(0,4):
            for j in range(0,4):
                if block_stat[i][j] == 'x':
                    Brow_count_x[index_Brow_count_x] = Brow_count_x[index_Brow_count_x] + 1
            index_Brow_count_x = index_Brow_count_x + 1

        for i in range(0,4):
            for j in range(0,4):
                if block_stat[i][j] == 'o':
                    Brow_count_o[index_Brow_count_o] = Brow_count_o[index_Brow_count_o] + 1
            index_Brow_count_o = index_Brow_count_o + 1





        #Counting Player in each column for both board and blocks
        for i in range(curr_block[1]*4, curr_block[1]*4 + 4):
            for j in range(curr_block[0]*4, curr_block[0]*4 + 4):
                if board_stat[j][i] == 'x':
                    col_count_x[index_col_count] = col_count_x[index_col_count] + 1
            index_col_count = index_col_count + 1

        for i in range(curr_block[1]*4, curr_block[1]*4 + 4):
            for j in range(curr_block[0]*4, curr_block[0]*4 + 4):
                if board_stat[j][i] == 'o':
                    col_count_o[index_col_count_o] = col_count_o[index_col_count_o] + 1
            index_col_count_o = index_col_count_o + 1

        for i in range(0,4):
            for j in range(0,4):
                if block_stat[j][i] == 'o':
                    Bcol_count_o[index_Bcol_count_o] = Bcol_count_o[index_Bcol_count_o] + 1
            index_Bcol_count_o = index_Bcol_count_o + 1

        for i in range(0,4):
            for j in range(0,4):
                if block_stat[j][i] == 'x':
                    Bcol_count_x[index_Bcol_count_x] = Bcol_count_x[index_Bcol_count_x] + 1
            index_Bcol_count_x = index_Bcol_count_x + 1





        #Assigning heuristic values to win based on count within row, column or diamond
        if flag == 'o':
            for i in range(curr_block[0], curr_block[0]+ 4):
                for j in range(curr_block[1], curr_block[1]+ 4):
                    #Heuristic based on number of Player moves in a row in a block
                    if Brow_count_x[i%4] == 1:
                        if Brow_count_o[i%4] == 3:
                            h = h + 1000
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 200
                        else:
                            h = h + 300

                    elif Brow_count_x[i%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 500
                        else:
                            h = h + 400
                    elif Brow_count_x[i%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 800
                        else:
                            h = h + 600
                    elif Brow_count_x[i%4] == 4:
                        h = h + 10000


                    #Heuristic based on number of Player moves in a column in a block
                    if Bcol_count_x[j%4] == 1:
                        if Bcol_count_o[j%4] == 3:
                            h = h + 1000
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 200
                        else:
                            h = h + 300

                    elif Bcol_count_x[j%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 500
                        else:
                            h = h + 400
                    elif Bcol_count_x[j%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 800
                        else:
                            h = h + 600
                    elif Bcol_count_x[j%4] == 4:
                        h = h + 10000

                    #Heuristic based on number of Player moves in each diamond in a block
                    #Top left diamond
                    if (i%4,j%4) in dia_1:
                        if Bdia_count_x[0] == 1:
                            if Bdia_count_o[0] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[0] == 2:
                            if Bdia_count_o[0] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[0] == 3:
                            h = h + 800
                        elif Bdia_count_x[0] == 4:
                            h = h + 10000

                    #Bottom Left diamond
                    if (i%4,j%4) in dia_2:
                        if Bdia_count_x[1] == 1:
                            if Bdia_count_o[1] == 3:
                                h = h + 1000
                            else:
                                h = h + 200

                        elif Bdia_count_x[1] == 2:
                            if Bdia_count_o[1] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[1] == 3:
                            h = h + 800
                        elif Bdia_count_x[1] == 4:
                            h = h + 10000

                    #Top Right diamond
                    if (i%4,j%4) in dia_3:
                        if Bdia_count_x[2] == 1:
                            if Bdia_count_o[2] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[2] == 2:
                            if Bdia_count_o[2] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[2] == 3:
                            h = h + 800
                        elif Bdia_count_x[2] == 4:
                            h = h + 10000

                    #Bottom right diamond
                    if (i%4,j%4) in dia_4:
                        if Bdia_count_x[3] == 1:
                            if Bdia_count_o[3] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[3] == 2:
                            if Bdia_count_o[3] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[3] == 3:
                            h = h + 800
                        elif Bdia_count_x[3] == 4:
                            h = h + 10000

                    # #Heuristic based on number of Player moves in each diamond
                    # #Top left diamond
                    # if (i%4,j%4) in dia_1:
                    #     if Bdia_count_o[0] == 1:
                    #         if Bdia_count_x[0] == 3:
                    #             h = h + 1000
                    #         else:
                    #             h = h + 200
                    #     elif Bdia_count_o[0] == 2:
                    #         if Bdia_count_x[0] == 2:
                    #             h = h + 800
                    #         else:
                    #             h = h + 400
                    #     elif Bdia_count_o[0] == 3:
                    #         h = h + 800
                    #     elif Bdia_count_o[0] == 4:
                    #         h = h + 10000
                    #
                    # #Bottom Left diamond
                    # if (i%4,j%4) in dia_2:
                    #     if Bdia_count_o[1] == 1:
                    #         if Bdia_count_x[1] == 3:
                    #             h = h + 1000
                    #         else:
                    #             h = h + 200
                    #
                    #     elif Bdia_count_o[1] == 2:
                    #         if Bdia_count_x[1] == 2:
                    #             h = h + 800
                    #         else:
                    #             h = h + 400
                    #     elif Bdia_count_o[1] == 3:
                    #         h = h + 800
                    #     elif Bdia_count_o[1] == 4:
                    #         h = h + 10000
                    #
                    # #Top Right diamond
                    # if (i%4,j%4) in dia_3:
                    #     if Bdia_count_o[2] == 1:
                    #         if Bdia_count_x[2] == 3:
                    #             h = h + 1000
                    #         else:
                    #             h = h + 200
                    #     elif Bdia_count_o[2] == 2:
                    #         if Bdia_count_x[2] == 2:
                    #             h = h + 800
                    #         else:
                    #             h = h + 400
                    #     elif Bdia_count_o[2] == 3:
                    #         h = h + 800
                    #     elif Bdia_count_o[2] == 4:
                    #         h = h + 10000
                    #
                    # #Bottom right diamond
                    # if (i%4,j%4) in dia_4:
                    #     if Bdia_count_o[3] == 1:
                    #         if Bdia_count_x[3] == 3:
                    #             h = h + 1000
                    #         else:
                    #             h = h + 200
                    #     elif Bdia_count_o[3] == 2:
                    #         if Bdia_count_x[3] == 2:
                    #             h = h + 800
                    #         else:
                    #             h = h + 400
                    #     elif Bdia_count_o[3] == 3:
                    #         h = h + 800
                    #     elif Bdia_count_o[3] == 4:
                    #         h = h + 10000

            for i in range(curr_block[0]*4, curr_block[0]*4 + 4):
                for j in range(curr_block[1]*4, curr_block[1]*4 + 4):
                    #Heuristic based on number of Player moves in a row in board
                    if row_count_x[i%4] == 1:
                        if row_count_o[i%4] == 3:
                            h = h + 100
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 20
                        else:
                            h = h + 30

                    elif row_count_x[i%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 50
                        else:
                            h = h + 40
                    elif row_count_x[i%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 80
                        else:
                            h = h + 60
                    elif row_count_x[i%4] == 4:
                        h = h + 1000


                    #Heuristic based on number of Player moves in a column in board
                    if col_count_x[j%4] == 1:
                        if col_count_o[j%4] == 3:
                            h = h + 100
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 20
                        else:
                            h = h + 30

                    elif col_count_x[j%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 50
                        else:
                            h = h + 40
                    elif col_count_x[j%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 80
                        else:
                            h = h + 60
                    elif col_count_x[j%4] == 4:
                        h = h + 1000


                    #Heuristic based on number of Player moves in each diamond in board
                    #Top left diamond
                    if (i%4,j%4) in dia_1:
                        if dia_count_x[0] == 1:
                            if dia_count_o[0] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_x[0] == 2:
                            if dia_count_o[0] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_x[0] == 3:
                            h = h + 80
                        elif dia_count_x[0] == 4:
                            h = h + 1000

                    #Bottom Left diamond
                    if (i%4,j%4) in dia_2:
                        if dia_count_x[1] == 1:
                            if dia_count_o[1] == 3:
                                h = h + 100
                            else:
                                h = h + 20

                        elif dia_count_x[1] == 2:
                            if dia_count_o[1] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_x[1] == 3:
                            h = h + 80
                        elif dia_count_x[1] == 4:
                            h = h + 1000

                    #Top Right diamond
                    if (i%4,j%4) in dia_3:
                        if dia_count_x[2] == 1:
                            if dia_count_o[2] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_x[2] == 2:
                            if dia_count_o[2] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_x[2] == 3:
                            h = h + 80
                        elif dia_count_x[2] == 4:
                            h = h + 1000

                    #Bottom right diamond
                    if (i%4,j%4) in dia_4:
                        if dia_count_x[3] == 1:
                            if dia_count_o[3] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_x[3] == 2:
                            if dia_count_o[3] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_x[3] == 3:
                            h = h + 80
                        elif dia_count_x[3] == 4:
                            h = h + 1000

        else:
            for i in range(curr_block[0], curr_block[0]+ 4):
                for j in range(curr_block[1], curr_block[1]+ 4):
                    #Heuristic based on number of Player moves in a row in a block
                    if Brow_count_x[i%4] == 1:
                        if Brow_count_o[i%4] == 3:
                            h = h + 1000
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 200
                        else:
                            h = h + 300

                    elif Brow_count_x[i%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 500
                        else:
                            h = h + 400
                    elif Brow_count_x[i%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 800
                        else:
                            h = h + 600
                    elif Brow_count_x[i%4] == 4:
                        h = h + 10000


                    #Heuristic based on number of Player moves in a column in a block
                    if Bcol_count_x[j%4] == 1:
                        if Bcol_count_o[j%4] == 3:
                            h = h + 1000
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 200
                        else:
                            h = h + 300

                    elif Bcol_count_x[j%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 500
                        else:
                            h = h + 400
                    elif Bcol_count_x[j%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 800
                        else:
                            h = h + 600
                    elif Bcol_count_x[j%4] == 4:
                        h = h + 10000

                    #Heuristic based on number of Player moves in each diamond in a block
                    #Top left diamond
                    if (i%4,j%4) in dia_1:
                        if Bdia_count_x[0] == 1:
                            if Bdia_count_o[0] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[0] == 2:
                            if Bdia_count_o[0] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[0] == 3:
                            h = h + 800
                        elif Bdia_count_x[0] == 4:
                            h = h + 10000

                    #Bottom Left diamond
                    if (i%4,j%4) in dia_2:
                        if Bdia_count_x[1] == 1:
                            if Bdia_count_o[1] == 3:
                                h = h + 1000
                            else:
                                h = h + 200

                        elif Bdia_count_x[1] == 2:
                            if Bdia_count_o[1] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[1] == 3:
                            h = h + 800
                        elif Bdia_count_x[1] == 4:
                            h = h + 10000

                    #Top Right diamond
                    if (i%4,j%4) in dia_3:
                        if Bdia_count_x[2] == 1:
                            if Bdia_count_o[2] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[2] == 2:
                            if Bdia_count_o[2] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[2] == 3:
                            h = h + 800
                        elif Bdia_count_x[2] == 4:
                            h = h + 10000

                    #Bottom right diamond
                    if (i%4,j%4) in dia_4:
                        if Bdia_count_x[3] == 1:
                            if Bdia_count_o[3] == 3:
                                h = h + 1000
                            else:
                                h = h + 200
                        elif Bdia_count_x[3] == 2:
                            if Bdia_count_o[3] == 2:
                                h = h + 800
                            else:
                                h = h + 400
                        elif Bdia_count_x[3] == 3:
                            h = h + 800
                        elif Bdia_count_x[3] == 4:
                            h = h + 10000

            for i in range(curr_block[0]*4, curr_block[0]*4 + 4):
                for j in range(curr_block[1]*4, curr_block[1]*4 + 4):
                    #Heuristic based on number of Player moves in a row in board
                    if row_count_o[i%4] == 1:
                        if row_count_x[i%4] == 3:
                            h = h + 100
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 20
                        else:
                            h = h + 30

                    elif row_count_o[i%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 50
                        else:
                            h = h + 40
                    elif row_count_o[i%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 80
                        else:
                            h = h + 60
                    elif row_count_o[i%4] == 4:
                        h = h + 1000


                    #Heuristic based on number of Player moves in a column in board
                    if col_count_o[j%4] == 1:
                        if col_count_x[j%4] == 3:
                            h = h + 100
                        if (i%4 == 0 and j%4 == 0) or (i%4 == 0 and j%4 == 3) or (i%4 ==3 and j%4 == 0) or (i%4 == 3 and j%4 == 3):
                            h = h + 20
                        else:
                            h = h + 30

                    elif col_count_o[j%4] == 2:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 50
                        else:
                            h = h + 40
                    elif col_count_o[j%4] == 3:
                        if(i%4 != 0 and j%4 != 0) or (i%4 != 0 and j%4 != 3) or (i%4 !=3 and j%4 != 0) or (i%4 != 3 and j%4 != 3):
                            h = h + 80
                        else:
                            h = h + 60
                    elif col_count_o[j%4] == 4:
                        h = h + 1000


                    #Heuristic based on number of Player moves in each diamond in board
                    #Top left diamond
                    if (i%4,j%4) in dia_1:
                        if dia_count_o[0] == 1:
                            if dia_count_x[0] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_o[0] == 2:
                            if dia_count_x[0] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_o[0] == 3:
                            h = h + 80
                        elif dia_count_o[0] == 4:
                            h = h + 1000

                    #Bottom Left diamond
                    if (i%4,j%4) in dia_2:
                        if dia_count_o[1] == 1:
                            if dia_count_x[1] == 3:
                                h = h + 100
                            else:
                                h = h + 20

                        elif dia_count_o[1] == 2:
                            if dia_count_x[1] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_o[1] == 3:
                            h = h + 80
                        elif dia_count_o[1] == 4:
                            h = h + 1000

                    #Top Right diamond
                    if (i%4,j%4) in dia_3:
                        if dia_count_o[2] == 1:
                            if dia_count_x[2] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_o[2] == 2:
                            if dia_count_x[2] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_o[2] == 3:
                            h = h + 80
                        elif dia_count_o[2] == 4:
                            h = h + 1000

                    #Bottom right diamond
                    if (i%4,j%4) in dia_4:
                        if dia_count_o[3] == 1:
                            if dia_count_x[3] == 3:
                                h = h + 100
                            else:
                                h = h + 20
                        elif dia_count_o[3] == 2:
                            if dia_count_x[3] == 2:
                                h = h + 80
                            else:
                                h = h + 40
                        elif dia_count_o[3] == 3:
                            h = h + 80
                        elif dia_count_o[3] == 4:
                            h = h + 1000


        return h

    def minimax(self, board, currentDepth, maxDepth, old_move, flag, alpha, beta):
        x = currentDepth
        max_reach = self.heuristic(board, old_move, flag)
        if(x == maxDepth):
            return max_reach

        actions = board.find_valid_move_cells(old_move)
        if(flag == 'x'):
            ans = -sys.maxint - 1
            for action in actions:
                newBoard = copy.deepcopy(board)
                newBoard.update(old_move, action , 'x');

                curMinimax = self.minimax(newBoard, currentDepth + 1, maxDepth, action, 'o', alpha, beta)
                if(curMinimax > ans):
                    if(currentDepth == 0):
                        self.optimalMove = action

                ans = max(ans, curMinimax)
                if(ans > beta or ans == beta):
                    return ans

                alpha = max(alpha, ans)
            return ans

        elif(flag == 'o'):
            ans = sys.maxint
            for action in actions:
                newBoard = copy.deepcopy(board)
                newBoard.update(old_move, action , 'o');

                curMinimax = self.minimax(newBoard, currentDepth + 1, maxDepth, action, 'x', alpha, beta)
                if(curMinimax < ans):
                    if(currentDepth == 0):
                        self.optimalMove = action
                ans = min(ans, curMinimax)
                if(ans < alpha or ans == alpha):
                    return ans
                beta = min(beta, ans)

            return ans

class TimedOutExc(Exception):
	pass

def handler(signum, frame):
	#print 'Signal handler called with signal', signum
	raise TimedOutExc()
