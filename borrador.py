from kivy.uix.label import Label

class ChatBoxApp(App):
    def build(self):
        self.messages = []

        # Layout
        layout = BoxLayout(orientation='vertical')

        # Mensajes del chat
        self.message_label = Label(text='', size_hint_y=8)

        # Entrada de texto
        self.text_input = TextInput(size_hint_y=0.5)

        # Botón de enviar
        send_button = Button(text='Enviar', on_press=self.send_message, size_hint_y=None, height=40)

        # Agregar widgets al layout
        layout.add_widget(self.message_label)
        layout.add_widget(self.text_input)
        layout.add_widget(send_button)

        return layout

    def send_message(self, instance):
        user_input = self.text_input.text
        response = self.get_bot_response(user_input)

        # Agregar mensajes al historial
        self.messages.append(f"Usuario: {user_input}")
        self.messages.append(f"Chatbot: {response}")

        # Actualizar el texto en el Label
        self.message_label.text = '\n'.join(self.messages)

        # Limpiar la entrada de texto
        self.text_input.text = ''

    def get_bot_response(self, user_input):
        # Aquí puedes implementar la lógica de tu chatbot
        # Por ejemplo, puedes usar una biblioteca de procesamiento de lenguaje natural como spaCy o NLTK
        # para generar respuestas basadas en el input del usuario.
        # Por ahora, simplemente devolvemos una respuesta estática.
        return "¡Hola! Soy un chatbot simple. ¿En qué puedo ayudarte?"

if __name__ == '__main__':
    ChatBoxApp().run()
