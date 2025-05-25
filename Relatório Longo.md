# Um Simulador Interativo para Análise da Dinâmica de Casas de Apostas Esportivas

## Resumo

A crescente popularidade das apostas esportivas online necessita de ferramentas que permitam uma compreensão mais profunda da dinâmica financeira e probabilística envolvida. Este trabalho descreve o desenvolvimento e a metodologia de um simulador interativo de uma casa de apostas esportivas, focado em jogos de futebol. O modelo permite a configuração de múltiplos parâmetros, incluindo o número de apostadores, seus perfis de comportamento (conservador, moderado, arriscado), a margem de lucro da casa e as características dos jogos. Detalhamos os métodos probabilísticos empregados na geração de resultados de jogos, no cálculo de odds, e na modelagem das decisões dos apostadores, como a frequência e o valor das apostas, utilizando distribuições Uniforme e de Poisson Truncada. O simulador permite a análise de métricas chave como faturamento, pagamentos, lucro da casa (GGR), e a evolução do saldo dos apostadores, oferecendo uma plataforma para investigar o impacto de diferentes estratégias e configurações no ecossistema de apostas. O objetivo é fornecer um instrumento analítico e educacional para o estudo da sustentabilidade da casa e das probabilidades de sucesso dos apostadores sob diversas condições.

**Palavras-chave:** Simulação de Apostas, Modelagem Probabilística, Apostas Esportivas, Análise de Risco, Comportamento do Apostador.

## 1. Introdução

O setor de apostas esportivas tem experimentado uma expansão global significativa, impulsionada pela digitalização e pela facilidade de acesso a plataformas online. Apesar da sua proeminência econômica e social, os mecanismos internos que regem o funcionamento das casas de apostas, especialmente a interação entre as probabilidades dos eventos, a formação de odds, a margem da casa e o comportamento dos apostadores, frequentemente carecem de transparência e compreensão aprofundada por parte do público e até mesmo de pesquisadores de áreas correlatas.

Este estudo propõe um modelo de simulação computacional como ferramenta para investigar a dinâmica operacional e financeira de uma casa de apostas esportivas. O objetivo principal é desenvolver um simulador interativo que permita aos usuários explorar como diferentes parâmetros e estratégias de apostas afetam tanto a lucratividade da casa quanto o desempenho financeiro dos apostadores. A simulação concentra-se em apostas no resultado final de partidas de futebol (vitória, empate, derrota) e modela o comportamento de apostadores com distintos perfis de aversão ao risco.

Ao permitir a manipulação de variáveis como a margem da casa, o volume de jogos, e as características comportamentais dos apostadores, o simulador visa elucidar conceitos fundamentais de probabilidade, expectativa de valor e gestão de risco no contexto das apostas, servindo como um laboratório virtual para experimentação e análise.

## 2. Metodologia

O simulador opera em rodadas discretas, onde em cada rodada um novo conjunto de eventos esportivos (jogos de futebol) é gerado, os apostadores tomam suas decisões, os resultados dos jogos são determinados e as apostas são liquidadas.

### 2.1. Geração de Probabilidades de Jogos

Para cada jogo de futebol simulado, são definidas as probabilidades "reais" para os três resultados possíveis: Vitória do Time da Casa (V), Empate (E), e Derrota do Time da Casa (D). Estas probabilidades são geradas estocasticamente:

*   A probabilidade de vitória do time da casa, $P(V)$, é amostrada de uma distribuição uniforme:
    $$ P(V) \\sim U(0.05, 0.70) $$
*   A probabilidade de empate, $P(E)$, também é amostrada de uma distribuição uniforme, porém com um intervalo diferente para refletir as tendências observadas no futebol:
    $$ P(E) \\sim U(0.10, 0.25) $$
*   A probabilidade de derrota do time da casa, $P(D)$, é então calculada como o complemento, assegurando que a soma das probabilidades seja unitária:
    $$ P(D) = 1 - P(V) - P(E) $$
