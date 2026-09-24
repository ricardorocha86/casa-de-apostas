import streamlit as st
import random # Adicionado para escolher frase aleatória

# Lista de jargões sarcásticos
jargoes_sarcasticos = [
    "Simule aqui o seu prejuízo com precisão estatística! 📉",
    "Apostar é emoção. Perder é certeza. 😅",
    "O azar é seu. O lucro é nosso. 💸",
    "Aposte tudo. Simule a falência com realismo. 🤑",
    "Perder nunca foi tão matematicamente previsível. 📊",
    "Estatística aplicada ao seu fracasso financeiro. 📚",
    "Quanto mais você aposta, mais a casa sorri. 😈",
    "A casa sempre vence. Sua carteira sempre perde. 🏠",
    "Venha perder com método científico! 🧪",
    "Sua derrota em números detalhados. 📑",
    "Faça sua fortuna sumir com estilo. 🎩",
    "Aqui, a única sorte é da casa. 🎰",
    "Cálculos avançados para prejuízos garantidos. 📐",
    "A emoção de apostar, a certeza de perder. 🎢",
    "Sua aposta é nosso lucro – garantido pela matemática. 🧮",
    "Perder dinheiro nunca foi tão educativo. 🎓",
    "A sorte sorriu – para a casa! 😏",
    "Aposte até entender o teorema da ruína. ⚠️",
    "A aposta é sua, mas a estatística é nossa. 📈",
    "Onde perder dinheiro vira ciência exata. 🥼"
]

# Escolher um jargão aleatório
jargao_completo = random.choice(jargoes_sarcasticos)

# Separar o texto do emoji (considerando que o emoji é o último caractere)
if jargao_completo and len(jargao_completo) > 1:
    jargao_texto = jargao_completo[:-1].strip() # Pega tudo menos o último caractere e remove espaços extras
    jargao_emoji = jargao_completo[-1] # Pega o último caractere (emoji)
else:
    jargao_texto = jargao_completo # Caso não tenha emoji ou seja muito curto
    jargao_emoji = ""

# Custom CSS for styling
st.markdown("""
<style>
    .main-title-container {
        padding: 25px; /* Increased padding */
        /* background-color: #f8f9fa; */ /* Old background */
        background-image: linear-gradient(to right, #6ab04c, #00500e); /* Green gradient updated */
        border-radius: 15px; /* Slightly more rounded */
        margin-bottom: 35px; /* Increased margin */
        text-align: center;
        border: none; /* Removed border for a cleaner look with gradient */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); /* Softer shadow for depth */
    }
    .main-title-text {
        font-size: 3.5em; /* Significantly larger font size */
        font-weight: bold;
        color: #ffffff; /* White text for better contrast on green gradient */
        margin-bottom: 10px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3); /* Subtle text shadow */
    }
    .subtitle-text {
        font-size: 1.3em; /* Slightly larger subtitle */
        color: #f0f0f0; /* Lighter white/grey for subtitle */
        margin-bottom: 8px; /* Adicionado espaço abaixo do subtítulo original */
    }
    .sarcastic-subtitle-text {
        font-size: 1.1em; /* Tamanho para o jargão */
        color: #e0e0e0; /* Cor um pouco mais escura que o subtítulo principal */
        /* font-style: italic; */ /* Removido daqui, será aplicado no span */
    }
    .sarcastic-text-italic {
        font-style: italic;
    }
    .sarcastic-emoji {
        font-style: normal; /* Garantir que o emoji não pegue itálico por herança */
    }
    .custom-subheader {
        font-size: 1.8em;
        font-weight: bold;
        color: #00500e; /* Bootstrap primary blue */
        border-bottom: 2px solid #00500e;
        padding-bottom: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
        font-size: 0.85em; /* Fonte menor que o normal */
        /* color: #757575; */ /* Removido pelo usuário, cor padrão do texto será usada ou definida por elementos internos */
        text-align: left; /* Alinhado à esquerda */
    }  
    .dev-name {
        font-size: 1.1em; /* Aumentado um pouco para mais destaque */
        font-weight: bold;
        /* color: #ffffff; */ /* Removido, será transparente */
        background-image: linear-gradient(to right, #00500e, #00500e);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        margin-left: 0px; 
    }
    .social-links p {
        margin-bottom: 0px; /* Espaçamento entre linhas dos links */
        line-height: 1.6; /* Melhorar a legibilidade dos links */
    }
    .social-links strong {
        color: #333; /* Cor mais escura para os rótulos dos links */
    }
    .footer a {
        color: #00500e; /* Cor verde para os links, combinando com o tema */
        text-decoration: none; /* Sem sublinhado por padrão */
    }
    .footer a:hover {
        text-decoration: underline; /* Sublinhado no hover */
        color: #6ab04c; /* Verde mais claro no hover */
    }
</style>
""", unsafe_allow_html=True)

