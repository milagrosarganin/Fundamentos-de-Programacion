def asignar_agenda(pacientes_del_dia, franjas, disponibilidad):
    """
    Asigna una franja horaria a cada paciente usando backtracking.
    
    Precondición: 
    - pacientes_del_dia es una lista de identificadores (ej. apellidos).
    - franjas es una lista de franjas horarias disponibles.
    - disponibilidad es un diccionario: paciente -> lista de franjas compatibles.
    
    Postcondición:
    - Devuelve un diccionario {franja: paciente} válido, o None si no hay solución.
    """
    def _backtrack(indice_paciente, asignacion):
        # Caso base: todos los pacientes fueron asignados exitosamente
        if indice_paciente == len(pacientes_del_dia):
            return asignacion.copy()
            
        paciente = pacientes_del_dia[indice_paciente]
        franjas_disponibles = disponibilidad.get(paciente, [])
        
        for franja in franjas_disponibles:
            # Poda: verificamos que la franja exista y no esté ya ocupada por otro paciente
            if franja in franjas and franja not in asignacion:
                # 1. Hacer la asignación
                asignacion[franja] = paciente
                
                # 2. Recurrir al siguiente paciente
                resultado = _backtrack(indice_paciente + 1, asignacion)
                if resultado is not None:
                    return resultado
                    
                # 3. Deshacer la asignación (Backtracking)
                del asignacion[franja]
                
        return None

    return _backtrack(0, {})

def probar_casos_modulo_4():
    """Ejecuta los casos de prueba para el módulo 4 y muestra la discusión."""
    print("--- CASO 1: CON SOLUCIÓN ---")
    pacientes_1 = ["Pérez", "Gómez", "López"]
    franjas = ["08:00", "08:30", "09:00", "09:30"]
    disp_1 = {"Pérez": ["08:00", "08:30"], "Gómez": ["08:30", "09:00"], "López": ["08:00", "09:30"]}
    print("Resultado:", asignar_agenda(pacientes_1, franjas, disp_1))
    
    print("\n--- CASO 2: SOBRE-RESTRINGIDO (SIN SOLUCIÓN) ---")
    disp_2 = {"Pérez": ["08:00"], "Gómez": ["08:00"], "López": ["08:00"]}
    print("Resultado:", asignar_agenda(pacientes_1, franjas, disp_2))
    
    print("\n--- DISCUSIÓN (Pregunta h) ---")
    print("Fuerza bruta: Para 'P' pacientes y 'F' franjas, sin considerar disponibilidad,")
    print("habría que explorar F^P posibles asignaciones en el peor caso. Con 3 pacientes")
    print("y 4 franjas, esto es 4^3 = 64 combinaciones posibles completas.")
    print("Poda: Al restringir el ciclo 'for' solo a las franjas disponibles de cada")
    print("paciente, y descartar inmediatamente las ya ocupadas, evitamos la construcción")
    print("de ramas enteras del árbol. Si un paciente tiene solo 1 franja libre,")
    print("la poda reduce instantáneamente sus opciones a 1, acelerando el algoritmo.")

if __name__ == "__main__":
    probar_casos_modulo_4()