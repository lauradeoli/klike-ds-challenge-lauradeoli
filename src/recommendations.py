# Funções ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

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

    if isinstance(valor_atual, bool) and isinstance(melhor_valor, bool):
        valor_atual = bool(valor_atual)
        melhor_valor = bool(melhor_valor)

    if diferenca_pct <= 0:
        return None

    return {'atributo': atributo, 'valor_atual': valor_atual, 'valor_recomendado': melhor_valor, 
            'metrica': metrica, 'diferenca_pct': float(diferenca_pct), 'mediana_atual': float(mediana_atual),
            'mediana_alternativa': float(melhor_mediana), 'n_atual': int(resumo.loc[valor_atual, 'count']),
            'n_alternativa': int(resumo.loc[melhor_valor, 'count'])}

def metrica_por_objetivo(objetivo):
    metricas_por_objetivo = {
    "traffic": "ctr",
    "engagement": "engagement_rate",
    "conversions": "roas",
    "awareness": "watch_time_ratio",
    "app_install": "conversion_rate"}
    return metricas_por_objetivo[objetivo]

def gerar_candidatas(campanha, dados):
    candidatas = []
    # Identificar a métrica principal da campanha
    metrica_principal = metrica_por_objetivo(campanha['objective'])
    metricas = ['ctr', 'conversion_rate', 'roas', 'watch_time_ratio', 'engagement_rate']
    metricas_ordenadas = [metrica_principal] + [m for m in metricas if m != metrica_principal]

    # Percorrer métricas e atributos modificáveis
    atributos = ["has_hook", "has_cta", "has_face", "has_subtitle", "text_density", "duration_group", "audio_group", "format"]
    for atributo in atributos:
        if pd.isna(campanha[atributo]):
            continue
        for metrica in metricas_ordenadas:
            resultado = melhor_alternativa(dados=dados, plataforma=campanha['platform'], atributo=atributo, metrica=metrica, 
                                                         valor_atual=campanha[atributo])
            if resultado is not None:
                resultado["metrica_principal"] = (metrica == metrica_principal)
                candidatas.append(resultado)
    
    return candidatas

def priorizar_recomendacoes(candidatas, max_recs=5, diferenca_minima=10):
    recs_finais = []
    
    recs_metrica_principal = [rec for rec in candidatas if rec["metrica_principal"]]
    recs_metrica_principal = sorted(recs_metrica_principal, key=lambda rec: rec["diferenca_pct"], reverse=True)
    
    recs_outras = [rec for rec in candidatas if not rec["metrica_principal"]]
    recs_outras = sorted(recs_outras, key=lambda rec: rec["diferenca_pct"], reverse=True)

    atributos_selecionados = set()

    for rec in recs_metrica_principal:
        if len(recs_finais) >= min(2, max_recs):
            break

        if rec["diferenca_pct"] >= diferenca_minima and rec["atributo"] not in atributos_selecionados:
            recs_finais.append(rec)
            atributos_selecionados.add(rec["atributo"])

    for rec in recs_outras:
        if len(recs_finais) >= max_recs:
            break

        if rec["diferenca_pct"] >= diferenca_minima and rec["atributo"] not in atributos_selecionados:
            recs_finais.append(rec)
            atributos_selecionados.add(rec["atributo"])

    recs_finais = sorted(recs_finais, key=lambda rec: rec["diferenca_pct"], reverse=True)
    return recs_finais

def aplicar_recomendacoes(campanha, recomendacoes, dados):
    campanha_modificada = campanha.copy()
    for rec in recomendacoes:
        atributo = rec["atributo"]

        if atributo in ["duration_group", "audio_group"]:
            coluna_original = {"duration_group": "video_duration_s", "audio_group": "music_voice_ratio"}[atributo]
            valor_recomendado = dados.loc[(dados["platform"] == campanha["platform"]) & (dados[atributo] == rec["valor_recomendado"]), 
                                          coluna_original].median()
            campanha_modificada[coluna_original] = float(valor_recomendado)
            
        campanha_modificada[atributo] = rec["valor_recomendado"]
            
    return campanha_modificada

def recommendations_engine(campanha, dados):
    candidatas = gerar_candidatas(campanha, dados)
    recomendacoes = priorizar_recomendacoes(candidatas)

    campanha_modificada = aplicar_recomendacoes(campanha, recomendacoes, dados)

    return {"recomendacoes": recomendacoes,"campanha_modificada": campanha_modificada}

