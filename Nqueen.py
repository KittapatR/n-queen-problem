# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:40:25 2019

@author: KittapatR

Eight-Queens Problem
"""
import random
import time
import sys

class queensBoard:
    def __init__(self, square):
        assert type(square) == int, "Invalid initialization"
        self.board = [[0 for n in range(square)] for m in range(square)]
        self.unguard = [[1 for n in range(square)] for m in range(square)]
        self.dim = square
        self.updating = False
        self.queens = 0
        self.queensElement = set()
        
    def __repr__(self):
        #Just display
        tmp = ""
        for i in range(self.dim):
            tmp += "| "
            for j in range(self.dim):
                if self.board[i][j] == 1 and self.unguard[i][j] == 1: Display = "A"
                elif self.board[i][j] == 1 and self.unguard[i][j] == 0: Display = "V"
                elif self.unguard[i][j] == 0: Display = ","
                else: Display = "."
                tmp += Display +" "
            tmp += "|\n"
        tmp += """
A = Guarded queen
V = Unguarded queen
. = Safe square
, = Unsafe square"""
        return tmp
    
    def __str__(self):
        #Just display
        tmp = ""
        for i in range(self.dim):
            tmp += "| "
            for j in range(self.dim):
                if self.board[i][j] == 1 and self.unguard[i][j] == 1: Display = "A"
                elif self.board[i][j] == 1 and self.unguard[i][j] == 0: Display = "V"
                elif self.unguard[i][j] == 0: Display = ","
                else: Display = "."
                tmp += Display +" "
            tmp += "|\n"
        tmp += """
