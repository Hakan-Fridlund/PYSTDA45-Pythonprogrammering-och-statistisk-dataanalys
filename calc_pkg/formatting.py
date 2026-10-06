# `formatting.py` ska innehålla en funktion 
# `pretty(op, a, b, result)` som returnerar en sträng, t.ex. `"3 * 7 = 21"` (op = +, -, *, / eller //).

def pretty(op, a, b, result):
    operators = "+-*/"
    if op not in operators:
        return ("unknown operator")
    else:
        return(f"{a} {op} {b} = {result}")