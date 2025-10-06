# Para correr el programa usar los siguentes comandos
# python serie3.py
# python serie3.py aabbccdd
# python serie3.py aabbccdd --trace



# PDA para L2 = { a^i b^i c^j d^j : i,j >= 1 }
# Acepta por pila en estado base Z0 tras consumir toda la entrada.

from typing import List, Tuple

class PDA_L2:
    def __init__(self, trace: bool = False):
        # Definición “conceptual”:
        # Q = {q0, q1, q2}, Σ = {a,b,c,d}, Γ = {A,B,Z0}, q0 = q0, Z0 = Z0, F = {q2}
        self.state = 'q0'
        self.stack: List[str] = ['Z0']
        self.trace = trace
        self.seen_a = 0
        self.seen_b = 0
        self.seen_c = 0
        self.seen_d = 0

    def _log(self, ch: str):
        if self.trace:
            print(f"[state={self.state:>2}] read='{ch}'  stack={self.stack}")

    def step(self, ch: str) -> bool:
        self._log(ch)

        if self.state == 'q0':
            if ch == 'a':
                self.stack.append('A')
                self.seen_a += 1
                return True
            elif ch == 'b' and self.stack and self.stack[-1] == 'A' and self.seen_a > 0:
                self.stack.pop()
                self.state = 'q1'
                self.seen_b += 1
                return True
            else:
                return False

        if self.state == 'q1':
            if ch == 'b' and self.stack and self.stack[-1] == 'A':
                self.stack.pop()
                self.seen_b += 1
                return True
            elif ch == 'c' and self.seen_b == self.seen_a and self.seen_b > 0:
                self.state = 'q2'
                self.stack.append('B')
                self.seen_c += 1
                return True
            else:
                return False

        if self.state == 'q2':
            if ch == 'c':
                self.stack.append('B')
                self.seen_c += 1
                return True
            elif ch == 'd' and self.stack and self.stack[-1] == 'B':
                self.stack.pop()
                self.seen_d += 1
                return True
            else:
                return False

        return False

    def accept(self, w: str) -> Tuple[bool, str]:
        if not w or any(ch not in 'abcd' for ch in w):
            return (False, "Caracter no válido (solo a,b,c,d).")
        if w[0] != 'a':
            return (False, "Debe iniciar con 'a'.")
        if 'ba' in w or 'cb' in w or 'dc' in w or 'da' in w or 'ca' in w or 'db' in w:
            return (False, "Orden inválido: debe ser a* b* c* d* con bloques en ese orden.")

        for ch in w:
            if not self.step(ch):
                return (False, f"Transición inválida en estado {self.state} con '{ch}' y pila {self.stack}.")

        # Condiciones de aceptación:
        # - Haber visto al menos un símbolo de cada pareja
        # - Igualdad de a y b; igualdad de c y d
        # - Pila en base (Z0) tras consumir todo
        ok_pairs = (self.seen_a == self.seen_b and self.seen_c == self.seen_d)
        ok_min = (self.seen_a >= 1 and self.seen_b >= 1 and self.seen_c >= 1 and self.seen_d >= 1)
        ok_stack = (self.stack == ['Z0'])
        ok_state = (self.state == 'q2')

        accepted = ok_pairs and ok_min and ok_stack and ok_state
        if accepted:
            return (True, "Cadena aceptada.")
        else:
            why = []
            if not ok_pairs: why.append("conteos no coinciden (a=b, c=d).")
            if not ok_min:  why.append("se requiere ≥1 de cada símbolo.")
            if not ok_stack: why.append("pila no regresó a Z0.")
            if not ok_state: why.append("no terminó en fase c/d (q2).")
            return (False, " ".join(why) if why else "Rechazada.")

def simulate(w: str, trace: bool = False) -> None:
    pda = PDA_L2(trace=trace)
    ok, msg = pda.accept(w)
    print(f"Input: {w!r} -> {'ACEPTADA' if ok else 'RECHAZADA'} | {msg}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        tests_ok = [
            "abcd", "aabbccdd", "aaabbbcccddd",
        ]
        tests_bad = [
            "", "a", "ab", "abc", "aabbd",      # faltan bloques
            "aaabbbccdddd",                      # c != d
            "aaabbbbcccddd",                     # a != b
            "aabbbccdd",                         # a != b
            "aabbcccdd",                         # c != d
            "ba", "abca", "abbc", "aacbbccdd",   # orden inválido
        ]
        print("=== PRUEBAS ESPERADAS COMO ACEPTADAS ===")
        for t in tests_ok:
            simulate(t, trace=False)
        print("\n=== PRUEBAS ESPERADAS COMO RECHAZADAS ===")
        for t in tests_bad:
            simulate(t, trace=False)
        print("\nUsa:  python serie3.py aabbccdd   (agrega --trace para ver la pila)")
    else:
        word = sys.argv[1]
        trace = ("--trace" in sys.argv[2:])
        simulate(word, trace=trace)