Após a geração, as probabilidades são validadas para garantir que $P(D) \\ge 0$. Em casos raros onde $P(D)$ poderia resultar negativa devido aos limites dos sorteios uniformes, $P(E)$ é reajustado para $1 - P(V)$ e $P(D)$ fixado em 0. Todas as probabilidades são arredondadas para duas casas decimais, e $P(D)$ é finalmente recalculada para garantir que $P(V) + P(E) + P(D) = 1.00$, corrigindo quaisquer pequenos desvios de arredondamento.

### 2.2. Cálculo de Odds pela Casa

As odds oferecidas pela casa de apostas são derivadas das probabilidades reais, mas ajustadas para incluir a margem de lucro da casa ($m$), um parâmetro configurável na simulação (e.g., $m = 0.05$ para uma margem de 5%).

Para um resultado $i \\in \\{V, E, D\\}$ com probabilidade real $P_i$:
1.  A odd justa ($\\text{Odd}_{\\text{justa},i}$) é o inverso da probabilidade real:
    $$ \\text{Odd}_{\\text{justa},i} = \\frac{1}{P_i} $$
    (Se $P_i = 0$, uma odd nominalmente alta, como 999.0, é atribuída).
2.  A odd da casa ($\\text{Odd}_{\\text{casa},i}$) é calculada aplicando a margem:
    $$ \\text{Odd}_{\\text{casa},i} = \\text{Odd}_{\\text{justa},i} \\times (1 - m) $$
As odds calculadas são arredondadas para duas casas decimais e um valor mínimo de 1.01 é garantido para todas as odds oferecidas, pois odds menores que isso não são praticáveis.

### 2.3. Simulação do Resultado do Jogo

O resultado final de cada partida é determinado probabilisticamente com base nas probabilidades reais $P(V), P(E), P(D)$, utilizando uma amostragem aleatória ponderada (equivalente a `numpy.random.choice`). Isso assegura que, ao longo de um grande número de simulações, a frequência dos resultados observados convirja para as probabilidades intrínsecas definidas.

### 2.4. Modelagem do Comportamento do Apostador

Os apostadores são caracterizados por perfis (Conservador, Moderado, Arriscado), cujos parâmetros influenciam suas decisões de aposta.

#### 2.4.1. Decisão de Apostar

Cada perfil possui uma `prob_decidir_apostar` específica. Em cada rodada, para cada apostador, um número aleatório $R \\sim U(0,1)$ é gerado. Se $R < \\text{prob_decidir_apostar}$ do seu perfil, o apostador participará da rodada de apostas.

#### 2.4.2. Quantidade de Apostas

Se um apostador decide participar, o número de apostas que ele deseja realizar ($k$) é determinado por uma **Distribuição de Poisson Truncada em 1**. A Distribuição de Poisson é dada por:
$$ P(X=k) = \\frac{\\lambda^k e^{-\\lambda}}{k!} $$
onde $\\lambda$ é o parâmetro `lambda_poisson` do perfil, representando a taxa média de apostas desejadas. A truncagem em 1 significa que se o valor amostrado da Poisson for 0, um novo valor é sorteado até que $k \\ge 1$. Isso garante que um apostador que decide apostar fará ao menos uma aposta.

#### 2.4.3. Valor da Aposta

O valor monetário de cada aposta individual é determinado pela função `calcular_valor_aposta`, que considera o saldo do usuário ($S$), seu perfil, e um valor mínimo global de aposta ($V_{\\min}$, e.g., R$ 5,00):
1.  Se $0 < S < V_{\\min}$, o apostador aposta todo o saldo $S$.
2.  Caso contrário, um percentual do saldo ($p_S$) é sorteado de uma distribuição uniforme definida pelos parâmetros `perc_saldo_aposta_min` e `perc_saldo_aposta_max` do perfil: $p_S \\sim U(p_{\\min}, p_{\\max})$. O valor proposto é $V_p = S \\times p_S$.
3.  Se $V_p < V_{\\min}$, o valor da aposta é ajustado para $V_{\\min}$. Caso contrário, mantém-se $V_p$.
4.  O valor final da aposta ($V_f$) é, por fim, limitado ao saldo disponível: $V_f = \\min(V_{\\text{ajustado}}, S)$.
Todos os valores são arredondados para duas casas decimais.

