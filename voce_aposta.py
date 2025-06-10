import streamlit as st
import numpy as np
import pandas as pd
import random

# --- Configurações e Constantes ---
SALDO_INICIAL = 100.0
VALOR_APOSTA_MINIMA = 5.0

# Times brasileiros famosos
TIMES_BRASILEIROS = [
    "Flamengo", "Palmeiras", "Corinthians", "São Paulo", 
    "Santos", "Vasco", "Botafogo", "Fluminense", 
    "Atlético-MG", "Cruzeiro", "Grêmio", "Internacional", 
    "Bahia", "Sport", "Ceará", "Fortaleza",
    "Athletico-PR", "Coritiba", "Chapecoense", "Avaí"
]

# --- Funções Auxiliares ---

def gerar_probabilidades_futebol():
    """Gera probabilidades para jogos de futebol (Vitória, Empate, Derrota)"""
    prob_vitoria = round(random.uniform(0.05, 0.70), 2)
    prob_empate = round(random.uniform(0.10, 0.25), 2)
    prob_derrota = round(1.0 - prob_vitoria - prob_empate, 2)
    
    if prob_derrota < 0:
        prob_empate = round(1.0 - prob_vitoria, 2)
        prob_derrota = 0.0
    
    total = prob_vitoria + prob_empate + prob_derrota
    if total != 1.0:
        prob_derrota = round(1.0 - prob_vitoria - prob_empate, 2)
    
    return [prob_vitoria, prob_empate, prob_derrota]

def calcular_odds_casa(probabilidades_reais, margem_casa=0.05):
    """Calcula as odds da casa com margem"""
    final_odds = []
    for p_real in probabilidades_reais:
        if p_real == 0:
            final_odds.append(999.0)
        else:
            fair_odd = 1 / p_real
            house_odd = round(fair_odd * (1 - margem_casa), 2)
            final_odds.append(max(1.01, house_odd))
    return final_odds

def simular_resultado_jogo(probabilidades_reais):
    """Simula o resultado de um jogo baseado nas probabilidades"""
    resultados = ["Vitória", "Empate", "Derrota"]
    return np.random.choice(resultados, p=probabilidades_reais)

def gerar_jogos_rodada():
    """Gera 6 jogos para a rodada com times brasileiros"""
    jogos = []
    times_usados = []
    
    for i in range(6):
        # Selecionar dois times diferentes que ainda não foram usados
        times_disponiveis = [t for t in TIMES_BRASILEIROS if t not in times_usados]
        time_casa = random.choice(times_disponiveis)
        times_disponiveis.remove(time_casa)
        time_fora = random.choice(times_disponiveis)
        
        times_usados.extend([time_casa, time_fora])
        
        probabilidades = gerar_probabilidades_futebol()
        odds = calcular_odds_casa(probabilidades)
        
        jogos.append({
            "id": i,
            "time_casa": time_casa,
            "time_fora": time_fora,
            "probabilidades": probabilidades,
            "odds_vitoria": odds[0],
            "odds_empate": odds[1],
            "odds_derrota": odds[2],
            "resultado": None  # Será definido quando calcular
        })
    
    return jogos

# --- Inicialização do Estado da Sessão ---
if 'voce_aposta_iniciado' not in st.session_state:
    st.session_state.voce_aposta_iniciado = False
    st.session_state.saldo_jogador = SALDO_INICIAL
    st.session_state.jogos_atual = []
    st.session_state.apostas_jogador = {}
    st.session_state.apostas_selecionadas = {}  # Para tracking das pills selecionadas
    st.session_state.historico_rodadas = []
    st.session_state.rodada_atual = 0
    st.session_state.aguardando_resultado = False

# --- Interface Principal ---
st.title("🎲 Você Aposta!")
st.badge('Página ainda em Construção!', icon='🚧', color='red')
st.divider()
# Mostrar descrição apenas se não começou a jogar
if not st.session_state.voce_aposta_iniciado:
    st.markdown("**Comece com R$ 100 e teste suas habilidades com os maiores times do Brasil!**")

