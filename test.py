

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"



class Ship:
    def __init__(self, bow, l , o):
        self.bow = bow
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6 ):
        self.size = size
        self.hid = hid

        self.count = 0
        self.filde = [["O"]*size for _ in range(size)]

        self.busy = []  # список занятых точек
        self.ships = [] # список короблей доски

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.filde):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace(" ", "o")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size )and(0 <= d.y < self.size))

    # Контур корабля и добавление корабля на доску

    def contour(self, ship, verb = False):
        near = [
            (-1,-1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1,-1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                self.filde[cur.x][cur.y] = "+"
                #if not (self.out(cur)) and cur not in self.busy:
                #    if verb:
                #       self.filde[cur.x][cur.y] = "."
                #   self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise B






b = Board()
b.contour(Ship(Dot(1,2), 4, 0))
print(b)