#### 2.4.4. Seleção do Jogo e do Resultado

Para cada aposta, o apostador seleciona um jogo aleatoriamente dentre os disponíveis na rodada. O resultado específico (V, E, ou D) para apostar naquele jogo também é escolhido de forma aleatória, com igual probabilidade (1/3) para cada opção. Este comportamento modela um apostador não informado ou impulsivo, que não analisa as odds ou probabilidades reais para tomar sua decisão.

### 2.5. Liquidação e Atualizações Financeiras

Após a determinação dos resultados dos jogos, as apostas são liquidadas. Se uma aposta é vencedora, o prêmio é $V_f \\times \\text{Odd}_{\\text{casa}}$. Os saldos dos usuários e as métricas financeiras da casa (faturamento, pagamentos, GGR) são atualizados. Todas as transações monetárias e saldos são consistentemente arredondados para duas casas decimais para manter a precisão financeira. O balanço pessoal de cada usuário (saldo atual - saldo inicial) também é recalculado ao final de cada rodada.

## 3. Parâmetros de Simulação e Métricas de Saída

O simulador permite a configuração de diversos parâmetros de entrada, incluindo: número de usuários, saldo inicial padrão, margem da casa, número de jogos por rodada, e os parâmetros comportamentais de cada perfil de apostador (probabilidade de apostar, $\\lambda$ da Poisson, percentuais mínimo e máximo do saldo para apostar).

As principais métricas de saída, disponíveis tanto por rodada quanto de forma acumulada, incluem:
*   **Métricas da Casa:** Faturamento total (handle), total de pagamentos (payouts), lucro bruto dos jogos (GGR = handle - payouts), margem de GGR.
*   **Métricas dos Usuários:** Número de usuários ativos (saldo > 0), lucrativos (saldo > saldo inicial), falidos (saldo = 0), e saldo médio.
*   **Métricas por Perfil:** Faturamento, pagamentos, GGR e número de apostas segmentados por perfil de apostador.
O sistema também armazena um histórico detalhado de todos os jogos e de todas as apostas individuais, permitindo análises retrospectivas e investigações sobre o desempenho de usuários específicos.

## 4. Discussão e Aplicações Potenciais

O modelo de simulação proposto oferece uma plataforma robusta para a análise quantitativa da dinâmica das casas de apostas esportivas. A capacidade de ajustar interativamente os parâmetros permite investigar uma variedade de cenários e hipóteses. Por exemplo, pode-se estudar:
*   A sensibilidade do GGR da casa à sua margem de lucro e ao volume de apostas.
*   A taxa de "sobrevivência" de diferentes perfis de apostadores sob várias configurações da casa.
*   O impacto do número de eventos disponíveis (jogos) na dispersão do capital entre os apostadores e na estabilidade financeira da casa.
*   A distribuição de lucros/prejuízos entre os apostadores e sua evolução temporal.

Como ferramenta educacional, o simulador pode auxiliar na demonstração de conceitos como valor esperado, variância em jogos de azar, e o efeito da margem da casa na rentabilidade de longo prazo das apostas. Para pesquisadores, pode servir de base para estudos mais complexos, incorporando, por exemplo, modelos de apostadores mais sofisticados que reagem às odds ou a resultados anteriores.

## 5. Conclusão

Este trabalho detalhou a concepção metodológica de um simulador de casa de apostas esportivas, com ênfase nos seus fundamentos probabilísticos e na modelagem do comportamento dos apostadores. A ferramenta desenvolvida é capaz de gerar cenários complexos e fornecer dados detalhados sobre as interações financeiras dentro do ecossistema de apostas. Acreditamos que este simulador representa um recurso valioso para fins educacionais, analíticos e de pesquisa, permitindo uma exploração transparente e controlada dos fatores que governam o arriscado, porém popular, mundo das apostas esportivas. Investigações futuras podem se concentrar na validação do modelo com dados reais do mercado e na expansão das suas funcionalidades para incluir outros tipos de apostas e comportamentos de apostadores mais elaborados.

---
*Este relatório foi gerado com base na funcionalidade completa e na estrutura do código do aplicativo `app.py` previamente desenvolvido.*
