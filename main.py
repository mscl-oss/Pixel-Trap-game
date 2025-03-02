import pygame
import sys
import random
import sqlite3
import argparse
import time as t

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1200, 700
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (153, 255, 153)
GREY = (192, 192, 192)

# Загрузка изображений
sprite_image = pygame.image.load('picts/Owlet_Monster_Run_6.png')
sprite_image1 = pygame.image.load('picts/Owlet_Monster_Jump_8.png')
sprite_image3 = pygame.image.load('picts/Owlet_Monster_Run_6inverse.png')
sprite_image4 = pygame.image.load('picts/Owlet_Monster_Jump_8inv.png')

doorimage = pygame.image.load('picts/door1.png')
doorimage = pygame.transform.scale(doorimage, (400, 200))
rect_dor = doorimage.get_rect(bottomright=(200, 370))
# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Sprite Example")

# Группы спрайтов
all_sprites = pygame.sprite.Group()
static_platforms = pygame.sprite.Group()
moving_platforms = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()

# Переменная для тряски экрана
shake_offset = (0, 0)
shake_duration = 0
shake_intensity = 0

# Переменная для отслеживания состояния проигрыша
game_over = False
lvdvgame = r'lvdvgame.db'


def terminate():
    t.sleep(1)
    pygame.quit()
    sys.exit()


def shake_screen(intensity, duration):
    global shake_offset, shake_duration, shake_intensity
    shake_intensity = intensity
    shake_duration = duration