def descrever_acao(recomendacao, campanha, campanha_modificada):
    atributo = recomendacao["atributo"]

    acoes_booleanas = {
        "has_hook": ("Adicionar um hook nos primeiros 3 segundos",
                     "Remover o hook inicial"),
        "has_cta": ("Adicionar uma chamada para ação (CTA)",
                    "Remover a chamada para ação (CTA)"),
        "has_subtitle": ("Adicionar legendas ao vídeo",
                         "Remover as legendas do vídeo"),
        "has_face": ("Incluir um rosto humano no vídeo",
                     "Remover a presença de rosto humano")}

    if atributo in acoes_booleanas:
        novo_valor = bool(campanha_modificada[atributo])
        return acoes_booleanas[atributo][0 if novo_valor else 1]
    elif atributo == "format":
        atual = campanha["format"]
        novo = campanha_modificada["format"]
        return f"Alterar o formato de vídeo de {atual} para {novo}"
    elif atributo == "text_density":
        traducoes = {"low": "baixa", "medium": "média", "high": "alta"}
        atual = traducoes.get(campanha["text_density"], campanha["text_density"])
        novo = traducoes.get(campanha_modificada['text_density'], campanha_modificada["text_density"])
        return f"Alterar a densidade de texto de {atual} para {novo}"
    elif atributo == "duration_group":
        atual = campanha["video_duration_s"]
        novo = campanha_modificada["video_duration_s"]
        verbo = "Reduzir" if novo < atual else "Aumentar"
        return (f"{verbo} a duração do vídeo de " f"{atual:.0f}s para aproximadamente {novo:.0f}s")
    elif atributo == "audio_group":
        atual = campanha["music_voice_ratio"] * 100
        novo = campanha_modificada["music_voice_ratio"] * 100
        verbo = "Reduzir" if novo < atual else "Aumentar"
        return (f"{verbo} a proporção de música no áudio " f"de {atual:.0f}% para aproximadamente {novo:.0f}%")
    else:
        raise ValueError(f"Atributo não reconhecido: {atributo}")

def descrever_evidencia(recomendacao, plataforma):
    nomes_metricas = {
    "ctr": "CTR",
    "roas": "ROAS",
    "engagement_rate": "taxa de engajamento",
    "conversion_rate": "taxa de conversão",
    "watch_time_ratio": "proporção assistida do vídeo"}
    metrica = recomendacao["metrica"]
    diferenca = recomendacao["diferenca_pct"]
    nome_metrica = nomes_metricas[metrica]

    return (f"Campanhas com essa característica na plataforma " f"{plataforma} apresentaram {nome_metrica} mediano " 
            f"{diferenca:.1f}% superior ao grupo atual.")

def apresentar_recomendacoes(campanha, resultado):
    recomendacoes = resultado["recomendacoes"]
    campanha_modificada = resultado["campanha_modificada"]

    campanha_id = campanha["campaign_id"]
    plataforma = campanha["platform"]

    objetivos = {
    "awareness": "Reconhecimento de marca",
    "traffic": "Tráfego",
    "conversions": "Conversões",
    "engagement": "Engajamento",
    "app_install": "Instalação de aplicativo"}

    objetivo = objetivos.get(campanha["objective"], campanha["objective"])

    print("=" * 65)
    print(f"RECOMENDAÇÕES PARA A CAMPANHA {campanha_id}")
    print(f"Plataforma: {plataforma} | Objetivo: {objetivo}")
    print("=" * 65)

    if not recomendacoes:
        print("\nNenhuma recomendação válida foi identificada.")
        return
    
    print(f"\n{len(recomendacoes)} recomendações identificadas:\n")

    for i, recomendacao in enumerate(recomendacoes, start=1):
        acao = descrever_acao(recomendacao, campanha, campanha_modificada)
        evidencia = descrever_evidencia(recomendacao, plataforma)
        print(f"{i}. {acao}.")
        print(f"   {evidencia}\n")

    print("-" * 65)
    print("Nota: as recomendações são baseadas em associações observadas no dataset e não garantem melhorias de performance.")

def preparar_dados(df):
    dados = df.copy()

    dados['duration_group'] = pd.qcut(dados['video_duration_s'], q=3, labels=['short', 'medium', 'long'])
    dados['audio_group'] = pd.qcut(dados['music_voice_ratio'], q=3, labels=['low_music', 'medium_music', 'high_music'])
    dados["conversion_rate"] = (dados["conversions"] / dados["clicks"].replace(0, np.nan))
    dados["watch_time_ratio"] = dados["avg_watch_time_s"] / dados["video_duration_s"].replace(0, np.nan)

    return dados
