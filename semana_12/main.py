from modulo_1 import crear_archivo_paciente
from modulo_2 import construir_indices, buscar_por_dni
from modulo_3 import listar_pacientes_ordenados
from modulo_4 import asignar_agenda
import binario
import random

def main():
    ruta_archivo = "pacientes.bin"
    
    # 1. Crear archivo de pacientes con datos simulados
    datos_crudos = binario.generar_datos_aleatorios(50)
    pacientes_prueba = []
    for dni, apellido, nombre, telefono, prioridad in datos_crudos:
        pacientes_prueba.append({
            "dni": dni,
            "apellido": apellido,
            "nombre": nombre,
            "telefono": telefono,
            "prioridad": prioridad
        })
        
    try:
        crear_archivo_paciente(ruta_archivo, pacientes_prueba)
        print("Archivo de pacientes creado con éxito.")
    except Exception as e:
        print(f"Aviso - Módulo 1 incompleto o error al crear archivo: {e}")

    # 2. Construir los índices en memoria
    try:
        indice_por_dni, indice_por_apellido = construir_indices(ruta_archivo)
        print("Índices construidos con éxito.")
    except Exception as e:
        print(f"Aviso - Módulo 2 incompleto o error al construir índices: {e}")
        indice_por_dni = {}
        indice_por_apellido = {}

    # 3. Menú interactivo principal
    while True:
        print("\n=== Consultorio Médico ===")
        print("1. Buscar paciente por DNI")
        print("2. Listar pacientes ordenados por Apellido")
        print("3. Listar pacientes ordenados por Prioridad")
        print("4. Resolver agenda del día")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            try:
                dni = int(input("Ingrese el DNI a buscar: "))
                
                # Pasamos directamente la ruta; leer_paciente (Módulo 1) se encarga de abrirlo
                paciente = buscar_por_dni(ruta_archivo, indice_por_dni, dni)
                if paciente:
                    print(f"Paciente encontrado: {paciente}")
                else:
                    print("Paciente no encontrado.")
            except ValueError:
                print("El DNI ingresado no es válido.")
            except Exception as e:
                print(f"Error durante la búsqueda: {e}")
                
        elif opcion == "2":
            try:
                pacientes_ord = listar_pacientes_ordenados(ruta_archivo, "apellido")
                print("\nPacientes ordenados por Apellido:")
                for p in pacientes_ord:
                    print(f"- {p['apellido']}, {p['nombre']} (Prioridad: {p['prioridad']})")
            except Exception as e:
                print(f"Error al listar: {e}")
                
        elif opcion == "3":
            try:
                pacientes_ord = listar_pacientes_ordenados(ruta_archivo, "prioridad")
                print("\nPacientes ordenados por Prioridad:")
                for p in pacientes_ord:
                    print(f"- [Prioridad {p['prioridad']}] {p['apellido']}, {p['nombre']}")
            except Exception as e:
                print(f"Error al listar: {e}")
                
        elif opcion == "4":
            # Tomamos 3 pacientes al azar (asegurando apellidos distintos) para la agenda
            apellidos_unicos = list(set([p["apellido"] for p in pacientes_prueba]))
            pacientes_del_dia = random.sample(apellidos_unicos, 3)
            franjas = ["08:00", "08:30", "09:00", "09:30", "10:00"]
            
            disponibilidad = {}
            for pac in pacientes_del_dia:
                disponibilidad[pac] = random.sample(franjas, random.randint(2, 3))
                
            print(f"\nPacientes del día: {pacientes_del_dia}")
            print(f"Disponibilidad generada: {disponibilidad}")
            
            asignacion = asignar_agenda(pacientes_del_dia, franjas, disponibilidad)
            if asignacion:
                print("\nAgenda asignada con éxito:")
                for franja, paciente in sorted(asignacion.items()): # sorted para ordenarlas cronológicamente
                    print(f"  {franja} hs -> Paciente: {paciente}")
            else:
                print("\nNo se pudo encontrar una asignación válida con las restricciones dadas.")
                
        elif opcion == "5":
            print("Saliendo del sistema de turnos. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
