from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.clock import Clock    

from cliente import cliente
import re
import os

r = re.compile(('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'))

class Demo(MDApp):
    nlinhas = 0
    content = ''
    def build(self):
        screen = Screen()

        self.ip_label = MDLabel(
            text = "IP",
            pos_hint = {'center_x':1.2,'center_y':0.8}
        )

        self.ip_tf = MDTextField(
            pos_hint = {'center_x':0.77,'center_y':0.75},
            size_hint = (0.15,0.9)
        )

        self.port_label = MDLabel(
            text = "Porta",
            pos_hint = {'center_x':1.4,'center_y':0.8}
        )

        self.port_tf = MDTextField(
            pos_hint = {'center_x':0.93,'center_y':0.75},
            size_hint = (0.08,0.2)
        )

        self.btn_ping = MDRectangleFlatButton(
            text = "Pingar",
            pos_hint = {'center_x':0.74,'center_y':0.65},
            on_press = self.ping
        )

        self.btn_connect = MDRectangleFlatButton(
            text = "Conectar",
            pos_hint = {'center_x':0.88,'center_y':0.65},
            on_press = self.connect
        )

        self.console_label = MDLabel(
            text = 'Console:',
            pos_hint = {'center_x':0.52,'center_y':0.9}
        )

        self.console = MDLabel(
            text = "",
            pos_hint = {'center_x':0.52,'center_y':0.8}
        )

        self.send_tf = MDTextField(
            pos_hint = {'center_x':0.45, 'center_y':0.1},
            size_hint = (0.8,0.1)
        )

        self.send_btn = MDRectangleFlatButton(
            text = 'enviar',
            pos_hint = {'center_x':0.91,'center_y':0.1},
            on_press = self.send,
            disabled = True
        )

        screen.add_widget(self.ip_label)
        screen.add_widget(self.ip_tf)
        screen.add_widget(self.port_label)
        screen.add_widget(self.port_tf)
        screen.add_widget(self.btn_ping)
        screen.add_widget(self.btn_connect)
        screen.add_widget(self.console_label)
        screen.add_widget(self.console)
        screen.add_widget(self.send_tf)
        screen.add_widget(self.send_btn)

        self.client = cliente.Client()
        Clock.schedule_interval(self.on_receive_data, 2)

        return screen

    def on_receive_data(self,increment):
        if(self.client.content):
            self.content = self.client.content
            self.write_to_console(f"Recebido: {self.content}")
            self.client.content = ''

    def write_to_console(self,text_to_write):
        self.console.text += text_to_write + '\n'

        if(self.nlinhas == 22):
            x = self.console.text.split('\n')
            self.console.text = '\n'.join(x[1::])
        else:
            self.console.pos_hint['center_y'] -= 0.015
            self.nlinhas += 1
            
    def on_stop(self):
        self.client.disconnect()

    def send(self,btn):
        self.client.send(self.send_tf.text)

    def connect(self,btn):
        if(self.btn_connect.text == "Conectar"):
            if(not r.match(self.ip_tf.text)):
                return
            
            try:
                int(self.port_tf.text)
            except:
                return
            
            if(self.client.connect(self.ip_tf.text,int(self.port_tf.text))):
                self.write_to_console(f"Conectado a {self.ip_tf.text} na porta {self.port_tf.text}")
                self.btn_connect.text = 'Desconectar'

                self.send_btn.disabled = False
                self.ip_tf.disabled = True
                self.port_tf.disabled = True

        elif(self.btn_connect.text == "Desconectar"):
            self.write_to_console('Desconetado')
            self.client.disconnect()
            self.btn_connect.text = "Conectar"

            self.send_btn.disabled = True
            self.ip_tf.disabled = False
            self.port_tf.disabled = False

    def ping(self,btn):
        if(not r.match(self.ip_tf.text)):
                return
        os.system("ping -c 1 " + self.ip_tf.text)

Demo().run()