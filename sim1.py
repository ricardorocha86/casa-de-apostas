import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from formatacao import brl, formatar_brl, numero_br, pct
from simulacao import (
    CORES_PERFIS, ESTRATEGIAS, LISTA_PERFIS, NUM_JOGOS_RODADA,
    criar_simulacao, perfis_config_padrao, simular_rodada,
)

AJUDA_LUCRO = (
    'O "lucro" aqui é o GGR (Gross Gaming Revenue): total apostado − total pago em prêmios. '
    "Não desconta impostos, bônus nem custos operacionais."
)


def nome_resultado(jogo, idx):
    """Traduz o índice do resultado (Vitória/Empate/Derrota do mandante) para o nome do vencedor."""
    return [jogo["mandante"], "Empate", jogo["visitante"]][idx]


# --- Estado da Sessão ---
if "perfis_config" not in st.session_state:
    st.session_state.perfis_config = perfis_config_padrao()
perfis_config = st.session_state.perfis_config
sim = st.session_state.get("sim")
iniciada = sim is not None

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Controles da Simulação")

    num_usuarios_input = st.number_input(
        "Número de Usuários Iniciais", min_value=1, max_value=1000, step=10,
        value=len(sim["usuarios"]) if iniciada else 100, disabled=iniciada,
    )
    saldo_inicial_input = st.number_input(
        "Saldo Inicial por Usuário (R$)", min_value=10, max_value=1000, step=10,
        value=int(sim["saldo_inicial"]) if iniciada else 100, disabled=iniciada,
    )
    margem_casa_input = st.slider(
        "Margem da Casa nas Odds (%)", min_value=0.0, max_value=20.0, step=0.1, format="%.1f%%",
        value=sim["margem_casa"] * 100 if iniciada else 5.0, disabled=iniciada,
    ) / 100.0

    st.subheader("Comportamento dos Usuários")
    st.caption("Parâmetros por perfil de apostador. Alterações valem a partir da próxima rodada.")
    for perfil in LISTA_PERFIS:
        cfg = perfis_config[perfil]
        with st.expander(f"**Perfil: {perfil}**", expanded=False):
            cfg["prob_decidir_apostar"] = st.slider(
                "Probabilidade de Decidir Apostar",
                min_value=0.05, max_value=1.0, step=0.05, format="%.2f",
                value=cfg["prob_decidir_apostar"], key=f"prob_apostar_{perfil}",
            )
            cfg["lambda_poisson"] = st.slider(
                "Média de Apostas Desejadas (λ)",
                min_value=0.5, max_value=7.0, step=0.1,
                value=cfg["lambda_poisson"], key=f"lambda_{perfil}",
                help="Distribuição Poisson truncada em 1 - sempre faz pelo menos 1 aposta se decidir apostar",
            )
            cfg["estrategia"] = st.selectbox(
                "Estratégia de Aposta",
                ESTRATEGIAS,
                index=ESTRATEGIAS.index(cfg["estrategia"]), key=f"estrategia_{perfil}",
                help=(
                    "Em qual resultado do jogo sorteado o usuário aposta (sorteio uniforme):  \n"
                    "Favorito: menor odd ou intermediária  \n"
                    "Aleatório: qualquer um dos três resultados  \n"
                    "Zebra: intermediária ou maior odd"
                ),
            )

    col1_btn, col2_btn = st.columns(2)
    rodar_1 = col1_btn.button("▶️ 1 Rodada", type="primary", use_container_width=True)
    rodar_10 = col2_btn.button("⏩ 10 Rodadas", type="primary", use_container_width=True)
    resetar = st.button("🔄 Resetar Simulação", use_container_width=True, disabled=not iniciada)

    if rodar_1 or rodar_10:
        if not iniciada:
            st.session_state.sim = criar_simulacao(num_usuarios_input, saldo_inicial_input, margem_casa_input)
        for _ in range(10 if rodar_10 else 1):
            simular_rodada(st.session_state.sim, perfis_config)
        st.rerun()

    if resetar:
        # Mantém as configurações dos perfis, descarta a simulação
        del st.session_state.sim
        st.rerun()

# --- Painel Principal ---
st.title("🎲 Simulador Principal: Os números 'ocultos' da casa de apostas!")

