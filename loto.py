import random

BARELLS = 90        # количество бочонков  в мешочке
CARD_LINES = 3      # число строчек на карочке
LINE_CELLS = 9      # число ячеек в строке
LINE_NUMS = 5       # число ячеек с номерами в сроке

# конфигурация игры (3 игрока, из них 2 робота)
GAME_PROFILE = [
    ['Робот 1', True],
    ['Робот 2', True],
    ['Человек 1', False]
    ]

# функция печати разделителя
def print_line(sign):
    print(sign * 3 * LINE_CELLS)

class Loto_bag():
    # класс работы с мешочком бочонков
    def __init__(self):
        # список ходов игры (перемешанные случайным образом бочонки)
        self.list_steps = random.sample(range(1, BARELLS + 1), BARELLS)
        # список сделанных ходов
        self.history_steps = []
        self.position = 0

    def game_step(self):
        # делаем ход в игре, переходим к позиции следующего бочонка
        self.history_steps.append(self.list_steps[self.position])
        self.position +=1

    def curr_bar(self):
        # возвращаем текущий бочонок
        return(self.list_steps[self.position-1])


class Loto_card():
    # класс работы с карточкой лото
    def __init__(self):
        self.name = ''
        self.robot = False
        # создание случайного списка чисел для карточки
        self.set_barell = random.sample(range(1, BARELLS + 1), LINE_NUMS * CARD_LINES)
        self.used_barells = []
        # создание карты позиций бочонков на карточке
        self.set_card = []
        for i in range(CARD_LINES):
            num_card = sorted(random.sample(range(LINE_CELLS), LINE_NUMS))
            self.set_card.append(num_card)


    #печать карточки
    def print_card(self):
        print_line('-')
        for i in range(CARD_LINES):
            str_line = ''
            pos_m = 0
            for cell in range(LINE_CELLS):
                if cell in self.set_card[i]:
                    if self.set_barell[pos_m+i*LINE_NUMS] in self.used_barells:  #число на карточке есть в списке использованных
                        str_line += '---'
                    else:
                        str_line += str(self.set_barell[pos_m+i*LINE_NUMS]).center(3,' ')   #число есть на карточке
                    pos_m +=1
                else:
                    str_line += '   '
            print(str_line)
        print_line('-')

    #закрытие бочонком номера на карточки
    def close_num_by_barell(self, barell):
        if barell in self.set_barell:
            self.used_barells.append(barell)
        # проверяем не все ли номера закрыты
        if len(self.used_barells) == LINE_NUMS * CARD_LINES:
            return True
        else:
            return False

if __name__ == '__main__':
    # Создание объекта класса бочонок
    bag = Loto_bag()

    # Создание объектов класса карточек игроков
    cards = []
    for gamer in GAME_PROFILE:
        card = Loto_card()
        card.name = gamer[0]
        card.robot = gamer[1]
        cards.append(card)

#список победителей игры
winner_list = []

#основной цикл игры
for i in range(BARELLS):
    print_line('*')
    #достаем очередной бочонок
    bag.game_step()
    print('Бочонок ', bag.curr_bar())
    print_line('*')

    #проверяем карточки игроков
    for game_card in cards:
        print('Ход ',game_card.name)
        if game_card.robot:
            win_status = game_card.close_num_by_barell(bag.curr_bar())
            game_card.print_card()
        else:
            game_card.print_card()
            answer_yes = input(game_card.name+' зачеркнуть '+str(bag.curr_bar())+' y/n? ') == 'y'
            check_ans = bag.curr_bar() in game_card.set_barell
            if answer_yes and check_ans \
                    or not answer_yes and not check_ans:
                win_status = game_card.close_num_by_barell(bag.curr_bar())
            else:
                print('Неверный ход! '+game_card.name+' проиграл!')
                #всех роботов записываем в список победителей
                winner_list = []
                for item in GAME_PROFILE:
                    if item[1]:
                        winner_list.append(item[0])
                break

        if win_status:
            winner_list.append(game_card.name)

    if len(winner_list) > 0:
        print('Выиграл(и) ', winner_list)
        print('Сделано ходов: ', i+1)
        break

