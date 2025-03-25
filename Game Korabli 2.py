from random import randint

# Исключения
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipsException(BoardException):
    pass

# Точка
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):  # Добавлено: метод __hash__ для хеширования
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# Корабль
class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow  # нос корабля (начальная точка)
        self.length = length  # длина корабля
        self.orientation = orientation  # направление: 0 - горизонтально, 1 - вертикально
        self.lives = length  # количество жизней корабля

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orientation == 0:
                cur_x += i
            else:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

# Игровая доска
class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0  # Счётчик уничтоженных кораблей

        self.field = [["0"] * size for _ in range(size)]

        self.busy = []  # Список занятых точек
        self.ships = []  # Список кораблей

    def __str__(self):
        res = "  | " + " | ".join(map(str, range(1, self.size + 1))) + " |"  # Корректный вывод координат для колонок
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "0")  # Прячем корабли для игрока
        return res

    def out(self, d):
        return not (0 <= d.x < self.size and 0 <= d.y < self.size)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not self.out(cur) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipsException()

        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return True
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)

# Игрок
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

# Компьютер
class AI(Player):
    def __init__(self, board, enemy):
        super().__init__(board, enemy)
        self.previous_shots = set()  # Добавлено: список для хранения выстреленных клеток AI

    def ask(self):
        while True:
            d = Dot(randint(0, 5), randint(0, 5))
            if d not in self.previous_shots:  # Изменение: проверка, чтобы не стрелять в одну и ту же клетку
                self.previous_shots.add(d)
                print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
                return d

# Пользователь
class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты!")  # Добавлено: сообщение о неправильном вводе
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")  # Добавлено: проверка на числовые значения
                continue

            x, y = int(x), int(y)

            if not (1 <= x <= self.board.size) or not (1 <= y <= self.board.size):
                print("Координаты вне диапазона!")  # Добавлено: проверка на правильность координат
                continue

            return Dot(x - 1, y - 1)

# Игра
class Game:
    def __init__(self, size=6):
        self.size = size

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None

                ship = Ship(Dot(randint(0, self.size - 1), randint(0, self.size - 1)), l, randint(0, 1))

                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipsException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def play(self):
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True  # Прячем корабли компьютера для игрока

        user = User(user_board, ai_board)
        ai = AI(ai_board, user_board)

        while True:
            print("Доска игрока:")
            print(user_board)
            print("Доска компьютера:")
            print(ai_board)

            if user.move():
                if ai_board.defeat():
                    print("Вы победили!")
                    break

            if ai.move():
                if user_board.defeat():
                    print("Компьютер победил!")
                    break

g = Game(size=6)
g.play()
