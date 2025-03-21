pole_size = 3
pole = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def draw_board():
    print("_" * 4 * pole_size)
    for i in range(pole_size):
        print((' ' * 3 + '|') * 3)
        print('', pole[i * 3], '|', pole[1 + i * 3], '|', pole[2 + i * 3], '|')
        print(('_' * 3 + '|') * 3)
    pass


def game_step(index, char):
    if (index > 9 or index < 1 or pole[index - 1]) in ('X', 'O'):
        return False

    pole[index - 1] = char
    return True

    pass


def check_win():
    win = False

    win_combo = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    )

    for pos in win_combo:
        if (pole[pos[0]] == pole[pos[1]] and pole[pos[1]] == pole[pos[2]]):
            win = pole[pos[0]]

    return win


def start_game():
    player = 'x'

    step = 1
    draw_board()

    while (step < 10) and (check_win() == False):
        index = input('ходит игрок' + player + '. Введите номер поля:')

        if (index == '0'):
            break

        if (game_step(int(index), player)):
            print('Вы сделали ход')

            if (player == 'x'):
                player = '0'
            else:
                player = 'x'

            draw_board()

            step += 1
        else:
            print('Неверный ход')

    if (step == 10):
        print('Ничья')
    else:
        print('выиграл ' + check_win())


print("hello my game")
start_game()