# Main Title Section
st.markdown(f"""
<div class="main-title-container">
    <p class="main-title-text">🎰 Bem-vindo ao Simulador de Casa de Apostas!</p> 
    <p class="sarcastic-subtitle-text">
        <span class="sarcastic-text-italic">{jargao_texto}</span><span class="sarcastic-emoji">{jargao_emoji}</span>
    </p>
</div>
""", unsafe_allow_html=True)

# Objetivo Section (Visible)
st.markdown('<p class="custom-subheader">🎯 Qual o nosso objetivo?</p>', unsafe_allow_html=True)
st.markdown("""
    - Este aplicativo foi criado para **explorar e entender de forma educativa a dinâmica financeira de uma casa de apostas esportivas**.
            
   - Através de simulações interativas, você poderá observar como diferentes fatores influenciam os resultados tanto para a casa quanto para os apostadores.
            
    - Nosso propósito é puramente **educacional e analítico**, buscando desmistificar o funcionamento das odds, margens e o impacto do comportamento dos usuários.
    
    - Veja como a margem da casa e os diferentes perfis de apostadores afetam a lucratividade e a sustentabilidade do sistema! 🏦⚽️🤑
    """)   

# Roteiro sugerido
st.markdown('<p class="custom-subheader">🧭 Por onde começar?</p>', unsafe_allow_html=True)
roteiro_col1, roteiro_col2 = st.columns(2)
with roteiro_col1:
    with st.container(border=True):
        st.markdown("**1º passo — Entenda as odds**")
        st.caption("Veja como probabilidade e margem da casa viram a odd oferecida, e quanto você perde em média por aposta.")
        st.page_link("calculadora_odds.py", label="Abrir a Calculadora de Odds", icon="📚")
with roteiro_col2:
    with st.container(border=True):
        st.markdown("**2º passo — Veja a casa funcionando**")
        st.caption("Simule centenas de apostadores rodada a rodada e acompanhe o \"lucro\" da casa e o saldo de cada um.")
        st.page_link("sim1.py", label="Abrir o Simulador Principal", icon="👩🏽‍💻")


# Expander 2: Algoritmo (Resumido)
with st.expander("📜 Entenda o Algoritmo da Simulação", expanded=False):
    st.markdown("""
    Cada rodada da simulação segue estes passos principais:

    1.  **Configuração da Rodada:** Usuários são inicializados (se primeira rodada) e estatísticas zeradas.
    2.  **Criação de Jogos:** Jogos fictícios são gerados com probabilidades de resultados (Vitória, Empate, Derrota) e odds da casa calculadas (incluindo margem).
    3.  **Atividade dos Usuários:**
        *   **Decisão de Apostar:** Usuários decidem se apostam (baseado no perfil).
        *   **Número de Apostas:** Quantidade de apostas definida (Poisson Truncada ≥ 1).
        *   **Execução das Apostas:** Para cada aposta:
            *   Valor: 10% do saldo (respeitando aposta mínima).
            *   Escolha: Jogo sorteado ao acaso; o resultado é sorteado entre as odds mais baixas (Conservador), todas (Moderado) ou as mais altas (Arriscado).
            *   Registro: Saldo debitado, estatísticas atualizadas.
    4.  **Determinação dos Resultados:** Resultados finais dos jogos são simulados.
    5.  **Liquidação de Apostas:** Apostas vencedoras são pagas, saldos de usuários e estatísticas da casa atualizados.
    6.  **Consolidação da Rodada:** Estatísticas finais da rodada e acumuladas são calculadas e armazenadas.
    """)

