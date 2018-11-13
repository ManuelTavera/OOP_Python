class Table:
    def __init__(self):
        self.table = [[None for x in range(8)] for y in range(8)]

    def available(self, x, y):
        return not self.table[x][y]

    def init_table(self):
        for i in range(8):
            for j in range(8):
                if i <= 2 and i % 2 == 0:
                    if j % 2 != 0:
                        self.table[i][j] = BlackCheckers(i, j)
                elif i <= 2 and i % 2 != 0:
                    if j % 2 == 0:
                        self.table[i][j] = BlackCheckers(i, j)

                elif i >= 5 and i % 2 != 0:
                    if j % 2 == 0:
                        self.table[i][j] = WhiteCheckers(i, j)

                elif i >= 5 and i % 2 == 0:
                    if j % 2 != 0:
                        self.table[i][j] = WhiteCheckers(i, j)
        return

    @staticmethod
    def in_bound(x, y):
        if y < 0 or y > 7 or x < 0 or x > 7:
            return False
        return True

    def __repr__(self):
        msg = ""
        for i in range(8):
            msg += " _________________________________________\n" + "%s" % (i + 1)
            for x in range(8):
                msg += '|' + "{}".format(self.table[i][x])
            msg += '| \n'
        return msg


tableChess = Table()


class Pieces:

    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        self.dama = False  # Future feature for pieces promotions
        self.set_pos(x, y)

    def set_pos(self, x, y):
        if not tableChess.in_bound(x, y) or not tableChess.available(x, y):
            raise IndexError
        else:
            tableChess.table[x][y] = self
            self.x = x
            self.y = y

    def remove(self):
        tableChess.table[self.x][self.y] = None

    def diagonal(self, x, y):
        return abs(self.x - x) == abs(self.y - y)

    @staticmethod
    def can_attack(other, cls, x, y):
        return isinstance(other, cls) and tableChess.in_bound(x, y) and tableChess.available(x, y)

    def move(self, inputs):
        pass

    def attack(self, other, *new_pos):
        # It could be added the same if as set_pos here, to check if new_pos is out of ChessBoard
            if tableChess.available(new_pos[0], new_pos[1]):
                self.set_pos(new_pos[0], new_pos[1])
                other.remove()

    def check_attack(self, other, atk_pos, reg_pos, cls, end_pos):
        if self.dama:
            if self.x < end_pos[0]:
                self.rmv_enemy(self.x, end_pos[0], cls)
            else:
                self.rmv_enemy(end_pos[0], self.x, cls)
            self.remove()
            self.set_pos(end_pos[0], end_pos[1])

        elif isinstance(other, cls):
            self.attack(other, atk_pos[0], atk_pos[1])
        else:
            self.set_pos(reg_pos[0], reg_pos[1])

    def rmv_enemy(self, st_pos_x, end_pos_x, cls):
        for x in range(st_pos_x, end_pos_x, 1):
            for y in range(0, 8, 1):
                other = tableChess.table[x][y]
                if self.diagonal(x, y) and isinstance(other, cls):
                    other.remove()

    def dama_inps(self, cls):
        flag = False
        for row in tableChess.table:
            for obj in row:
                if isinstance(obj, cls) and self.diagonal(obj.x, obj.y):
                    # Check lower right side of board
                    if obj.x > self.x and self.y < obj.y and self.can_attack(obj, cls, obj.x+1, obj.y+1):
                        flag = True
                    # Check lower left side of board
                    elif obj.y < self.y and obj.x > self.x and self.can_attack(obj, cls, obj.x+1, obj.y-1):
                        flag = True
                    # Check upper left side of board
                    elif obj.x < self.x and obj.y < self.y and self.can_attack(obj, cls, obj.x-1, obj.y-1):
                        flag = True
                    # Check upper right side of board
                    elif obj.y > self.y and obj.x < self. x and self.can_attack(obj, cls, obj.x-1, obj.y+1):
                        flag = True
        return flag


class WhiteCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self, inputs):
        if self.dama:
            x = inputs[0] - 1
            y = inputs[1] - 1
            if tableChess.in_bound(x, y) and tableChess.available(x, y) and self.diagonal(x, y):
                self.check_attack(None, None, None, BlackCheckers, (x, y))
        else:
            # There was an IndexError here not to long ago >.>
            if inputs == 'Right' or inputs == 'R':
                self.remove()
                other = tableChess.table[self.x - 1][self.y + 1]
                self.check_attack(other, (self.x - 2, self.y + 2), (self.x - 1, self.y + 1), BlackCheckers, None)

            elif inputs == "Left" or inputs == 'L':
                self.remove()
                other = tableChess.table[self.x - 1][self.y - 1]
                self.check_attack(other, (self.x - 2, self.y - 2), (self.x - 1, self.y - 1), BlackCheckers, None)

            if self.x == 0:
                self.dama = True

    def keep_attack(self):
        flag = False
        if self.dama:
            flag = self.dama_inps(BlackCheckers)  # Function define in BaseClass Pieces
        else:
            flag = self.reg_search(self.x, self.y)
        return flag

    def reg_search(self, x, y):
        # Check Right
        if tableChess.in_bound(x-1, y+1):
            other = tableChess.table[x-1][y+1]
            if self.can_attack(other, BlackCheckers, x-2, y+2):
                return True
        # Check Left
        if tableChess.in_bound(x-1, y-1):
            other = tableChess.table[x-1][y-1]
            if self.can_attack(other, BlackCheckers, x-2, y-2):
                return True
        return False

    def __repr__(self):
        if self.dama:
            return "D.WT"
        return " WT "


class BlackCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)

    """ It is the same functions as WhiteCheckers the only change its the coord Black Pieces will move to"""
    # Here too, was the same IndexError >.>
    def move(self, inputs):
        if self.dama:
            x = inputs[0] - 1
            y = inputs[1] - 1
            if tableChess.in_bound(x, y) and tableChess.available(x, y) and self.diagonal(x, y):
                self.check_attack(None, None, None, WhiteCheckers, (x, y))

        else:
            if inputs == "Right" or inputs == 'R':
                self.remove()
                other = tableChess.table[self.x + 1][self.y - 1]
                self.check_attack(other, (self.x + 2, self.y - 2), (self.x + 1, self.y - 1), WhiteCheckers, None)

            elif inputs == "Left" or inputs == 'L':
                self.remove()
                other = tableChess.table[self.x + 1][self.y + 1]
                self.check_attack(other, (self.x + 2, self.y + 2), (self.x + 1, self.y + 1), WhiteCheckers, None)

            if self.x == 7:
                self.dama = True

    def keep_attack(self):
        flag = False
        if self.dama:
            flag = self.dama_inps(WhiteCheckers)  # Function define in BaseClass Pieces
        else:
            flag = self.reg_search(self.x, self.y)
        return flag

    def reg_search(self, x, y):
        # Check Right
        if tableChess.in_bound(x + 1, y - 1):
            other = tableChess.table[x + 1][y - 1]
            if self.can_attack(other, WhiteCheckers, x + 2, y - 2):
                return True
        # Check Left
        if tableChess.in_bound(x + 1, y + 1):
            other = tableChess.table[x + 1][y + 1]
            if self.can_attack(other, WhiteCheckers, x + 2, y + 2):
                return True
        return False

    def __repr__(self):
        if self.dama:
            return "D.BK"
        return " BK "


def pick_pieces(table):
    valid_pos = ['1', '2', '3', '4', '5', '6', '7', '8', ',']
    valid_mov = ["Right", "Left", 'L', 'R']
    while True:
        inputs = input().split()
        if valid_input(inputs[0], valid_pos):
            pos = [int(x) for x in inputs[0] if x != ',']
            objects = table.table[pos[0] - 1][pos[1] - 1]
            '''Here whe have to check if objects is a None type or Pieces type
               If it is a Piece type, we have to check whether it can attack or move only
            '''
            if isinstance(objects, Pieces):
                if objects.dama:
                    if valid_input(inputs[1], valid_pos):
                        mov = [int(x) for x in inputs[1] if x != ',']
                        move_pieces(pos, mov, objects)
                else:
                    if inputs[1] in valid_mov:
                        move_pieces(pos, inputs[1], objects)
        print(tableChess)


def move_pieces(pos, mov, objects):
    try:
        objects.move(mov)
    except IndexError:
        """If it's an Illegal move, set old coordinates to object and Show Error"""
        objects.set_pos(pos[0] - 1, pos[1] - 1)


def valid_input(inputs, valid_list):
    for inp in inputs:
        if inp not in valid_list:
            return False
    return True



w = WhiteCheckers(4, 4)
w.dama = True
b1 = BlackCheckers(2,6)
b2 = BlackCheckers(3,3)
b3 = BlackCheckers(7,7)
b4 = BlackCheckers(6,2)
print(tableChess)
w.keep_attack()
