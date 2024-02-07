from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

from random import randint


class Duck(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class DuckGame(Widget):
    ducks = ReferenceListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DUCK_NUMBERS = 5
        for i in range(DUCK_NUMBERS):
            duck = Duck(center=self.center)
            self.ducks.append(duck)
            self.add_widget(duck)

    def release_duck(self):
        for duck in self.ducks:
            duck.center = self.center
            duck.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        for duck in self.ducks:
            duck.move()

            # bounce off top and bottom

            if (duck.y < 0) or (duck.top > self.height):
                duck.velocity_y *= -1

            # bounce off left and right
            if (duck.x < 0) or (duck.right > self.width):
                duck.velocity_x *= -1


class DuckApp(App):
    def build(self):
        game = DuckGame()
        game.release_duck()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    DuckApp().run()
