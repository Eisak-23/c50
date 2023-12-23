from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from eth_account import Account
from mnemonic import Mnemonic
from web3 import Web3

infura_url= "https://sepolia.infura.io/v3/6cfa3e90aa544d3cad27fecc8926ecf0"


class HelloWorldScreen(Screen):
    def __init__(self, **kwargs):
        super(HelloWorldScreen, self).__init__(**kwargs)
        background_image = Image(source='giphy.gif', anim_delay=1 / 30.0, allow_stretch=True, keep_ratio=False, anim_loop=0)
        layout = BoxLayout(orientation='vertical', spacing=10)
        self.message_label = Label(text="¡I love Blockchain!")
        self.input_box = TextInput(hint_text='Write a message...', multiline=False,  size=(100,200))
        send_button = Button(text='Send', on_press=self.send_message, size_hint_y=None, height=30, width=10, size_hint=(None, None), size=(300,50), background_color=(0, 0.7, 0, 1))

        layout.add_widget(self.message_label)
        layout.add_widget(self.input_box)
        layout.add_widget(send_button)
        self.add_widget(background_image)
        self.add_widget(layout)

    def send_message(self, instance):
        message_text = self.input_box.text
        response = self.process_command(message_text)
        self.message_label.text = response
       

    def process_command(self, command):
        command = command.lower()
        
        
        if command == '/help':
            return "Hello! I'm a Blockchain bot. You can ask me about concepts like blocks, transactions, smart contracts, etc."
        elif command == '/block':
            return "A block is a fundamental unit of data in a blockchain that contains information about transactions and other details.\n Blocks are linked together through cryptography to form the blockchain."
        elif command == '/transaction':
            return "A transaction is the act of sending or receiving cryptocurrencies between two parties on a blockchain. It contains information about the amount of cryptocurrencies transferred, sender and recipient addresses, and other digital signatures for security."
        elif command == '/smart_contract':
            return "A smart contract is a self-executing program with predefined terms and conditions written in code\n. It runs on a blockchain and is used to automate and enforce agreements without the need for intermediaries."
        elif command == '/hello':
            user_name = self.manager.get_screen('login').username_input.text
            return f"Hello {user_name}, How are You?"
        
        elif command == '/mnemonic':
            return "A mnemonic phrase is a sequence of easily memorable words used to generate cryptographic keys for security\n. For instance, correct owl single piano could represent a unique and secure key."
        
        elif command == '/pof':
            return "Proof of Work\n\n is a consensus algorithm in blockchain where participants (miners)\n solve complex mathematical puzzles to validate transactions and create new blocks.\n The first to solve it gets the right to add the block and is rewarded with cryptocurrency. Example: Bitcoin miners use computational power to compete in solving mathematical puzzles, contributing to the security of the network"
        
        elif command == '/pos':
            return "Proof of Stake\n is a blockchain consensus mechanism where validators are chosen to create new blocks based on the amount of cryptocurrency they hold and are willing to stake as collateral\n. This aims to achieve consensus in a more energy-efficient way compared to Proof of Work.Example: In a Proof of Stake system, validators with more staked coins have higher chances of being selected to validate transactions and create new blocks."
        
        elif command == '/balance':
            user_name = self.manager.get_screen('login').username_input.text
            w3 = Web3(Web3.HTTPProvider(infura_url))

        # Obtener el saldo en wei
            balance_wei = w3.eth.get_balance(user_name)
            return f"The balance of  {user_name}  is {balance_wei} ETH."
        
        elif command == '/block_number':
          
            w3 = Web3(Web3.HTTPProvider(infura_url))

        # Obtener el número de bloques
            block_number = w3.eth.block_number
            return f"The Number is {block_number}"
        else:
            return "Sorry, I don't understand that command. using commands like\n /help, /block, /transaction, /smart_contract,  /pof,  /pos,  /mnemonic,  /block_number, /balance."
    
        
  
        
        
        
       

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Layout
        background_image = Image(source='giphy.gif', anim_delay=1 / 30.0, allow_stretch=True, keep_ratio=False, anim_loop=0)
        layout = BoxLayout(orientation='vertical', spacing=10)

        # Input fields for login
        self.username_input = TextInput(hint_text='Address', multiline=True, size_hint_y=None, height=10, width=10, size_hint=(None, None), size=(600, 40))
        self.password_input = TextInput(hint_text='Password', multiline=False, size_hint_y=None, height=40, width=10, size_hint=(None, None), size=(600, 40))
        
        # Login button
        login_button = Button(text='Login', on_press=self.login_user, size_hint_y=None, height=40, width=10, size_hint=(None, None), size=(600, 40))
        back_button = Button(text='Back', on_press=self.go_back, size_hint_y=None, height=30, width=10, size_hint=(None, None), size=(300, 50), background_color=(1, 0, 0, 1))
        layout.add_widget(back_button)

        # Add widgets to the layout
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.pos_hint = {'center_x': 0.55, 'center_y': 0.75}
        self.add_widget(background_image)
        self.add_widget(layout)
        
    def login_user(self, instance):
        # Access values from input fields
        entered_address = self.username_input.text
        entered_mnemonic = self.password_input.text
        try:
            # Verify if the derived address and private key match the entered ones
            if self.validate_mnemonic(entered_mnemonic, entered_address):
                print("Good: Mnemonic is valid for the given address.")
                self.manager.current = 'hello_world'

                # Additional logic can be implemented here, such as validating the address further.

            else:
                print("Bad: Mnemonic does not match the given address.")
                popup = Popup(title='Hello!', content=Label(text='Bad: Mnemonic does not match the given address.'), size_hint=(None, None), size=(400, 200))
                popup.open()

        except ValueError as e:
            print(f"Error: {e}")
            return False

    def validate_mnemonic(self, mnemonic, expected_address):
        # Create an instance of the Mnemonic class and specify the language
        Account.enable_unaudited_hdwallet_features()
        try:
            # Create an instance of the Mnemonic class and specify the language
            mnemo = Mnemonic("english")  # Adjust the language as needed

            # Derive the account from the mnemonic phrase
            account = Account.from_mnemonic(mnemonic)

            cleaned_expected_address = expected_address.lower().replace(" ", "").replace("\n", "")
            cleaned_actual_address = account.address.lower().replace(" ", "").replace("\n", "")

            # Check if the derived address matches the expected address
            return cleaned_actual_address == cleaned_expected_address
        except Exception as e:
            print(f"Error: An unexpected error occurred. {e}")
            return False
    
    def go_back(self, instance):
        self.manager.current = 'main'
        
        
