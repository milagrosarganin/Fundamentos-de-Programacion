import os
import random
from Problema_3 import (
    binario_a_jsonl, 
    jsonl_a_binario, 
    procesar_streaming, 
    binario_a_json_indentado
)
from Problema_2 import crear_agenda

def generar_agenda_prueba(ruta, cantidad):
    """Genera un archivo binario de prueba con datos sintéticos."""
    contactos = []
    dominios = ["example.com", "fi.uba.ar", "gmail.com"]
    for i in range(cantidad):
        id_contacto = i + 1
        nombre = f"Contacto_{i:05d}"
        telefono = f"11-4000-{random.randint(1000, 9999)}"
        email = f"user{i:05d}@{random.choice(dominios)}"
        contactos.append((id_contacto, nombre, telefono, email))
        
    crear_agenda(ruta, contactos)

if __name__ == "__main__":
    random.seed(42) # Requerido por la consigna
    ARCHIVO_BIN = "agenda_10k.bin"
    ARCHIVO_JSONL = "agenda_10k.jsonl"
    ARCHIVO_JSON = "agenda_10k.json"
    ARCHIVO_RESTAURADO = "agenda_restaurada.bin"

    print("1. Generando agenda binaria de 10.000 contactos...")
    generar_agenda_prueba(ARCHIVO_BIN, 10000)

    print("2. Ejecutando migraciones...")
    binario_a_jsonl(ARCHIVO_BIN, ARCHIVO_JSONL)
    jsonl_a_binario(ARCHIVO_JSONL, ARCHIVO_RESTAURADO)
    binario_a_json_indentado(ARCHIVO_BIN, ARCHIVO_JSON)

    print("3. Probando procesamiento streaming...")
    cantidad = procesar_streaming(ARCHIVO_JSONL, "example.com")
    print(f"   -> Contactos con dominio @example.com: {cantidad}")

    print("\n--- COMPARACIÓN DE TAMAÑOS ---")
    tamaños = {
        "Binario (struct)": os.path.getsize(ARCHIVO_BIN),
        "JSON Lines": os.path.getsize(ARCHIVO_JSONL),
        "JSON plano (indent=2)": os.path.getsize(ARCHIVO_JSON)
    }

    for formato, bytes_size in tamaños.items():
        kb_size = bytes_size / 1024
        print(f"{formato.ljust(25)}: {bytes_size} bytes ({kb_size:.2f} KB)")