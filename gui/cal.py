import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class MyApp(App):
    def build(self):
        box = BoxLayout(orientation="vertical")
        input_box = BoxLayout()
        sign_box = BoxLayout()

        self.result = Label(text="Result")
        self.value_input_1 = TextInput(text="0")
        self.value_input_2 = TextInput(text="0")
        plus_sign = Button(text="+", on_press=self.on_click_submit_button)
        multiply_sign = Button(text="*", on_press=self.on_click_submit_button)

        sign_box.add_widget(plus_sign)
        sign_box.add_widget(multiply_sign)
        input_box.add_widget(self.value_input_1)
        input_box.add_widget(self.value_input_2)
        box.add_widget(input_box)
        box.add_widget(sign_box)
        box.add_widget(self.result)

        return box

    def on_click_submit_button(self, ev):
        print(ev.text)
        input_1 = float(self.value_input_1.text)
        input_2 = float(self.value_input_2.text)
        result = 0

        match (ev.text):
            case "+":
                result = input_1 + input_2
            case "*":
                result = input_1 * input_2

        self.result.text = f"Result: {str(result)}"


if __name__ == "__main__":
    MyApp().run()
