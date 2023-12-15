from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3

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
        layout = BoxLayout(orientation='vertical')

        # Registro / Inicio de sesión
        self.register_button = Button(text='Registrarse', on_press=self.register_user)
        self.login_button = Button(text='Iniciar Sesión', on_press=self.login_user)

        # Agregar widgets al layout
        layout.add_widget(self.register_button)
        layout.add_widget(self.login_button)

        self.add_widget(layout)

    def register_user(self, instance):
        # Cambiar a la pantalla de registro
        self.manager.current = 'registration'
        # Llamar al método de registro en la pantalla de registro
        self.manager.get_screen('registration').register_user()

    def login_user(self, instance):
        user_input = self.text_input.text
        if user_input in self.manager.get_screen('registration').users:
            print(f"Inicio de sesión exitoso para el usuario con dirección: {user_input}")
        else:
            print("Usuario no encontrado. Regístrate primero.")


class ChatBoxApp(App):
    def build(self):
        sm = ScreenManager()

        main_screen = MainScreen(name='main')
        registration_screen = RegistrationScreen(name='registration')

        sm.add_widget(main_screen)
        sm.add_widget(registration_screen)

        return sm

if __name__ == '__main__':
    ChatBoxApp().run()
