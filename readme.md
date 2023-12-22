# Proyecto de ChatBox en Kivy

## Descripción del Proyecto

El proyecto ChatBox es una aplicación interactiva desarrollada en Kivy, un marco de interfaz de usuario de Python para aplicaciones multitáctiles. La aplicación simula un sistema de chat interactivo centrado en conceptos relacionados con blockchain.

## Estructura de Archivos

### Archivos Principales

1.  **main.py**: El archivo principal que contiene la lógica principal de la aplicación.
2.  **giphy.gif**: Una imagen utilizada como fondo en varias pantallas de la aplicación.

### Clases y Módulos

1.  **HelloWorldScreen (hello_world_screen.py)**: Una clase que define la pantalla principal de la aplicación. Contiene un cuadro de entrada de texto, un botón de envío y responde a comandos específicos relacionados con blockchain.
    
2.  **LoginScreen (login_screen.py)**: Clase que implementa la pantalla de inicio de sesión. Permite a los usuarios ingresar su dirección y una frase mnemotécnica para acceder a la aplicación.
    
3.  **RegistrationScreen (registration_screen.py)**: Clase que gestiona la pantalla de registro de usuarios. Genera una dirección, una frase mnemotécnica y una clave privada para el usuario y muestra esta información.
    
4.  **MainScreen (main_screen.py)**: Clase que define la pantalla principal de la aplicación. Proporciona opciones para registrarse e iniciar sesión.
    
5.  **ChatBoxApp (main.py)**: La clase principal que inicializa y ejecuta la aplicación Kivy.
    

### Librerías Externas

1.  **eth_account**: Utilizado para manejar cuentas de Ethereum, derivar claves privadas y verificar la validez de las frases mnemotécnicas.
2.  **mnemonic**: Utilizado para generar frases mnemotécnicas aleatorias.
3.  **web3**: Utilizado para interactuar con nodos Ethereum y obtener información, como saldos y números de bloque.

## Uso de la Aplicación

1.  **Inicio de Sesión**: Al hacer clic en "Login" desde la pantalla principal, se accede a la pantalla de inicio de sesión. Se ingresa la dirección y la frase mnemotécnica para autenticarse.
    
2.  **Registro de Usuario**: Al hacer clic en "Sign up" desde la pantalla principal, se accede a la pantalla de registro. Se generan una dirección, una frase mnemotécnica y una clave privada para el usuario.
    
3.  **Interacción con el ChatBox**: En la pantalla principal, se puede interactuar con el ChatBox escribiendo comandos específicos como "/help" o "/block". La respuesta se mostrará en la etiqueta correspondiente.
    
4.  **Obtención de Saldo**: Es posible obtener el saldo en ETH de la dirección ingresada utilizando el comando "/balance" seguido de la dirección.
    
5.  **Consulta de Número de Bloque**: Se puede obtener el número de bloque actual utilizando el comando "/block_number".
    
6.  **Conceptos de Blockchain**: La aplicación proporciona información sobre conceptos clave de blockchain como Proof of Work ("/pof"), Proof of Stake ("/pos"), transacciones ("/transaction"), etc.
    

## Decisiones de Diseño

1.  **Kivy Framework**: Se eligió Kivy debido a su capacidad para crear interfaces de usuario atractivas y su soporte multiplataforma.
    
2.  **Uso de Imágenes**: Se incorporaron imágenes (giphy.gif) como fondo para mejorar la estética de la aplicación.
    
3.  **Gestión de Pantallas**: Se implementó un sistema de gestión de pantallas para facilitar la transición entre las distintas secciones de la aplicación.
    
4.  **Integración con Ethereum**: Se utilizó la biblioteca web3 para interactuar con nodos Ethereum a través de Infura y obtener información en tiempo real.
    

## Conclusión

La aplicación ChatBox ofrece una experiencia interactiva para aprender sobre conceptos de blockchain de una manera amigable. La combinación de Kivy y bibliotecas especializadas permite una interfaz gráfica intuitiva y funcionalidades específicas de blockchain. ¡Disfruta explorando el mundo de blockchain a través de ChatBox!