A = Guarded queen
V = Unguarded queen
. = Safe square
, = Unsafe square"""
        return tmp
    
    def dim(self):
        return self.dim
    
    def numQueens(self):
        return self.queens
    
    def queensPosition(self):
        return self.queensElement
    
    def placeQueen(self, row, column):
        #Placing queen on the board
        assert [type(row),type(column)] == [int,int], "Invalid value"
        assert 0 <= row < self.dim and 0 <= column < self.dim, "Out of board"
        if self.board[column][row] == 1: return "Fail to place a queen"
        else:
            self.updating = True
            self.board[column][row] = 1
            self.queens += 1
            self.safetyUpdate(row,column,0)
            self.queensElement.add((row,column))
            self.updating = False
        
    def safetyUpdate(self, row, column, guarded):
        #To tell us, it is guarded or not by a condition.
        assert self.updating, "Cannot disturb"
        unguarded1 = row - column
        unguarded2 = row + column
        for i in range(self.dim):
                if i == column: self.unguard[i] = [guarded for n in range(row)]+[1]+[guarded for n in range(self.dim - row - 1)]
                else:
                    self.unguard[i][row] = guarded
                    if 0 <= unguarded1 + i < self.dim: self.unguard[i][unguarded1 + i] = guarded
                    if 0 <= unguarded2 - i < self.dim: self.unguard[i][unguarded2 - i] = guarded
                    
    def unguarded(self, row, column):
        return bool(self.unguard[column][row])
        
    def remove(self, row, column):
        #Remove existing queen
        assert [type(row),type(column)] == [int,int], "Invalid value"
        assert 0 <= row < self.dim and 0 <= column < self.dim, "Out of board"
        if self.board[column][row] == 0: return "Fail to remove a queen"
        else:
            self.updating = True
            self.board[column][row] = 0
            self.queens -= 1
            self.safetyUpdate(row,column,1)
            self.queensElement.remove((row, column))
            for i in range(self.dim):
                for j in range(self.dim):
                    if self.board[i][j] == 1: self.safetyUpdate(j, i, 0)
            self.updating = False
    
    def reset(self):
        #Clear all of queens
        reset = queensBoard(self.dim)
        self.__class__ = reset.__class__
        self.__dict__ = reset.__dict__
        return self


class NqueenSolver:
    
    def __init__(self, n):
        self.queensBoard = queensBoard(n)
        self.solutionDB = set()
    
    def solutionRecursive(self, row = 0, column = 0, decrease = False):
        if self.queensBoard.dim == 0: self.solutionDB.add(0); return len(self.solutionDBA )
        if [row, column] == [0, 0]:
            self.queensBoard.reset()
            self.solutionDB = set()
        if not(row < self.queensBoard.dim):
            if column != 0: return self.solutionRecursive(self.queensBoard.board[column - 1].index(1), column - 1, True)
            else: 
                if 1 in self.queensBoard.board[column]:
                    remove = self.queensBoard.board[column].index(1)
                    self.queensBoard.remove(remove, column)
                    return self.solutionRecursive(remove + 1, column)
                else:
                    return len(self.solutionDB)
        if decrease:
                self.queensBoard.remove(row, column)
                return self.solutionRecursive(row + 1, column)
        if self.queensBoard.unguarded(row, column) and (self.queensBoard.queensPosition() not in self.solutionDB):
            self.queensBoard.placeQueen(row, column)
            if self.queensBoard.numQueens() == self.queensBoard.dim:
                if self.queensBoard.queensPosition() not in self.solutionDB:
                    self.solutionDB.add(frozenset(self.queensBoard.queensPosition()))
                    print("Import Data",len(self.solutionDB))
                self.queensBoard.remove(self.queensBoard.board[column].index(1), column)
                if 1 in self.queensBoard.board[column - 1]: return self.solutionRecursive(self.queensBoard.board[column - 1].index(1), column - 1, True)
                else: return len(self.solutionDB)
            else: 
                return self.solutionRecursive(0, column + 1)
        else:
            return self.solutionRecursive(row + 1, column)
    
    def solution(self):
        
        #Reset board for no disturbation of results
        self.queensBoard.reset()
        self.solutionDB = set()
        
        #Initialize some iteratives
        row = 0
        column = 0
        decrease = False
        
        #Loop will be ended by if the first column cannot place queen anymore.
        while row < self.queensBoard.dim or self.queensBoard.numQueens() != 0:
            
            #Case 1: if the row is out of the board,
            if not(row < self.queensBoard.dim):
                #It will go back to previous column,
                if column != 0:
                    row = self.queensBoard.board[column - 1].index(1)
                    column -= 1
                    decrease = True
                #or if it is the first column, it will insteadly move the first queen to next row.
                else:
                    if 1 in self.queensBoard.board[column]:
                        remove = self.queensBoard.board[column].index(1)
                        self.queensBoard.remove(remove, column)
                        row = remove + 1
            
            #Case 2: if it comes from the previous, then it will move a recent queen to next row.
            elif decrease:
                self.queensBoard.remove(row, column)
                decrease = False
                row += 1
                
            #Case 3: if the expected place is unguarded, place it.
            elif self.queensBoard.unguarded(row, column) and (self.queensBoard.queensPosition() not in self.solutionDB): 
                self.queensBoard.placeQueen(row, column)
                #When the queens are placed correctly, the placement of queens will be recorded to a database.
                if self.queensBoard.numQueens() == self.queensBoard.dim:
                    if self.queensBoard.queensPosition() not in self.solutionDB: 
                        self.solutionDB.add(frozenset(self.queensBoard.queensPosition()))
                        # print("Import Data",len(self.solutionDB))
                    self.queensBoard.remove(self.queensBoard.board[column].index(1), column)
               #Then undo the move and find new solutions.     
                    column -= 1     
                    if 1 not in self.queensBoard.board[column]: break
                    row = self.queensBoard.board[column].index(1)
                    decrease = True
                else:
                    column += 1
                    row = 0
            #Case 4: if the expected place is guarded, move a place by row.
            else:
                row += 1
        
        #Get some summary
        if self.queensBoard.dim == 0: self.solutionDB.add(0)
        return len(self.solutionDB)
    
    def solutionExample(self, randomize = True, index = 0):
        #Random some solutions or select it by hand
        if len(self.solutionDB) == 0: self.solution()
        if randomize: Queen = random.choice(list(self.solutionDB))
        else: Queen = list(self.solutionDB)[index]
        
        for queen in Queen:
            self.queensBoard.placeQueen(queen[0],queen[1])
        return self.queensBoard
        self.queensBoard.reset()

    def timeComplexity(self):
        start1 = time.time()
        self.solution()
        end1 = time.time()
        start2 = time.time()
        self.solutionRecursive()
        end2 = time.time()
        duration1 = end1 - start1
        duration2 = end2 - start2
        if duration1 > duration2: return "Recursive wins by " + str(duration1 - duration2)
        else: return "Iterative wins by "+ str(duration2 - duration1)

def main():
    try:
        while True:
            terminal_input = int(input('Number of columns in a board (0 to exit): '))
            if terminal_input == 0: break
            board = NqueenSolver(terminal_input)
            while True:
                choice = input('''Type number:
1. Number of solution
2. Example solution
3. Exit
''')
                if choice == '1': print(board.solution())
                elif choice == '2': 
                    no_example = int(input('Type what number would you like from -1 to {} (-1 to random): '.format(board.solution()-1)))
                    print(board.solutionExample(randomize = True if no_example == -1 else False, index = no_example if no_example != -1 else 0))
                elif choice == '3': break
                else: print('no choice for this one')

    except: #this traps for unexpected system errors
        input("Unexpected error: ", sys.exc_info()[0])
        raise # this line can be erased. It is here to raise another error so you can see which line to debug.
    else:
        input("\nNormal Termination.   Goodbye!")
if __name__ == "__main__":
    main()