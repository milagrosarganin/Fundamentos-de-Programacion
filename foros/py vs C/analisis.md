# Foro "paso de argumentos a funciones por valor y por referencia en distintos lenguajes

### Para esta actividad, decidí contrastar el modelo de paso de argumentos de Python con el de C, ya que expone muy bien cómo cada lenguaje abstrae el manejo de la memoria.

## El Modelo de Python (Paso por Asignación / Referencia a Objetos)
    En Python, todo es un objeto que vive en el Heap, y las variables son referencias en el Stack. Al pasar un argumento a una función, se copia esa referencia. El comportamiento final depende de la mutabilidad del objeto.


## El Modelo de C (Paso por Valor Estricto)
    A diferencia de Python, C copia el valor físico de la variable. Si pasamos un entero, se hace una copia aislada en el nuevo Stack Frame. Para lograr el efecto de "modificar el original" (como hace Python con las listas), en C estamos obligados a pasar explícitamente la dirección de memoria usando punteros (* y &).


## Conclusión y Contraste

    Lo que en Python ocurre de forma "invisible" mediante el aliasing de objetos mutables, en C requiere manejo explícito de la memoria. Python simplifica la sintaxis, pero esto nos obliga a ser sumamente cuidadosos documentando los efectos secundarios, ya que una simple función puede alterar estructuras de datos completas en el entorno global si no usamos copias profundas.

## Información

    En python usé listas, en C existen los arrays los cuales también son mutables pero no tan libremente, ya que cuando se crean se les da un tamaño fijo y solo pueden tener todos sus datos int o todos floats.