class RegistrationScreen(Screen):

    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)

        self.users = {}

        # Layout
        background_image = Image(source='giphy.gif', anim_delay=1 / 30.0, allow_stretch=True, keep_ratio=False, anim_loop=0)
        layout = BoxLayout(orientation='vertical')

        # Field to show  about  user
        self.address_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.mnemonic_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.private_key_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)
        self.balance_label = TextInput(readonly=True, multiline=False, size_hint_y=None, height=40)

        # Button back
        back_button = Button(text='Back', on_press=self.go_back, size_hint_y=None, height=40, background_color=(1, 0, 0, 1))

        # adds widgets to layout
        layout.add_widget(self.address_label)
        layout.add_widget(self.mnemonic_label)
        layout.add_widget(self.private_key_label)
        layout.add_widget(self.balance_label)
        layout.add_widget(back_button)
        self.add_widget(background_image)

        self.add_widget(layout)
    





    def go_back(self, instance):
        self.manager.current = 'main'

    def register_user(self):
        
        # Generate a phrase 
        Account.enable_unaudited_hdwallet_features()
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(128)  # 128 bit 

        account = Account.from_mnemonic(mnemonic)

        # save information in a directory
        self.users[account.address] = {
            'mnemonic': mnemonic,
            'private_key': account._private_key.hex()
        }

        # Mostrar información del usuario en los campos de texto
        self.address_label.text = f"Address: {account.address}"
        self.mnemonic_label.text = f"Mnemonic Phrase: {mnemonic}"
        self.private_key_label.text = f"Private Key: {account._private_key.hex()}"

          # get the  balance of ETH
        balance_wei = self.get_eth_balance(account.address)
    
        w3 = Web3(Web3.HTTPProvider(infura_url))
        balance_eth = w3.from_wei(balance_wei, 'ether')
        self.balance_label.text = f"Balance of ETH: {balance_eth} ETH"

    def get_eth_balance(self, address):
    
     
        w3 = Web3(Web3.HTTPProvider(infura_url))

        # Balance of wei
        balance_wei = w3.eth.get_balance(address)
        return balance_wei



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)



        # background
        
        background_image = Image(source='giphy.gif', anim_delay=1 / 30.0, allow_stretch=True, keep_ratio=False, anim_loop=0)

        # Create main design

        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10, pos_hint={'right': 1})

        # sign up / login
        self.register_button = Button(text='Sign up', on_press=self.register_user, size=(200, 50), padding=(10, 50), size_hint=(None, None), background_color=(0.2, 0.5, 0.9, 1))
     
        self.login_screen_button = Button(text='Login', on_press=self.show_login_screen, size=(200, 50), padding=(10, 50), size_hint=(None, None))
       
       

        # adds widgets to layout
        layout.add_widget(self.register_button)
        layout.add_widget(self.login_screen_button)
        layout.pos_hint = {'center_x': 0.85, 'center_y': 0.85}
        self.add_widget(background_image)
        self.add_widget(layout)
      



    def register_user(self, instance):
    # Switch to the registration screen
        self.manager.current = 'registration'
    # Call the registration method on the registration screen
        self.manager.get_screen('registration').register_user()

    def show_login_screen(self, instance):
    # Switch to the login screen
        self.manager.current = 'login'


class ChatBlockApp(App):
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
    ChatBlockApp().run()
