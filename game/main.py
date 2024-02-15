from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Transform, Rotate

import random
import math


class Shooter(Widget):
    mouse_position_x = NumericProperty(0)
    mouse_position_y = NumericProperty(0)
    angle = NumericProperty(90)

    def move(self, mouse_position):
        # print(mouse_position, mouse_position[0])
        # print("center pos", self.center)
        # print("mouse pos", mouse_position)

        angle = math.degrees(
            math.atan(
                (self.center_y - mouse_position[1])
                / (self.center_x - mouse_position[0])
            )
        )
        # print(mouse_position[1] - self.center_y, mouse_position[0] - self.center_x)
        # print("angle", angle)
        # print("x =", self.mouse_position_x, mouse_position[0])
        # print("y =", self.mouse_position_y, mouse_position[1])

        if (
            self.mouse_position_x == mouse_position[0]
            and self.mouse_position_y == mouse_position[1]
        ):
            # print("no update")
            return

        print("->", self.angle, angle)

        if angle > 0:
            angle = self.angle - angle

        print("n ang", angle)
        self.angle = angle

        self.mouse_position_x = mouse_position[0]
        self.mouse_position_y = mouse_position[1]

        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=angle, origin=self.center)

        with self.canvas.after:
            PopMatrix()


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
            duck.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            self.ducks.append(duck)
            self.add_widget(duck)

        Window.bind(mouse_pos=self.mouse_pos)

        self.buttom_line_y = self.top * self.buttom_line_ratio
        self.mouse_position = (0, 0)

    def mouse_pos(self, window, pos):
        print("mouse 0>", pos)
        self.mouse_position = pos

    def release_duck(self):
        for duck in self.ducks:

            position = (
                random.randint(0, Window.width - duck.center_x),
                random.randint(
                    self.buttom_line_y + 2 * duck.top, Window.height - duck.top
                ),
            )
            duck.center = position

            for col_duck in self.ducks:
                if col_duck == duck:
                    continue
                if not duck.collide_widget(col_duck):
                    continue

                while duck.collide_widget(col_duck):
                    duck.center_x += 2

            duck.move()

    def update(self, dt):
        self.buttom_line_y = self.top * self.buttom_line_ratio
        for duck in self.ducks:
            if (duck.y < self.buttom_line_y) or (duck.top > self.height):
                duck.velocity_y *= -1

            if (duck.x < 0) or (duck.right > self.width):
                duck.velocity_x *= -1

            duck.move()

            for col_duck in self.ducks:
                if duck == col_duck:
                    continue

                if duck.collide_widget(col_duck):
                    duck.velocity_y *= -1
                    col_duck.velocity_y *= -1
                    duck.velocity_x *= -1
                    col_duck.velocity_x *= -1
                    duck.move()

        self.ids.shooter.move(self.mouse_position)


class DuckApp(App):
    def build(self):
        game = DuckGame()
        game.release_duck()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    DuckApp().run()
