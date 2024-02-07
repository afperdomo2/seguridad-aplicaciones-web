# biblioteca para realizar cifrado y descifrado de mensajes utilizando una clave simétrica
from cryptography.fernet import Fernet

# Generar una clave
key = Fernet.generate_key()

# Crear una instancia de Fernet
cipher_suite = Fernet(key)

# Cifrar un mensaje
# Se define un mensaje en forma de bytes b
message = b"Este es un mensaje secreto"

# El mensaje cifrado se almacena en la variable encrypted_message
encrypted_message = cipher_suite.encrypt(message)

# Descifrar el mensaje
# Se utiliza la misma instancia de Fernet para descifrar el mensaje cifrado
decrypted_message = cipher_suite.decrypt(encrypted_message)

# Imprimir los resultados
print("Mensaje original:", message)
print("Mensaje cifrado:", encrypted_message)
print("Mensaje descifrado:", decrypted_message)
