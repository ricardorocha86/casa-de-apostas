"""Lógica da simulação da casa de apostas (independente do Streamlit)."""
import copy
import random

import numpy as np
from faker import Faker

VALOR_APOSTA_MINIMA = 5.0
PERC_SALDO_APOSTA = 0.10  # Cada aposta usa 10% do saldo atual
RESULTADOS = ["Vitória", "Empate", "Derrota"]  # Do ponto de vista do mandante

TIMES_BRASILEIROS = [
    "Flamengo", "Palmeiras", "Corinthians", "São Paulo",
    "Santos", "Vasco", "Botafogo", "Fluminense",
    "Atlético-MG", "Cruzeiro", "Grêmio", "Internacional",
    "Bahia", "Sport", "Ceará", "Fortaleza",
    "Athletico-PR", "Coritiba", "Chapecoense", "Avaí",
]
NUM_JOGOS_RODADA = len(TIMES_BRASILEIROS) // 2  # Todos os times jogam em toda rodada

# Estratégia: em qual resultado do jogo sorteado o usuário aposta
#   Favorito → menor odd ou intermediária | Aleatório → qualquer resultado | Zebra → intermediária ou maior odd
ESTRATEGIAS = ["Favorito", "Aleatório", "Zebra"]

PERFIS_CONFIG_DEFAULT = {
    "Conservador": {"prob_decidir_apostar": 0.60, "lambda_poisson": 1.5, "estrategia": "Favorito"},
    "Moderado": {"prob_decidir_apostar": 0.80, "lambda_poisson": 2.5, "estrategia": "Aleatório"},
    "Arriscado": {"prob_decidir_apostar": 0.95, "lambda_poisson": 3.5, "estrategia": "Zebra"},
}
LISTA_PERFIS = list(PERFIS_CONFIG_DEFAULT)
CORES_PERFIS = {"Conservador": "#20B2AA", "Moderado": "#FFD700", "Arriscado": "#d62728"}

fake = Faker("pt_BR")


def perfis_config_padrao():
    return copy.deepcopy(PERFIS_CONFIG_DEFAULT)


def gerar_probabilidades_futebol():
    """
    Probabilidades (Vitória, Empate, Derrota) do mandante:
    - Vitória ~ U(0.05, 0.70)
    - Empate ~ U(0.10, 0.25)
    - Derrota = 1 - Vitória - Empate (sempre >= 0.05 com esses intervalos)
    """
    prob_vitoria = round(random.uniform(0.05, 0.70), 2)
    prob_empate = round(random.uniform(0.10, 0.25), 2)
    prob_derrota = round(1.0 - prob_vitoria - prob_empate, 2)
    return [prob_vitoria, prob_empate, prob_derrota]


def calcular_odds_casa(probabilidades_reais, margem_casa):
    """Odd da casa = (1 / p) × (1 - margem), arredondada e com mínimo de 1.01."""
    return [max(1.01, round((1 / p) * (1 - margem_casa), 2)) for p in probabilidades_reais]


def poisson_truncada_em_1(lambda_param):
    """Amostra de uma Poisson(λ) condicionada a valores >= 1."""
    while True:
        valor = np.random.poisson(lambda_param)
        if valor >= 1:
            return int(valor)


def calcular_valor_aposta(saldo_usuario):
    if saldo_usuario <= 0:
        return 0.0
    # Sem saldo para a aposta mínima → aposta tudo o que tem
    if saldo_usuario < VALOR_APOSTA_MINIMA:
        return round(saldo_usuario, 2)
    valor = max(saldo_usuario * PERC_SALDO_APOSTA, VALOR_APOSTA_MINIMA)
    return round(min(valor, saldo_usuario), 2)


def escolher_resultado(odds, estrategia):
    """
    Índice do resultado apostado, sorteado de forma uniforme entre:
    - Favorito: a menor odd e a intermediária
    - Zebra: a intermediária e a maior odd
    - Aleatório: os três resultados
    """
    por_odd = sorted(range(len(odds)), key=lambda i: odds[i])  # [menor, intermediária, maior]
    if estrategia == "Favorito":
        return random.choice(por_odd[:2])
    if estrategia == "Zebra":
        return random.choice(por_odd[1:])
    return random.randrange(len(odds))


def gerar_jogos_rodada(margem_casa):
    times = random.sample(TIMES_BRASILEIROS, len(TIMES_BRASILEIROS))
    jogos = []
    for i in range(NUM_JOGOS_RODADA):
        mandante, visitante = times[2 * i], times[2 * i + 1]
        probabilidades = gerar_probabilidades_futebol()
        jogos.append({
            "descricao": f"{mandante} x {visitante}",
            "mandante": mandante,
            "visitante": visitante,
            "probabilidades_reais": probabilidades,
            "odds_casa": calcular_odds_casa(probabilidades, margem_casa),
            "idx_resultado_final": None,
            "resultado_final": None,
        })
    return jogos


