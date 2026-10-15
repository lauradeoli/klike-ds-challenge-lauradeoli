def comparar_atributo(dados, atributo, metrica, atual, alternativa):
    df = dados.groupby(['platform', atributo], observed=True)[metrica].agg(['count', 'median'])
    grupo_atual = df.xs(atual, level=atributo)['median']
    grupo_alternativa = df.xs(alternativa, level=atributo)['median']
    diferenca_pct = ((grupo_alternativa - grupo_atual) / grupo_atual) * 100
    return diferenca_pct

