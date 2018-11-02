class Table:
    def __init__(self):
        self.table = [[None for x in range(8)] for y in range(8)]

    def available(self, x, y):
        return self.table[x][y]

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
        self.x = x
        self.y = y
        tableChess.table[x][y] = self

    def remove(self):
        tableChess.table[self.x][self.y] = None

    def diagonal(self, other):
        return abs(self.x - other.x) == abs(self.y - other.y)

    def can_attack(self, other):
        return abs(self.y - other.y) == 1 and self.diagonal(other)


class WhiteCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dama = False

    def move(self, inputs):
        if inputs == 'Right' or inputs == 'R':
            self.remove()
            self.set_pos(self.x - 1, self.y + 1)

        elif inputs == "Left" or inputs == 'L':
            self.remove()
            self.set_pos(self.x - 1, self.y - 1)


    def attack(self, other):
        if Pieces.can_attack(self, other):
            if self.y < other.y:
                pass

    def __repr__(self):
        return " WT "


class BlackCheckers(Pieces):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dama = False

    def move(self, inputs):
        if inputs == "Right" or inputs == 'R':
            self.remove()
            self.set_pos(self.x + 1, self.y - 1)

        elif inputs == "Left" or inputs == 'L':
            self.remove()
            self.set_pos(self.x + 1, self.y + 1)

    def __repr__(self):
        return " BK "


def init_table(table):
    for i in range(8):
        for j in range(8):
            if i <= 2 and i % 2 == 0:
                if j % 2 != 0:
                    table.table[i][j] = BlackCheckers(i, j)
            elif i <= 2 and i % 2 != 0:
                if j % 2 == 0:
                    table.table[i][j] = BlackCheckers(i, j)

            elif i >= 5 and i % 2 != 0:
                if j % 2 == 0:
                    table.table[i][j] = WhiteCheckers(i, j)

            elif i >= 5 and i % 2 == 0:
                if j % 2 != 0:
                    table.table[i][j] = WhiteCheckers(i, j)
    return


def pick_pieces(table):
    while True:
        inputs = input().split()
        pos, mov = valid_input(inputs)
        if not mov:
            """print(Movimiento Invalido)"""
        else:
            objects = table.table(pos[0], pos[1])
            if isinstance(objects, WhiteCheckers) or isinstance(objects, BlackCheckers):
                try:
                    objects.move(mov)
                    break
                except ValueError:
                    pass
            else:
                """print(La casilla seleccionada no es una pieza)"""


def valid_input(inputs):
    valid_pos = ['1','2','3','4','5','6','7','8', ',']
    valid_mov = ['Right', 'Left', 'R', 'L']
    pos = inputs[0]
    mov = inputs[1]
    for num in pos:
        if num not in valid_pos:
            return None, None
    if mov not in valid_mov:
        return None, None
    return [int(x) for x in pos if x != ','], mov


init_table(tableChess)
print(tableChess)
pick_pieces(tableChess)
print(tableChess)
