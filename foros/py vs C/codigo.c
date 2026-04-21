#include <stdio.h>

// Paso por valor: copia aislada en el Stack
void intentar_modificar(int n) {
    n = 99; 
}

// Paso de puntero: acceso explícito a la memoria original
void modificar_real(int *p) {
    *p = 99; // Desreferenciación: modifica el valor en esa dirección
}

int main() {
    int numero = 10;
    
    intentar_modificar(numero);
    printf("Paso por valor: %d\n", numero); // Salida: 10 (Intacto)
    
    // Le pasamos la dirección de memoria (&) de la variable
    modificar_real(&numero);
    printf("Paso por puntero: %d\n", numero); // Salida: 99 (Modificado)
    
    return 0;
}