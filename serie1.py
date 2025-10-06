class AutomataPila:
    """
    Simulador de Autómata de Pila (Pushdown Automaton - PDA)
    
    P = {Q, Σ, Γ, q0, Z0, δ, F}
    Donde:
    - Q = {q0, q1, q2}: Conjunto de estados
    - Σ = {0, 1}: Alfabeto de entrada
    - Γ = {X, Z0}: Alfabeto de la pila
    - q0: Estado inicial
    - Z0: Símbolo inicial de la pila
    - δ: Función de transición
    - F = {q2}: Conjunto de estados finales
    """
    
    def __init__(self):
        # Definición de los componentes del autómata
        self.Q = {'q0', 'q1', 'q2'}  # Estados
        self.Sigma = {'0', '1'}       # Alfabeto de entrada
        self.Gamma = {'X', 'Z0'}      # Alfabeto de la pila
        self.q0 = 'q0'                # Estado inicial
        self.Z0 = 'Z0'                # Símbolo inicial de pila
        self.F = {'q2'}               # Estados finales
        
        # Función de transición δ
        # Formato: (estado_actual, símbolo_entrada, tope_pila) -> (nuevo_estado, lista_símbolos_a_apilar)
        # ε representa la cadena vacía (transición epsilon)
        # Los símbolos se apilan de izquierda a derecha, por lo que el último será el tope
        self.delta = {
            ('q0', '0', 'Z0'): ('q0', ['X', 'X', 'Z0']),    # Primer 0
            ('q0', '0', 'X'): ('q0', ['X', 'X', 'X']),      # Siguientes 0s
            ('q0', '1', 'X'): ('q1', []),                    # Primer 1
            ('q1', '1', 'X'): ('q1', []),                    # Siguientes 1s
            ('q1', 'ε', 'Z0'): ('q2', ['Z0'])                # Estado final
        }
    
    def simular(self, cadena):
        """
        Simula el procesamiento de una cadena por el autómata de pila
        
        Args:
            cadena: String de entrada compuesto por 0s y 1s
            
        Returns:
            bool: True si la cadena es aceptada, False en caso contrario
        """
        # Inicialización
        estado_actual = self.q0
        pila = [self.Z0]  
        indice = 0
        
        print(f"\n{'='*60}")
        print(f"Procesando cadena: '{cadena}'")
        print(f"{'='*60}")
        print(f"Estado inicial: {estado_actual}, Pila: {pila}")
        
        while indice <= len(cadena):
            if not pila:
                print(f"ERROR: Pila vacía en el índice {indice}")
                return False
                
            tope = pila[-1]  
            
            if indice >= len(cadena):
                break
            
            simbolo = cadena[indice]
            if (estado_actual, simbolo, tope) in self.delta:
                nuevo_estado, apilar = self.delta[(estado_actual, simbolo, tope)]
                print(f"Leyendo '{simbolo}': ({estado_actual}, {simbolo}, {tope}) -> ({nuevo_estado}, {''.join(apilar)})")
                pila.pop()  # Desapilar el tope
                pila.extend(reversed(apilar))  
                print(f"  Estado: {nuevo_estado}, Pila: {pila}")
                estado_actual = nuevo_estado
                indice += 1
                
                # Intentar transiciones epsilon después de cada movimiento
                tope = pila[-1] if pila else None
                while tope and (estado_actual, 'ε', tope) in self.delta:
                    nuevo_estado, apilar = self.delta[(estado_actual, 'ε', tope)]
                    print(f"Transición ε: ({estado_actual}, ε, {tope}) -> ({nuevo_estado}, {''.join(apilar)})")
                    pila.pop()
                    pila.extend(reversed(apilar))
                    print(f"  Estado: {nuevo_estado}, Pila: {pila}")
                    estado_actual = nuevo_estado
                    tope = pila[-1] if pila else None
            else:
                print(f"ERROR: No hay transición para ({estado_actual}, {simbolo}, {tope})")
                return False
    
        # Verificar si llegamos a un estado final
        aceptada = estado_actual in self.F
        
        print(f"\n{'='*60}")
        print(f"Estado final: {estado_actual}")
        print(f"Pila final: {pila}")
        print(f"¿Cadena aceptada? {'SÍ' if aceptada else 'NO'}")
        print(f"{'='*60}\n")
        
        return aceptada


# Funcion principal para probar el autómata
def main():
    pda = AutomataPila()
    
    print("\n" + "="*60)
    print("AUTÓMATA DE PILA - EJEMPLOS")
    print("="*60)
    
    # Ejemplos de cadenas a probar
    cadenas_prueba = [
        "0011",      # Aceptada: 2 ceros seguidos de 2 unos
        "000111",    # Aceptada: 3 ceros seguidos de 3 unos
        "01",        # Aceptada: 1 cero seguido de 1 uno
        "00001111",  # Aceptada: 4 ceros seguidos de 4 unos
        "001",       # Rechazada: más ceros que unos
        "0111",      # Rechazada: más unos que ceros
        "0101",      # Rechazada: intercalados (no en el lenguaje)
        "11",        # Rechazada: no comienza con 0
        "",          # Rechazada: cadena vacía
        "00",        # Rechazada: solo ceros
        "011"       # Aceptada: 1 cero y 2 unos
    ]
    
    # Probar cada cadena
    for cadena in cadenas_prueba:
        resultado = pda.simular(cadena)
        input("Presiona Enter para continuar...")
    
    # Deducción del lenguaje
    print("\n" + "="*60)
    print("="*60)
    print("""
Analizando las transiciones del autómata:

1. δ(q0, 0, Z0) = (q0, XXZ0): Por cada '0' leído, apilamos dos 'X'
2. δ(q0, 0, X) = (q0, XX): Continúa apilando dos 'X' por cada '0'
3. δ(q0, 1, X) = (q1, ε): Al leer '1', cambiamos a q1 y desapilamos un 'X'
4. δ(q1, 1, X) = (q1, ε): Por cada '1' en q1, desapilamos un 'X'
5. δ(q1, ε, Z0) = (q2, Z0): Cuando la pila tiene solo Z0, vamos a q2 (estado final)

CONCLUSIÓN:
El lenguaje aceptado es: L(P) = {0ⁿ1²ⁿ | n ≥ 1}

Es decir, cadenas que tienen:
- n ceros (0) seguidos de
- 2n unos (1)
- donde n es mayor o igual a 1

Este autómata reconoce cadenas donde el número de unos es exactamente
el doble del número de ceros, y todos los ceros aparecen antes que los unos.
    """)


if __name__ == "__main__":
    main()