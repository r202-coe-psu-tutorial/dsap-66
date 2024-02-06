import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class Container(BoxLayout):

    def on_click_submit_button(self, text):
        input_1 = float(self.ids["value_input_1"].text)
        input_2 = float(self.ids["value_input_2"].text)
        result = 0

        match (text):
            case "+":
                result = input_1 + input_2
            case "*":
                result = input_1 * input_2
            case "/":
                result = input_1 / input_2
            case "-":
                result = input_1 - input_2

        self.ids["result"].text = f"Result: {str(result)}"


class CalApp(App):
    def build(self):
        return Container()


if __name__ == "__main__":
    CalApp().run()
