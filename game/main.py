from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.clock import Clock
from kivy.vector import Vector

from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Transform, Rotate

import random
import math


class RotatableWidget(Widget):
    mouse_position_x = NumericProperty(0)
    mouse_position_y = NumericProperty(0)
    angle = NumericProperty(90)

    def get_angle(self, mouse_position):

        try:
            angle = math.degrees(
                math.atan(
                    (self.center_y - mouse_position[1])
                    / (self.center_x - mouse_position[0])
                )
            )
        except Exception as e:
            return 0

        if angle > 0:
            return angle

        return 180 + angle

    def rotate(self, mouse_position):

        if (
            self.mouse_position_x == mouse_position[0]
            and self.mouse_position_y == mouse_position[1]
        ):
            return

        angle = self.get_angle(mouse_position)
        move_angle = 0
        if angle > 0:
            move_angle = angle - self.angle
        else:
            move_angle = angle - self.angle

        if angle < 0 or angle > 180:
            return

        self.angle = angle

        self.mouse_position_x = mouse_position[0]
        self.mouse_position_y = mouse_position[1]

        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=move_angle, origin=self.center)

        with self.canvas.after:
            PopMatrix()


class Shooter(RotatableWidget):

    def move(self, mouse_position):
        self.rotate(mouse_position)


class Bullet(RotatableWidget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Duck(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class DuckGame(Widget):
    ducks = ReferenceListProperty()
    buttom_line_ratio = NumericProperty(0.3)
    bullets = ReferenceListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DUCK_NUMBERS = 2
        for i in range(DUCK_NUMBERS):
            duck = Duck(center=self.center)
            duck.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            self.ducks.append(duck)
            self.add_widget(duck)

        Window.bind(mouse_pos=self.mouse_pos)
        Window.bind(on_mouse_down=self.on_mouse_down)

        self.buttom_line_y = self.top * self.buttom_line_ratio
        self.mouse_position = (0, 0)

    def mouse_pos(self, window, pos):
        self.mouse_position = pos

    def on_mouse_down(self, sdl, x, y, button, modifiers):
        bullet = Bullet(center=(self.ids.shooter.center_x, self.ids.shooter.top))

        bullet.rotate((x, y))
        angle = bullet.get_angle((x, y))
        move_angle = 0
        if angle > 0:
            move_angle = angle - bullet.angle
        else:
            move_angle = angle - bullet.angle

        bullet.velocity = Vector(0, 1).rotate(move_angle)

        self.add_widget(bullet)
        self.bullets.append(bullet)

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
        removable_bullets = []
        for bullet in self.bullets:
            bullet.move()

            if bullet.right < 0 or bullet.x > self.width:
                removable_bullets.append(bullet)

            if bullet.y > self.height or bullet.top < 0:
                removable_bullets.append(bullet)

        for bullet in removable_bullets:
            self.bullets.remove(bullet)
            self.remove_widget(bullet)


class DuckApp(App):
    def build(self):
        game = DuckGame()
        game.release_duck()

        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    DuckApp().run()
