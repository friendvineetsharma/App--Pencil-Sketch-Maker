from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
import cv2

Window.size=(300,500)

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: '8dp'
        padding: '8dp'
        Image:
            id: image
            source: ''
        MDRectangleFlatButton:
            text: 'Upload'
            halign: 'center'
            pos_hint: {'center_x': 0.5 , 'center_y':0.6 }
            on_press: root.callback()

        MDRectangleFlatButton:
            text: 'Convert'
            halign: 'center'
            pos_hint: {'center_x': 0.5 , 'center_y':0.6 }
            on_press: root.convert()

        MDRectangleFlatButton:
            halign: 'center'
            pos_hint: {'center_x': 0.5 , 'center_y':0.5 }
            text: 'Clear'
            on_press: root.clear()

<LoadDialog>:
    id: widget
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.selection)
""")


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MenuScreen(Screen):
    im=Image(source='')

    def callback(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self,filename):
        try:
            self.ids.image.source = filename[0]
        except:
            pass

        self.dismiss_popup()


    def convert(self):
        if self.ids.image.source == '':
            self.callback()
        else:
            img = cv2.imread(self.ids.image.source, 1)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_invert = cv2.bitwise_not(img_gray)
            img_smoothing = cv2.GaussianBlur(img_invert, (21, 21),sigmaX=0, sigmaY=0)
            final_img = cv2.divide(img_gray, 255-img_smoothing, scale=256)
            cv2.imwrite('1.jpg', final_img)
            self.ids.image.source = '1.jpg'

    def clear(self):
        self.ids.image.source = ''



class TestApp(MDApp):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))

        return sm


if __name__ == '__main__':
    TestApp().run()
