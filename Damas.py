class Table:
    def __init__(self):
        self.table = [[None for x in range(8)] for y in range(8)]

    def avalaible(self, x, y):
        return self.table[x][y]

    def __repr__(self):
        msg = ""
        for i in range(8):
            msg += " _________________________________________\n" + "%s" % (i+1)
            for x in range(8):
                msg += '|' + "{}".format(self.table[i][x])
            msg += '| \n'
        return msg


class Pieces:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.set_pos(x, y)

    def set_pos(self, x, y):
        tableChess.table[x][y] = self

    def remove(self):
        tableChess.table[self.x][self.y] = None

    def diagonal(self, other):
        return abs(self.x - other.x) == abs(self.y - other.y)

    def move(self, inputs):
        if inputs == 'Right':
            self.x, self.y = self.x + 1, self.y + 1
        else:
            pass



class WhiteCheckers(Pieces):
    def __repr__(self):
        return " W  "


class BlackCheckers(Pieces):
    def __repr__(self):
        return " B  "


