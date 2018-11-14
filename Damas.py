import os
import sys


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

    def check_pcs(self):
        blackP = 0
        whiteP = 0
        game_block = True
        for row in self.table:
            for obj in row:
                if isinstance(obj, WhiteCheckers):
                    whiteP += 1
                    coord_list = ((obj.x+1, obj.y+1), (obj.x+1, obj.y-1), (obj.x-1, obj.y+1), (obj.x-1, obj.y-1))
                    game_block = self.check_coord(obj, coord_list)

                elif isinstance(obj, BlackCheckers):
                    blackP += 1
                    coord_list = ((obj.x-1, obj.y+1), (obj.x-1, obj.y-1), (obj.x+1, obj.y+1), (obj.x+1, obj.y-1))
                    game_block = self.check_coord(obj, coord_list)
        return blackP, whiteP, game_block

    def check_coord(self, obj, coord_list):
        if obj.dama:
            for x, y in coord_list:
                if self.in_bound(x, y) and self.available(x, y):
                    return False
        else:
            for x, y in coord_list[2:]:
                if self.in_bound(x, y) and self.available(x, y):
                    return False

    def end_game(self):
        whiteP, blackP, game_block = self.check_pcs()
        if game_block or whiteP == 0 or blackP == 0:
            return True
        return False

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
        self.dama = False
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

        elif isinstance(other, cls) and tableChess.available(atk_pos[0], atk_pos[1]):
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
                self.check_attack(None, [], None, BlackCheckers, (x, y))
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
                self.check_attack(None, [], None, WhiteCheckers, (x, y))

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


def clean(board, msg=None):
    if msg is not None:
        print(msg)
        os.system('pause')
    os.system('cls')
    print(board)


def pick_pieces(table, player, valid_pos, valid_mov, keep_atk=False):
    end_turn = False
    able_to_atk = True
    while True:
        inputs = input().split()
        if valid_input(inputs[0], valid_pos):
            pos = [int(x) for x in inputs[0] if x != ',']
            objects = table.table[pos[0] - 1][pos[1] - 1]
            '''Here whe have to check if objects is a None type or Pieces type
               And check whether the pieces belongs to player or not
            '''
            if isinstance(objects, player):
                if not objects.keep_attack():
                    able_to_atk = False

                if objects.dama:
                    if valid_input(inputs[1], valid_pos):
                        mov = [int(x) for x in inputs[1] if x != ',']
                        end_turn = move_pieces(pos, mov, objects, table)
                    else:
                        clean(table, 'Movimiento Invalido')
                else:
                    if inputs[1] in valid_mov:
                        end_turn = move_pieces(pos, inputs[1], objects, table)
                    else:
                        clean(table, 'Movimiento Invalido')

                if objects.keep_attack():
                    keep_atk = True

                if end_turn:
                    break
            else:
                clean(table, "No es el turno de la ficha seleccionada")
        else:
            clean(table, 'Entrada Invalida')

    if keep_atk and able_to_atk:
        clean(table, 'Puedes Atacar Denuevo con la misma pieza')
        return pick_pieces(table, player, valid_pos, valid_mov, False)


def move_pieces(pos, mov, objects, board):
    end_turn = False
    try:
        objects.move(mov)
        end_turn = True
    except IndexError:
        """If it's an Illegal move, set old coordinates to object and Show Error"""
        objects.set_pos(pos[0] - 1, pos[1] - 1)
        clean(board, "Movimiento Invalido")
    return end_turn


def valid_input(inputs, valid_list):
    flag = True
    if inputs:
        for inp in inputs:
            if inp not in valid_list:
                flag = False
    else:
        flag = False
    return flag


def game(board):
    print("Bienvenido al Juego de Damas")
    print("Para Mover una pieza no promovida es con esta notacion: x,y + Right, Left, R, L")
    print("Por ejemplo, 5,5 Right")
    print("Para mover a una pieza promovida es asi: x,y x,y")
    print("Por ejemplo, 5,5 6,6")
    print("Las blancas juegan primero")
    os.system('pause')
    os.system('cls')
    valid_pos = ['1', '2', '3', '4', '5', '6', '7', '8', ',']
    valid_mov = ["Right", "Left", 'L', 'R']
    p1 = WhiteCheckers
    p2 = BlackCheckers
    board.init_table()
    print(board)
    while not board.end_game():
        pick_pieces(board, p1, valid_pos, valid_mov)
        clean(board)
        pick_pieces(board, p2, valid_pos, valid_mov)
        clean(board)
    clean(board, 'Se termino el juego')


game(tableChess)