if not iniciada:
    st.info("👈 Configure os parâmetros na barra lateral e clique em **▶️ 1 Rodada** ou **⏩ 10 Rodadas**.")
    st.stop()

usuarios = sim["usuarios"]
rodadas = sim["rodadas"]
saldo_inicial = sim["saldo_inicial"]
ultima = rodadas[-1]
stats = ultima["stats"]
df_historico = pd.DataFrame([r["stats"] for r in rodadas]).set_index("rodada")

st.header(f"📊 Resultados da Rodada {ultima['numero']}")

# PRIMEIRA LINHA - Métricas da Casa/Rodada
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
handle_rodada = stats["total_apostado"]
percentual_ggr = (stats["ggr"] / handle_rodada * 100) if handle_rodada > 0 else 0
m_col1.metric("Faturamento da Rodada", brl(handle_rodada))
m_col2.metric("Pagamentos da Rodada", brl(stats["total_pago"]))
m_col3.metric('"Lucro" da Rodada', brl(stats["ggr"]), delta=pct(percentual_ggr), help=AJUDA_LUCRO)
m_col4.metric("Nº de Apostas", numero_br(stats["num_apostas"], 0))
m_col5.metric("Valor Médio Apostado", brl(handle_rodada / stats["num_apostas"] if stats["num_apostas"] else 0))

# SEGUNDA LINHA - Métricas dos Usuários
u_col1, u_col2, u_col3, u_col4, u_col5 = st.columns(5)
u_col1.metric("Total de Usuários", numero_br(len(usuarios), 0))
u_col2.metric("Usuários Lucrativos", numero_br(stats["usuarios_lucrativos"], 0),
              help=f"Saldo acima do inicial ({brl(saldo_inicial)})")
u_col3.metric("Usuários Ativos", numero_br(stats["usuarios_ativos"], 0), help="Saldo > R$ 0,00 (ainda tem dinheiro)")
u_col4.metric("Usuários Falidos", numero_br(stats["usuarios_zerados"], 0), help="Saldo = R$ 0,00 (sem dinheiro)")
u_col5.metric("Saldo Médio", brl(stats["saldo_medio"]))

# TERCEIRA LINHA - Volume por perfil
v_cols = st.columns(5)
for col, perfil in zip(v_cols, LISTA_PERFIS):
    col.metric(f"Volume {perfil}", brl(stats["apostado_por_perfil"][perfil]))
st.markdown("---")

analise_col1, analise_col2 = st.columns([1, 1.3], gap="large")

with analise_col1:
    st.markdown("#### 🎮 Jogos e Odds da Rodada")
    volume_por_jogo = [0.0] * NUM_JOGOS_RODADA
    for a in ultima["apostas"]:
        volume_por_jogo[a["idx_jogo"]] += a["valor_apostado"]
    df_jogos = pd.DataFrame([
        {
            "Jogo": jogo["descricao"],
            "Mandante": jogo["odds_casa"][0],
            "Empate": jogo["odds_casa"][1],
            "Visitante": jogo["odds_casa"][2],
            "Resultado": nome_resultado(jogo, jogo["idx_resultado_final"]),
            "Volume": volume_por_jogo[i],
        }
        for i, jogo in enumerate(ultima["jogos"])
    ])
    st.dataframe(
        formatar_brl(df_jogos, ["Volume"]),
        column_config={c: st.column_config.NumberColumn(c, format="%.2f") for c in ["Mandante", "Empate", "Visitante"]},
        use_container_width=True, hide_index=True,
    )

with analise_col2:
    st.markdown("#### 💰 Top 10 Maiores Pagamentos da Rodada")
    if ultima["apostas"]:
        maiores = sorted(ultima["apostas"], key=lambda a: a["valor_ganho"], reverse=True)[:10]
        df_maiores = pd.DataFrame([
            {
                "Usuário": usuarios[a["id_usuario"]]["nome"],
                "Perfil": a["perfil_usuario"],
                "Jogo": a["jogo_desc"],
                "Aposta": nome_resultado(ultima["jogos"][a["idx_jogo"]], a["idx_resultado_apostado"]),
                "Valor": a["valor_apostado"],
                "Odd": a["odd_no_momento"],
                "Pago": a["valor_ganho"],
                "Status": "✅" if a["ganhou"] else "❌",
            }
            for a in maiores
        ])
        st.dataframe(
            formatar_brl(df_maiores, ["Valor", "Pago"]),
            column_config={"Odd": st.column_config.NumberColumn("Odd", format="%.2f")},
            use_container_width=True, hide_index=True,
        )
    else:
        st.write("Nenhuma aposta nesta rodada.")

