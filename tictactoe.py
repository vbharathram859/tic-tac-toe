import numpy as np
def main():
    player_1 = AI()
    player_2 = Human_Player()
    t = TicTacToe(player_1, player_2)
    t.play_game()

class TicTacToe(object):
    def __init__(self, player_1, player_2):  # player_1, player_2 are objects, player_1 starts
        self.state = np.zeros((3, 3))  # empty board
        player_1.set_player(1)  # use 1 to denote this players moves in self.state
        player_2.set_player(2)
        self.player_1 = player_1
        self.player_2 = player_2

    def __str__(self):
        string = ""
        for i in range(3):
            string += " "  # add space before each x or o
            for j in range(3):
                if self.state[i, j] == 0:  # blank
                    string += "   "
                elif self.state[i, j] == 1:  # player 1
                    string += " x "
                else:  # player 2
                    string += " o "
                if j != 2:  # add a vertical bar
                    string += "|"
            if i!=2:  # add a horizontal bar
                string+= "\n—————————————\n"
        string += "\n———————————————————————————————————\n"  # to separate the moves
        return string

    def play_game(self):
        cur = 1  # player 1 starts
        while not check_draw(self.state) and not check_win(self.state, cur):  # if the game is not over
            print(self)
            self.move(cur)  # player should make their move
            if cur == 1:  # switch turn
                cur = 2
            else:
                cur = 1
        if check_draw(self.state):  # if it is a draw
            print(self)
            print("\nIt's a tie!")
        elif check_win(self.state, 1)[0] == 1:  # if player 1 won
            print(self)
            print(f"\n{self.player_1.get_name()} wins!")
        else:  # if player 2 won
            print(self)
            print(f"\n{self.player_2.get_name()} wins!")

    def move(self, cur):
        if cur == 1:  # if it is player one's turn, they should make a move
            self.state = self.player_1.move(self.state)
        else:  # else call player two's move function
            self.state = self.player_2.move(self.state)


class Human_Player(object):
    def __init__(self):
        self.name = "Human"

    def set_player(self, player):
        self.player = player

    def move(self, state):
        row = input("Which row would you like your move to be in? ")
        column = input("Which column would you like your move to be in? ")
        print("\n")
        try: # check if tey gave a number
            row = int(row)
            column = int(column)
        except:
            print("Illegal move")
            return self.move(state)
        if row > 3 or row < 1:  # if they gave a legal number for row
            print("Illegal move")
            return self.move(state)
        if column > 3 or column < 1:  # if they gave a legal number for column
            print("Illegal move")
            return self.move(state)
        if state[row - 1, column - 1] != 0:  # if this space has been used
            print("Illegal move")
            return self.move(state)
        else:  # otherwise it is legal, so change state
            state[row - 1, column - 1] = self.player
        return state

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class AI(object):
    def __init__(self):
        self.name = "Computer"

    def set_player(self, player):
        self.player = player

    def move(self, state):
        print(f"{self.name} move:\n")
        move = minimax(state, self.player, self.player)  # find the right move using minimax
        return move[1]  # move[0] is score, move[1] is board

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

def check_win(state, player):  # player is either 1 or 2, depening on whether we are cheking if player 1 won or if player 2 won
    for i in range(3):
        if state[i][0]==state[i][1]==state[i][2] and state[i][0] != 0:  # horizontal win
            if player == state[i][0]:  # if player won, return 1
                return 1, state
            return -1, state  # else return -1
        elif state[0][i]==state[1][i]==state[2][i] and state[0][i] != 0:  # vertical win
            if player == state[0][i]:  # if player won, return 1
                return 1, state
            return -1, state  # else return -1
    if state[0][0]==state[1][1]==state[2][2] and state[0][0] != 0:  # left to right diagonal
        if player == state[0][0]:  # if player won, return 1
            return 1, state
        return -1, state  # else return -1
    if state[2][0]==state[1][1]==state[0][2] and state[0][2] != 0:  # right to left diagonal
        if player == state[0][2]:  # if player won, return 1
            return 1, state
        return -1, state  # else return -1
    return False

def check_draw(state):
    return len(np.where(state==0)[0])==0  # if there are no blank spaces

def rotations(state):
    rot = []
    for i in range(1, 4):
        rot.append(np.rot90(state, i))  # rot90 returns a copy of a numpy array rotated 90 degrees i times
    return rot

def reflections(state):
    reflr = np.fliplr(state)  # flip in the left right direction
    refud = np.flipud(state)  # flip in the up down direction
    return [reflr, refud]

def equiv(state):
    return reflections(state)+rotations(state)  # return the rotations and reflections as one list

def minimax(state, player, cur):
    win = check_win(state, player)
    if win is not False:  # win is False if nobody won yet
        return win  # if it is not False, then it is either 1 or -1 depending on who won

    empty = np.where(state==0)  # all the empty spaces
    children = []

    if len(empty[0]) == 0:  # if it's a draw
        return 0, state

    for i in range(len(empty[0])):  # go through every empty space
        new_state = state.copy()
        new_state[empty[0][i], empty[1][i]] = cur  # simulate that move

        old = False  # whether we have found minimax of an equivalent state already
        same = equiv(new_state)  # list of all equivalent board states

        for item in same:
            for child in children:
                if np.array_equal(item, child[1]):  # if we have already computed minimax of an equivalent state
                    children.append((child[0], new_state))
                    old = True
                    break

        if cur == 1 and not old:
            children.append((minimax(new_state, player, 2)[0], new_state))  # find minimax of each child
        elif not old:
            children.append((minimax(new_state, player, 1)[0], new_state))
    if player == cur:  # if we want the max
        return max(children, key=lambda x:x[0])
    return min(children, key=lambda x:x[0])  # otherwise other players turn, and they will choose min


main()