def criar_simulacao(num_usuarios, saldo_inicial, margem_casa):
    usuarios = []
    for i in range(num_usuarios):
        usuarios.append({
            "id": i,  # id == posição na lista
            "nome": fake.name(),
            "perfil": LISTA_PERFIS[i % len(LISTA_PERFIS)],
            "saldo": float(saldo_inicial),
            "saldos": [float(saldo_inicial)],  # Saldo ao fim de cada rodada (índice 0 = inicial)
            "rodadas_apostou": 0,
            "num_apostas": 0,
            "total_apostado": 0.0,
        })
    return {
        "saldo_inicial": float(saldo_inicial),
        "margem_casa": float(margem_casa),
        "usuarios": usuarios,
        "rodadas": [],  # Cada item: {"numero", "jogos", "apostas", "stats"}
    }


def simular_rodada(sim, perfis_config):
    numero = len(sim["rodadas"]) + 1
    usuarios = sim["usuarios"]
    jogos = gerar_jogos_rodada(sim["margem_casa"])

    stats = {
        "rodada": numero,
        "total_apostado": 0.0,
        "total_pago": 0.0,
        "num_apostas": 0,
        "apostado_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
        "pago_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
    }
    apostas = []

    # 1. Usuários decidem se apostam, quantas vezes e em quê (jogo ao acaso, resultado pela estratégia)
    for user in usuarios:
        cfg = perfis_config[user["perfil"]]
        if user["saldo"] <= 0 or random.random() >= cfg["prob_decidir_apostar"]:
            continue
        user["rodadas_apostou"] += 1

        for _ in range(poisson_truncada_em_1(cfg["lambda_poisson"])):
            valor = calcular_valor_aposta(user["saldo"])
            if valor <= 0:
                break
            j = random.randrange(len(jogos))
            r = escolher_resultado(jogos[j]["odds_casa"], cfg["estrategia"])
            odd = jogos[j]["odds_casa"][r]
            apostas.append({
                "id_usuario": user["id"],
                "perfil_usuario": user["perfil"],
                "idx_jogo": j,
                "jogo_desc": jogos[j]["descricao"],
                "idx_resultado_apostado": r,
                "resultado_apostado": RESULTADOS[r],
                "valor_apostado": valor,
                "odd_no_momento": odd,
                "ganhou": False,
                "valor_ganho": 0.0,
            })
            user["saldo"] = round(user["saldo"] - valor, 2)
            user["total_apostado"] = round(user["total_apostado"] + valor, 2)
            user["num_apostas"] += 1
            stats["total_apostado"] += valor
            stats["num_apostas"] += 1
            stats["apostado_por_perfil"][user["perfil"]] += valor

    # 2. Resultados dos jogos (sorteados depois das apostas)
    for jogo in jogos:
        idx = int(np.random.choice(len(RESULTADOS), p=jogo["probabilidades_reais"]))
        jogo["idx_resultado_final"] = idx
        jogo["resultado_final"] = RESULTADOS[idx]

    # 3. Liquidação
    for aposta in apostas:
        if aposta["idx_resultado_apostado"] == jogos[aposta["idx_jogo"]]["idx_resultado_final"]:
            premio = round(aposta["valor_apostado"] * aposta["odd_no_momento"], 2)
            aposta["ganhou"] = True
            aposta["valor_ganho"] = premio
            user = usuarios[aposta["id_usuario"]]
            user["saldo"] = round(user["saldo"] + premio, 2)
            stats["total_pago"] += premio
            stats["pago_por_perfil"][aposta["perfil_usuario"]] += premio

    # 4. Consolidação
    saldo_inicial = sim["saldo_inicial"]
    for user in usuarios:
        user["saldo"] = max(0.0, round(user["saldo"], 2))
        user["saldos"].append(user["saldo"])

    stats["ggr"] = stats["total_apostado"] - stats["total_pago"]
    stats["saldo_medio"] = sum(u["saldo"] for u in usuarios) / len(usuarios) if usuarios else 0.0
    stats["usuarios_ativos"] = sum(1 for u in usuarios if u["saldo"] > 0)
    stats["usuarios_lucrativos"] = sum(1 for u in usuarios if u["saldo"] > saldo_inicial)
    stats["usuarios_zerados"] = sum(1 for u in usuarios if u["saldo"] == 0)
    stats["usuarios_ativos_por_perfil"] = {
        p: sum(1 for u in usuarios if u["perfil"] == p and u["saldo"] > 0) for p in LISTA_PERFIS
    }

    sim["rodadas"].append({"numero": numero, "jogos": jogos, "apostas": apostas, "stats": stats})
