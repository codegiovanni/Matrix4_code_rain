import os
from random import choice, randrange

import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1650, 600
FONT_SIZE = 10
ALPHA = 100

pg.init()

screen = pg.display.set_mode(RES)
surface = pg.Surface(RES, pg.SRCALPHA)
surface.set_alpha(ALPHA)

clock = pg.time.Clock()

katakana_chars = ['ァ', 'ア', 'ィ', 'イ', 'ゥ', 'ウ', 'ェ', 'エ', 'ォ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ', 'ケ']

# full katakana
# katakana_chars = ['゠', 'ァ', 'ア', 'ィ', 'イ', 'ゥ', 'ウ', 'ェ', 'エ', 'ォ', 'オ', 'カ', 'ガ', 'キ', 'ギ', 'ク', 'グ',
#                   'ケ', 'ゲ', 'コ', 'ゴ', 'サ', 'ザ', 'シ', 'ジ', 'ス', 'ズ', 'セ', 'ゼ', 'ソ', 'ゾ', 'タ', 'ダ', 'チ',
#                   'ヂ', 'ッ', 'ツ', 'ヅ', 'テ', 'デ', 'ト', 'ド', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'バ', 'パ', 'ヒ',
#                   'ビ', 'ピ', 'フ', 'ブ', 'プ', 'ヘ', 'ベ', 'ペ', 'ホ', 'ボ', 'ポ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ャ',
#                   'ヤ', 'ュ', 'ユ', 'ョ', 'ヨ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ヮ', 'ワ', 'ヰ', 'ヱ', 'ヲ', 'ン', 'ヴ',
#                   'ヵ', 'ヶ', 'ヷ', 'ヸ', 'ヹ', 'ヺ', '・', 'ー', 'ヽ', 'ヾ', 'ヿ']


class Symbol:
    def __init__(self, x, y, font_size, speed, direction):
        self.direction = direction
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = - 100
        self.font_size = font_size
        self.speed = speed
        self.char_change_speed = randrange(20, 40)
        self.value = choice(katakana_chars)
        self.font_increase = 0

    def draw(self, color_shift):
        self.font_increase_speed = int(self.y / 80)
        self.font_increase = self.font_size + self.font_increase_speed if 0 < self.y < HEIGHT else 0
        font = pg.font.Font('font/ms mincho.ttf', self.font_increase, bold=True)
        frames = pg.time.get_ticks()
        if not frames % self.char_change_speed:
            self.value = choice(katakana_chars)

        if self.direction:
            self.y = self.y + self.speed if self.y < HEIGHT else self.y0
        if not self.direction:
            self.y = self.y - self.speed if self.y > 0 else HEIGHT - self.y0

        if color_shift < 8:
            self.char = font.render(self.value, True, (255 - 32 * color_shift, 255, 255 - 32 * color_shift))
        if color_shift >= 8:
            self.char = font.render(self.value, True, (0, 255 - 22 * (color_shift - 8), 0))

        screen.blit(self.char, (self.x, self.y))


class SymbolColumn:
    def __init__(self, x, y, font_size, direction):
        self.direction = direction
        self.column_height = randrange(5, 20)
        self.speed = randrange(5, 20)
        self.font_size = font_size + 3

        if self.direction:
            self.symbols = [Symbol(x=x, y=i, font_size=self.font_size, speed=self.speed, direction=True) for i in
                            range(y, y - (self.font_size + 10) * self.column_height, -(self.font_size + 10))]
        if not self.direction:
            self.symbols = [Symbol(x=x, y=i, font_size=self.font_size, speed=self.speed, direction=False) for i in
                            range(y, y + (self.font_size + 10) * self.column_height, (self.font_size + 10))]

    def draw(self):
        [symbol.draw(color_shift=i) for i, symbol in enumerate(self.symbols)]


symbol_columns1 = [SymbolColumn(x=i, y=0, font_size=8, direction=True) for i in range(750, 950, 200)]
symbol_columns2 = [SymbolColumn(x=i, y=0, font_size=6, direction=True) for i in range(650, 1050, 400)]
symbol_columns3 = [SymbolColumn(x=i, y=0, font_size=4, direction=True) for i in range(600, 1100, 100)]
symbol_columns4 = SymbolColumn(x=850, y=0, font_size=10, direction=False)
symbol_columns5 = [SymbolColumn(x=i, y=0, font_size=8, direction=False) for i in range(775, 975, 100)]
symbol_columns6 = [SymbolColumn(x=i, y=0, font_size=6, direction=False) for i in range(625, 1025, 200)]
symbol_columns7 = [SymbolColumn(x=i, y=0, font_size=4, direction=False) for i in range(610, 1060, 50)]

step = 0
zoom_step = 1
k = 1
running = True
while running:

    screen.blit(surface, (0, 0))
    surface.fill(pg.Color('black'))

    [symbol_column.draw() for symbol_column in symbol_columns1 if 0.5 < step < 4]
    [symbol_column.draw() for symbol_column in symbol_columns2 if 1.5 < step < 4.5]
    [symbol_column.draw() for symbol_column in symbol_columns3 if 2.5 < step < 5]

    if step > 2:
        symbol_columns4.draw()

    [symbol_column.draw() for symbol_column in symbol_columns5 if step > 2.5]
    [symbol_column.draw() for symbol_column in symbol_columns6 if step > 3]
    [symbol_column.draw() for symbol_column in symbol_columns7 if step > 3.5]

    [exit() for i in pg.event.get() if i.type == pg.QUIT]

    pg.display.update()

    zoom_width = WIDTH // 3 + zoom_step
    zoom_height = HEIGHT // 3 + zoom_step
    zoomed_screen = pg.transform.smoothscale(screen, (zoom_width, zoom_height))

    zoomed_screen.set_alpha(ALPHA - 20)

    if step > 3:
        screen.blit(zoomed_screen, (WIDTH // 2 - zoom_width // 2, HEIGHT // 2 - zoom_height // 2 - 100))
        zoom_step += 2 * k
        if zoom_step > 450:
            k = 0

    clock.tick(60)
    step += 0.01