# --- Sidebar com Controles ---
with st.sidebar:
    st.header("🎮 Controles")
    
    # Botão principal baseado no estado atual
    if not st.session_state.voce_aposta_iniciado:
        # Estado inicial - mostrar botão de começar
        if st.button("🎮 Começar a Jogar", type="primary", use_container_width=True):
            st.session_state.voce_aposta_iniciado = True
            st.session_state.jogos_atual = gerar_jogos_rodada()
            st.session_state.apostas_jogador = {}
            st.session_state.apostas_selecionadas = {}
            st.session_state.rodada_atual += 1
            st.session_state.aguardando_resultado = False
            st.rerun()
    
    elif st.session_state.aguardando_resultado:
        # Estado vendo resultados - mostrar botão de próxima rodada
        if st.session_state.saldo_jogador >= VALOR_APOSTA_MINIMA:
            if st.button("⚽ Próxima Rodada", type="primary", use_container_width=True):
                st.session_state.jogos_atual = gerar_jogos_rodada()
                st.session_state.apostas_jogador = {}
                st.session_state.apostas_selecionadas = {}
                st.session_state.rodada_atual += 1
                st.session_state.aguardando_resultado = False
                st.rerun()
        else:
            st.error("💸 Saldo insuficiente para continuar!")
            st.write("Você precisa resetar o jogo para jogar novamente.")
    
    else:
        # Estado apostando - mostrar botão de computar rodada
        tem_apostas = bool(st.session_state.apostas_jogador)
        if st.button(f"🏆 Computar Rodada {st.session_state.rodada_atual}", 
                    type="primary" if tem_apostas else "secondary",
                    disabled=not tem_apostas,
                    use_container_width=True):
            # Simular resultados dos jogos
            total_ganho = 0.0
            total_apostado = sum(float(valor) for valor in st.session_state.apostas_jogador.values())
            resultados_detalhados = []
            
            for jogo in st.session_state.jogos_atual:
                resultado = simular_resultado_jogo(jogo["probabilidades"])
                jogo["resultado"] = resultado
            
            # Criar resultados para TODOS os jogos (apostados ou não)
            for jogo in st.session_state.jogos_atual:
                jogo_id = jogo["id"]
                
                # Verificar se há apostas neste jogo
                apostas_do_jogo = {}
                for aposta_key, valor_aposta in st.session_state.apostas_jogador.items():
                    if aposta_key.startswith(f"{jogo_id}_"):
                        tipo_aposta = aposta_key.split("_")[1]
                        apostas_do_jogo[tipo_aposta] = valor_aposta
                
                if apostas_do_jogo:
                    # Há apostas neste jogo - processar cada uma
                    for tipo_aposta, valor_aposta in apostas_do_jogo.items():
                        ganho = 0.0
                        acertou = False
                        
                        # Verificar se acertou
                        if ((tipo_aposta == "vitoria" and jogo["resultado"] == "Vitória") or
                            (tipo_aposta == "empate" and jogo["resultado"] == "Empate") or
                            (tipo_aposta == "derrota" and jogo["resultado"] == "Derrota")):
                            
                            if tipo_aposta == "vitoria":
                                ganho = valor_aposta * jogo["odds_vitoria"]
                            elif tipo_aposta == "empate":
                                ganho = valor_aposta * jogo["odds_empate"]
                            elif tipo_aposta == "derrota":
                                ganho = valor_aposta * jogo["odds_derrota"]
                            
                            total_ganho += ganho
                            acertou = True
                        
                        resultados_detalhados.append({
                            "jogo": f"{jogo['time_casa']} vs {jogo['time_fora']}",
                            "resultado": jogo["resultado"],
                            "aposta": tipo_aposta.title(),
                            "valor_apostado": valor_aposta,
                            "ganho": ganho,
                            "status": "✅ Acertou" if acertou else "❌ Errou"
                        })
                else:
                    # Não há apostas neste jogo
                    resultados_detalhados.append({
                        "jogo": f"{jogo['time_casa']} vs {jogo['time_fora']}",
                        "resultado": jogo["resultado"],
                        "aposta": "-",
                        "valor_apostado": 0.0,
                        "ganho": 0.0,
                        "status": "🚫 Sem aposta"
                    })
            
            # Atualizar saldo
            st.session_state.saldo_jogador = st.session_state.saldo_jogador - total_apostado + total_ganho
            
            # Salvar no histórico
            st.session_state.historico_rodadas.append({
                "rodada": st.session_state.rodada_atual,
                "total_apostado": total_apostado,
                "total_ganho": total_ganho,
                "lucro": total_ganho - total_apostado,
                "resultados": resultados_detalhados,
                "jogos": st.session_state.jogos_atual.copy()
            })
            
            st.session_state.aguardando_resultado = True
            st.rerun()
        
        if not tem_apostas:
            st.info("💡 Faça pelo menos uma aposta para computar a rodada.")
    
    # Botão de resetar sempre disponível quando o jogo estiver iniciado
    if st.session_state.voce_aposta_iniciado:
        st.divider()
        if st.button("🔄 Resetar Jogo", use_container_width=True):
            st.session_state.voce_aposta_iniciado = False
            st.session_state.saldo_jogador = SALDO_INICIAL
            st.session_state.jogos_atual = []
            st.session_state.apostas_jogador = {}
            st.session_state.apostas_selecionadas = {}
            st.session_state.historico_rodadas = []
            st.session_state.rodada_atual = 0
            st.session_state.aguardando_resultado = False
            st.rerun()

