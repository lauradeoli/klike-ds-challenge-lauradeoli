def comparar_atributo(dados, atributo, metrica, atual, alternativa):
    df = dados.groupby(['platform', atributo], observed=True)[metrica].agg(['count', 'median'])
    grupo_atual = df.xs(atual, level=atributo)['median']
    grupo_alternativa = df.xs(alternativa, level=atributo)['median']
    diferenca_pct = ((grupo_alternativa - grupo_atual) / grupo_atual) * 100
    return diferenca_pct

def melhor_alternativa(dados, plataforma, atributo, metrica, valor_atual):
    df = dados[dados['platform'] == plataforma]
    resumo = df.groupby(atributo, observed=True)[metrica].agg(['count', 'median'])
    # Considera só grupos com pelo menos 10 campanhas
    resumo = resumo[resumo['count'] >= 10]

    if valor_atual not in resumo.index:
        return None

    mediana_atual = resumo.loc[valor_atual, 'median']
    # Remove a categoria atual das alternativas
    alternativas = resumo.drop(index=valor_atual)

    if alternativas.empty or mediana_atual <= 0:
        return None

    # Seleciona alternativa com maior mediana
    melhor_valor = alternativas['median'].idxmax()
    melhor_mediana = alternativas.loc[melhor_valor, 'median']

    diferenca_pct = (melhor_mediana - mediana_atual) / mediana_atual * 100

    if diferenca_pct <= 0:
        return None

    return {'atributo': atributo, 'valor_atual': valor_atual, 'valor_recomendado': melhor_valor, 
            'metrica': metrica, 'diferenca_pct': diferenca_pct}