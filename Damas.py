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
        self.set_pos(x, y)

    def set_pos(self, x, y):
        if y < 0 or not tableChess.available(x, y) or x < 0:
            raise IndexError
        else:
            tableChess.table[x][y] = self
            self.x = x
            self.y = y

    def remove(self):
        tableChess.table[self.x][self.y] = None

    def diagonal(self, other):
        return abs(self.x - other.x) == abs(self.y - other.y)

    def can_attack(self, other):
        return abs(self.y - other.y) == 1 and self.diagonal(other) and type(self) != type(other)

    def move(self, inputs):
        pass

    def attack(self, other, *new_pos):
            if tableChess.available(new_pos[0], new_pos[1]):
                self.set_pos(new_pos[0], new_pos[1])
                other.remove()


class WhiteCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dama = False  # Future feature for pieces promotions

    def move(self, inputs):
        if inputs == 'Right' or inputs == 'R':
            self.remove()
            other = tableChess.table[self.x - 1][self.y + 1]  # Fix IndexError Here
            self.check_attack(other, (self.x - 2, self.y + 2),(self.x - 1, self.y + 1))
            '''other = tableChess.table[self.x + 1][self.y - 1]
            self.remove()
            if isinstance(other, BlackCheckers):
                self.attack(other, other.x - 1, other.y + 1)
            else:
                self.set_pos(self.x - 1, self.y + 1)'''

        elif inputs == "Left" or inputs == 'L':
            self.remove()
            other = tableChess.table[self.x - 1][self.y - 1]
            self.check_attack(other, (self.x - 2, self.y - 2), (self.x - 1, self.y - 1))

        ''' other = tableChess.table[self.x - 1][self.y - 1]
                    self.remove()
                    if isinstance(other, BlackCheckers):
                        self.attack(other, other.x - 1, other.y - 1)
                    else:
                        self.set_pos(self.x - 1, self.y - 1)'''

    def check_attack(self, other, atk_pos, reg_pos):
        if isinstance(other, BlackCheckers):
            self.attack(other, atk_pos[0], atk_pos[1])
        else:
            self.set_pos(reg_pos[0], reg_pos[1])

    def __repr__(self):
        return " WT "


class BlackCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dama = False  # Future feature for pieces promotions

    def move(self, inputs):
        if inputs == "Right" or inputs == 'R':
            self.remove()
            self.set_pos(self.x + 1, self.y - 1)

        elif inputs == "Left" or inputs == 'L':
            self.remove()
            self.set_pos(self.x + 1, self.y + 1)

    def __repr__(self):
        return " BK "


def pick_pieces(table):
    while True:
        inputs = input().split()
        pos, mov = valid_input(inputs)
        if not mov:
            """print(Movimiento Invalido)"""
        else:
            objects = table.table[pos[0] - 1][pos[1] - 1]
            '''Here whe have to if objects is a None type or Pieces type
               If it is a Piece type, we have to check whether it can attack or move only
            '''
            if isinstance(objects, Pieces):
                try:
                    objects.move(mov)
                except IndexError:
                    """If it's an out of bound move, set old coordinates to object and Show Error"""
                    objects.set_pos(pos[0] - 1, pos[1] - 1)
        print(tableChess)


def move_pieces(pos, mov, objects):
    pass


def valid_input(inputs):
    valid_pos = ['1', '2', '3', '4', '5', '6', '7', '8', ',']
    valid_mov = ['Right', 'Left', 'R', 'L']
    pos = inputs[0]
    mov = inputs[1]
    for num in pos:
        if num not in valid_pos:
            return None, None
    if mov not in valid_mov:
        return None, None
    return [int(x) for x in pos if x != ','], mov


# tableChess.init_table()
# print(tableChess)
# pick_pieces(tableChess)
# print(tableChess)


w = WhiteCheckers(1,6)
B = BlackCheckers(0,7)
print(tableChess)
pick_pieces(tableChess)