def draw_game_over_screen():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    draw_text_with_shadow('Game Over', font, RED, BLACK, WIDTH // 2 - 135, HEIGHT // 2 - 50)
    draw_text_with_shadow('Press any key to continue', small_font, BLACK, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 20)

    with sqlite3.connect(lvdvgame) as db:
        cursor = db.cursor()

        # SQL-запрос для увеличения значения quantity на 1
        query = "UPDATE Deaths SET quantity = quantity + 1"

        # Выполнение запроса
        cursor.execute(query)

        # Сохранение изменений
        db.commit()


def draw_text_with_shadow(text, font, text_color, shadow_color, x, y):
    text_surface = font.render(text, True, text_color)
    shadow_surface = font.render(text, True, shadow_color)

    # Рисуем тень (смещаем на 2 пикселя вниз и вправо)
    screen.blit(shadow_surface, (x + 2, y + 2))
    # Рисуем основной текст
    screen.blit(text_surface, (x, y))


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = doorimage
        self.rect = self.image.get_rect(topleft=(x, y))


# Класс для создания уровней
class Level:
    def __init__(self, level_number, player):
        super().__init__()
        self.flagoo = True
        self.is_paused = None
        self.pause_start_time = None
        self.flaglev51 = True
        self.moving_platform_level6_1 = None
        self.platform5_start_time = None
        self.platform5_moving = None
        self.moving_platform_level5_1 = None
        self.d = None
        self.level_number = level_number
        self.player = player
        self.platforms = []
        self.moving_platform1 = None
        self.moving_platform2 = None
        self.moving_platform_level3_1 = None
        self.moving_platform_level3_2 = None
        self.timer_platform1 = None
        self.timer_platform2 = None
        self.platform1_moving = False
        self.platform2_moving = False
        self.platform4_moving = False
        self.platform4_start_time = None
        self.create_level()
        self.flag = True
        self.flaglev4 = True
        self.flaglev5 = True
        self.platform5_moving = False
        self.platform5_start_time = None

    def reset(self):
        self.flagoo = True
        self.is_paused = None
        self.pause_start_time = None
        self.flaglev51 = True
        self.moving_platform_level6_1 = None
        self.platform5_start_time = None
        self.platform5_moving = None
        self.moving_platform_level5_1 = None
        self.d = None
        self.platforms = []
        self.moving_platform1 = None
        self.moving_platform2 = None
        self.moving_platform_level3_1 = None
        self.moving_platform_level3_2 = None
        self.timer_platform1 = None
        self.timer_platform2 = None
        self.platform1_moving = False
        self.platform2_moving = False
        self.platform4_moving = False
        self.platform4_start_time = None
        self.create_level()
        self.flag = True
        self.flaglev4 = True
        self.flaglev5 = True
        self.platform5_moving = False
        self.platform5_start_time = None

    def create_level(self):
        if self.level_number == 1:
            Platform(0, 382, 700, 350)
            Platform(0, 0, 1200, 250)
            # Создаем движущуюся платформу и сохраняем ссылку на нее
            self.moving_platform1 = MovePl(700, 382, 200, 350, speed=30, move_horizontal=False, is_moving=False,
                                           direction=1)
            self.platforms.append(self.moving_platform1)  # Добавляем платформу в список
            Platform(780, 382, 450, 350)
            self.d = Door(780, 254)
            all_sprites.add(self.d)
            self.x = 940
        elif self.level_number == 2:
            Platform(0, 382, 700, 350)
            Platform(0, 0, 1200, 250)
            # Создаем две движущиеся платформы и сохраняем ссылки на них
            self.moving_platform1 = MovePl(700, 382, 100, 350, speed=30, move_horizontal=False, is_moving=False,
                                           direction=1)
            self.moving_platform2 = MovePl(830, 382, 100, 350, speed=30, move_horizontal=False, is_moving=False,
                                           direction=1)
            self.platforms.extend([self.moving_platform1, self.moving_platform2])  # Добавляем платформы в список
            Platform(780, 382, 50, 350)
            Platform(930, 382, 400, 350)
            self.d = Door(800, 254)
            all_sprites.add(self.d)
            self.x = 950
        elif self.level_number == 3:
            Platform(0, 0, 1200, 250)
            Platform(0, 382, 300, 350)
            Platform(650, 382, 700, 350)
            # Создаем две движущиеся платформы для уровня 3
            self.moving_platform_level3_1 = MovePl(300, 382, 200, 350, speed=10, move_horizontal=True, is_moving=False, direction=-1)
            self.moving_platform_level3_2 = MovePl(650, 382, 200, 350, speed=10, move_horizontal=True, is_moving=False, direction=-1)
            self.platforms.extend(
                [self.moving_platform_level3_1, self.moving_platform_level3_2])  # Добавляем платформы в список
            self.d = Door(780, 254)
            all_sprites.add(self.d)
            self.x = 940
        elif self.level_number == 4:
            Platform(0, 0, 1200, 250)
            Platform(0, 382, 100, 350)
            self.moving_platform_level4_1 = MovePl(100, 382, 900, 350, speed=15, move_horizontal=True, is_moving=False,
                                                   direction=1)
            Platform(1000, 382, 300, 350)
            self.platforms.append(self.moving_platform_level4_1)
            self.d = Door(860, 254)
            all_sprites.add(self.d)
            self.x = 1005
        elif self.level_number == 5:
            Platform(0, 0, 1200, 250)
            Platform(0, 382, 100, 350)
            self.moving_platform_level4_1 = MovePl(100, 382, 500, 350, speed=15, move_horizontal=True, is_moving=False,
                                                   direction=1)
            Platform(500, 382, 400, 350)
            self.moving_platform_level5_1 = MovePl(900, 382, 100, 350, speed=15, move_horizontal=True, is_moving=False,
                                                   direction=-1)
            self.platforms.append(self.moving_platform_level5_1)
            Platform(1000, 382, 300, 350)
            self.d = Door(860, 254)
            all_sprites.add(self.d)
            self.x = 1000
        elif self.level_number == 6:
            Platform(0, 382, 450, 350)
            Platform(575, 382, 700, 350)
            self.moving_platform_level6_1 = MovePl(640, 382, 100, 350, speed=15, move_horizontal=False, is_moving=False,
                                                   direction=-1)
            self.platforms.append(self.moving_platform_level6_1)
            self.d = Door(780, 254)
            all_sprites.add(self.d)
            self.x = 940
        elif self.level_number == 0:
            Platform(0, 300, 1200, 350)

            # Создаем движущуюся платформу и сохраняем ссылку на нее
            self.moving_platform1 = MovePl(700, 150, 200, 350, speed=1, move_horizontal=True, is_moving=False)
            self.platforms.append(self.moving_platform1)  # Добавляем платформу в список
        elif level == 50:
            self.d = Door(200, 350)
            all_sprites.add(self.d)

    def update(self):

        # Проверяем условие для уровня 1 и 2
        if self.level_number in [1, 2] and self.player.rect.x > 680:
            # Включаем движение только для moving_platform1
            if self.moving_platform1:
                self.moving_platform1.set_moving(True)

        # Проверяем условие для уровня 2
        if self.level_number == 2 and self.player.rect.x > 800:
            # Включаем движение только для moving_platform2
            if self.moving_platform2:
                self.moving_platform2.set_moving(True)

        # Логика для уровня 3
        if self.level_number == 3:
            if self.player.rect.x > 428:
                # Включаем движение платформ и запускаем таймеры только один раз
                if not self.platform1_moving and self.timer_platform1 is None and self.flag:
                    self.moving_platform_level3_1.set_moving(True)
                    self.platform1_moving = True
                    self.timer_platform1 = pygame.time.get_ticks()  # Запускаем таймер для платформы 1

                if not self.platform2_moving and self.timer_platform2 is None and self.flag:
                    self.flag = False
                    self.moving_platform_level3_2.set_moving(True)
                    self.platform2_moving = True
                    self.timer_platform2 = pygame.time.get_ticks()  # Запускаем таймер для платформы 2

            # Останавливаем платформу 1 через 1 секунду
            if self.platform1_moving and self.timer_platform1 is not None:
                if pygame.time.get_ticks() - self.timer_platform1 >= 300:  # 300 мс = 0.3 секунды
                    self.moving_platform_level3_1.set_moving(False)
                    self.platform1_moving = False
                    self.timer_platform1 = None  # Сбрасываем таймер

            # Останавливаем платформу 2 через 1 секунду
            if self.platform2_moving and self.timer_platform2 is not None:
                if pygame.time.get_ticks() - self.timer_platform2 >= 300:  # 300 мс = 0.3 секунды
                    self.moving_platform_level3_2.set_moving(False)
                    self.platform2_moving = False
                    self.timer_platform2 = None  # Сбрасываем таймер

        # Логика для уровня 4
        # Логика для уровня 4
        if self.level_number == 4 and self.player.rect.x >= 90 and self.flaglev4:
            print('aboba')

            if not self.platform4_moving and self.platform4_start_time is None:
                print('aboba1')

                # Запускаем таймер
                self.platform4_start_time = pygame.time.get_ticks()
                self.platform4_moving = True  # Устанавливаем флаг движения
                if self.moving_platform_level4_1 is not None:
                    self.moving_platform_level4_1.set_moving(True)  # Запускаем движение платформы
                    print("Платформа начала движение")

            # Если прошло 200 мс, останавливаем платформу
            if self.platform4_moving and self.platform4_start_time is not None:
                if pygame.time.get_ticks() - self.platform4_start_time >= 100:

                    if self.moving_platform_level4_1 is not None:
                        self.moving_platform_level4_1.set_moving(False)  # Останавливаем платформу

                        # Принудительно сбросить скорость
                        self.moving_platform_level4_1.speed = 0

                    self.platform4_moving = False  # Сбрасываем флаг
                    self.platform4_start_time = None  # Сбрасываем таймер
        if self.level_number == 4 and self.player.rect.x >= 600:
            self.platform4_moving = None
            self.platform4_start_time = None
            if not self.platform4_moving and self.platform4_start_time is None:

                # Запускаем таймер
                self.platform4_start_time = pygame.time.get_ticks()
                self.platform4_moving = True  # Устанавливаем флаг движения
                if self.moving_platform_level4_1 is not None:
                    self.moving_platform_level4_1.speed = 6
                    # Запускаем движение платформы
                    print("Платформа начала движение")

            # Если прошло 200 мс, останавливаем платформу
            if self.platform4_moving and self.platform4_start_time is not None:
                if pygame.time.get_ticks() - self.platform4_start_time >= 500:
                    print('aboba3')

                    if self.moving_platform_level4_1 is not None:
                        self.moving_platform_level4_1.set_moving(False)  # Останавливаем платформу
                        print('Платформа остановлена')

                        # Принудительно сбросить скорость
                        self.moving_platform_level4_1.speed = 0

                    self.platform4_moving = False  # Сбрасываем флаг
                    self.platform4_start_time = None  # Сбрасываем таймер
        if self.level_number == 5 and self.player.rect.x >= 500 and self.flaglev5:
            print('aboba')

            if not self.platform4_moving and self.platform4_start_time is None:
                print('aboba1')

                # Запускаем таймер
                self.platform4_start_time = pygame.time.get_ticks()
                self.platform4_moving = True  # Устанавливаем флаг движения
                if self.moving_platform_level4_1 is not None:
                    self.moving_platform_level4_1.set_moving(True)  # Запускаем движение платформы
                    print("Платформа начала движение")
                    self.flaglev5 = False

        if self.level_number == 5 and self.player.rect.x >= 880:
            if not self.platform5_moving and self.platform5_start_time is None:
                print('Starting platform 5 movement')
                self.platform5_start_time = pygame.time.get_ticks()
                self.platform5_moving = True
                if self.moving_platform_level5_1 is not None:
                    self.moving_platform_level5_1.set_moving(True)
                    print("Platform 5 started moving")

            # Check if 300 milliseconds have passed
            if self.platform5_moving and self.platform5_start_time is not None:
                if pygame.time.get_ticks() - self.platform5_start_time >= 300:
                    print('Stopping platform 5 movement')
                    if self.moving_platform_level5_1 is not None:
                        self.moving_platform_level5_1.set_moving(False)  # Stop the platform
                        self.moving_platform_level5_1.speed = 0  # Reset the speed
                    self.platform5_moving = False  # Reset the movement flag
                    self.platform5_start_time = None  # Reset the timer
        if self.level_number == 6:
            if self.player.rect.x >= 550 and self.player.rect.y < HEIGHT:
                # Первая фаза: вертикальное движение платформы
                if self.flaglev5 and not self.platform5_moving:
                    print('Starting platform 5 movement')
                    self.platform5_start_time = pygame.time.get_ticks()
                    self.platform5_moving = True
                    if self.moving_platform_level6_1 is not None:
                        self.moving_platform_level6_1.set_moving(True)
                        self.moving_platform_level6_1.move_horizontal = False  # Движение по вертикали
                        self.moving_platform_level6_1.speed = 15
                        print("Platform 5 started moving (vertical)")

                # Остановка платформы через 300 мс
                if self.platform5_moving and self.platform5_start_time is not None:
                    if pygame.time.get_ticks() - self.platform5_start_time >= 300:
                        print('Stopping platform 5 movement (vertical)')
                        if self.moving_platform_level6_1 is not None:
                            self.moving_platform_level6_1.set_moving(False)
                            self.moving_platform_level6_1.speed = 0
                        self.platform5_moving = False
                        self.platform5_start_time = None
                        self.flaglev5 = False  # Завершаем первую фазу

                # Вторая фаза: горизонтальное движение платформы
                if not self.flaglev5 and self.flaglev51:
                    if not self.platform5_moving and self.platform5_start_time is None and self.flagoo:
                        print('Starting platform 5 movement (horizontal)')
                        self.platform5_start_time = pygame.time.get_ticks()
                        self.platform5_moving = True
                        self.flagoo = False

                        if self.moving_platform_level6_1 is not None:
                            self.moving_platform_level6_1.set_moving(True)
                            self.moving_platform_level6_1.move_horizontal = True  # Движение по горизонтали
                            self.moving_platform_level6_1.speed = 10
                            print("Platform 5 started moving (horizontal)")
                            self.flagoo = False

                        if pygame.time.get_ticks() - self.platform5_start_time >= 120:
                            print('Stopping platform 5 movement (horizontal)')
                            if self.moving_platform_level6_1 is not None:
                                self.moving_platform_level6_1.set_moving(False)
                                self.flagoo = False
                                self.moving_platform_level6_1.speed = 0
                                self.moving_platform_level6_1.direction = -1  # Меняем направление
                                self.moving_platform_level6_1.move_horizontal = not self.moving_platform_level6_1.move_horizontal

                                # Начинаем паузу
                                self.pause_start_time = pygame.time.get_ticks()
                                self.is_paused = True
                    # Остановка платформы через 108 мс

            if self.platform5_moving and self.platform5_start_time is not None and not self.flagoo and self.player.rect.x < 500:
                self.moving_platform_level6_1.set_moving(False)
                self.flagoo = False
                self.moving_platform_level6_1.speed = 0
                self.moving_platform_level6_1.direction = -1  # Меняем направление
                self.moving_platform_level6_1.move_horizontal = not self.moving_platform_level6_1.move_horizontal
                # Начинаем паузу
                self.pause_start_time = pygame.time.get_ticks()
                self.is_paused = True

                self.platform5_moving = False
                self.platform5_start_time = None

                # Пауза перед возобновлением движения
            if self.is_paused:
                if pygame.time.get_ticks() - self.pause_start_time >= 500:  # Пауза 1000 мс (1 секунда)
                    print('Resuming platform 5 movement')
                    if self.moving_platform_level6_1 is not None:
                        self.moving_platform_level6_1.direction = 1
                        self.moving_platform_level6_1.set_moving(True)
                        self.moving_platform_level6_1.speed = 10
                    self.is_paused = False
                    self.flaglev51 = False  # Завершаем вторую фазу

    def check_player_movement(self):
        """Метод для проверки и блокировки движения игрока."""
        if self.player.rect.x >= self.x != 0:  # Если игрок достиг нужной координаты
            self.player.can_move = False  # Блокируем движение
        else:
            self.player.can_move = True  # Разрешаем движение


start_time = pygame.time.get_ticks()
current_time = pygame.time.get_ticks()


# Класс AnimatedSprite
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, sheet_jump, sheet_inverse, sheet_jump_inverse, columns, rows, x, y):
        super().__init__(all_sprites)
        self.rect_single = None
        self.frames_run = []
        self.frames_jump = []
        self.frames_run_inverse = []
        self.frames_jump_inverse = []

        self.cut_sheet(sheet, columns, rows, self.frames_run)
        self.cut_sheet(sheet_jump, 8, 1, self.frames_jump)
        self.cut_sheet(sheet_inverse, columns, rows, self.frames_run_inverse)
        self.cut_sheet(sheet_jump_inverse, 8, 1, self.frames_jump_inverse)

        self.cur_frame = 0
        self.image = self.frames_run[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 200
        self.animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1000
        self.moving_left = False
        self.moving_right = False
        self.on_ground = False
        self.was_jump_key_pressed = False
        self.health = 100
        self.width = pygame.display.get_surface().get_width()
        self.can_move = True  # Флаг, разрешающий или запрещающий движение
        self.line = False
        self.reset()

    def reset(self):
        """Сбрасывает состояние игрока к начальным значениям."""
        self.cur_frame = 0
        self.image = self.frames_run[self.cur_frame]
        self.rect = self.image.get_rect(topleft=(0, HEIGHT // 2))  # Сбрасываем позицию
        self.is_jumping = False
        self.jump_velocity = 0
        self.moving_left = False
        self.moving_right = False
        self.on_ground = False
        self.was_jump_key_pressed = False
        self.health = 100
        self.can_move = True
        self.line = False
        self.moving_left = False
        self.moving_right = False

    def is_on_ground(self):
        check_rect = pygame.Rect(self.rect.left, self.rect.bottom + 1, self.rect.width, 1)
        return (
                any(check_rect.colliderect(platform.rect) for platform in static_platforms) or
                any(check_rect.colliderect(platform.rect) for platform in moving_platforms)
        )

    def cut_sheet(self, sheet, columns, rows, frames_list):
        self.rect_single = pygame.Rect(0, 0, sheet.get_width() // columns,
                                       sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect_single.w * i, self.rect_single.h * j)
                frames_list.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect_single.size)))

    def update(self, dt):
        now = pygame.time.get_ticks()
        print(self.rect.x, self.rect.y)
        if not self.on_ground:
            self.jump_velocity += self.gravity * dt
            self.rect.y += self.jump_velocity * dt

        if self.on_ground:
            self.is_jumping = False
            self.jump_velocity = 0

        # Проверка столкновений с платформами
        hits = pygame.sprite.spritecollide(self, static_platforms, False)
        for platform in hits:
            if self.jump_velocity >= 0:
                if (self.rect.bottom > platform.rect.top) and platform.rect.top != 0:
                    if self.rect.center[0] >= self.width and self.rect.bottom - platform.rect.top > 10:
                        self.rect.left = self.width
                    else:
                        self.rect.bottom = platform.rect.top
                        self.is_jumping = False
                        self.jump_velocity = 0
                        self.on_ground = True

        hits1 = pygame.sprite.spritecollide(self, moving_platforms, False)
        for move in hits1:
            if self.rect.bottom > move.rect.top and self.rect.bottom - move.rect.top < 10:
                self.rect.bottom = move.rect.top
                self.is_jumping = False
                self.jump_velocity = 0
                self.on_ground = True
                # Убираем принудительное движение игрока вместе с платформой
                # self.rect.x += move.speed * move.direction * dt * 60
            else:
                if self.rect.right > move.rect.left > self.rect.left:
                    self.rect.right = move.rect.left
                elif self.rect.left < move.rect.right < self.rect.right:
                    self.rect.left = move.rect.right

        if pygame.sprite.spritecollideany(self, spikes_group):
            self.take_damage(10)

        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.cur_frame = (self.cur_frame + 1) % 6
            if self.is_jumping:
                if self.moving_left:
                    self.image = self.frames_jump_inverse[
                        self.cur_frame % len(self.frames_jump_inverse)]
                else:
                    self.image = self.frames_jump[self.cur_frame % len(self.frames_jump)]
            else:
                if self.moving_left:
                    self.image = self.frames_run_inverse[
                        self.cur_frame % len(self.frames_run_inverse)]
                elif self.moving_right:
                    self.image = self.frames_run[self.cur_frame % len(self.frames_run)]
                else:
                    self.image = self.frames_run[self.cur_frame % len(self.frames_run)]

        if self.on_ground and not self.is_on_ground():
            self.on_ground = False
            self.jump_velocity = 0
        if self.rect.y > HEIGHT:
            global start_time, line1, game_over
            self.line = True

            if line1:  # Если line1 еще True
                start_time = pygame.time.get_ticks()  # Запоминаем время, когда line1 стало False
                shake_screen(intensity=10, duration=20)
                line1 = False  # Устанавливаем line1 в False

            # Если line1 уже False, проверяем, прошла ли 1 секунда
            if not line1:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - start_time  # Время, прошедшее с момента изменения line1

                if elapsed_time > 3000:  # Если прошла 1 секунда
                    game_over = True  # Устанавливаем game_over в True

    def move(self, dx, dt):
        if not self.can_move:
            global line1
            if line1:
                shake_screen(intensity=10, duration=20)
                with sqlite3.connect(lvdvgame) as db:
                    cursor = db.cursor()
                    if level == 1:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level1 = 1"
                    if level == 2:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level2 = 1"
                    if level == 3:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level3 = 1"
                    if level == 4:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level4 = 1"
                    if level == 5:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level5 = 1"
                    if level == 6:
                        # SQL-запрос для увеличения значения quantity на 1
                        query = "UPDATE Level SET Level6 = 1"
                    # Выполнение запроса
                    cursor.execute(query)

                    # Сохранение изменений
                    db.commit()

                line1 = False
                terminate()
            # Если движение заблокировано, выходим из метода
            return

        old_x = self.rect.x
        self.rect.x += dx * self.speed * dt

        hits = pygame.sprite.spritecollide(self, static_platforms, False)
        for platform in hits:
            if dx > 0:
                if self.rect.right > platform.rect.left and old_x <= platform.rect.left - self.rect.width:
                    self.rect.right = platform.rect.left
            elif dx < 0:
                if self.rect.left < platform.rect.right <= old_x:
                    self.rect.left = platform.rect.right

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.jump_velocity = -300
            self.on_ground = False

    def take_damage(self, amount):
        global flager
        global line1
        self.health -= amount
        if self.health <= 0 and flager:
            print("Игрок умер!")
            flager = False
            if line1:
                shake_screen(intensity=10, duration=20)
                line1 = False
            global game_over
            game_over = True


