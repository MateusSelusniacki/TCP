from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivy.clock import Clock    

from server import server

class Demo(MDApp):
    def build(self):
        screen = Screen()

        self.port_label = MDLabel(
            text = "Port",
            pos_hint = {"center_x":1.3,"center_y":0.8}    
        )

        self.port_tf = MDTextField(
            pos_hint = {"center_x":0.85,"center_y":0.75},
            size_hint = (0.1,0.2)
        )

        self.start_button = MDRectangleFlatButton(
            text = 'Iniciar',
            pos_hint = {"center_x":0.95,"center_y":0.75},
            on_press = self.btn_start
        )

        self.recv_data_label = MDLabel(
            text = "Dados recebidos",
            pos_hint = {"center_x":0.6,"center_y":0.95}
        )

        self.recv_data = MDLabel(
            text = "",
            pos_hint = {"center_x":0.6,"center_y":0.8}
        )

        self.sended_data_label = MDLabel(
            text = "Dados enviados",
            pos_hint = {"center_x":0.6,"center_y":0.5}
        )

        self.sended_data = MDLabel(
            text = "",
            pos_hint = {"center_x":0.6,"center_y":0.35}
        )

        self.data_to_send_label = MDLabel(
            text = "Send data",
            pos_hint = {"center_x":0.55,"center_y":0.15}
        )

        self.data_to_send = MDTextField(
            pos_hint = {"center_x":0.45,"center_y":0.1},
            size_hint = (0.8,1)
        )

        self.send_data = MDRectangleFlatButton(
            text = 'Enviar',
            on_press = self.btn_send,
            pos_hint = {"center_x":0.92,"center_y":0.1},
            disabled = True
        )

        screen.add_widget(self.port_label)
        screen.add_widget(self.port_tf)
        screen.add_widget(self.start_button)
        screen.add_widget(self.recv_data_label)
        screen.add_widget(self.recv_data)    
        screen.add_widget(self.sended_data_label)
        screen.add_widget(self.sended_data)
        screen.add_widget(self.data_to_send_label)
        screen.add_widget(self.data_to_send)
        screen.add_widget(self.send_data)

        self.s = server.Server()

        return screen
    
    def on_receive_data(self,increment):
        self.recv_data.text += self.s.content
        self.s.content = ""

        for i in range(1,len(self.recv_data.text)):
            if(i%70 == 0 and self.recv_data.text[i] != '\n'):
                self.recv_data.text = self.recv_data.text[0:i] + '\n' + self.recv_data.text[i::]
                if(i == 560):
                    self.recv_data.text = self.recv_data.text[70::]

    def btn_send(self,btn):
        self.s.send(self.data_to_send.text)
        self.sended_data.text += self.data_to_send.text

        for i in range(1,len(self.sended_data.text)):
            if(i%70 == 0 and self.sended_data.text[i] != '\n'):
                self.sended_data.text = self.sended_data.text[0:i] + '\n' + self.sended_data.text[i::]
                if(i == 560):
                    self.sended_data.text = self.sended_data.text[70::]
    
    def btn_start(self,btn):
        if(btn.text == 'Iniciar'):
            try:
                int(self.port_tf.text)
            except:
                return

            btn.text = 'Parar'
            
            self.s.start(int(self.port_tf.text))
            Clock.schedule_interval(self.on_receive_data, 2)
            self.send_data.disabled = False

        elif(btn.text == 'Parar'):
            btn.text = 'Iniciar'

            self.s.stop()
            Clock.unschedule(self.on_receive_data)
            self.send_data.disabled = True
            
Demo().run()