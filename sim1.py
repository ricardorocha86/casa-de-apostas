import streamlit as st
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from faker import Faker # Adicionado

# --- Constantes e Configurações Iniciais ---
VALOR_APOSTA_MINIMA = 5

# Perfis de Jogador e suas configurações (AGORA AJUSTÁVEL NA SIDEBAR)
# Estes serão os valores padrão que podem ser sobrescritos pela UI
PERFIS_CONFIG_DEFAULT = {
    "Conservador": {
        "lambda_poisson": 1.5,
        "prob_decidir_apostar": 0.6, # 60% de chance de apostar
        "cor": "#1f77b4" # Azul padrão plotly
    },
    "Moderado": {
        "lambda_poisson": 2.5,
        "prob_decidir_apostar": 0.8, # 80% de chance de apostar
        "cor": "#ff7f0e" # Laranja padrão plotly
    },
    "Arriscado": {
        "lambda_poisson": 3.5,
        "prob_decidir_apostar": 0.95, # 95% de chance de apostar
        "cor": "#d62728" # Vermelho padrão plotly
    }
}
LISTA_PERFIS = list(PERFIS_CONFIG_DEFAULT.keys())

fake = Faker('pt_BR')

# --- Funções Auxiliares ---

def gerar_probabilidades_futebol():
    """
    Gera probabilidades para jogos de futebol (Vitória, Empate, Derrota)
    - Vitória: U(0.05, 0.70)
    - Empate: U(0.10, 0.25)  
    - Derrota: 1 - Vitória - Empate
    """
    # Gerar probabilidade de vitória
    prob_vitoria = round(random.uniform(0.05, 0.70), 2)
    
    # Gerar probabilidade de empate
    prob_empate = round(random.uniform(0.10, 0.25), 2)
    
    # Calcular probabilidade de derrota
    prob_derrota = round(1.0 - prob_vitoria - prob_empate, 2)
    
    # Garantir que as probabilidades sejam válidas
    if prob_derrota < 0:
        # Se derrota ficou negativa, ajustar empate
        prob_empate = round(1.0 - prob_vitoria, 2)
        prob_derrota = 0.0
    
    # Normalizar para garantir que soma seja exatamente 1.0
    total = prob_vitoria + prob_empate + prob_derrota
    if total != 1.0:
        prob_derrota = round(1.0 - prob_vitoria - prob_empate, 2)
    
    return [prob_vitoria, prob_empate, prob_derrota]

def calcular_odds_casa(probabilidades_reais, margem_casa_global):
    final_odds = []
    for p_real in probabilidades_reais:
        if p_real == 0:
            final_odds.append(999.0)
        else:
            fair_odd = 1 / p_real
            house_odd = round(fair_odd * (1 - margem_casa_global), 2)
            final_odds.append(max(1.01, house_odd)) # Garante odd mínima
    return final_odds

def simular_resultado_jogo(probabilidades_reais, resultados_possiveis):
    return np.random.choice(resultados_possiveis, p=probabilidades_reais)

def poisson_truncada_em_1(lambda_param):
    """
    Gera um número aleatório de uma distribuição Poisson truncada em 1.
    Ou seja, só retorna valores >= 1.
    
    Args:
        lambda_param: Parâmetro lambda da distribuição Poisson
    
    Returns:
        int: Número >= 1 seguindo distribuição Poisson truncada
    """
    while True:
        valor = np.random.poisson(lambda_param)
        if valor >= 1:
            return valor

# FUNÇÃO para calcular valor da aposta com base no perfil e regras
def calcular_valor_aposta(saldo_usuario, perfil_usuario_config):
    if saldo_usuario <= 0:
        return 0.0

    # REGRA 3 PRIMEIRO: Se valor mínimo > saldo do usuário → aposta todo o saldo
    if VALOR_APOSTA_MINIMA > saldo_usuario:
        return round(saldo_usuario, 2)

    # 1. SEMPRE gera valor da aposta baseado no perfil (uniforme entre min e max %)
    valor_proposto = saldo_usuario * 0.10 # FIXO em 10% do saldo

    # 2. Se valor proposto < valor mínimo → aposta valor mínimo
    if valor_proposto < VALOR_APOSTA_MINIMA:
        valor_final_aposta = VALOR_APOSTA_MINIMA
    else:
        valor_final_aposta = valor_proposto
    
    # Garantir que não aposta mais que o saldo disponível
    valor_final_aposta = min(valor_final_aposta, saldo_usuario)
    
    return round(valor_final_aposta, 2)


# --- Inicialização do Estado da Sessão Streamlit ---
if 'simulacao_iniciada' not in st.session_state:
    st.session_state.simulacao_iniciada = False
    st.session_state.rodada_atual = 0
    st.session_state.usuarios = []
    st.session_state.historico_casa = []
    st.session_state.jogos_da_rodada_anterior = []
    st.session_state.apostas_da_rodada_anterior = []
    st.session_state.historico_jogos = []  # Histórico de todos os jogos por rodada
    st.session_state.historico_apostas = []  # Histórico de todas as apostas por rodada
    
    # Inicializa configs dos perfis no session_state para serem ajustáveis
    st.session_state.perfis_config_dinamico = PERFIS_CONFIG_DEFAULT.copy()

    # Estatísticas acumuladas (incluindo por perfil)
    st.session_state.casa_stats_acumuladas = {
        "total_apostado": 0.0, "total_pago": 0.0, "ggr": 0.0,
        "num_apostas": 0,
        "apostado_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
        "pago_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
        "ggr_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
        "num_apostas_por_perfil": {p: 0 for p in LISTA_PERFIS}
    }

# --- Interface Streamlit ---