# Expander 3: Distribuições (Resumido e Focado)
with st.expander("🎲 Distribuições de Probabilidade Utilizadas", expanded=False):
    st.markdown(r"""
    Principais distribuições que moldam a simulação:

    -   **Resultados dos Jogos (Futebol):**
        *   $P(\text{Vitória}) \sim \text{Uniforme}(0.05,\ 0.70)$
        *   $P(\text{Empate}) \sim \text{Uniforme}(0.10,\ 0.25)$
        *   $P(\text{Derrota}) = 1 - P(\text{Vitória}) - P(\text{Empate})$

    -   **Decisão de Apostar na Rodada (por Usuário):**
        *   Modelo: Bernoulli $X \sim \text{Bernoulli}(p)$, em que $p$ é a probabilidade de decidir apostar (do perfil).

    -   **Quantidade de Apostas (se usuário aposta):**
        *   Modelo: Poisson Truncada em 1
        *   Parâmetro $\lambda$: Média de Apostas Desejadas (do perfil), $Y \sim \text{Pois}(\lambda)$.

    -   **Escolha do Jogo e Resultado para Apostar:**
        *   Jogo: Uniforme discreta entre os jogos da rodada.
        *   Resultado: Uniforme discreta, com as opções definidas pelo perfil — **Conservador** sorteia entre a menor odd e a intermediária, **Moderado** entre os três resultados e **Arriscado** entre a intermediária e a maior odd.

    -   **Simulação do Resultado Final de um Jogo:**
        *   Modelo: Discreto, com probabilidades $P(\text{Vitória}), P(\text{Empate}), P(\text{Derrota})$ reais do jogo.
    """)

# Expander 4: O que explorar
with st.expander("🚀 Explore as Possibilidades!", expanded=False):
    st.markdown("""
    -   **Ajustar Parâmetros:** Na barra lateral da página de simulação (`Simulador Principal`), você pode definir o número de usuários, saldo inicial, margem da casa e configurar detalhadamente o comportamento de cada perfil de apostador.
    -   **Avançar Rodadas:** Acompanhe a evolução do sistema rodada a rodada, ou avance 10 rodadas de uma vez.
    -   **Analisar Resultados:** Observe métricas como faturamento, lucro da casa, número de apostas, saldo médio dos usuários, e muito mais.
    
    **Divirta-se explorando e aprendendo!**
    """)

# Footer Section
st.markdown(""" 
<div class="footer">
        <p>
            <span class="dev-name">Ricardo Rocha</span>
        </p>
    <div class="social-links">
        <p>
            <strong>Instagram:</strong> <a href="https://instagram.com/ricardorocha.86" target="_blank">instagram.com/ricardorocha.86</a><br>
            <strong>LinkedIn:</strong> <a href="https://linkedin.com/in/ricardorocha86" target="_blank">linkedin.com/in/ricardorocha86</a><br>
            <strong>GitHub:</strong> <a href="https://github.com/ricardorocha86" target="_blank">github.com/ricardorocha86</a><br>
            <strong>Streamlit:</strong> <a href="https://share.streamlit.io/user/ricardorocha86" target="_blank">share.streamlit.io/user/ricardorocha86</a>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)