# --- Métricas do Cabeçalho ---
if st.session_state.voce_aposta_iniciado:
    # Calcular estatísticas
    total_apostado_historico = sum(r['total_apostado'] for r in st.session_state.historico_rodadas)
    total_ganho_historico = sum(r['total_ganho'] for r in st.session_state.historico_rodadas)
    lucro_total = total_ganho_historico - total_apostado_historico
    
    # Calcular porcentagem de lucro
    if total_apostado_historico > 0:
        lucro_percentual = (lucro_total / total_apostado_historico) * 100
    else:
        lucro_percentual = 0.0
    
    # Calcular quantidade e porcentagem de apostas ganhas
    total_apostas_feitas = sum(len([r for r in rodada['resultados'] if r['aposta'] != '-']) for rodada in st.session_state.historico_rodadas)
    apostas_ganhas = sum(sum(1 for resultado in r['resultados'] if resultado['status'] == '✅ Acertou') for r in st.session_state.historico_rodadas)
    
    if total_apostas_feitas > 0:
        percentual_apostas_ganhas = (apostas_ganhas / total_apostas_feitas) * 100
    else:
        percentual_apostas_ganhas = 0.0
    
    # Exibir métricas em uma linha de 6 colunas
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("💰 Saldo Inicial", f"R$ {SALDO_INICIAL:.2f}")
    with col2:
        st.metric("💵 Saldo Atual", f"R$ {st.session_state.saldo_jogador:.2f}")
    with col3:
        delta_lucro = f"R$ {lucro_total:.2f}" if lucro_total != 0 else None
        st.metric("📈 Lucro Total", f"R$ {lucro_total:.2f}", delta=delta_lucro)
    with col4:
        delta_perc = f"{lucro_percentual:.1f}%" if lucro_percentual != 0 else None
        st.metric("📊 Lucro %", f"{lucro_percentual:.1f}%", delta=delta_perc)
    with col5:
        st.metric("🎯 Apostas Feitas", f"{total_apostas_feitas}")
    with col6:
        st.metric("✅ Taxa de Acerto", f"{percentual_apostas_ganhas:.1f}%")

