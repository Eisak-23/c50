from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3
import socket
import threading



class HelloWorldScreen(Screen):
    def __init__(self, **kwargs):
        super(HelloWorldScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Área de mensajes
        self.message_history = TextInput(multiline=True, readonly=True, size_hint_y=0.8)

        # Campo de entrada para mensajes
        self.message_input = TextInput(multiline=False, hint_text='Mensaje...', size_hint_y=0.1)

        # Botón de enviar mensaje
        send_button = Button(text='Enviar', on_press=self.send_message, size_hint_y=0.1)

        # Botón para agregar usuario
        add_user_button = Button(text='Agregar Usuario', on_press=self.add_user, size_hint_y=0.1)

        # Cuadro de entrada para la dirección del usuario
        self.user_address_input = TextInput(multiline=False, hint_text='Dirección del Usuario...', size_hint_y=0.1)

        # Etiqueta para mostrar el estado de conexión del usuario
        self.user_status_label = Label(text='', size_hint_y=0.1)

        # Agregar widgets al layout
        layout.add_widget(self.message_history)
        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        layout.add_widget(add_user_button)
        layout.add_widget(self.user_address_input)
        layout.add_widget(self.user_status_label)

        self.add_widget(layout)

        # Lista para almacenar las direcciones de los usuarios agregados
        self.added_users = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 9999))
        self.server_socket.listen(5)

        # Lista para almacenar las conexiones de clientes
        self.client_sockets = []

        # Aceptar conexiones en segundo plano
        threading.Thread(target=self.accept_connections).start()


    def add_user(self, instance):
        user_address = self.user_address_input.text

        # Verificar si la dirección ya ha sido agregada
        if user_address in self.added_users:
            self.user_status_label.text = f"Usuario {user_address} ya ha sido agregado"
            return

        # Verificar si la dirección es válida en la blockchain (puedes usar web3 para hacer esta verificación)
        is_valid_address = self.validate_blockchain_address(user_address)

        if is_valid_address:
            self.added_users.append(user_address)
            self.user_status_label.text = f"Usuario {user_address} agregado correctamente"
        else:
            self.user_status_label.text = f"Dirección no válida en la blockchain"

        


    def validate_blockchain_address(self, address):
        # Infura es un servicio gratuito para acceder a la red Ethereum
        infura_url = "https://sepolia.infura.io/v3/6cfa3e90aa544d3cad27fecc8926ecf0"
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Verificar si la dirección es válida
        is_valid_address = w3.is_address(address)

        return is_valid_address


    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.message_history.text += f"\nOtro usuario: {message}"
            except:
                break

        print(f"Cliente {addr[0]}:{addr[1]} desconectado")
        self.client_sockets.remove(client_socket)
        client_socket.close()

    def send_message(self, instance):
        message = self.message_input.text

        # Enviar el mensaje a todos los clientes conectados
        for client_socket in self.client_sockets:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except:
                # Manejar la excepción en caso de desconexión del cliente
                pass

        # Mostrar el mensaje en el área de mensajes
        self.message_history.text += f"\nTú: {message}"

        # Limpiar el campo de entrada
        self.message_input.text = ''






class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Campos de entrada para el inicio de sesión
        self.username_input = TextInput(hint_text='Address', multiline=True, size_hint_y=None, height=10, width=10, size_hint=(None, None), size=(600, 40))
        self.password_input = TextInput(hint_text='Password', multiline=False, size_hint_y=None, height=40, width=10, size_hint=(None, None), size=(600, 40))

        # Botón de inicio de sesión
        login_button = Button(text='Iniciar Sesión', on_press=self.login_user, size_hint_y=None, height=10, width=10, size_hint=(None, None), size=(600, 40))

        # Agregar widgets al layout
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.pos_hint = {'center_x': 0.55, 'center_y': 0.75}

        self.add_widget(layout)

    def login_user(self, instance):
        # Acceder a los valores de los campos de entrada
       
        entered_address = self.username_input.text
        entered_mnemonic = self.password_input.text
        try:
            # Verificar si la dirección y la clave privada derivadas coinciden con las ingresadas
            if self.validate_mnemonic(entered_mnemonic, entered_address):
                print("Good: Mnemonic is valid for the given address.")
                self.manager.current = 'hello_world'

    

                # Aquí puedes continuar con la lógica adicional, como verificar la validez de la dirección, etc.

            else:
                print("Bad: Mnemonic does not match the given address.")
                popup = Popup(title='¡Hola!', content=Label(text='Bad: Mnemonic does not match the given address.'), size_hint=(None, None), size=(400, 200))
                popup.open()

        except ValidationError as e:
            print(f"Error: {e}")
            return False

    def validate_mnemonic(self, mnemonic, expected_address):
        # Crear una instancia de la clase Mnemonic y especificar el idioma
        Account.enable_unaudited_hdwallet_features()
        try:
            # Crear una instancia de la clase Mnemonic y especificar el idioma
            mnemo = Mnemonic("english")  # Ajusta el idioma según sea necesario

            # Derivar la cuenta desde la frase mnemotécnica
            account = Account.from_mnemonic(mnemonic)

            cleaned_expected_address = expected_address.lower().replace(" ", "").replace("\n", "")
            cleaned_actual_address = account.address.lower().replace(" ", "").replace("\n", "")

            # Verificar si la dirección derivada coincide con la dirección esperada
            return cleaned_actual_address == cleaned_expected_address
        except Exception as e:
            print(f"Error: An unexpected error occurred. {e}")
            return False

