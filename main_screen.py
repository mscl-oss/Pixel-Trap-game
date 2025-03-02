import os
import sys
import pygame
import sqlite3

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = WIDTH, HEIGHT = 1200, 700
FPS = 50
FONT = pygame.font.Font('fonts/minecraft-ten-font-cyrillic.ttf', 50)
lvdvgame = r'lvdvgame.db'


class LEVEL:
    def __init__(self, screen, x, y, is_opened):
        self.x = x
        self.y = y
        self.is_opened = is_opened
        self.width, self.height = 75, 90
        if is_opened:
            img = pygame.transform.scale(load_image('opened_level.png'), (self.width, self.height))
            screen.blit(img, (x, y))
        else:
            img = pygame.transform.scale(load_image('closed_level.png'), (self.width, self.height))
            screen.blit(img, (x, y))


def load_image(name, colorkey=None):
    fullname = os.path.join('picts', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def death_amount():
    with sqlite3.connect(lvdvgame) as db:
        cursor = db.cursor()

        # SQL-запрос для получения кол-ва смертей
        query = "SELECT * FROM Deaths"

        # Выполнение запроса
        res = cursor.execute(query)

        # Запись кол-ва смертей в переменную
        am = list(res)[0][0]
    return am


def complited_levels():
    with sqlite3.connect(lvdvgame) as db:
        cursor = db.cursor()

        # SQL-запрос для получения данных о пройденных уровнях
        query = "SELECT * FROM level"

        # Выполнение запроса
        res = cursor.execute(query)

        # Запись кол-ва смертей в переменную
        am = list(res)[0]
    return am


def draw_screen():
    # кнопки
    intro_text = ["Играть",
                  "Статистика",
                  "Помощь",
                  "Закрыть"]
    title = 'Pixel Trap'

    # фон
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    bro = pygame.transform.scale(load_image('Owlet_Monster-Photoroom.png'), (100, 100))
    screen.blit(bro, (850, 450))

    string_rendered = FONT.render(title, 1, pygame.Color('#F3DA0B'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 20
    intro_rect.x = WIDTH // 2 - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)

    text_coord = 150
    for line in intro_text:
        string_rendered = FONT.render(line, 1, pygame.Color('#FFCF40'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_screen():
    draw_screen()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                print(pos)

                if 50 <= pos[0] <= 290 and 180 <= pos[1] <= 230:
                    print('start')
                    open_choose_level_window(complited_levels())
                    draw_screen()

                if 50 <= pos[0] <= 445 and 280 <= pos[1] <= 330:
                    print('open_stat')
                    text = [f"Количество смертей : {death_amount()}"]
                    open_window(text)
                    draw_screen()

                if 50 <= pos[0] <= 325 and 370 <= pos[1] <= 430:
                    print('open_help')
                    text = ["A, D / стрелки : ходьба",
                            "W / Space / стрелка : прыжок",
                            "Цель игры : дойти до двери"]
                    open_window(text)
                    draw_screen()

                if 50 <= pos[0] <= 345 and 465 <= pos[1] <= 515:
                    print('close_app')
                    if open_dialog_window(['Вы действительно хотите', 'закрыть игру?']):
                        terminate()
                    draw_screen()

        pygame.display.flip()
        clock.tick(FPS)


def open_window(help_text):
    img = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    pygame.draw.rect(img, (0, 0, 0, 150), (0, 0, WIDTH, WIDTH))
    screen.blit(img, (0, 0))

    string_rendered = FONT.render('Закрыть', 1, pygame.Color('#F3DA0B'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 500

    intro_rect.x = WIDTH // 2 - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)

    text_coord = 200
    for line in help_text:
        string_rendered = FONT.render(line, 1, pygame.Color('#FFCF40'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 450 <= pos[0] <= 745 and 520 <= pos[1] <= 570:
                    running = False
                print(pos)


def open_dialog_window(text):
    img = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    pygame.draw.rect(img, (0, 0, 0, 150), (0, 0, WIDTH, WIDTH))
    screen.blit(img, (0, 0))

    string_rendered = FONT.render('Нет', 1, pygame.Color('#F3DA0B'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 500
    intro_rect.x = WIDTH // 2 - intro_rect.width // 2 - 100
    screen.blit(string_rendered, intro_rect)

    string_rendered = FONT.render('Да', 1, pygame.Color('#F3DA0B'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 500
    intro_rect.x = WIDTH // 2 - intro_rect.width // 2 + 100
    screen.blit(string_rendered, intro_rect)

    text_coord = 200
    for line in text:
        string_rendered = FONT.render(line, 1, pygame.Color('#FFCF40'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WIDTH // 2 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pygame.display.flip()
    running = True
    res = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 440 <= pos[0] <= 555 and 520 <= pos[1] <= 570:
                    running = False
                    res = False
                if 650 <= pos[0] <= 750 and 520 <= pos[1] <= 585:
                    running = False
                    res = True
                print(pos)
    return res


def open_choose_level_window(open_levels):
    img = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

    pygame.draw.rect(img, (0, 0, 0, 150), (0, 0, WIDTH, WIDTH))
    screen.blit(img, (0, 0))

    fon = pygame.transform.scale(load_image('empty_map.png'), (WIDTH, HEIGHT - 150))
    screen.blit(fon, (0, 0))

    level1 = LEVEL(screen, 200, 300, True)
    level2 = LEVEL(screen, 275, 140, open_levels[0])
    level3 = LEVEL(screen, 450, 100, open_levels[1])
    level4 = LEVEL(screen, 600, 250, open_levels[2])
    level5 = LEVEL(screen, 775, 325, open_levels[3])
    level6 = LEVEL(screen, 850, 175, open_levels[4])

    pts = [(296, 307), (299, 283), (301, 258), (359, 206), (393, 191), (421, 188), (533, 203), (558, 221),
           (579, 256), (676, 351), (708, 379), (754, 406), (868, 408), (908, 387), (920, 349), (900, 320), (887, 281)]
    for i in pts:
        pygame.draw.rect(screen, 'black', (i[0], i[1], 6, 6))

    levels = [level1, level2, level3, level4, level5, level6]

    # кнопка закрыть
    string_rendered = FONT.render('Закрыть', 1, pygame.Color('#F3DA0B'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 550

    intro_rect.x = WIDTH // 2 - intro_rect.width // 2
    screen.blit(string_rendered, intro_rect)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if 450 <= pos[0] <= 745 and 570 <= pos[1] <= 620:
                    running = False
                for i in levels:
                    if i.x <= pos[0] <= i.x + i.width and i.y <= pos[1] <= i.y + i.height and i.is_opened:
                        draw_screen()
                        # запускаем уровень
                        indx = levels.index(i) + 1
                        print(f'Запуск уровня: {indx}')
                        cmd = "python main.py --level " + str(indx)
                        print(cmd)
                        os.system(cmd)
                        running = False
                        break
                print(pos)


if __name__ == '__main__':
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Pixel Trap')

    icon = pygame.image.load('picts/icon.jpg')
    pygame.display.set_icon(icon)
    start_screen()
