# Definición de la función de cifrado César que toma un texto y un valor de desplazamiento como entrada.
def cifrado_cesar(texto, desplazamiento):
    resultado = ""  # Variable para almacenar el texto cifrado.

    for caracter in texto:  # Itera a través de cada carácter en el texto de entrada.
        if caracter.isalpha():  # Verifica si el carácter es una letra del alfabeto.
            mayusculas = (
                "A" if caracter.isupper() else "a"
            )  # Determina si el carácter es mayúscula o minúscula.
            codigo_caracter = ord(caracter) - ord(
                mayusculas
            )  # Convierte el carácter a un número (0-25).
            codigo_caracter = (
                codigo_caracter + desplazamiento
            ) % 26  # Aplica el cifrado César con el desplazamiento.
            caracter_ofuscado = chr(
                codigo_caracter + ord(mayusculas)
            )  # Convierte el número cifrado de nuevo a carácter.
            resultado += caracter_ofuscado  # Agrega el carácter cifrado al resultado.
        else:
            resultado += caracter  # Si el carácter no es una letra, se agrega al resultado sin modificarlo.

    return resultado  # Devuelve el texto cifrado.


# Función principal del programa.
def main():
    texto_original = input(
        "Ingrese el texto a ofuscar: "
    )  # Solicita al usuario que ingrese el texto original.
    desplazamiento = int(
        input("Ingrese el valor de desplazamiento: ")
    )  # Solicita al usuario el valor de desplazamiento.

    texto_ofuscado = cifrado_cesar(
        texto_original, desplazamiento
    )  # Llama a la función de cifrado César.

    # Imprime el texto original y el texto cifrado.
    print("Texto Original: ", texto_original)
    print("Texto Ofuscado: ", texto_ofuscado)


# Comprueba si el script se ejecuta como programa principal.
if __name__ == "__main__":
    main()  # Llama a la función principal si se cumple la condición.
