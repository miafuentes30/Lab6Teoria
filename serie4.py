# serie4.py
# Verificación computacional (estilo "pumping lemma checker") para:
# L5 = { 0^k 1^k 2^k : k >= 0 }
# Objetivo: dado un p, probar empíricamente que s = 0^p 1^p 2^p es un testigo:
# para toda descomposición uvxyz con |vxy|<=p y |vy|>0, existe i (0 o 2) tal que u v^i x y^i z ∉ L5.

from typing import List, Tuple
import argparse

def in_L5(w: str) -> bool:
    # Debe ser 0^a 1^b 2^c con a=b=c.
    i = 0
    n = len(w)
    while i < n and w[i] == '0':
        i += 1
    a = i
    j = i
    while j < n and w[j] == '1':
        j += 1
    b = j - i
    k = j
    while k < n and w[k] == '2':
        k += 1
    c = k - j
    # Debe consumir todo y tener a=b=c
    return k == n and a == b == c

def all_decompositions(s: str, p: int):
    # Genera todas las 5-particiones s = u v x y z con |vxy| <= p y |vy| > 0
    n = len(s)
    for a in range(0, n+1):
        b_limit = min(n, a + p)  # vxy debe quedar dentro de una ventana de tamaño <= p
        for b in range(a, b_limit+1):          # corte después de v
            for c in range(b, b_limit+1):      # corte después de x
                for d in range(c, b_limit+1):  # corte después de y
                    u, v, x, y, z = s[:a], s[a:b], s[b:c], s[c:d], s[d:]
                    if len(v) + len(y) == 0:
                        continue  # requiere |vy| > 0
                    yield (u, v, x, y, z)

def pump(u: str, v: str, x: str, y: str, z: str, i: int) -> str:
    return u + v * i + x + y * i + z

def witness_for_p(p: int, try_i_values=(0, 2), verbose=False) -> Tuple[bool, Tuple[str, Tuple[str, str, str, str, str]]]:
    """Devuelve (ok, counter) donde:
       ok=True  si s=0^p1^p2^p funciona (todas las descomposiciones rompen L5 con algún i en try_i_values)
       ok=False si se encontró una descomposición que NO se puede romper con esos i (sería muy raro teóricamente)
    """
    s = "0"*p + "1"*p + "2"*p
    assert in_L5(s), "El testigo debe pertenecer a L5"

    for dec in all_decompositions(s, p):
        u, v, x, y, z = dec
        # ¿Existe un i elegido que rompa la pertenencia?
        broken = False
        for i in try_i_values:
            w = pump(u, v, x, y, z, i)
            if not in_L5(w):
                broken = True
                if verbose:
                    print(f"[OK] Descomp. rompe con i={i}:")
                    print(f"     u='{u}', v='{v}', x='{x}', y='{y}', z='{z}'")
                    print(f"     bombeado -> '{w[:60] + ('...' if len(w)>60 else '')}'  ∉ L5")
                break
        if not broken:
            # Esta descomposición no se rompió con los i probados
            return (False, (s, dec))
    return (True, (s, ("", "", "", "", "")))

def explain_reasoning():
    msg = """
Idea (coincide con la prueba teórica):
Sea p el largo de bombeo. Tomamos s = 0^p 1^p 2^p ∈ L5.
En cualquier descomposición s = u v x y z con |vxy| ≤ p y |vy| > 0,
el bloque vxy queda contenido a lo sumo en dos de los tres segmentos consecutivos (0^p)(1^p)(2^p).

Casos:
1) v y/o y están totalmente dentro de un mismo bloque (solo 0s o solo 1s o solo 2s):
   - Bombear con i=0 o i=2 desbalancea las cantidades y rompe a=b=c, luego sale de L5.

2) vxy cruza exactamente un límite entre bloques (por ejemplo, 0^p|1^p):
   - Al bombear, cambian dos bloques adyacentes en distinta medida (p. ej., 0s y 1s), 
     pero el tercero permanece igual (2s). Nuevamente, se rompe a=b=c.

Como este razonamiento vale para toda descomposición válida, L5 NO es CFL por el Lema de Bombeo.
"""
    print(msg)

def main():
    parser = argparse.ArgumentParser(description="Comprobación empírica del Lema de Bombeo para L5 = {0^k1^k2^k}.")
    parser.add_argument("--p", type=int, default=6, help="Supuesto largo de bombeo p (por defecto 6).")
    parser.add_argument("--trace", action="store_true", help="Muestra descomposiciones que se rompen (verbose).")
    parser.add_argument("--reason", action="store_true", help="Imprime el esquema del argumento teórico.")
    args = parser.parse_args()

    if args.reason:
        explain_reasoning()

    ok, info = witness_for_p(args.p, try_i_values=(0, 2), verbose=args.trace)
    s, dec = info
    print(f"Testigo elegido: s = 0^{args.p} 1^{args.p} 2^{args.p} (longitud {len(s)})")
    if ok:
        print("Resultado: Para TODA descomposición válida, existe i∈{0,2} tal que el bombeo NO pertenece a L5.")
        print("Conclusión (consistente con la teoría): L5 NO es un lenguaje libre de contexto.")
    else:
        u, v, x, y, z = dec
        print("Advertencia: se halló una descomposición que no se rompió con i∈{0,2} (inusual).")
        print("Descomposición:", f"u='{u}', v='{v}', x='{x}', y='{y}', z='{z}'")

if __name__ == "__main__":
    main()
