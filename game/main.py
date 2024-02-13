from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

from random import randint


class Gun(Widget):
    pass


class Duck(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class DuckGame(Widget):
    ducks = ReferenceListProperty()
    buttom_line_ratio = NumericProperty(0.3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DUCK_NUMBERS = 2
        for i in range(DUCK_NUMBERS):
            duck = Duck(center=self.center)
            self.ducks.append(duck)
            self.add_widget(duck)

        self.gun = Gun()
        self.gun.x = 250
        self.add_widget(self.gun)

        Window.bind(on_motion=self.on_motion)

    def on_motion(self, *args):
        print("--->")
        for arg in args:
            print(arg)

    def release_duck(self):
        for duck in self.ducks:
            duck.center = (randint(80, 120), randint(400, 500))
            duck.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        buttom_line_y = self.top * self.buttom_line_ratio

        for duck in self.ducks:
            duck.move()

            # bounce off top and bottom

            # if (duck.y < self.center_y) or (duck.top > self.height):
            # print(duck.top, duck.center)
            if (duck.y < buttom_line_y) or (duck.top > self.height):
                duck.velocity_y *= -1

            # bounce off left and right
            if (duck.x < 0) or (duck.right > self.width):
                duck.velocity_x *= -1

            for duck2 in self.ducks:
                if duck == duck2:
                    continue

                # print("duck", duck.y, duck.top, duck.x, duck.right)
                # print("duck2", duck2.y, duck2.top, duck2.x, duck2.right)
                if duck.y < duck2.top or duck.top < duck2.y:
                    duck.velocity_y *= -1
                    duck2.velocity_y *= -1


class DuckApp(App):
    def build(self):
        game = DuckGame()
        game.release_duck()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    DuckApp().run()
