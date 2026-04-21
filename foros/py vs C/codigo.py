# Ejemplo en Python
def modificar_entero(n):
    n = 99  # Reasignación: crea una referencia local a un nuevo objeto.

def modificar_lista(datos):
    datos.append(99)  # Mutación in-place: actúa sobre la misma dirección de memoria.

# Pruebas
numero = 10
modificar_entero(numero)
print(numero)  # Salida: 10 (El inmutable no cambia)

lista = [10]
modificar_lista(lista)
print(lista)   # Salida: [10, 99] (El mutable sufre el efecto secundario)