# --- Exibição dos Jogos e Sistema de Apostas ---
if st.session_state.voce_aposta_iniciado and st.session_state.jogos_atual:
    
    if st.session_state.aguardando_resultado:
        # Mostrar resultados da rodada
        st.subheader(f"🏆 Resultados da Rodada {st.session_state.rodada_atual}")
        
        ultima_rodada = st.session_state.historico_rodadas[-1]
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric("💸 Total Apostado", f"R$ {ultima_rodada['total_apostado']:.2f}")
        with col_res2:
            st.metric("💰 Total Ganho", f"R$ {ultima_rodada['total_ganho']:.2f}")
        with col_res3:
            st.metric("📈 Lucro/Prejuízo", f"R$ {ultima_rodada['lucro']:.2f}", delta=f"{ultima_rodada['lucro']:.2f}")
        
        # Tabela completa com todos os jogos da rodada
        if ultima_rodada['resultados']:
            df_resultados = pd.DataFrame(ultima_rodada['resultados'])
            # Reorganizar colunas de forma mais intuitiva
            df_resultados = df_resultados[['jogo', 'resultado', 'aposta', 'valor_apostado', 'ganho', 'status']]
            df_resultados.columns = ['🏟️ Jogo', '⚽ Resultado', '🎯 Aposta', '💸 Valor (R$)', '💰 Ganho (R$)', '📊 Status']
            
            st.dataframe(df_resultados, use_container_width=True, hide_index=True)
    
    else:
        # Interface de apostas
        st.subheader(f"⚽ Jogos Disponíveis - Rodada {st.session_state.rodada_atual} - Escolha suas Apostas!")
        
        if st.session_state.saldo_jogador < VALOR_APOSTA_MINIMA:
            st.error(f"Saldo insuficiente! Você precisa de pelo menos R$ {VALOR_APOSTA_MINIMA:.2f} para apostar.")
        else:
            # Layout 2x3 para os jogos
            for linha in range(2):
                cols = st.columns(3)
                for col_idx in range(3):
                    jogo_idx = linha * 3 + col_idx
                    if jogo_idx < len(st.session_state.jogos_atual):
                        jogo = st.session_state.jogos_atual[jogo_idx]
                        
                        with cols[col_idx]:
                            # Header do jogo - simplificado
                            st.markdown(f"""
                            <div style="border: 1px solid #28a745; border-radius: 8px; padding: 10px; text-align: center; background-color: #f8f9fa; margin-bottom: 10px;">
                                <strong>{jogo['time_casa']} vs {jogo['time_fora']}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Pills para as odds
                            opcoes_odds = [
                                f"🏠 {jogo['odds_vitoria']:.2f}",
                                f"🤝 {jogo['odds_empate']:.2f}",
                                f"✈️ {jogo['odds_derrota']:.2f}"
                            ]
                            
                            # Verificar qual opção está selecionada
                            opcao_selecionada = None
                            chave_vitoria = f"{jogo_idx}_vitoria"
                            chave_empate = f"{jogo_idx}_empate"
                            chave_derrota = f"{jogo_idx}_derrota"
                            
                            if chave_vitoria in st.session_state.apostas_selecionadas:
                                opcao_selecionada = opcoes_odds[0]
                            elif chave_empate in st.session_state.apostas_selecionadas:
                                opcao_selecionada = opcoes_odds[1]
                            elif chave_derrota in st.session_state.apostas_selecionadas:
                                opcao_selecionada = opcoes_odds[2]
                            
                            # Pills para seleção
                            pill_selecionada = st.pills(
                                "Odds:",
                                opcoes_odds,
                                default=opcao_selecionada,
                                key=f"pills_{jogo_idx}"
                            )
                            
                            # Se uma pill foi selecionada, mostrar slider para valor
                            if pill_selecionada:
                                # Determinar o tipo de aposta
                                if "🏠" in pill_selecionada:
                                    tipo_aposta = "vitoria"
                                    chave_aposta = chave_vitoria
                                elif "🤝" in pill_selecionada:
                                    tipo_aposta = "empate"
                                    chave_aposta = chave_empate
                                else:
                                    tipo_aposta = "derrota"
                                    chave_aposta = chave_derrota
                                
                                # Marcar como selecionada
                                st.session_state.apostas_selecionadas[chave_aposta] = True
                                
                                # Slider para valor da aposta e ganho potencial em duas colunas
                                col_valor, col_ganho = st.columns(2)
                                
                                with col_valor:
                                    valor_atual = st.session_state.apostas_jogador.get(chave_aposta, 0.0)
                                    valor_aposta = st.slider(
                                        f"Valor (R$)",
                                        min_value=0.0,
                                        max_value=float(st.session_state.saldo_jogador),
                                        value=valor_atual,
                                        step=5.0,
                                        key=f"valor_{chave_aposta}"
                                    )
                                
                                with col_ganho:
                                    if valor_aposta > 0:
                                        # Calcular ganho potencial
                                        if tipo_aposta == "vitoria":
                                            ganho_potencial = valor_aposta * jogo['odds_vitoria']
                                        elif tipo_aposta == "empate":
                                            ganho_potencial = valor_aposta * jogo['odds_empate']
                                        else:
                                            ganho_potencial = valor_aposta * jogo['odds_derrota']
                                        
                                        st.metric("Ganho Potencial", f"R$ {ganho_potencial:.2f}")
                                        st.session_state.apostas_jogador[chave_aposta] = valor_aposta
                                    else:
                                        st.metric("Ganho Potencial", "R$ 0,00")
                                        if chave_aposta in st.session_state.apostas_jogador:
                                            del st.session_state.apostas_jogador[chave_aposta]
                            else:
                                # Remover seleções anteriores se nenhuma pill está selecionada
                                for chave in [chave_vitoria, chave_empate, chave_derrota]:
                                    if chave in st.session_state.apostas_selecionadas:
                                        del st.session_state.apostas_selecionadas[chave]
                                    if chave in st.session_state.apostas_jogador:
                                        del st.session_state.apostas_jogador[chave]

# --- Histórico de Rodadas (apenas se não estiver no estado inicial) ---
if st.session_state.historico_rodadas and st.session_state.voce_aposta_iniciado:
    st.subheader("📈 Histórico de Desempenho")
    
    # Métricas gerais
    total_apostado_historico = sum(r['total_apostado'] for r in st.session_state.historico_rodadas)
    total_ganho_historico = sum(r['total_ganho'] for r in st.session_state.historico_rodadas)
    lucro_total = total_ganho_historico - total_apostado_historico
    
    col_hist1, col_hist2, col_hist3, col_hist4 = st.columns(4)
    with col_hist1:
        st.metric("🎯 Rodadas Jogadas", len(st.session_state.historico_rodadas))
    with col_hist2:
        st.metric("💸 Total Apostado", f"R$ {total_apostado_historico:.2f}")
    with col_hist3:
        st.metric("💰 Total Ganho", f"R$ {total_ganho_historico:.2f}")
    with col_hist4:
        st.metric("📊 Lucro Total", f"R$ {lucro_total:.2f}")
    
    # Tabela do histórico
    with st.expander("📋 Detalhes do Histórico", expanded=False):
        df_historico = pd.DataFrame([
            {
                "Rodada": r['rodada'],
                "Apostado (R$)": r['total_apostado'],
                "Ganho (R$)": r['total_ganho'],
                "Lucro (R$)": r['lucro']
            }
            for r in st.session_state.historico_rodadas
        ])
        st.dataframe(df_historico, use_container_width=True, hide_index=True)

# Instruções para usuários novos
if not st.session_state.voce_aposta_iniciado:
    st.subheader("🎯 Como Jogar")
    
    col_inst1, col_inst2 = st.columns(2)
    
    with col_inst1:
        st.markdown("""
        **📋 Instruções:**
        
        1. **🎮 Começar**: Clique em "Começar a Jogar" na sidebar
        2. **⚽ Apostar**: Escolha as odds clicando nas pills
        3. **💰 Valor**: Use o slider para definir o valor da aposta
        4. **🏆 Computar**: Clique em "Computar Rodada" para ver resultados
        5. **🔄 Continuar**: Use "Próxima Rodada" para jogar mais
        """)
    
    with col_inst2:
        st.markdown("""
        **💡 Dicas:**
        
        - Você começa com **R$ 100,00**
        - Aposta mínima: **R$ 5,00**
        - Pode apostar em **quantos jogos quiser**
        - **Ganho potencial** é mostrado em tempo real
        - Use **"Resetar Jogo"** para recomeçar a qualquer momento
        """) 