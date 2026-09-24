import streamlit as st

from formatacao import brl_md, pct


# Estilo personalizado
st.markdown("""
<style>
    .main-title-container {
        padding: 25px;
        background-image: linear-gradient(to right, #6ab04c, #00500e);
        border-radius: 15px;
        margin-bottom: 35px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .main-title-text {
        font-size: 3.0em;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 10px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .subtitle-text {
        font-size: 1.2em;
        color: #f0f0f0;
        margin-bottom: 8px;
    }
    .formula-box {
        background-color: #f8f9fa;
        border-left: 4px solid #00500e;
        padding: 15px;
        margin: 15px 0;
        border-radius: 5px;
    }
    .highlight-box {
        background-color: #e8f5e8;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #00500e;
        margin: 15px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ffc107;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<div class="main-title-container">
    <p class="main-title-text">📚 Calculadora de Odds Didática</p> 
    <p class="subtitle-text">Entenda como probabilidades e margens da casa formam as odds</p>
</div>
""", unsafe_allow_html=True)

# Explicação introdutória
st.markdown("""
## 🎯 Uma introdução ao assunto

As casas de apostas são empresas que lucram oferecendo apostas em eventos esportivos. Para garantir seu lucro, elas usam conceitos matemáticos fundamentais que todo apostador deveria conhecer.

**O processo é simples:**
1. **Estimam as probabilidades reais** de cada resultado possível
2. **Convertem essas probabilidades em odds "justas"** usando matemática
3. **Aplicam uma margem de lucro** reduzindo ligeiramente essas odds
4. **Oferecem as odds finais** ao público, garantindo lucro a longo prazo

Esta ferramenta permite que você experimente esse processo na prática, ajustando probabilidades e vendo como as odds são calculadas em tempo real.
""")

st.markdown("---")

# === SEÇÃO 1: CONCEITOS BÁSICOS ===
st.header("📖 Conceitos Fundamentais")

st.markdown(r"""
As apostas esportivas envolvem três conceitos matemáticos interligados que determinam quanto você pode ganhar ou perder.

**Probabilidade** é a quantificação da incerteza de um evento acontecer, expressa entre 0 e 1 (ou 0% a 100%).
            
**Odds (cotações)** são o multiplicador que determina quanto você ganha se sua aposta for vencedora. Elas são calculadas diretamente a partir das probabilidades. A fórmula da **Odd Justa = 1 ÷ Probabilidade**. 
            
Por exemplo, se a probabilidade de vitória é 50%, a odd justa seria 1 ÷ 0.5 = 2.00. Isso significa que você ganha R\$ 2,00 para cada R\$ 1,00 apostado.

Porém, as casas de apostas não oferecem odds justas. Elas aplicam uma **margem da casa** reduzindo ligeiramente as odds. 
            
A fórmula da **Odd Final = Odd Justa × (1 - Margem da Casa)**. Se a margem for 5% e a odd justa for 2.00, a odd final será 2.00 × (1 - 0.05) = 1.90.

O **Retorno Esperado** mostra se uma aposta é matematicamente favorável. Um resultado negativo indica que, a longo prazo, você perderá dinheiro. Com probabilidade de 50% e odd final de 1.90, o retorno esperado seria (0.5 × 1.90) - 1 = -0.05 ou -5%.

Finalmente, o **Ganho Potencial = Aposta × Odd Final**. Se você apostar R\$ 100 em uma odd de 1.90, seu ganho potencial será R\$ 190 (incluindo sua aposta inicial).

Este sistema garante que as casas de apostas sempre tenham vantagem matemática, independentemente dos resultados individuais dos jogos.
""")

st.markdown("---")

# === SEÇÃO 2: CALCULADORA INTERATIVA ===
st.header("🧮 Calculadora Interativa de Odds")

st.markdown("**Configure um jogo de futebol e veja como as odds são calculadas:**")