class RegistrationScreen(Screen):

    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)

        self.users = {}

        # Layout
        layout = BoxLayout(orientation='vertical')

        # Campos de texto para mostrar información del usuario
        self.address_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.mnemonic_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.private_key_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.balance_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)

        # Botón de volver
        back_button = Button(text='Volver', on_press=self.go_back, size_hint_y=None, height=40)

        # Agregar widgets al layout
        layout.add_widget(self.address_label)
        layout.add_widget(self.mnemonic_label)
        layout.add_widget(self.private_key_label)
        layout.add_widget(self.balance_label)
        layout.add_widget(back_button)

        self.add_widget(layout)
    





    def go_back(self, instance):
        self.manager.current = 'main'

    def register_user(self):
        # Generar una frase semilla aleatoria
        Account.enable_unaudited_hdwallet_features()
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(128)  # 128 es la longitud en bits, ajusta según sea necesario

        # Derivar la cuenta desde la frase semilla
        account = Account.from_mnemonic(mnemonic)

        # Almacenar información del usuario en el diccionario
        self.users[account.address] = {
            'mnemonic': mnemonic,
            'private_key': account._private_key.hex()
        }

        # Mostrar información del usuario en los campos de texto
        self.address_label.text = f"Dirección: {account.address}"
        self.mnemonic_label.text = f"Frase Mnemotécnica: {mnemonic}"
        self.private_key_label.text = f"Llave privada: {account._private_key.hex()}"

          # Obtener y mostrar el saldo de ETH
        balance_wei = self.get_eth_balance(account.address)
        infura_url = "https://sepolia.infura.io/v3/6cfa3e90aa544d3cad27fecc8926ecf0"
        w3 = Web3(Web3.HTTPProvider(infura_url))
        balance_eth = w3.from_wei(balance_wei, 'ether')
        self.balance_label.text = f"Saldo de ETH: {balance_eth} ETH"

    def get_eth_balance(self, address):
        # Conectar a un nodo Ethereum (aquí se usa Infura como ejemplo)
        infura_url = "https://sepolia.infura.io/v3/6cfa3e90aa544d3cad27fecc8926ecf0"
        
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Obtener el saldo en wei
        balance_wei = w3.eth.get_balance(address)
        return balance_wei



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10, pos_hint={'right': 1})

        # Registro / Inicio de sesión
        self.register_button = Button(text='Registrarse', on_press=self.register_user, size=(200, 50), padding=(10, 50), size_hint=(None, None))
     
        self.login_screen_button = Button(text='Iniciar Sesión', on_press=self.show_login_screen, size=(200, 50), padding=(10, 50), size_hint=(None, None))
       
       

        # Agregar widgets al layout
        layout.add_widget(self.register_button)
        layout.add_widget(self.login_screen_button)
        layout.pos_hint = {'center_x': 0.85, 'center_y': 0.85}
        self.add_widget(layout)



    def register_user(self, instance):
        # Cambiar a la pantalla de registro
        self.manager.current = 'registration'
        # Llamar al método de registro en la pantalla de registro
        self.manager.get_screen('registration').register_user()

    
    def show_login_screen(self, instance):
        # Cambiar a la pantalla de inicio de sesión
        self.manager.current = 'login'


class ChatBoxApp(App):
    def build(self):
        sm = ScreenManager()

        main_screen = MainScreen(name='main')
        registration_screen = RegistrationScreen(name='registration')
        login_screen = LoginScreen(name='login')
        hello_world_screen = HelloWorldScreen(name='hello_world')
       
        sm.add_widget(main_screen)
        sm.add_widget(login_screen)
        sm.add_widget(registration_screen)
        sm.add_widget(hello_world_screen)
      

        return sm

if __name__ == '__main__':
    ChatBoxApp().run()
