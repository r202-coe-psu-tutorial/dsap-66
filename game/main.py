from kivy.app import App
from kivy.uix.widget import Widget


class DuckGame(Widget):
    pass


class DuckApp(App):
    def build(self):
        return DuckGame()


if __name__ == "__main__":
    DuckApp().run()
