import struct
import random

# Configuración del formato binario (Registro de tamaño fijo)
FORMATO = '=i20s20s15si'
NOMBRE_ARCHIVO = 'datos_50.bin'

def generar_datos_aleatorios(cantidad):
    nombres = [
        "Milagros", "Tomi", "Camila", "Santiago", "Renata", "Juan", "Maria", 
        "Carlos", "Lucia", "Pedro", "Ana", "Diego", "Sofia", "Facundo", "Micaela", 
        "Joaquin", "Valentina", "Mateo", "Martina", "Lucas", "Florencia", "Agustin"
    ]
    apellidos = [
        "Arganin", "Oroz", "Berho", "Gomez", "Lopez", "Rodriguez", "Fernandez", 
        "Perez", "Gonzalez", "Martinez", "Sanchez", "Romero", "Sosa", "Torres", 
        "Ramirez", "Ruiz", "Benitez", "Acosta", "Medina", "Herrera", "Gimenez"
    ]
    
    registros = []
    dnis_usados = set()
    
    while len(registros) < cantidad:
        # Generar DNI único
        dni = random.randint(20000000, 50000000)
        if dni in dnis_usados:
            continue
        dnis_usados.add(dni)
        
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        # Generar un número de teléfono ficticio de Buenos Aires
        telefono = f"11{random.randint(10000000, 99999999)}"
        prioridad = random.randint(1, 3)
        
        registros.append((dni, apellido, nombre, telefono, prioridad))
        
    return registros

def crear_archivo_50():
    registros = generar_datos_aleatorios(50)
    
    print(f"Creando archivo binario '{NOMBRE_ARCHIVO}' con 50 registros...")
    with open(NOMBRE_ARCHIVO, 'wb') as f:
        for dni, apellido, nombre, telefono, prioridad in registros:
            # Preparar los strings convirtiéndolos a bytes con tamaño fijo
            ap_bytes = apellido.encode('utf-8')[:20].ljust(20, b'\x00')
            nom_bytes = nombre.encode('utf-8')[:20].ljust(20, b'\x00')
            tel_bytes = telefono.encode('utf-8')[:15].ljust(15, b'\x00')
            
            # Empaquetar los datos estructurados
            bloque_binario = struct.pack(FORMATO, dni, ap_bytes, nom_bytes, tel_bytes, prioridad)
            f.write(bloque_binario)
    print("¡Archivo de 50 personas creado con éxito!\n")

def leer_archivo_50():
    print(f"Leyendo contenido de '{NOMBRE_ARCHIVO}':")
    tamano_registro = struct.calcsize(FORMATO)
    contador = 0
    
    try:
        with open(NOMBRE_ARCHIVO, 'rb') as f:
            while True:
                bytes_leidos = f.read(tamano_registro)
                if not bytes_leidos or len(bytes_leidos) < tamano_registro:
                    break
                
                # Desempaquetar los bytes estructurados
                dni, ap_bytes, nom_bytes, tel_bytes, prioridad = struct.unpack(FORMATO, bytes_leidos)
                
                # Decodificar quitando los bytes nulos (\x00) de relleno
                apellido = ap_bytes.decode('utf-8').strip('\x00')
                nombre = nom_bytes.decode('utf-8').strip('\x00')
                telefono = tel_bytes.decode('utf-8').strip('\x00')
                
                contador += 1
                print(f"{contador:02d} | DNI: {dni} | Nombre: {apellido:10}, {nombre:10} | Tel: {telefono} | Prioridad: {prioridad}")
                
        print(f"\nTotal de registros leídos: {contador}")
    except FileNotFoundError:
        print("El archivo no existe.")

if __name__ == '__main__':
    crear_archivo_50()
    leer_archivo_50()