flager = True
line1 = True


# Класс статичной платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(static_platforms)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))


# Класс движущейся платформы
class MovePl(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=0, move_horizontal=True, is_moving=True, direction=1):
        super().__init__(moving_platforms)
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed  # Скорость движения
        self.move_horizontal = move_horizontal  # Движение по горизонтали или вертикали
        self.direction = direction  # Направление движения: 1 (вправо/вниз) или -1 (влево/вверх)
        self.is_moving = is_moving  # Должна ли платформа двигаться

    def update(self, dt):
        if self.is_moving:  # Проверяем, должна ли платформа двигаться
            if self.move_horizontal:
                # Движение по горизонтали
                self.rect.x += self.speed * self.direction * dt * 60
                if self.rect.left < 0:
                    self.direction *= -1  # Меняем направление при достижении границы экрана
            else:
                # Движение по вертикали
                self.rect.y += self.speed * self.direction * dt * 60

    def set_moving(self, is_moving):
        """Метод для изменения состояния is_moving."""
        self.is_moving = is_moving


# Класс шипов
class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, direction="up"):
        super().__init__(spikes_group)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction

        if direction == "up":
            points = [(0, height), (width // 2, 0), (width, height)]
        elif direction == "down":
            points = [(0, 0), (width // 2, height), (width, 0)]
        elif direction == "left":
            points = [(width, 0), (0, height // 2), (width, height)]
        elif direction == "right":
            points = [(0, 0), (width, height // 2), (0, height)]
        else:
            raise ValueError("Неправильное направление шипов. Используйте 'up', 'down', 'left' или 'right'.")

        pygame.draw.polygon(self.image, GREY, points)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = BLACK
        self.speed_x = random.uniform(-5, 5)
        self.speed_y = random.uniform(-5, 5)
        self.lifetime = 70

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1

    def check_collision(self, platforms):
        """Проверяет столкновение частицы с платформами."""
        particle_rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        for platform in platforms:
            if particle_rect.colliderect(platform.rect):
                # Отскок от платформы
                if self.speed_y > 0:  # Частица движется вниз
                    self.y = platform.rect.top - self.size
                    self.speed_y *= -1  # Меняем направление по вертикали
                elif self.speed_y < 0:  # Частица движется вверх
                    self.y = platform.rect.bottom + self.size
                    self.speed_y *= -1

                if self.speed_x > 0:  # Частица движется вправо
                    self.x = platform.rect.left - self.size
                    self.speed_x *= -1  # Меняем направление по горизонтали
                elif self.speed_x < 0:  # Частица движется влево
                    self.x = platform.rect.right + self.size
                    self.speed_x *= -1


level = 1


# Главная функция игры
def main():
    global level

    parser = argparse.ArgumentParser()
    parser.add_argument("--level", type=int)
    args = parser.parse_args()
    print(args.level)
    print('Запуск успешен')
    level = args.level

    clock = pygame.time.Clock()

    pygame.display.set_caption('Pixel Trap')
    icon = pygame.image.load('picts/icon.jpg')
    pygame.display.set_icon(icon)

    dragon = AnimatedSprite(sprite_image, sprite_image1, sprite_image3, sprite_image4, 6, 1, 0, HEIGHT // 2)
    all_sprites.add(dragon)
    current_level = Level(level, dragon)

    # Создаем группу для двери


    while True:
        dt = clock.tick(FPS) / 1000

        global shake_offset, shake_duration, shake_intensity
        if shake_duration > 0:
            shake_offset = (random.randint(-shake_intensity, shake_intensity),
                            random.randint(-shake_intensity, shake_intensity))
            shake_duration -= 1
        else:
            shake_offset = (0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        current_level.check_player_movement()

        dx = 0
        if dragon.can_move:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
                dragon.moving_left = True
                dragon.moving_right = False
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
                dragon.moving_right = True
                dragon.moving_left = False
            else:
                dragon.moving_left = False
                dragon.moving_right = False

            if not dragon.was_jump_key_pressed and (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
                dragon.jump()
                dragon.was_jump_key_pressed = True
            elif not (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
                dragon.was_jump_key_pressed = False

        dragon.move(dx, dt)

        current_level.update()
        all_sprites.update(dt)
        static_platforms.update(dt)
        moving_platforms.update(dt)
        spikes_group.update()

        screen.fill(WHITE)



        # Отрисовка всех спрайтов
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x + shake_offset[0], sprite.rect.y + shake_offset[1]))

        # Отрисовка платформ
        for platform in static_platforms:
            screen.blit(platform.image, (platform.rect.x + shake_offset[0], platform.rect.y + shake_offset[1]))

        for platform in moving_platforms:
            screen.blit(platform.image, (platform.rect.x + shake_offset[0], platform.rect.y + shake_offset[1]))

        # Отрисовка шипов
        for spike in spikes_group:
            screen.blit(spike.image, (spike.rect.x + shake_offset[0], spike.rect.y + shake_offset[1]))

        if game_over:
            draw_game_over_screen()
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False
                        reset_game()

        pygame.display.flip()


def reset_game():
    global game_over, flager, line1, level, current_level, dragon

    # Сброс глобальных переменных
    game_over = False
    flager = True
    line1 = True

    # Очищаем группы спрайтов
    all_sprites.empty()
    static_platforms.empty()
    moving_platforms.empty()
    spikes_group.empty()
    main()

    # Сбрасываем состояние игрока


if __name__ == "__main__":
    main()
