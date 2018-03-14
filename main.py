import time, pygame, lib

def get_center(surface, sprite):
    return (surface.w/2 - sprite.w/2,
            surface.h/2 - sprite.h/2)

# Эта сцена ожидания наследуется от нашей сцены из lib
class WaitScene(lib.Scene):
    def __init__(self, time = 1000, *argv):
        lib.Scene.__init__(self, *argv)
        self.run = 0
        self.time = time

    def _event(self, event):
        # Здесь нам нужно обработать все события.
        # Если есть объекты которым нужны события их нужно
        # оповестить здесь, так как event.get() отчищает очередь событий,
        # а в объектах нужно брать из очереди только нужные события.
        # Здесь можно обработать все.
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                self.the_end()
                self.set_next_scene ( MenuScene ( ) )

        if not self.run < self.time:
            self.the_end()

    def _update(self, dt):
        self.run += dt

# Эта сцена позволит показать наш логотип
class ShowScene(lib.Scene):
    # Как видите мы создаем при старте сцены наш логотип(загружая его из файла)
    # и анимацию.
    def _start(self):
        sprite = self.manager.get_image('logo.png')
        self.sprite = pygame.transform.scale(sprite, (sprite.get_rect().w * 5,
                                             sprite.get_rect().h * 5))

        self.plambir = lib.Transparent(3000)
        self.plambir.start()

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                self.the_end()
                self.set_next_scene ( MenuScene ( ) )

        if not self.plambir.is_start():
            self.the_end()

    def _update(self, dt):
        self.plambir.update(dt)

    def _draw(self, dt):
        self.display.fill((255,255,255))
        # Как видите мы рисуем логотип, сначала пропустив его через анимацию
        # прозрачности.
        self.display.blit(self.plambir.get_sprite(self.sprite),
                          get_center(self.display.get_rect(),
                                     self.sprite.get_rect()))

# Эта сцена исчезновения логотипа, так как она не особо от сцены
# появления отличается, мы просто кое что изменим в инициализации
# класса ShowScene.
class HideScene(ShowScene):
    def _start(self):
        ShowScene._start(self)

        self.plambir.toggle()
        self.plambir.set_time(1000)

class Menu:
    def __init__(self, position = (0,0), loop = True):
        self.index = 0
        self.x = position[0]
        self.y = position[1]
        self.menu = list()

    # Метод перемещающий нас в низ циклично по всем элементам.
    def down(self):
        self.index += 1
        if self.index >= len(self.menu):
            self.index = 0

    # Тоже самое но в вверх.
    def up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.menu)-1

    # Добавляет новый элемент, нужно передать 2 изображения.
    # На 1 не выбранный вид элемента.
    # На 2 выбранный элемент
    def add_menu_item(self, no_select, select, func):
        self.menu.append({ 'no select' : no_select,
                           'select' : select,
                           'func' : func })

    def call(self):
        self.menu[self.index]['func']()

    def draw(self, display):
        index = 0
        x = self.x
        y = self.y
        for item in self.menu:
            if self.index == index:
                display.blit(item['select'], (x, y))
                y += item['select'].get_rect().h
            else:
                display.blit(item['no select'], (x, y))
                y += item['no select'].get_rect().h
            index += 1

class MenuScene(lib.Scene):
    def item_call(self):
        print("item_call")
        self.the_end()

    def _start(self):
        self.menu = Menu((330,300))

        # Именно таким образом мы можем получить текст в pygame
        # В данном случае мы используем системный шрифт.
        font      = pygame.font.SysFont("Monospace", 40, bold=False, italic=False)
        font_bold = pygame.font.SysFont("Monospace", 40, bold=True, italic=False)
        item = u"Новая игра"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)
        item = u"Настройки"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)
        item = u"Выход"
        self.menu.add_menu_item(font.render(item,True,(0,0,0)),
                                font_bold.render(item,True,(0,0,0)),
                                self.item_call)

    def _event(self, event):
        for e in event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.menu.down()
                elif e.key == pygame.K_UP:
                    self.menu.up()
                elif e.key == pygame.K_RETURN:
                    self.menu.call()

    def _draw(self, dt):
        self.display.fill((255,255,255))
        self.menu.draw(self.display)


if __name__ == '__main__':
    # Вот так хитро все и закрутилось.
    # ждем, показываем, ждем, скрываем, ждем, меню.
    scene = WaitScene(1000, ShowScene(WaitScene(500, HideScene(WaitScene(1000,MenuScene())))))
    game = lib.Game(640, 480, scene = scene)
    game.set_caption("plambir", "icon.png")

    game.game_loop()

if __name__ == '__main__':
    # Вот так хитро все и закрутилось.
    # ждем, показываем, ждем, скрываем, ждем.
    scene = WaitScene(1000, ShowScene(WaitScene(500, HideScene(WaitScene(1000)))))
    game = lib.Game(640, 480, scene = scene)
    game.set_caption("plambir", "icon.png")

    game.game_loop()