# Sidebar para Controles
with st.sidebar:
    st.header("⚙️ Controles da Simulação")
    
    num_usuarios_input = st.number_input("Número de Usuários Iniciais", min_value=1, max_value=1000, value=100, step=10, disabled=st.session_state.simulacao_iniciada)
    saldo_inicial_input = st.number_input("Saldo Inicial por Usuário (R$)", min_value=10, max_value=1000, value=100, step=10, disabled=st.session_state.simulacao_iniciada)
    margem_casa_input = st.slider("Margem da Casa nas Odds (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1, format="%.1f%%", disabled=st.session_state.simulacao_iniciada) / 100.0
    
  
    st.subheader("Comportamento dos Usuários")
    
    st.caption("Parâmetros por Perfil de Apostador:")
    # Usar st.session_state para configs de perfil para persistência entre reruns de botões
    if 'perfis_config_dinamico' not in st.session_state:
        st.session_state.perfis_config_dinamico = PERFIS_CONFIG_DEFAULT.copy()

    for perfil in LISTA_PERFIS:
        with st.expander(f"**Perfil: {perfil}**", expanded=False):
            # 1. Probabilidade de decidir apostar (primeiro)
            st.session_state.perfis_config_dinamico[perfil]["prob_decidir_apostar"] = st.slider(
                "Probabilidade de Decidir Apostar", 
                min_value=0.05, max_value=1.0, 
                value=st.session_state.perfis_config_dinamico[perfil]["prob_decidir_apostar"], 
                step=0.05, format="%.2f", key=f"prob_apostar_{perfil}"
            )
            
            # 2. Média de apostas (segundo)
            st.session_state.perfis_config_dinamico[perfil]["lambda_poisson"] = st.slider(
                "Média de Apostas Desejadas (λ)", 
                min_value=0.5, max_value=7.0, 
                value=st.session_state.perfis_config_dinamico[perfil]["lambda_poisson"], 
                step=0.1, key=f"lambda_{perfil}",
                help="Distribuição Poisson truncada em 1 - sempre faz pelo menos 1 aposta se decidir apostar"
            )
            
            # 3. Percentuais do saldo (terceiro)
            # cols_perc = st.columns(2)
            # st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_min"] = cols_perc[0].number_input(
            #     "Min % Saldo", 0.01, 0.98, 
            #     value=st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_min"], 
            #     step=0.01, format="%.2f", key=f"min_perc_{perfil}"
            # )
            # st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_max"] = cols_perc[1].number_input(
            #     "Max % Saldo", 0.02, 0.99, 
            #     value=st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_max"], 
            #     step=0.01, format="%.2f", key=f"max_perc_{perfil}"
            # )
            
            # if st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_min"] >= \
            #    st.session_state.perfis_config_dinamico[perfil]["perc_saldo_aposta_max"]:
            #     st.warning(f"Para **{perfil}**, Min % deve ser menor que Max %.", icon="⚠️")

    # Validação global antes de permitir iniciar/continuar
    pode_continuar = True # Adicionado para manter a variável, agora sempre permite se não houver outros erros

    col1_btn, col2_btn = st.columns(2)
    with col1_btn:
        if st.button("▶️ Iniciar / Próxima Rodada", type="primary", use_container_width=True, disabled=not pode_continuar):
            st.session_state.simulacao_iniciada = True
            st.session_state.rodada_atual += 1

            # Inicializar usuários na primeira rodada (COM NOVOS CAMPOS)
            if st.session_state.rodada_atual == 1:
                # Salvar saldo inicial no session_state para uso posterior
                st.session_state.saldo_inicial = float(saldo_inicial_input)
                st.session_state.margem_casa_fixa = float(margem_casa_input) # Salvar margem da casa
                st.session_state.usuarios = []
                for i in range(num_usuarios_input):
                    # Distribuição de perfis mais uniforme
                    perfil_usuario = LISTA_PERFIS[i % len(LISTA_PERFIS)]
                    st.session_state.usuarios.append({
                        "id": i,
                        "nome": fake.name(), # NOVO
                        "email": fake.email(), # NOVO
                        "perfil": perfil_usuario, # NOVO
                        "saldo": float(saldo_inicial_input),
                        "rodadas_apostou": 0,
                        "total_apostado_pessoal": 0.0,
                        "balanco_pessoal": 0.0
                    })
                # Resetar estatísticas acumuladas
                st.session_state.casa_stats_acumuladas = {
                    "total_apostado": 0.0, "total_pago": 0.0, "ggr": 0.0,
                    "num_apostas": 0,
                    "apostado_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                    "pago_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                    "ggr_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                    "num_apostas_por_perfil": {p: 0 for p in LISTA_PERFIS}
                }
                st.session_state.historico_casa = []


            # --- LÓGICA DA RODADA ---
            # Estatísticas da rodada (incluindo por perfil)
            stats_rodada_casa = {
                "rodada": st.session_state.rodada_atual,
                "total_apostado_rodada": 0.0,
                "total_pago_rodada": 0.0,
                "ggr_rodada": 0.0,
                "num_apostas_rodada": 0,
                "apostado_por_perfil_rodada": {p: 0.0 for p in LISTA_PERFIS},
                "pago_por_perfil_rodada": {p: 0.0 for p in LISTA_PERFIS},
                "ggr_por_perfil_rodada": {p: 0.0 for p in LISTA_PERFIS},
                "num_apostas_por_perfil_rodada": {p: 0 for p in LISTA_PERFIS},
                "saldo_medio_fim_rodada": 0.0
            }
            
            apostas_nesta_rodada = []
            jogos_da_rodada = []

            # 1. Gerar Jogos para a Rodada (sempre 10 jogos)
            num_jogos_desta_rodada = 10 # Valor fixo
            jogos_da_rodada = []
            # Usar a margem da casa definida no início da simulação se já tiver sido iniciada
            margem_casa_atual = st.session_state.margem_casa_fixa if 'margem_casa_fixa' in st.session_state and st.session_state.rodada_atual > 1 else margem_casa_input

            for j in range(num_jogos_desta_rodada):
                resultados_possiveis = ["Vitória", "Empate", "Derrota"] # Fixo para Futebol
                probabilidades_reais = gerar_probabilidades_futebol()
                odds_casa = calcular_odds_casa(probabilidades_reais, margem_casa_atual)
                
                jogos_da_rodada.append({
                    "id_jogo": f"JOGO_{st.session_state.rodada_atual}_{j+1}",
                    "descricao": f"Jogo {j+1}",
                    "resultados_possiveis": resultados_possiveis,
                    "probabilidades_reais": probabilidades_reais,
                    "odds_casa": odds_casa,
                    "resultado_final": None, # Será definido após as apostas
                    "idx_resultado_final": -1
                })

            # st.session_state.jogos_da_rodada_anterior = jogos_da_rodada # Movido para depois da resolução
            st.session_state.apostas_da_rodada_anterior = [] # Limpar apostas antes de coletar novas

            # 2. Usuários Decidem Apostar e Realizam Apostas (COM LÓGICA DE PERFIL)
            for user in st.session_state.usuarios:
                perfil_config_atual = st.session_state.perfis_config_dinamico[user["perfil"]]
                prob_apostar_perfil = perfil_config_atual["prob_decidir_apostar"]
                
                # PASSO 1: Usuário decide SE vai apostar na rodada
                if random.random() < prob_apostar_perfil:
                    user["rodadas_apostou"] += 1
                    
                    # PASSO 2: Decide QUANTAS apostas vai fazer (Poisson truncada em 1)
                    lambda_usuario = perfil_config_atual["lambda_poisson"]
                    qtde_apostas_desejadas = poisson_truncada_em_1(lambda_usuario)
                    
                    # PASSO 3: Faz as apostas enquanto tiver dinheiro
                    apostas_feitas = 0
                    for _ in range(qtde_apostas_desejadas):
                        # Verifica se ainda tem dinheiro para apostar
                        if user["saldo"] <= 0:
                            break
                        
                        # Calcula valor da aposta
                        valor_aposta_calculado = calcular_valor_aposta(user["saldo"], perfil_config_atual)
                        
                        # Se não consegue apostar nem o valor mínimo, para
                        if valor_aposta_calculado <= 0:
                            break

                        # Escolhe jogo e resultado para apostar
                        jogo_escolhido = random.choice(jogos_da_rodada)
                        idx_resultado_escolhido = random.randint(0, len(jogo_escolhido["resultados_possiveis"]) - 1)
                        resultado_apostado_desc = jogo_escolhido["resultados_possiveis"][idx_resultado_escolhido]
                        odd_apostada = jogo_escolhido["odds_casa"][idx_resultado_escolhido]

                        # Registra a aposta
                        apostas_nesta_rodada.append({
                            "id_aposta": f"AP_{user['id']}_{user['rodadas_apostou']}_{apostas_feitas}", 
                            "id_usuario": user["id"], "perfil_usuario": user["perfil"],
                            "id_jogo": jogo_escolhido["id_jogo"], "jogo_desc": jogo_escolhido["descricao"],
                            "resultado_apostado": resultado_apostado_desc, "idx_resultado_apostado": idx_resultado_escolhido,
                            "valor_apostado": valor_aposta_calculado, "odd_no_momento": odd_apostada,
                            "ganhou": None, "valor_ganho": 0.0
                        })
                        
                        # Debita do saldo do usuário
                        user["saldo"] = round(user["saldo"] - valor_aposta_calculado, 2)
                        user["total_apostado_pessoal"] = round(user["total_apostado_pessoal"] + valor_aposta_calculado, 2)
                        user["balanco_pessoal"] = round(user["balanco_pessoal"] - valor_aposta_calculado, 2)
                        
                        # Atualiza estatísticas da rodada
                        stats_rodada_casa["total_apostado_rodada"] += valor_aposta_calculado
                        stats_rodada_casa["num_apostas_rodada"] += 1
                        stats_rodada_casa["apostado_por_perfil_rodada"][user["perfil"]] += valor_aposta_calculado
                        stats_rodada_casa["num_apostas_por_perfil_rodada"][user["perfil"]] += 1
                        
                        apostas_feitas += 1
            
            st.session_state.apostas_da_rodada_anterior = apostas_nesta_rodada
            
            # Salvar apostas no histórico
            st.session_state.historico_apostas.append({
                "rodada": st.session_state.rodada_atual,
                "apostas": apostas_nesta_rodada.copy()
            })

            # 3. Resolver Jogos (Simular resultado DEPOIS das apostas)
            for jogo in jogos_da_rodada:
                if jogo["resultado_final"] is None: # Só simula se ainda não tiver resultado
                    jogo["resultado_final"] = simular_resultado_jogo(jogo["probabilidades_reais"], jogo["resultados_possiveis"])
                    jogo["idx_resultado_final"] = jogo["resultados_possiveis"].index(jogo["resultado_final"])
            
            st.session_state.jogos_da_rodada_anterior = jogos_da_rodada # Agora atualiza com resultados
            
            # Salvar no histórico
            st.session_state.historico_jogos.append({
                "rodada": st.session_state.rodada_atual,
                "jogos": jogos_da_rodada.copy()
            })

            # 4. Liquidar Apostas (COM LÓGICA DE PERFIL)
            for aposta in apostas_nesta_rodada:
                jogo_correspondente = next(j for j in jogos_da_rodada if j["id_jogo"] == aposta["id_jogo"])
                # Não precisa buscar user aqui, já temos o perfil na aposta.
                # Mas para atualizar saldo, precisamos do user:
                user_da_aposta = next(u for u in st.session_state.usuarios if u["id"] == aposta["id_usuario"])

                if aposta["idx_resultado_apostado"] == jogo_correspondente["idx_resultado_final"]:
                    aposta["ganhou"] = True
                    valor_ganho_bruto = round(aposta["valor_apostado"] * aposta["odd_no_momento"], 2)
                    aposta["valor_ganho"] = valor_ganho_bruto
                    
                    user_da_aposta["saldo"] = round(user_da_aposta["saldo"] + valor_ganho_bruto, 2)
                    user_da_aposta["balanco_pessoal"] = round(user_da_aposta["balanco_pessoal"] + valor_ganho_bruto, 2)
                    
                    stats_rodada_casa["total_pago_rodada"] += valor_ganho_bruto
                    stats_rodada_casa["pago_por_perfil_rodada"][aposta["perfil_usuario"]] += valor_ganho_bruto
                else:
                    aposta["ganhou"] = False

            # 5. Atualizar Estatísticas Finais da Rodada
            for user in st.session_state.usuarios:
                # Garante que saldo não fique negativo e arredonda para evitar problemas de precisão
                user["saldo"] = max(0, round(user["saldo"], 2))
                # Recalcular balanço pessoal de forma consistente para evitar erros de arredondamento
                saldo_inicial_ref = getattr(st.session_state, 'saldo_inicial', 100.0)
                user["balanco_pessoal"] = round(user["saldo"] - saldo_inicial_ref, 2)
            
            stats_rodada_casa["ggr_rodada"] = stats_rodada_casa["total_apostado_rodada"] - stats_rodada_casa["total_pago_rodada"]
            for p in LISTA_PERFIS:
                stats_rodada_casa["ggr_por_perfil_rodada"][p] = stats_rodada_casa["apostado_por_perfil_rodada"][p] - \
                                                              stats_rodada_casa["pago_por_perfil_rodada"][p]

            saldos_usuarios = [u['saldo'] for u in st.session_state.usuarios]
            stats_rodada_casa["saldo_medio_fim_rodada"] = sum(saldos_usuarios) / len(saldos_usuarios) if saldos_usuarios else 0.0
            
            # Adicionar estatísticas de usuários por categoria
            saldo_inicial_ref = getattr(st.session_state, 'saldo_inicial', 100.0)
            stats_rodada_casa["usuarios_ativos"] = sum(1 for u in st.session_state.usuarios if u['saldo'] > 0)
            stats_rodada_casa["usuarios_lucrativos"] = sum(1 for u in st.session_state.usuarios if u['saldo'] > saldo_inicial_ref)
            stats_rodada_casa["usuarios_zerados"] = sum(1 for u in st.session_state.usuarios if u['saldo'] == 0)
            
            # Adicionar estatísticas de usuários ativos por perfil
            stats_rodada_casa["usuarios_ativos_por_perfil"] = {}
            for perfil in LISTA_PERFIS:
                stats_rodada_casa["usuarios_ativos_por_perfil"][perfil] = sum(
                    1 for u in st.session_state.usuarios if u['perfil'] == perfil and u['saldo'] > 0
                )
            
            st.session_state.historico_casa.append(stats_rodada_casa)

            # Atualizar estatísticas acumuladas
            st.session_state.casa_stats_acumuladas["total_apostado"] += stats_rodada_casa["total_apostado_rodada"]
            st.session_state.casa_stats_acumuladas["total_pago"] += stats_rodada_casa["total_pago_rodada"]
            st.session_state.casa_stats_acumuladas["ggr"] = st.session_state.casa_stats_acumuladas["total_apostado"] - \
                                                          st.session_state.casa_stats_acumuladas["total_pago"]
            st.session_state.casa_stats_acumuladas["num_apostas"] += stats_rodada_casa["num_apostas_rodada"]
            for p in LISTA_PERFIS:
                st.session_state.casa_stats_acumuladas["apostado_por_perfil"][p] += stats_rodada_casa["apostado_por_perfil_rodada"][p]
                st.session_state.casa_stats_acumuladas["pago_por_perfil"][p] += stats_rodada_casa["pago_por_perfil_rodada"][p]
                st.session_state.casa_stats_acumuladas["ggr_por_perfil"][p] = st.session_state.casa_stats_acumuladas["apostado_por_perfil"][p] - \
                                                                            st.session_state.casa_stats_acumuladas["pago_por_perfil"][p]
                st.session_state.casa_stats_acumuladas["num_apostas_por_perfil"][p] += stats_rodada_casa["num_apostas_por_perfil_rodada"][p]


    with col2_btn:
        if st.button("🔄 Resetar Simulação", use_container_width=True):
            # Mantém as configs da sidebar, mas reseta o resto
            st.session_state.simulacao_iniciada = False
            st.session_state.rodada_atual = 0
            st.session_state.usuarios = []
            st.session_state.historico_casa = []
            st.session_state.jogos_da_rodada_anterior = []
            st.session_state.apostas_da_rodada_anterior = []
            st.session_state.historico_jogos = []
            st.session_state.historico_apostas = []
            # Resetar saldo inicial também
            if 'saldo_inicial' in st.session_state:
                del st.session_state.saldo_inicial
            # Não resetar st.session_state.perfis_config_dinamico aqui
            st.session_state.casa_stats_acumuladas = {
                "total_apostado": 0.0, "total_pago": 0.0, "ggr": 0.0,
                "num_apostas": 0,
                "apostado_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                "pago_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                "ggr_por_perfil": {p: 0.0 for p in LISTA_PERFIS},
                "num_apostas_por_perfil": {p: 0 for p in LISTA_PERFIS}
            }
            st.rerun()

# --- Painel Principal ---
if not st.session_state.simulacao_iniciada:
    st.info("👈 Configure os parâmetros na barra lateral e clique em 'Iniciar / Próxima Rodada'.")
    if not pode_continuar:
        st.error("Existem erros de configuração nos Perfis de Apostador na barra lateral. Ajuste-os para continuar.")
else:
    st.title("🎲 Simulador Principal: Os números 'ocultos' da casa de apostas! ")
    st.header(f"📊 Resultados da Rodada: {st.session_state.rodada_atual}")
    
    if st.session_state.historico_casa:
        stats_ultima_rodada = st.session_state.historico_casa[-1]
        
        # PRIMEIRA LINHA - Métricas da Casa/Rodada
        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        
        # Faturamento, Pagamentos, Lucro
        m_col1.metric("Faturamento Rodada", f"R$ {stats_ultima_rodada['total_apostado_rodada']:.2f}")
        m_col2.metric("Pagamentos Rodada", f"R$ {stats_ultima_rodada['total_pago_rodada']:.2f}")
        
        ggr_rodada_val = stats_ultima_rodada['ggr_rodada']
        handle_rodada = stats_ultima_rodada['total_apostado_rodada']
        
        # Calcular percentual do Lucro em relação ao Faturamento
        if handle_rodada > 0:
            percentual_ggr = (ggr_rodada_val / handle_rodada) * 100
        else:
            percentual_ggr = 0
        
        delta_text = f"{percentual_ggr:.1f}%"
        delta_color_ggr = "normal"
        
        m_col3.metric("Lucro Rodada", f"R$ {ggr_rodada_val:.2f}", 
                      delta=delta_text, delta_color=delta_color_ggr)
        
        # Número de apostas
        num_apostas = stats_ultima_rodada['num_apostas_rodada']
        m_col4.metric("Nº Apostas Rodada", num_apostas)
        
        # Valor médio apostado na rodada
        valor_medio_apostado = (handle_rodada / num_apostas) if num_apostas > 0 else 0
        m_col5.metric("Valor Médio Apostado", f"R$ {valor_medio_apostado:.2f}")

        # SEGUNDA LINHA - Métricas dos Usuários
        u_col1, u_col2, u_col3, u_col4, u_col5 = st.columns(5)
        
        total_usuarios = len(st.session_state.usuarios)
        
        # Calcular usuários lucrativos (saldo > saldo inicial)
        saldo_inicial_ref = getattr(st.session_state, 'saldo_inicial', 100.0)  # Fallback para 100 se não existir
        usuarios_lucrativos = sum(1 for u in st.session_state.usuarios if u['saldo'] > saldo_inicial_ref)
        perc_lucrativos = (usuarios_lucrativos / total_usuarios * 100) if total_usuarios > 0 else 0
        
        # Calcular usuários ativos (saldo > 0)
        usuarios_ativos = sum(1 for u in st.session_state.usuarios if u['saldo'] > 0) 
        
        # Calcular usuários falidos (saldo = 0)
        usuarios_falidos = sum(1 for u in st.session_state.usuarios if u['saldo'] == 0) 
        
        # Saldo médio (total de dinheiro / total de usuários)
        total_dinheiro = sum(u['saldo'] for u in st.session_state.usuarios)
        saldo_medio = total_dinheiro / total_usuarios if total_usuarios > 0 else 0
        
        u_col1.metric("Total de Usuários", total_usuarios)
        u_col2.metric("Usuários Lucrativos", usuarios_lucrativos)
        u_col3.metric("Usuários Ativos", usuarios_ativos, help="Saldo > R$ 0,00 (ainda tem dinheiro)")
        u_col4.metric("Usuários Falidos", usuarios_falidos, help="Saldo = R$ 0,00 (sem dinheiro)")
        u_col5.metric("Saldo Médio", f"R$ {saldo_medio:.2f}")

         
        
        # Criar 5 colunas para as métricas
        result_col1, result_col2, result_col3, result_col4, result_col5 = st.columns(5)
        
        if st.session_state.apostas_da_rodada_anterior:
            apostas = st.session_state.apostas_da_rodada_anterior
            
            # Volume por perfil (3 primeiras colunas)
            volume_por_perfil = {}
            for a in apostas:
                perfil = a['perfil_usuario']
                volume_por_perfil[perfil] = volume_por_perfil.get(perfil, 0) + a['valor_apostado']
            
            result_col1.metric("Volume Conservador", f"R$ {volume_por_perfil.get('Conservador', 0):.2f}")
            result_col2.metric("Volume Moderado", f"R$ {volume_por_perfil.get('Moderado', 0):.2f}")
            result_col3.metric("Volume Arriscado", f"R$ {volume_por_perfil.get('Arriscado', 0):.2f}") 
        else:
            result_col1.write("Nenhuma estatística disponível.")
        st.markdown("---")
 
        # Criar 2 colunas para as tabelas na proporção 1:2
        analise_col1, analise_col2 = st.columns([1, 2], gap="large")
        
        with analise_col1:
            st.markdown("#### 🎮 Jogos e Odds da Rodada")
            if st.session_state.jogos_da_rodada_anterior and st.session_state.apostas_da_rodada_anterior:
                # Calcular volume por jogo
                volume_por_jogo = {}
                for a in st.session_state.apostas_da_rodada_anterior:
                    jogo = a['jogo_desc']
                    volume_por_jogo[jogo] = volume_por_jogo.get(jogo, 0) + a['valor_apostado']
                
                jogos_info = []
                for jogo in st.session_state.jogos_da_rodada_anterior:
                    volume = volume_por_jogo.get(jogo["descricao"], 0)
                    
                    jogos_info.append({
                        "Jogo": jogo["descricao"],
                        "Vitória": f"{jogo['odds_casa'][0]:.2f}",
                        "Empate": f"{jogo['odds_casa'][1]:.2f}",
                        "Derrota": f"{jogo['odds_casa'][2]:.2f}",
                        "Resultado": jogo["resultado_final"],
                        "Volume": f"R$ {volume:.2f}"
                    })
                
                df_jogos = pd.DataFrame(jogos_info)
                st.dataframe(df_jogos, use_container_width=True, hide_index=True)
            else:
                st.write("Nenhum jogo na rodada anterior.")
        
        with analise_col2:
            st.markdown("#### 💰 Top 10 Maiores Pagamentos da Rodada")
            if st.session_state.apostas_da_rodada_anterior:
                # Ordenar apostas por valor pago (maiores pagamentos primeiro)
                apostas_ordenadas = sorted(st.session_state.apostas_da_rodada_anterior, 
                                         key=lambda x: x["valor_ganho"], reverse=True)
                
                # Calcular quantas linhas mostrar para ter 6 colunas como a tabela de jogos
                num_linhas = df_jogos.shape[0]  # Mesmo número de colunas que a tabela de jogos
                
                maiores_apostas = []
                for i, aposta in enumerate(apostas_ordenadas[:num_linhas]):
                    # Buscar nome do usuário
                    usuario = next(u for u in st.session_state.usuarios if u['id'] == aposta['id_usuario'])
                    
                    maiores_apostas.append({
                        "Usuário": usuario['nome'],
                        "Perfil": aposta['perfil_usuario'],
                        "Jogo": aposta['jogo_desc'],
                        "Aposta": aposta['resultado_apostado'],
                        "Valor": f"R$ {aposta['valor_apostado']:.2f}",
                        "Odd": f"{aposta['odd_no_momento']:.2f}",
                        "Pago": f"R$ {aposta['valor_ganho']:.2f}",
                        "Status": "✅" if aposta['ganhou'] else "❌"
                    })
                
                df_maiores_apostas = pd.DataFrame(maiores_apostas)
                st.dataframe(df_maiores_apostas, use_container_width=True, hide_index=True)
            else:
                st.write("Nenhuma aposta na rodada anterior.")

    st.markdown("---")
    st.header("📈 Estatísticas Acumuladas da Casa")
    
    casa_acum = st.session_state.casa_stats_acumuladas
    df_historico = pd.DataFrame(st.session_state.historico_casa)

    # Métricas Chave Acumuladas - Todas na mesma linha
    ac_col1, ac_col2, ac_col3, ac_col4, ac_col5, ac_col6 = st.columns(6)
    
    ac_col1.metric("Faturamento Acumulado", f"R$ {casa_acum['total_apostado']:.2f}")
    ac_col2.metric("Pagamentos Acumulado", f"R$ {casa_acum['total_pago']:.2f}")
    
    ggr_acum_val = casa_acum['ggr']
    # Para GGR negativo, queremos vermelho, então usamos valor positivo no delta com inverse
    if ggr_acum_val < 0:
        delta_val_acum = abs(ggr_acum_val)
        delta_color_ggr_acum = "inverse"
    else:
        delta_val_acum = ggr_acum_val
        delta_color_ggr_acum = "normal"
    ac_col3.metric("Lucro Acumulado", f"R$ {ggr_acum_val:.2f}", 
                   delta=f"{delta_val_acum:.2f}", delta_color=delta_color_ggr_acum)
    
    margem_ggr_acumulada = (casa_acum['ggr'] / casa_acum['total_apostado'] * 100) if casa_acum['total_apostado'] > 0 else 0
    ac_col4.metric("Margem Lucro Acum. (%)", f"{margem_ggr_acumulada:.2f}%")
    
    # Lucro médio por rodada
    num_rodadas = st.session_state.rodada_atual if st.session_state.rodada_atual > 0 else 1
    lucro_medio_por_rodada = ggr_acum_val / num_rodadas
    ac_col5.metric("Lucro Médio/Rodada", f"R$ {lucro_medio_por_rodada:.2f}")
    
    ac_col6.metric("Total Apostas Acum.", casa_acum['num_apostas'])
    
    # Gráficos Acumulados em Colunas
    if len(df_historico) > 1: # Alterado de > 0 para > 1
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.subheader("Evolução do Lucro da Casa") # Lucro por rodada + Lucro Acumulado
            df_historico_acum_plot = df_historico.set_index('rodada').copy()
            df_historico_acum_plot['Lucro Acumulado'] = df_historico_acum_plot['ggr_rodada'].cumsum()
            df_historico_acum_plot['Lucro na Rodada'] = df_historico_acum_plot['ggr_rodada']
            st.line_chart(df_historico_acum_plot[['Lucro na Rodada', 'Lucro Acumulado']], 
                          color=["#006400", "#90ee90"]) 

        with g_col2:
            st.subheader("Faturamento vs. Pagamentos")
            df_faturamento_pagamentos = df_historico.set_index('rodada')[['total_apostado_rodada', 'total_pago_rodada']].copy()
            df_faturamento_pagamentos.columns = ['Faturamento', 'Pagamentos']
            st.line_chart(df_faturamento_pagamentos)

        # Nova seção com 3 colunas
        g_col3, g_col4, g_col5 = st.columns(3)
        
        with g_col3:
            st.markdown("### Evolução dos Usuários (%)")
            # A condição len(df_historico) > 1 já está aqui e é a correta
            # Calcular proporções em relação ao total de usuários
            total_usuarios_sim = len(st.session_state.usuarios) # Usar uma variável diferente para evitar conflito
            if total_usuarios_sim > 0: # Adicionar verificação para evitar divisão por zero
                df_usuarios_evolucao = df_historico.set_index('rodada')[['usuarios_lucrativos', 'usuarios_zerados']].copy()
                
                # Converter para percentuais
                df_usuarios_evolucao['Lucrativos (%)'] = (df_usuarios_evolucao['usuarios_lucrativos'] / total_usuarios_sim * 100).round(1)
                df_usuarios_evolucao['Zerados (%)'] = (df_usuarios_evolucao['usuarios_zerados'] / total_usuarios_sim * 100).round(1)
                
                # Usar apenas as colunas de percentual
                df_usuarios_evolucao_perc = df_usuarios_evolucao[['Lucrativos (%)', 'Zerados (%)']].copy()
                st.line_chart(df_usuarios_evolucao_perc, color=["#006400", "#d62728"])  # Verde Escuro, Vermelho
            else:
                st.write("Nenhum usuário na simulação para calcular percentuais.")
        
        with g_col4:
            st.subheader("Usuários Ativos por Perfil")
            # A condição len(df_historico) > 1 já está aqui e é a correta
            # Criar DataFrame com usuários ativos por perfil
            dados_perfil = []
            for _, row in df_historico.iterrows():
                linha_perfil = {'rodada': row['rodada']}
                for perfil_nome in LISTA_PERFIS: # Renomear para evitar conflito com a variável 'perfil' de st.expander
                    linha_perfil[perfil_nome] = row['usuarios_ativos_por_perfil'][perfil_nome]
                dados_perfil.append(linha_perfil)
            
            df_perfil_evolucao = pd.DataFrame(dados_perfil).set_index('rodada') 
            cores_perfil_corrigidas_final = ["#d62728", "#20B2AA", "#FFD700"]

            st.line_chart(df_perfil_evolucao, color=cores_perfil_corrigidas_final)
        
        with g_col5:
            st.subheader("Saldo Médio dos Usuários")
            # A condição len(df_historico) > 1 será verificada pelo if geral no início desta seção
            df_saldo_medio = df_historico.set_index('rodada')[['saldo_medio_fim_rodada']].copy()
            df_saldo_medio.columns = ['Saldo Médio']
            st.line_chart(df_saldo_medio, color=["#2ca02c"]) # Verde
    else:
        st.write("Execute pelo menos 2 rodadas para visualizar os gráficos de evolução.")


    # Seletor de rodada e detalhes
    st.markdown("--- ") # Adicionando um separador
    st.header("🔍 Explorar Jogos e Apostas por Rodada") # Adicionando um header para a seção
    if st.session_state.historico_jogos:
        # Seletor de rodada
        rodadas_disponiveis = [h["rodada"] for h in st.session_state.historico_jogos]
        rodada_selecionada = st.selectbox(
            "Selecione a rodada para visualizar:",
            options=rodadas_disponiveis,
            index=len(rodadas_disponiveis)-1,  # Última rodada por padrão
            format_func=lambda x: f"Rodada {x}"
        )
        
        # Encontrar dados da rodada selecionada
        jogos_rodada_selecionada = next(h["jogos"] for h in st.session_state.historico_jogos if h["rodada"] == rodada_selecionada)
        apostas_rodada_selecionada = next(h["apostas"] for h in st.session_state.historico_apostas if h["rodada"] == rodada_selecionada)
        
        # Tabs para jogos e apostas
        tab_jogos, tab_apostas = st.tabs(["🎮 Jogos", "💰 Apostas"])
        
        with tab_jogos:
            st.subheader(f"Jogos da Rodada {rodada_selecionada}")
            if jogos_rodada_selecionada:
                df_jogos = pd.DataFrame(jogos_rodada_selecionada)
                st.dataframe(df_jogos, 
                             column_config={
                                 "id_jogo": st.column_config.TextColumn("ID", width="small"),
                                 "descricao": st.column_config.TextColumn("Jogo", width="small"),
                                 "resultados_possiveis": st.column_config.ListColumn("Resultados", width="medium"),
                                 "probabilidades_reais": st.column_config.ListColumn("Probs Reais", help="Probabilidades reais de cada resultado", width="medium"),
                                 "odds_casa": st.column_config.ListColumn("Odds da Casa", width="medium"),
                                 "resultado_final": st.column_config.TextColumn("Vencedor", width="small"),
                                 "idx_resultado_final": None # Ocultar coluna
                             }, use_container_width=True, hide_index=True)
            else:
                st.write("Nenhum jogo encontrado para esta rodada.")
        
        with tab_apostas:
            st.subheader(f"Apostas da Rodada {rodada_selecionada}")
            if apostas_rodada_selecionada:
                # Criar DataFrame com todas as apostas e adicionar nome do usuário
                df_apostas = pd.DataFrame(apostas_rodada_selecionada)
                # Adicionar coluna com nome do usuário
                df_apostas['nome_usuario'] = df_apostas['id_usuario'].apply(
                    lambda user_id: next(u['nome'] for u in st.session_state.usuarios if u['id'] == user_id)
                )
                
                # Métricas da rodada selecionada
                total_apostas = len(df_apostas)
                total_apostado = df_apostas['valor_apostado'].sum()
                total_ganho = df_apostas['valor_ganho'].sum()
                apostas_vencedoras = df_apostas['ganhou'].sum()
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total de Apostas", total_apostas)
                col2.metric("Total Faturado", f"R$ {total_apostado:.2f}")
                col3.metric("Total Pago", f"R$ {total_ganho:.2f}")
                col4.metric("Apostas Vencedoras", f"{apostas_vencedoras}/{total_apostas}")
                
                # Reordenar colunas para mostrar usuário primeiro
                colunas_apostas_ordenadas = [
                    "nome_usuario", "perfil_usuario", "jogo_desc", "resultado_apostado", 
                    "valor_apostado", "odd_no_momento", "ganhou", "valor_ganho"
                ]
                df_apostas_ordenado = df_apostas[colunas_apostas_ordenadas]
                
                st.dataframe(df_apostas_ordenado,
                             column_config={
                                 "nome_usuario": st.column_config.TextColumn("Usuário", width="medium"),
                                 "perfil_usuario": st.column_config.TextColumn("Perfil", width="small"),
                                 "jogo_desc": st.column_config.TextColumn("Jogo", width="small"),
                                 "resultado_apostado": st.column_config.TextColumn("Aposta", width="medium"),
                                 "valor_apostado": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", width="small"),
                                 "odd_no_momento": st.column_config.NumberColumn("Odd", format="%.2f", width="small"),
                                 "ganhou": st.column_config.CheckboxColumn("Ganhou?", width="small"),
                                 "valor_ganho": st.column_config.NumberColumn("Prêmio (R$)", format="R$ %.2f", width="small")
                             }, use_container_width=True, hide_index=True)
            else:
                st.write("Nenhuma aposta encontrada para esta rodada.")
    else:
        st.write("Nenhuma rodada foi realizada ainda. Execute pelo menos uma rodada para visualizar os dados.")
            
    st.markdown("--- ") # Adicionando um separador
    st.header("👤 Detalhes dos Usuários") # Adicionando um header para a seção
    if st.session_state.usuarios:
        # Calcular número de apostas por usuário
        df_usuarios = pd.DataFrame(st.session_state.usuarios)
        
        # Contar apostas por usuário em todo o histórico
        apostas_por_usuario = {}
        for rodada_apostas in st.session_state.historico_apostas:
            for aposta in rodada_apostas["apostas"]:
                user_id = aposta["id_usuario"]
                apostas_por_usuario[user_id] = apostas_por_usuario.get(user_id, 0) + 1
        
        # Adicionar coluna de número de apostas
        df_usuarios['num_apostas_total'] = df_usuarios['id'].map(lambda x: apostas_por_usuario.get(x, 0))
        
        # Reordenar colunas para melhor visualização
        colunas_ordenadas = [
            "nome", "perfil", "saldo", "num_apostas_total", "rodadas_apostou", 
            "total_apostado_pessoal", "balanco_pessoal"
        ]
        df_usuarios_ordenado = df_usuarios[colunas_ordenadas]
        
        st.dataframe(df_usuarios_ordenado,
                     column_config={
                         "nome": st.column_config.TextColumn("Nome", width="medium"),
                         "perfil": st.column_config.TextColumn("Perfil", width="small"),
                         "saldo": st.column_config.NumberColumn("Saldo (R$)", format="R$ %.2f", width="small",
                            help="Saldo atual do usuário."),
                         "num_apostas_total": st.column_config.NumberColumn("Nº de Apostas Feitas", width="small",
                            help="Número total de apostas feitas pelo usuário."),
                         "rodadas_apostou": st.column_config.NumberColumn("Nº Rodadas C/ Aposta", width="small"),
                         "total_apostado_pessoal": st.column_config.NumberColumn("Total Faturado (R$)", format="R$ %.2f", width="small"),
                         "balanco_pessoal": st.column_config.NumberColumn("Balanço Pessoal (R$)", format="R$ %.2f", width="small",
                            help="Ganhos - Perdas.")
                     }, use_container_width=True, height=400, hide_index=True)
            
    st.markdown("--- ") # Adicionando um separador
    st.header("📊 Histórico Individual do Usuário") # Adicionando um header para a seção
    if st.session_state.usuarios and st.session_state.historico_apostas:
        # Seletor de usuário (ordenado alfabeticamente)
        usuarios_opcoes = [(u['id'], u['nome']) for u in st.session_state.usuarios]
        usuarios_opcoes_ordenadas = sorted(usuarios_opcoes, key=lambda x: x[1])  # Ordenar por nome
        usuario_selecionado_id = st.selectbox(
            "Selecione o usuário para visualizar o histórico:",
            options=[u[0] for u in usuarios_opcoes_ordenadas],
            format_func=lambda x: next(u[1] for u in usuarios_opcoes_ordenadas if u[0] == x),
            key="select_usuario_historico"
        )
        
        if usuario_selecionado_id is not None:
            # Buscar dados do usuário selecionado
            usuario_selecionado = next(u for u in st.session_state.usuarios if u['id'] == usuario_selecionado_id)
            
            # Coletar todas as apostas do usuário
            apostas_usuario = []
            for rodada_apostas in st.session_state.historico_apostas:
                for aposta in rodada_apostas["apostas"]:
                    if aposta["id_usuario"] == usuario_selecionado_id:
                        aposta_com_rodada = aposta.copy()
                        aposta_com_rodada["rodada"] = rodada_apostas["rodada"]
                        apostas_usuario.append(aposta_com_rodada)
            
            if apostas_usuario:
                # Métricas do usuário
                st.markdown(f"### 📈 Estatísticas de {usuario_selecionado['nome']}")
                
                hist_col1, hist_col2, hist_col3, hist_col4, hist_col5 = st.columns(5)
                
                total_apostas_usuario = len(apostas_usuario)
                total_apostado_usuario = sum(a['valor_apostado'] for a in apostas_usuario)
                total_ganho_usuario = sum(a['valor_ganho'] for a in apostas_usuario)
                apostas_vencedoras_usuario = sum(1 for a in apostas_usuario if a['ganhou'])
                taxa_acerto_usuario = (apostas_vencedoras_usuario / total_apostas_usuario * 100) if total_apostas_usuario > 0 else 0
                
                hist_col1.metric("Total de Apostas", total_apostas_usuario)
                hist_col2.metric("Total Apostado", f"R$ {total_apostado_usuario:.2f}")
                hist_col3.metric("Total Ganho", f"R$ {total_ganho_usuario:.2f}")
                hist_col4.metric("Taxa de Acerto", f"{taxa_acerto_usuario:.1f}%")
                hist_col5.metric("Lucro/Prejuízo", f"R$ {total_ganho_usuario - total_apostado_usuario:.2f}")
                
                st.markdown("---")
                
                # Tabela com histórico completo
                st.markdown("### 📋 Histórico Completo de Apostas")
                
                # Preparar dados para a tabela
                historico_dados = []
                for aposta in sorted(apostas_usuario, key=lambda x: x['rodada'], reverse=True):
                    historico_dados.append({
                        "Rodada": aposta['rodada'],
                        "Jogo": aposta['jogo_desc'],
                        "Aposta": aposta['resultado_apostado'],
                        "Valor": f"R$ {aposta['valor_apostado']:.2f}",
                        "Odd": f"{aposta['odd_no_momento']:.2f}",
                        "Resultado": "✅" if aposta['ganhou'] else "❌",
                        "Prêmio": f"R$ {aposta['valor_ganho']:.2f}",
                        "Lucro": f"R$ {aposta['valor_ganho'] - aposta['valor_apostado']:.2f}"
                    })
                
                df_historico_usuario = pd.DataFrame(historico_dados)
                st.dataframe(df_historico_usuario,
                             column_config={
                                 "Rodada": st.column_config.NumberColumn("Rodada", width="small"),
                                 "Jogo": st.column_config.TextColumn("Jogo", width="small"),
                                 "Aposta": st.column_config.TextColumn("Aposta", width="medium"),
                                 "Valor": st.column_config.TextColumn("Valor", width="small"),
                                 "Odd": st.column_config.TextColumn("Odd", width="small"),
                                 "Resultado": st.column_config.TextColumn("Resultado", width="small"),
                                 "Prêmio": st.column_config.TextColumn("Prêmio", width="small"),
                                 "Lucro": st.column_config.TextColumn("Lucro/Prejuízo", width="small")
                             }, use_container_width=True, hide_index=True)
                
                # Gráfico de saldo por rodada (se houver múltiplas rodadas)
                rodadas_usuario = sorted(list(set(a['rodada'] for a in apostas_usuario)))
                if len(rodadas_usuario) > 1:
                    st.markdown("### 📈 Saldo por Rodada")
                    
                    # Calcular saldo ao final de cada rodada para TODOS os usuários
                    saldo_inicial_ref = getattr(st.session_state, 'saldo_inicial', 100.0)
                    
                    # Coletar todas as rodadas que existem
                    todas_rodadas = set()
                    for rodada_apostas in st.session_state.historico_apostas:
                        todas_rodadas.add(rodada_apostas["rodada"])
                    todas_rodadas = sorted(list(todas_rodadas))
                    
                    # Criar DataFrame com saldo de todos os usuários por rodada
                    dados_todos_usuarios = {}
                    dados_usuario_selecionado = {}
                    
                    # Incluir rodada 0 (inicial) para mostrar o ponto de partida
                    rodadas_para_grafico = [0] + todas_rodadas
                    
                    for usuario in st.session_state.usuarios:
                        # Coletar apostas deste usuário
                        apostas_user = []
                        for rodada_apostas in st.session_state.historico_apostas:
                            for aposta in rodada_apostas["apostas"]:
                                if aposta["id_usuario"] == usuario['id']:
                                    aposta_com_rodada = aposta.copy()
                                    aposta_com_rodada["rodada"] = rodada_apostas["rodada"]
                                    apostas_user.append(aposta_com_rodada)
                        
                        # Calcular saldo por rodada para este usuário
                        saldo_atual = saldo_inicial_ref
                        dados_saldo_user = [saldo_inicial_ref]  # Começar com saldo inicial
                        
                        for rodada in todas_rodadas:
                            # Calcular resultado da rodada
                            apostas_rodada = [a for a in apostas_user if a['rodada'] == rodada]
                            resultado_rodada = sum(a['valor_ganho'] - a['valor_apostado'] for a in apostas_rodada)
                            saldo_atual += resultado_rodada
                            dados_saldo_user.append(saldo_atual)
                        
                        # Separar usuário selecionado dos outros
                        nome_usuario = usuario['nome']
                        if usuario['id'] == usuario_selecionado_id:
                            dados_usuario_selecionado[nome_usuario] = dados_saldo_user
                        else:
                            dados_todos_usuarios[nome_usuario] = dados_saldo_user
                    
                    # Criar gráfico com plotly
                    fig = go.Figure()
                    
                    # Primeiro adicionar as linhas cinzas (outros usuários)
                    for nome_usuario, dados_saldo in dados_todos_usuarios.items():
                        fig.add_trace(go.Scatter(
                            x=rodadas_para_grafico,
                            y=dados_saldo,
                            mode='lines',
                            name=nome_usuario,
                            line=dict(color='rgba(192, 192, 192, 0.5)', width=1),
                            showlegend=False,
                            hovertemplate=f'<b>{nome_usuario}</b><br>Rodada: %{{x}}<br>Saldo: R$ %{{y:.2f}}<extra></extra>'
                        ))
                    
                    # Depois adicionar a linha verde do usuário selecionado (por cima)
                    usuario_selecionado_nome = next(u['nome'] for u in st.session_state.usuarios if u['id'] == usuario_selecionado_id)
                    if dados_usuario_selecionado:
                        for nome_usuario, dados_saldo in dados_usuario_selecionado.items():
                            fig.add_trace(go.Scatter(
                                x=rodadas_para_grafico,
                                y=dados_saldo,
                                mode='lines',
                                name=f'{nome_usuario} (Selecionado)',
                                line=dict(color='#2ca02c', width=3),
                                showlegend=False,
                                hovertemplate=f'<b>{nome_usuario} (Selecionado)</b><br>Rodada: %{{x}}<br>Saldo: R$ %{{y:.2f}}<extra></extra>'
                            ))
                    
                    # Adicionar linha horizontal do saldo inicial
                    fig.add_hline(y=saldo_inicial_ref, line_dash="dash", line_color="green", 
                                 opacity=0.5, annotation_text=f"Saldo Inicial (R$ {saldo_inicial_ref:.2f})")
                    
                    # Configurar layout
                    fig.update_layout(
                        title="Evolução do Saldo - Todos os Usuários",
                        xaxis_title="Rodada",
                        yaxis_title="Saldo (R$)", 
                        showlegend=False,
                        height=500
                    )
                    
                    # Mostrar gráfico
                    st.plotly_chart(fig, use_container_width=True)
                    
            else:
                st.write(f"{usuario_selecionado['nome']} ainda não fez nenhuma aposta.")
    else:
        st.write("Nenhum usuário ou histórico de apostas disponível.")