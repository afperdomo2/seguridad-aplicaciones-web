import json
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from datetime import datetime


# Función para cargar registros desde un archivo JSON
def cargar_registro_desde_json(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []


# Función para guardar registros en un archivo JSON
def guardar_en_json(nombre_archivo, registro):
    with open(nombre_archivo, "w") as archivo:
        json.dump(registro, archivo, indent=4)


# Función para generar una clave a partir de una contraseña utilizando PBKDF2HMAC
def generar_clave_desde_contraseña(contraseña):
    salt = b"salt_unico_y_random"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,
        backend=default_backend(),
    )
    clave_derivada = kdf.derive(contraseña.encode())
    return base64.urlsafe_b64encode(clave_derivada)


# Función para guardar datos en un archivo binario
def guardar_en_archivo(nombre_archivo, datos):
    with open(nombre_archivo, "ab") as archivo:
        archivo.write(datos + b"\n")  # Agrega el mensaje cifrado con un salto de línea


# Función para guardar datos en un archivo de texto
def guardar_en_archivo_texto(nombre_archivo, datos):
    with open(nombre_archivo, "a") as archivo:
        archivo.write(datos + "\n")  # Agrega el mensaje cifrado con un salto de línea


# Función para guardar el registro en un archivo JSON
def guardar_en_json(nombre_archivo, registro):
    with open(nombre_archivo, "w") as archivo:
        json.dump(registro, archivo, indent=4)


# Función para cifrar un mensaje, guardarlo y registrar la operación
def cifrar_y_guardar(contraseña, mensaje, registro):
    key = generar_clave_desde_contraseña(contraseña)
    cipher_suite = Fernet(key)

    encrypted_message = cipher_suite.encrypt(mensaje)

    # Obtener la fecha y hora actual
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Formatear el registro como una cadena de texto
    entrada = f"{fecha_hora} | Mensaje original: {mensaje.decode()} | Mensaje cifrado: {encrypted_message.decode()}"

    # Guardar en el archivo de registro de texto
    registro.append(entrada)
    guardar_en_archivo_texto("registro.txt", entrada)

    # Guardar en el archivo de registro JSON
    registro.append(
        {
            "Fecha y Hora": fecha_hora,
            "Mensaje Original": mensaje.decode(),
            "Mensaje Cifrado": encrypted_message.decode(),
        }
    )
    guardar_en_json("registro.json", registro)

    # Guardar el mensaje cifrado en un archivo separado
    guardar_en_archivo("mensaje_cifrado.txt", encrypted_message)


# Función para leer datos desde un archivo binario
def leer_desde_archivo(nombre_archivo):
    with open(nombre_archivo, "rb") as archivo:
        return archivo.read().splitlines()


# Función para descifrar un mensaje y mostrarlo
def descifrar_y_mostrar(contraseña):
    key = generar_clave_desde_contraseña(contraseña)
    cipher_suite = Fernet(key)

    encrypted_message_from_file = leer_desde_archivo("mensaje_cifrado.txt")[-1]

    try:
        decrypted_message = cipher_suite.decrypt(encrypted_message_from_file)
        print("Mensaje descifrado:", decrypted_message.decode())
    except Exception as e:
        print(f"Error al descifrar: {e}")


# Inicializar el registro cargando datos existentes desde el archivo JSON
registro = cargar_registro_desde_json("registro.json")

# Solicitar una contraseña al usuario para cifrar
contraseña_cifrado = input("Ingrese su contraseña para cifrar el mensaje: ")

# Solicitar un mensaje al usuario para cifrar
mensaje_a_cifrar = input("Ingrese el mensaje a cifrar: ")

# Cifrar el mensaje y guardar en archivos
cifrar_y_guardar(contraseña_cifrado, mensaje_a_cifrar.encode(), registro)

# Mostrar el mensaje cifrado por consola
encrypted_message_from_file = leer_desde_archivo("mensaje_cifrado.txt")[-1]
print("Mensaje cifrado:", encrypted_message_from_file.decode())

# Solicitar la contraseña al usuario para descifrar
contraseña_descifrado = input("Ingrese su contraseña para descifrar el mensaje: ")

# Descifrar el mensaje y mostrar
descifrar_y_mostrar(contraseña_descifrado)

# Guardar el registro actualizado en el archivo JSON
guardar_en_json("registro.json", registro)