st.markdown("---")
st.header("📈 Estatísticas Acumuladas da Casa")

total_apostado_acum = df_historico["total_apostado"].sum()
total_pago_acum = df_historico["total_pago"].sum()
ggr_acum = total_apostado_acum - total_pago_acum
margem_realizada = (ggr_acum / total_apostado_acum * 100) if total_apostado_acum > 0 else 0

ac_col1, ac_col2, ac_col3, ac_col4, ac_col5, ac_col6 = st.columns(6)
ac_col1.metric("Faturamento Acumulado", brl(total_apostado_acum))
ac_col2.metric("Pagamentos Acumulados", brl(total_pago_acum))
ac_col3.metric('"Lucro" Acumulado', brl(ggr_acum), delta=brl(ggr_acum), help=AJUDA_LUCRO)
ac_col4.metric(
    'Margem de "Lucro" Acum.', pct(margem_realizada, 2),
    help=f"Margem configurada nas odds: {pct(sim['margem_casa'] * 100)}. "
         "Com muitas apostas, a margem realizada tende a ela.",
)
ac_col5.metric('"Lucro" Médio/Rodada', brl(ggr_acum / len(rodadas)))
ac_col6.metric("Total de Apostas Acum.", numero_br(df_historico["num_apostas"].sum(), 0))

if len(rodadas) > 1:
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.subheader('Evolução do "Lucro" da Casa')
        df_lucro = pd.DataFrame({
            '"Lucro" Acumulado': df_historico["ggr"].cumsum(),
            '"Lucro" na Rodada': df_historico["ggr"],
        })
        st.line_chart(df_lucro, color=["#006400", "#90ee90"])

    with g_col2:
        st.subheader("Faturamento vs. Pagamentos")
        df_fat_pag = df_historico[["total_apostado", "total_pago"]].rename(
            columns={"total_apostado": "Faturamento", "total_pago": "Pagamentos"}
        )
        st.line_chart(df_fat_pag)

    g_col3, g_col4, g_col5 = st.columns(3)
    with g_col3:
        st.subheader("Evolução dos Usuários (%)")
        df_usuarios_evolucao = pd.DataFrame({
            "Lucrativos (%)": (df_historico["usuarios_lucrativos"] / len(usuarios) * 100).round(1),
            "Zerados (%)": (df_historico["usuarios_zerados"] / len(usuarios) * 100).round(1),
        })
        st.line_chart(df_usuarios_evolucao, color=["#006400", "#d62728"])

    with g_col4:
        st.subheader("Usuários Ativos por Perfil")
        perfis_ordenados = sorted(LISTA_PERFIS)  # Ordem alfabética = ordem das cores no gráfico
        df_perfil_evolucao = pd.DataFrame(df_historico["usuarios_ativos_por_perfil"].tolist(),
                                          index=df_historico.index)[perfis_ordenados]
        st.line_chart(df_perfil_evolucao, color=[CORES_PERFIS[p] for p in perfis_ordenados])

    with g_col5:
        st.subheader("Saldo Médio dos Usuários")
        st.line_chart(df_historico[["saldo_medio"]].rename(columns={"saldo_medio": "Saldo Médio"}),
                      color=["#2ca02c"])
else:
    st.write("Execute pelo menos 2 rodadas para visualizar os gráficos de evolução.")


st.markdown("---")
st.header("🔍 Explorar Jogos e Apostas por Rodada")
numero_sel = st.selectbox(
    "Selecione a rodada para visualizar:",
    options=[r["numero"] for r in rodadas],
    index=len(rodadas) - 1,
    format_func=lambda x: f"Rodada {x}",
)
rodada_sel = rodadas[numero_sel - 1]

