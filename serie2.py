
# Gramática original: S -> 0 S 1 | 1 S 0 | ε
# GNF equivalente usada:
#   S -> 0 S B | 1 S A | ε
#   A -> 0
#   B -> 1

from collections import deque
import argparse
from typing import List, Tuple, Dict

# ---------- 1) Gramática en GNF ----------
def gnf_grammar():
    G = {
        "S": [("0", ["S", "B"]), ("1", ["S", "A"]), ("", [])],
        "A": [("0", [])],
        "B": [("1", [])],
    }
    return G

def print_gnf(G):
    def rhs_to_str(t, vars_):
        if t == "":
            return "ε"
        return t + (" " + " ".join(vars_) if vars_ else "")
    for V in ["S", "A", "B"]:
        prods = G[V]
        rhs = " | ".join(rhs_to_str(t, vs) for (t, vs) in prods)
        print(f"{V} -> {rhs}")

# ---------- 2) PDA a partir de GNF ----------
class NPDA:
    def __init__(self, G: Dict[str, List[Tuple[str, List[str]]]], start_var="S", bottom_symbol="$"):
        self.G = G
        self.start_var = start_var
        self.bottom = bottom_symbol

    def _initial_stack(self) -> List[str]:
        return [self.bottom, self.start_var]

    def accepts(self, w: str, max_steps: int = 20000) -> bool:
        start_conf = (0, tuple(self._initial_stack()))
        Q = deque([start_conf])
        seen = set([start_conf])
        steps = 0

        while Q:
            pos, stack = Q.popleft()
            steps += 1
            if steps > max_steps:
                return False

            stack = list(stack)

            if pos == len(w) and stack == [self.bottom]:
                return True

            if not stack:
                continue

            top = stack.pop()

            if top in self.G:
                if pos < len(w):
                    a = w[pos]
                    for (t, alphas) in self.G[top]:
                        if t != "" and t == a:
                            new_stack = stack.copy()
                            for sym in reversed(alphas):
                                new_stack.append(sym)
                            conf = (pos + 1, tuple(new_stack))
                            if conf not in seen:
                                seen.add(conf)
                                Q.append(conf)
                for (t, alphas) in self.G[top]:
                    if t == "" and not alphas:
                        conf = (pos, tuple(stack))
                        if conf not in seen:
                            seen.add(conf)
                            Q.append(conf)

        return False

# ---------- 3) Ejemplos ----------
def generate_examples() -> List[str]:
    base = ["", "01", "10", "0011", "1100", "0110", "1001", "0101", "1010"]
    out = base + ["0", "1", "000", "111", "001", "010", "101", "011", "0100"]
    return out

def main():
    parser = argparse.ArgumentParser(description="Forma normal de Greibach y PDA para S -> 0S1 | 1S0 | ε")
    parser.add_argument("--show-gnf", action="store_true", help="Muestra la gramática en GNF.")
    parser.add_argument("--check", nargs="*", help="Verifica cadenas específicas (usa ε para cadena vacía).")
    parser.add_argument("--demo", action="store_true", help="Ejecuta una demostración con ejemplos típicos.")
    args = parser.parse_args()

    G = gnf_grammar()
    if args.show_gnf:
        print("Gramática en GNF equivalente:")
        print_gnf(G)
        print()

    pda = NPDA(G)

    if args.demo:
        samples = generate_examples()
        print("=== DEMO ===")
        for s in samples:
            print(f"Input: '{s or 'ε'}' ->", "ACEPTADA" if pda.accepts(s) else "RECHAZADA")

    if args.check is not None:
        for s in args.check:
            if s == "ε":
                s = ""
            ok = pda.accepts(s)
            print(f"Input: '{s or 'ε'}' ->", "ACEPTADA" if ok else "RECHAZADA")

if __name__ == "__main__":
    main()
