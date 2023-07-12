from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
import speech_recognition as sr
import openai

openai.api_key = "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"

username_helper = """
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        pos_hint: {"center_x": 0.5}
        MDTextField:
            id: text_field
            hint_text: "Send a Message"
            icon_right: "android"
            size_hint_x: 0.9
        MDFillRoundFlatButton:
            text: "Submit"
            size_hint_x: 0.15
            on_release: app.on_submit_button_click()
        MDFillRoundFlatButton:
            id: voice_button
            text: "Voice"
            size_hint_x: 0.15
            on_release: app.on_voice_button_click()
"""

result_helper = """
Screen:
    ScrollView:
        MDLabel:
            id: result_label
            text: ""
            halign: 'center'
            font_size: '24sp'
            size_hint_y: None
            adaptive_height: True
    MDFillRoundFlatButton:
        text: "Go Back"
        pos_hint: {"center_x": 0.5, "center_y": 0.1}
        on_release: app.on_go_back_button_click()
"""
kv = """
Screen:
    BoxLayout:
        orientation: 'vertical'
        AsyncImage:
            source: 'Logo.png'
            size_hint: 0.9, 0.1  # Adjust the size of the SmartTile
            size: self.texture_size
"""

class DemoApp(MDApp):
    username_screen = None
    result_screen = None
    
    def build(self):
        #self.icon_app=MDFillRoundFlatButton(icon="images\Logo.png")
        #self.screen = Builder.load_string(kv)
        #return screen
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        
        
        self.username_screen = Builder.load_string(username_helper)
        self.result_screen = Builder.load_string(result_helper)
        self.screen = Builder.load_string(kv)
        
        screen = Screen()
        screen.add_widget(self.username_screen)
        screen.add_widget(self.screen)
        return screen
    
    def on_submit_button_click(self):
        text = self.username_screen.ids.text_field.text
        print(f"User input: {text}")
        
        def generate_text(text):
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=text,
                max_tokens=2000,
                top_p=1,
                temperature=0,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].text

        self.result_screen.ids.result_label.text = generate_text(text)
        self.root.clear_widgets()
        self.root.add_widget(self.result_screen)
    
    def on_voice_button_click(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        try:
            print("Recognizing...")
            voice_input_text = r.recognize_google(audio)

            def generate_text1():
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=voice_input_text,
                    max_tokens=2000,
                    top_p=1,
                    temperature=0,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                return response.choices[0].text

            self.username_screen.ids.text_field.text += voice_input_text
            self.result_screen.ids.result_label.text = generate_text1()
            self.root.clear_widgets()
            self.root.add_widget(self.result_screen)
                        
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
    
    def on_go_back_button_click(self):
        self.root.clear_widgets()
        self.root.add_widget(self.username_screen)
    
    
DemoApp().run()
