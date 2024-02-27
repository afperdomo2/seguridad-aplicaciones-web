from cryptography.fernet import Fernet

# Genera una clave de cifrado aleatoria
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Mensaje a cifrar
mensaje_original = "¡Hola, mundo!"

# Cifrar el mensaje
mensaje_cifrado = cipher_suite.encrypt(mensaje_original.encode())

# Descifrar el mensaje
mensaje_descifrado = cipher_suite.decrypt(mensaje_cifrado).decode()

# Imprimir resultados
print("Mensaje Original:", mensaje_original)
print("Mensaje Cifrado:", mensaje_cifrado)
print("Mensaje Descifrado:", mensaje_descifrado)
