def classificar_fosforo(p, argila):
    if argila > 60:
        if p < 3:
            return "Muito baixo"
        elif p < 6:
            return "Baixo"
        elif p < 12:
            return "Médio"
        else:
            return "Alto"
    else:
        if p < 5:
            return "Muito baixo"
        elif p < 10:
            return "Baixo"
        elif p < 20:
            return "Médio"
        else:
            return "Alto"

def calcular_v(ca, mg, k, ctc):
    return ((ca + mg + k) / ctc) * 100

def interpretar(dados):
    classe_p = classificar_fosforo(dados["p"], dados["argila"])
    v = calcular_v(dados["ca"], dados["mg"], dados["k"], dados["ctc"])
    return f"P: {classe_p} | V%: {round(v,2)}"