# Controles na sidebar
with st.sidebar:
    st.header("⚙️ Configurações do Jogo")
    
    st.subheader("🏠 Margem da Casa")
    margem_casa = st.slider("Margem da Casa (%)", 0.0, 25.0, 5.0, 0.5) / 100

    st.subheader("💵 Sua Aposta")
    valor_aposta = st.number_input("Valor Apostado (R$)", min_value=1.0, max_value=100000.0, value=100.0, step=10.0)

# Inputs na página principal
st.subheader("🏆 Probabilidades Reais")
col1, col2, col3 = st.columns(3)

with col1:
    prob_vitoria = st.slider("Probabilidade de Vitória (%)", 0, 100, 50, 1) / 100

with col2:
    prob_empate = st.slider("Probabilidade de Empate (%)", 0, 100, 25, 1) / 100

with col3:
    # Coluna vazia conforme solicitado
    pass

# Calcular automaticamente a probabilidade de derrota
prob_derrota = 1.0 - prob_vitoria - prob_empate
if prob_derrota < 0:
    prob_derrota = 0
    prob_empate = 1.0 - prob_vitoria
    st.warning(f"⚠️ Vitória + Empate passavam de 100%. O Empate foi ajustado para {pct(prob_empate * 100)} e a Derrota ficou em 0%.")

# Calcular odds
odds_justas = [1/prob_vitoria if prob_vitoria > 0 else 999, 
               1/prob_empate if prob_empate > 0 else 999, 
               1/prob_derrota if prob_derrota > 0 else 999]

odds_com_margem = [odd * (1 - margem_casa) for odd in odds_justas]

# Calcular retorno esperado
retornos_esperados = [prob * odd - 1 for prob, odd in zip([prob_vitoria, prob_empate, prob_derrota], odds_com_margem)]

# Display dos resultados
col1, col2, col3 = st.columns(3)

resultados = ["Vitória", "Empate", "Derrota"]
probabilidades = [prob_vitoria, prob_empate, prob_derrota]
cores = ["#28a745", "#ffc107", "#dc3545"]

for i, (col, resultado, prob, cor) in enumerate(zip([col1, col2, col3], resultados, probabilidades, cores)):
    with col:
        st.markdown(f"""
        <div style="background-color: {cor}; color: white; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 10px;">
            <h3>{resultado}</h3>
            <h4>{pct(prob * 100)}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas de odds em 3 colunas
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            st.metric("Odd Justa", f"{odds_justas[i]:.2f}", border=True)
        with subcol2:
            st.metric("Odd Final", f"{odds_com_margem[i]:.2f}", border=True)
        with subcol3:
            st.metric("Retorno Esperado", pct(retornos_esperados[i] * 100), border=True)

        if prob > 0:
            st.caption(
                f"Apostando {brl_md(valor_aposta)}: recebe **{brl_md(valor_aposta * odds_com_margem[i])}** se acertar. "
                f"Perda esperada: **{brl_md(-retornos_esperados[i] * valor_aposta)}** por aposta."
            )

# === SEÇÃO 3: DICAS E CONCLUSÕES ===
st.markdown("---")
st.header("🎓 Conclusões e Dicas Importantes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="highlight-box">
        <h4>✅ O que aprendemos:</h4>
        <ul>
            <li>As odds são inversamente proporcionais às probabilidades</li>
            <li>A margem da casa sempre reduz as odds oferecidas</li>
            <li>O retorno esperado é sempre negativo para o apostador</li>
            <li>Quanto maior a margem, maior o lucro da casa</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ Pontos de atenção:</h4>
        <ul>
            <li>Apostas são sempre desfavoráveis matematicamente</li>
            <li>A "sorte" no curto prazo não muda a matemática</li>
            <li>A casa sempre tem vantagem estatística</li>
            <li>Diversão deve ser o único motivo para apostar</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.success("🎉 Parabéns! Agora você entende como as casas de apostas calculam suas odds e mantêm sua vantagem matemática!") 