# Dentro de la clase ChatScreen

from kivy.uix.label import Label

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        # ... (código anterior)

        # Botón para agregar usuario
        add_user_button = Button(text='Agregar Usuario', on_press=self.add_user, size_hint_y=0.1)

        # Cuadro de entrada para la dirección del usuario
        self.user_address_input = TextInput(multiline=False, hint_text='Dirección del Usuario...', size_hint_y=0.1)

        # Etiqueta para mostrar el estado de conexión del usuario
        self.user_status_label = Label(text='', size_hint_y=0.1)

        # Agregar widgets al layout
        layout.add_widget(add_user_button)
        layout.add_widget(self.user_address_input)
        layout.add_widget(self.user_status_label)

        self.add_widget(layout)

    def add_user(self, instance):
        user_address = self.user_address_input.text

        # Verificar si la dirección es válida en la blockchain (puedes usar web3 para hacer esta verificación)
        is_valid_address = self.validate_blockchain_address(user_address)

        if is_valid_address:
            # Agregar lógica para verificar si el usuario está conectado a la red local
            is_user_connected = self.check_user_connection(user_address)

            if is_user_connected:
                self.user_status_label.text = f"Usuario {user_address} está conectado"
            else:
                self.user_status_label.text = f"Usuario {user_address} NO está conectado"
        else:
            self.user_status_label.text = f"Dirección no válida en la blockchain"

    def validate_blockchain_address(self, address):
        # Aquí deberías implementar la lógica para verificar si la dirección es válida en la blockchain
        # Puedes usar web3 para hacer esta verificación
        # Devuelve True si la dirección es válida, False de lo contrario
        return True  # Reemplazar con tu lógica de validación

    def check_user_connection(self, address):
        # Aquí deberías implementar la lógica para verificar si el usuario está conectado a la red local
        # Puedes usar la lista de sockets u otra lógica para hacer esta verificación
        # Devuelve True si el usuario está conectado, False de lo contrario
        return True  # Reemplazar con tu lógica de verificación

    # ... (resto del código)
