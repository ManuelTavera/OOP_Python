class Table:
    def __init__(self):
        self.table = [[None for x in range(8)] for y in range(8)]

    def avalaible(self, x, y):
        return self.table[x][y]

    def __repr__(self):
        msg = ""
        for i in range(8):
            msg += " _________________________________________\n" + "%s" % (8-i)
            for x in range(8):
                msg += '|' + "{}".format(self.table[i][x])
            msg += '| \n'
        return msg


class Pieces:
    def __init__(self, x, y):
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        tableChess.table[x][y] = self

    def remove(self):
        tableChess.table[self.x][self.y] = None

    def diagonal(self, other):
        return abs(self.x - other.x) == abs(self.y - other.y)


class WhiteCheckers(Pieces):
    def move(self, inputs):
        try:
            if inputs == "Right":
                self.remove()
                self.set_pos(self.x - 1, self.y + 1)

            elif inputs == "Left":
                self.remove()
                pass

        except IndexError:
            pass

    def __repr__(self):
        return " W  "


class BlackCheckers(Pieces):
    def __repr__(self):
        return " B  "


tableChess = Table()
b = WhiteCheckers(4, 7)
print(tableChess)
