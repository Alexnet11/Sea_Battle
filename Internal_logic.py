from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x},{self.y})"


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрельнуть за пределы игрового поля"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    def __init__(self, bow, l, o):
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

    def shooten(self, shot):        # метот который показывает попали ли мы в корабль, соделжится ли точка в корабле
        return shot in self.dots


class Board:                                         # создаём игровое поле
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0
        self.filde = [["0"]*size for _ in range(size)]

        self.busy = []  # список занятых точек
        self.ships = [] # список короблей доски


    # Добавляем корабль
    def add_ship(self, ship):

        for d in ship.dots:                      # каждая точка корабля
             if self.out(d) or d in self.busy:   # не выходит за границу (первый метод) и точка не занята
                raise BoardWrongShipException()  # выбрасываем исключение

        for d in ship.dots:
            self.filde[d.x][d.y] = "▄"           # пройдёмся по точкам корабля и поставим в эти точки квадратик
            self.busy.append(d)                  # запишим эти тоски с писок занятых.

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:  # если точка не выходит за границы доски и если не занята ещё
                    if verb:
                        self.filde[cur.x][cur.y] = "."
                    self.busy.append(cur)  # то мы эту точку добавляем в список занятых точек

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.filde):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("▄", "0")
        return res


    def out(self, d):  # проверяем находятся ли точки в рамках игрового поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))


    # делаем выстрел
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:                            # проходимся в списке по короблям
            if ship.shooten(d):                            # проверяем принадлежит ли точка какому ни будт кораблю
                ship.lives -= 1
                self.filde[d.x][d.y] = "X"
                if ship.lives == 0:                    # если у корабля кончились жизни
                    self.count += 1                    # прибовляем к сётчику унечтоженных кораблей единицу
                    self.contour(ship, verb = True)    # обводим его по контуру
                    print("Корабль уничтожен")
                    return False                       # возвращаем фолс, чтобы сказать что код делать дельше не надо
                else:
                    print("Корабль ранен!")
                    return True

        self.filde[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self): # метод обнуления списка бизи
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


# КЛАСС ИГРОКА
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self): # в методе бесконечного цыкла мы пытаемся сделать выстрел
        while True:
            try:
                target = self.ask()                     # просим компьютер или польхзователя дать кординаты выстрела
                repeat = self.enemy.shot(target)        # выполняем выстрел
                return repeat
            except BoardException as e:
                print(e)


# КЛАСС КОМПЬЮТЕР/ПОЛЬЗОВАТЕЛЬ
class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0,5))
        print(f"Ход компьютера:{d.x + 1} {d.y + 1}")
        return d

class User (Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите число")
                continue

            x, y = int(x), int(y)
            return Dot(x -1, y -1)

# КЛАСС ИГРА И ГЕНЕРАЦИЯ ДОСКИ

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()                     # генерируем две случайные доски для компьютера и игрока
        co = self.random_board()
        co.hid = True                                # для комптютера скрываем корабли

        # создаём двух игроков
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def try_board(self):                             #  в методе пытаемся каждый корабль раставить на доску
        lens = [3, 2, 2, 1, 1, 1, 1]                 # список с длинами короблей
        board = Board(size=self.size)
        attempts = 0                                 # количество попыток поставить корабли
        for l in lens:                               # для каждой длины коробля
            while True:
                attempts += 1
                if attempts > 2000:                  #сли попыток было больше указонного числа то возвращаем пустую доску
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship) # если корабль добавле делаем брейк
                    break
                except BoardWrongShipException: # если выбросилось исключение делаем итерацию занова
                    pass
        board.begin()
        return board



    # функция приветсвия
    def greet(self):
        print("---------------------")
        print("  Приветствуем вас   ")
        print("       в игре        ")
        print("     морской бой     ")
        print("---------------------")
        print("   формат ввода: х y ")
        print(" x - номер строки    ")
        print(" y - номер столбца   ")

    def loop(self):
        num = 0                            # номер хода
        while True:                        # выводим доски пользовеля и компьютера
            print("_" * 20)
            print("Доска пользователя")
            print(self.us.board)
            print("_" * 20)
            print("Доска компьютера")
            print(self.ai.board)
            if num % 2 == 0:               # действуем в зависимости от номера хода
                print("Ходит пользователь")
                repeat = self.us.move()
            else:
                print("Ходит компьютер")
                repeat = self.ai.move()

            if repeat:                  # чтобы ход осьался у того же игрока, чтобы увелечения хода не произошла
                num -= 1

            if self.ai.board.defeat():
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()