tab_jogos, tab_apostas = st.tabs(["🎮 Jogos", "💰 Apostas"])

with tab_jogos:
    st.subheader(f"Jogos da Rodada {numero_sel}")
    df_jogos_sel = pd.DataFrame([
        {
            "Jogo": jogo["descricao"],
            "P(Mandante)": jogo["probabilidades_reais"][0] * 100,
            "P(Empate)": jogo["probabilidades_reais"][1] * 100,
            "P(Visitante)": jogo["probabilidades_reais"][2] * 100,
            "Odd Mandante": jogo["odds_casa"][0],
            "Odd Empate": jogo["odds_casa"][1],
            "Odd Visitante": jogo["odds_casa"][2],
            "Resultado": nome_resultado(jogo, jogo["idx_resultado_final"]),
        }
        for jogo in rodada_sel["jogos"]
    ])
    config_jogos = {
        c: st.column_config.NumberColumn(c, format="%.0f%%", help="Probabilidade real do resultado")
        for c in ["P(Mandante)", "P(Empate)", "P(Visitante)"]
    }
    config_jogos.update({
        c: st.column_config.NumberColumn(c, format="%.2f")
        for c in ["Odd Mandante", "Odd Empate", "Odd Visitante"]
    })
    st.dataframe(df_jogos_sel, column_config=config_jogos, use_container_width=True, hide_index=True)

with tab_apostas:
    st.subheader(f"Apostas da Rodada {numero_sel}")
    apostas_sel = rodada_sel["apostas"]
    if apostas_sel:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Apostas", numero_br(len(apostas_sel), 0))
        col2.metric("Total Faturado", brl(sum(a["valor_apostado"] for a in apostas_sel)))
        col3.metric("Total Pago", brl(sum(a["valor_ganho"] for a in apostas_sel)))
        col4.metric("Apostas Vencedoras", f"{sum(a['ganhou'] for a in apostas_sel)}/{len(apostas_sel)}")

        df_apostas = pd.DataFrame([
            {
                "Usuário": usuarios[a["id_usuario"]]["nome"],
                "Perfil": a["perfil_usuario"],
                "Jogo": a["jogo_desc"],
                "Aposta": nome_resultado(rodada_sel["jogos"][a["idx_jogo"]], a["idx_resultado_apostado"]),
                "Valor": a["valor_apostado"],
                "Odd": a["odd_no_momento"],
                "Ganhou?": a["ganhou"],
                "Prêmio": a["valor_ganho"],
            }
            for a in apostas_sel
        ])
        st.dataframe(
            formatar_brl(df_apostas, ["Valor", "Prêmio"]),
            column_config={
                "Odd": st.column_config.NumberColumn("Odd", format="%.2f"),
                "Ganhou?": st.column_config.CheckboxColumn("Ganhou?"),
            },
            use_container_width=True, hide_index=True,
        )
    else:
        st.write("Nenhuma aposta nesta rodada.")

st.markdown("---")
st.header("👤 Detalhes dos Usuários")
df_usuarios = pd.DataFrame([
    {
        "Nome": u["nome"],
        "Perfil": u["perfil"],
        "Saldo": u["saldo"],
        "Nº de Apostas": u["num_apostas"],
        "Nº Rodadas c/ Aposta": u["rodadas_apostou"],
        "Total Faturado": u["total_apostado"],
        "Balanço Pessoal": u["saldo"] - saldo_inicial,
    }
    for u in usuarios
])
st.dataframe(
    formatar_brl(df_usuarios, ["Saldo", "Total Faturado", "Balanço Pessoal"]),
    column_config={
        "Saldo": st.column_config.Column("Saldo", help="Saldo atual do usuário."),
        "Nº de Apostas": st.column_config.NumberColumn("Nº de Apostas", help="Total de apostas feitas pelo usuário."),
        "Total Faturado": st.column_config.Column("Total Faturado", help="Total apostado pelo usuário (faturamento da casa)."),
        "Balanço Pessoal": st.column_config.Column("Balanço Pessoal", help="Saldo atual − saldo inicial."),
    },
    use_container_width=True, height=400, hide_index=True,
)

