import struct

# Constantes del formato — única fuente de verdad
FORMATO_REGISTRO = '<i32s16s40s'
TAM_REGISTRO     = struct.calcsize(FORMATO_REGISTRO)  # 92
TAM_NOMBRE       = 32
TAM_TELEFONO     = 16
TAM_EMAIL        = 40

def empaquetar_contacto(id, nombre, telefono, email):
    """Empaqueta un contacto en bytes con el formato del registro.

    Precondición: id es un int32 válido; nombre, telefono, email son str
                   cuyos equivalentes en UTF-8 caben en TAM_NOMBRE,
                   TAM_TELEFONO y TAM_EMAIL bytes respectivamente.
    Postcondición: devuelve un objeto bytes de exactamente TAM_REGISTRO.
    """
    nombre_b   = nombre.encode('utf-8')     # str → bytes
    telefono_b = telefono.encode('utf-8')
    email_b    = email.encode('utf-8')
    return struct.pack(FORMATO_REGISTRO, id, nombre_b, telefono_b, email_b)

def desempaquetar_contacto(datos):
    """Desempaqueta un registro de TAM_REGISTRO bytes en una tupla legible.

    Precondición: datos es un bytes de longitud TAM_REGISTRO.
    Postcondición: devuelve (id, nombre, telefono, email) con los campos
                   de texto convertidos a str UTF-8, sin los \\x00 de relleno.
    """
    id, nombre_b, telefono_b, email_b = struct.unpack(FORMATO_REGISTRO, datos)
    nombre   = nombre_b.rstrip(b'\x00').decode('utf-8')
    telefono = telefono_b.rstrip(b'\x00').decode('utf-8')
    email    = email_b.rstrip(b'\x00').decode('utf-8')
    return id, nombre, telefono, email

def leer_contacto(archivo, k):
    """Lee el registro k-ésimo del archivo y lo devuelve como tupla.

    Precondición: archivo está abierto en modo 'rb' o 'r+b'; k es un
                   índice válido (0 ≤ k < cantidad_registros).
    Postcondición: el cursor queda posicionado al final del registro leído;
                    devuelve (id, nombre, telefono, email).
    """
    archivo.seek(k * TAM_REGISTRO)       # posición del k-ésimo
    datos = archivo.read(TAM_REGISTRO)     # exactamente 92 bytes
    return desempaquetar_contacto(datos)

def crear_agenda(ruta, contactos):
    """Crea un archivo binario nuevo con los contactos indicados.

    Precondición: contactos es una lista de tuplas (id, nombre, telefono, email).
    Postcondición: el archivo en 'ruta' contiene len(contactos) registros
                    consecutivos de longitud fija. Si ya existía, se sobrescribe.
    """
    with open(ruta, 'wb') as archivo:      # 'wb': crea o sobrescribe
        for id, nombre, telefono, email in contactos:
            datos = empaquetar_contacto(id, nombre, telefono, email)
            archivo.write(datos)

def actualizar_email(ruta, k, email_nuevo):
    """Reemplaza el email del registro k-ésimo sin tocar los demás campos.

    Precondición: ruta apunta a un archivo válido; 0 ≤ k < cantidad.
    Postcondición: el registro k-ésimo queda con el nuevo email; los demás
                    registros del archivo no se modifican.
    """
    with open(ruta, 'r+b') as archivo:     # 'r+b': actualiza in situ
        id, nombre, telefono, _ = leer_contacto(archivo, k)
        datos = empaquetar_contacto(id, nombre, telefono, email_nuevo)
        archivo.seek(k * TAM_REGISTRO)            # volver a la posición del registro
        archivo.write(datos)                        # sobrescribe exactamente 92 bytes

if __name__ == '__main__':
    crear_agenda('agenda.bin', [
        (1, 'Alice', '555-1234', 'alice@example.com'),
        (2, 'Bob', '555-5678', 'bob@example.com'),
        (3, 'Charlie', '555-9012', 'charlie@example.com'),
        (4, 'David', '555-3456', 'david@example.com'),
    ])

    actualizar_email('agenda.bin', 1, 'bob.new@example.com')

    with open('agenda.bin', 'rb') as archivo:
        for k in range(4):
            print(leer_contacto(archivo, k))