st.markdown("---")
st.header("📊 Histórico Individual do Usuário")
nomes_por_id = {u["id"]: u["nome"] for u in usuarios}
usuario_sel_id = st.selectbox(
    "Selecione o usuário para visualizar o histórico:",
    options=sorted(nomes_por_id, key=nomes_por_id.get),
    format_func=nomes_por_id.get,
    key="select_usuario_historico",
)
usuario_sel = usuarios[usuario_sel_id]

apostas_usuario = [
    (rodada, a)
    for rodada in rodadas
    for a in rodada["apostas"]
    if a["id_usuario"] == usuario_sel_id
]

if apostas_usuario:
    st.markdown(f"### 📈 Estatísticas de {usuario_sel['nome']}")
    total_apostado_usuario = sum(a["valor_apostado"] for _, a in apostas_usuario)
    total_ganho_usuario = sum(a["valor_ganho"] for _, a in apostas_usuario)
    taxa_acerto_usuario = sum(a["ganhou"] for _, a in apostas_usuario) / len(apostas_usuario) * 100

    hist_col1, hist_col2, hist_col3, hist_col4, hist_col5 = st.columns(5)
    hist_col1.metric("Total de Apostas", numero_br(len(apostas_usuario), 0))
    hist_col2.metric("Total Apostado", brl(total_apostado_usuario))
    hist_col3.metric("Total Ganho", brl(total_ganho_usuario))
    hist_col4.metric("Taxa de Acerto", pct(taxa_acerto_usuario))
    hist_col5.metric("Lucro/Prejuízo", brl(total_ganho_usuario - total_apostado_usuario))

    st.markdown("---")
    st.markdown("### 📋 Histórico Completo de Apostas")
    df_historico_usuario = pd.DataFrame([
        {
            "Rodada": rodada["numero"],
            "Jogo": a["jogo_desc"],
            "Aposta": nome_resultado(rodada["jogos"][a["idx_jogo"]], a["idx_resultado_apostado"]),
            "Valor": a["valor_apostado"],
            "Odd": a["odd_no_momento"],
            "Resultado": "✅" if a["ganhou"] else "❌",
            "Prêmio": a["valor_ganho"],
            "Lucro/Prejuízo": a["valor_ganho"] - a["valor_apostado"],
        }
        for rodada, a in reversed(apostas_usuario)
    ])
    st.dataframe(
        formatar_brl(df_historico_usuario, ["Valor", "Prêmio", "Lucro/Prejuízo"]),
        column_config={"Odd": st.column_config.NumberColumn("Odd", format="%.2f")},
        use_container_width=True, hide_index=True,
    )

    if len(rodadas) > 1:
        st.markdown("### 📈 Saldo por Rodada")
        eixo_rodadas = list(range(len(rodadas) + 1))

        # Todos os outros usuários num único traço (separados por None) para o gráfico continuar leve
        xs, ys, nomes = [], [], []
        for u in usuarios:
            if u["id"] == usuario_sel_id:
                continue
            xs += eixo_rodadas + [None]
            ys += u["saldos"] + [None]
            nomes += [u["nome"]] * len(eixo_rodadas) + [None]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=xs, y=ys, text=nomes, mode="lines",
            line=dict(color="rgba(192, 192, 192, 0.5)", width=1),
            hovertemplate="<b>%{text}</b><br>Rodada: %{x}<br>Saldo: R$ %{y:,.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=eixo_rodadas, y=usuario_sel["saldos"], mode="lines",
            line=dict(color="#2ca02c", width=3),
            hovertemplate=f"<b>{usuario_sel['nome']} (Selecionado)</b><br>"
                          "Rodada: %{x}<br>Saldo: R$ %{y:,.2f}<extra></extra>",
        ))
        fig.add_hline(y=saldo_inicial, line_dash="dash", line_color="green", opacity=0.5,
                      annotation_text=f"Saldo Inicial ({brl(saldo_inicial)})")
        fig.update_layout(
            title="Evolução do Saldo - Todos os Usuários",
            xaxis_title="Rodada", yaxis_title="Saldo (R$)",
            showlegend=False, height=500,
            separators=",.",  # Decimal com vírgula e milhar com ponto
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.write(f"{usuario_sel['nome']} ainda não fez nenhuma aposta.")
