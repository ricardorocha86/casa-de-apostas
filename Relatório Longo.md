# 🎲 Relatório Detalhado: Simulador de Casa de Apostas Avançado

**Versão do Documento:** 1.0
**Data da Última Atualização:** {{ CURRENT_DATE }}

## 📜 Introdução

### 1.1. Motivação e Justificativa

O mercado de apostas esportivas tem crescido exponencialmente, movimentando bilhões globalmente e atraindo um número cada vez maior de participantes. No entanto, a dinâmica interna de uma casa de apostas, os modelos probabilísticos subjacentes e os fatores que determinam sua lucratividade (e, por consequência, o desempenho dos apostadores) muitas vezes permanecem obscuros para o público geral.

Este projeto nasceu da necessidade de criar uma ferramenta educacional e analítica que permitisse desmistificar o funcionamento de uma casa de apostas. A ideia central é oferecer um ambiente de simulação interativo onde usuários pudessem:

*   Compreender como as odds são calculadas e como a margem da casa (também conhecida como juice ou vig) impacta os retornos potenciais.
*   Analisar o efeito de diferentes comportamentos e estratégias de apostas no saldo individual e no ecossistema da casa.
*   Visualizar de forma clara as métricas financeiras chave de uma operação de apostas, como faturamento (handle), pagamentos (payouts) e lucro (Gross Gaming Revenue - GGR).
*   Explorar conceitos de probabilidade, risco e aleatoriedade em um contexto prático e envolvente.

O simulador visa, portanto, preencher uma lacuna ao fornecer uma plataforma robusta para experimentação e aprendizado, tanto para entusiastas de apostas quanto para estudantes de estatística, finanças ou ciência de dados.

### 1.2. Objetivos do Projeto

Os objetivos principais e secundários do desenvolvimento deste simulador são:

**Objetivos Principais:**

1.  Modelar o Ciclo de Vida de uma Casa de Apostas: Simular a criação de jogos, a definição de odds, o recebimento de apostas de múltiplos usuários com diferentes perfis, a liquidação dessas apostas e o acompanhamento das finanças da casa.
2.  Implementar Perfis de Apostadores Distintos: Criar modelos de comportamento de apostadores (Conservador, Moderado, Arriscado) com parâmetros configuráveis para observar como diferentes abordagens ao risco impactam os resultados individuais e da casa.
3.  Desenvolver um Dashboard Interativo e Informativo: Utilizar a biblioteca **Streamlit** para criar uma interface web rica em visualizações de dados, métricas em tempo real e acumuladas, e ferramentas de análise histórica.

**Objetivos Secundários:**

1.  Explorar Modelos Probabilísticos: Aplicar distribuições de probabilidade (como a Uniforme e a de Poisson) para simular eventos como resultados de jogos e o número de apostas por usuário.
2.  Permitir Configuração Flexível: Oferecer ao usuário controle sobre parâmetros chave da simulação, como número de usuários, saldo inicial, margem da casa e características dos perfis de apostadores.
3.  Garantir Realismo e Precisão: Implementar lógicas de cálculo financeiro (arredondamentos, valor mínimo de aposta) que reflitam práticas comuns no setor.
4.  Fornecer Capacidade de Análise Histórica: Permitir que o usuário explore dados de rodadas anteriores para entender tendências e padrões.
5.  Criar Código Modular e Extensível: Desenvolver uma base de código que possa ser facilmente compreendida e expandida com novas funcionalidades no futuro.

### 1.3. Escopo do Simulador

O escopo deste simulador abrange as seguintes funcionalidades e características:

*   Tipo de Aposta: Foco em apostas esportivas em jogos de futebol, especificamente no mercado de resultado final (Vitória do Time da Casa, Empate, Vitória do Time Visitante).
*   Usuários: Geração de um número configurável de usuários fictícios com nomes e e-mails (gerados pela biblioteca **Faker** para fins de ilustração, sem coleta ou armazenamento de dados reais).
*   Perfis de Usuários: Três perfis pré-definidos (Conservador, Moderado, Arriscado) com parâmetros de comportamento ajustáveis na interface.
*   Simulação por Rodadas: O sistema opera em rodadas discretas. Em cada rodada, novos jogos são criados, os usuários podem fazer apostas, os jogos são resolvidos e as apostas são liquidadas.
*   Métricas Financeiras: Cálculo e exibição de faturamento, pagamentos, lucro (GGR), tanto por rodada quanto de forma acumulada. Inclui também métricas por perfil de usuário.
*   Métricas de Usuário: Acompanhamento de saldo, número de apostas, balanço pessoal, status (lucrativo, ativo, falido).
*   Interface Gráfica: Um dashboard web construído com **Streamlit**, apresentando tabelas, gráficos e controles interativos.
*   Histórico: Armazenamento e visualização de dados de jogos e apostas de todas as rodadas, além do histórico individual de cada usuário.

**Fora do Escopo (Limitações Atuais):**

*   Apostas ao vivo (in-play betting).
*   Múltiplos tipos de mercados de apostas (e.g., handicap asiático, total de gols).
*   Sistemas de bônus ou promoções para usuários.
*   Recursos de depósito ou saque de fundos.
*   Autenticação de usuários ou persistência de dados entre sessões do navegador além do estado da sessão **Streamlit**.
*   Modelos de IA avançados para predição de resultados de jogos ou comportamento de apostadores (as probabilidades e decisões são baseadas em distribuições estatísticas e regras pré-definidas).

## ⚙️ Arquitetura e Metodologia

### 2.1. Tecnologias Utilizadas

O simulador foi construído utilizando um conjunto de bibliotecas Python bem estabelecidas no ecossistema de ciência de dados e desenvolvimento web:

*   **Python 3.x**: Linguagem de programação principal, escolhida por sua simplicidade, vasta gama de bibliotecas e forte comunidade.
*   **Streamlit**: Framework open-source para a criação rápida de aplicações web interativas para projetos de dados. É o coração da interface do usuário, permitindo a criação de widgets, gráficos e tabelas dinâmicas com código Python puro.
*   **Pandas**: Biblioteca fundamental para manipulação e análise de dados. Utilizada para criar DataFrames que armazenam e organizam os dados de usuários, jogos, apostas e históricos, facilitando a sua exibição e processamento.
*   **NumPy**: Biblioteca essencial para computação numérica em Python. Empregada para operações matemáticas, geração de números aleatórios (e.g., para distribuições de probabilidade) e manipulação eficiente de arrays.
*   **Matplotlib** (indiretamente via **Streamlit**): Embora não seja chamada diretamente em muitos casos, **Streamlit** utiliza **Matplotlib** закулисами para renderizar alguns de seus gráficos. É a base para muitas visualizações em Python.
*   **Faker**: Biblioteca para geração de dados fictícios. Utilizada para criar nomes e e-mails para os usuários simulados, adicionando um toque de realismo sem a necessidade de dados reais.

### 2.2. Estrutura do Código (`app.py`)

Todo o código da aplicação reside em um único arquivo, `app.py`. Esta decisão foi tomada para simplificar a implantação e o compartilhamento inicial do projeto, típico de muitas aplicações **Streamlit**. A estrutura interna do `app.py` pode ser dividida nas seguintes seções principais:

1.  **Importações e Constantes:**
    *   Importação das bibliotecas necessárias.
    *   Definição de constantes globais, como `VALOR_APOSTA_MINIMA` e as configurações padrão para os `PERFIS_CONFIG_DEFAULT`.

2.  **Funções Auxiliares:**
    *   `gerar_probabilidades_futebol()`: Gera as probabilidades reais para os três resultados de um jogo de futebol (Vitória, Empate, Derrota).
    *   `calcular_odds_casa()`: Calcula as odds oferecidas pela casa, aplicando a margem de lucro configurada sobre as probabilidades reais.
    *   `simular_resultado_jogo()`: Determina o resultado final de um jogo com base em suas probabilidades reais.
    *   `poisson_truncada_em_1()`: Gera o número de apostas que um usuário deseja fazer, garantindo que seja pelo menos 1, usando uma distribuição de Poisson modificada.
    *   `calcular_valor_aposta()`: Define o valor monetário de uma aposta individual, considerando o saldo do usuário, seu perfil e o valor mínimo de aposta.

3.  **Inicialização do Estado da Sessão Streamlit (`st.session_state`):**
    *   Verifica e inicializa variáveis de estado que precisam persistir entre interações do usuário e re-renderizações da página. Isso inclui `simulacao_iniciada`, `rodada_atual`, listas para `usuarios`, `historico_casa`, `historico_jogos`, `historico_apostas`, e as configurações dinâmicas dos perfis (`perfis_config_dinamico`).
    *   As estatísticas acumuladas da casa também são inicializadas aqui.

4.  **Interface Streamlit (`st.set_page_config`, `st.title`, `st.sidebar`, etc.):**
    *   Configuração da página (layout, título).
    *   Barra Lateral (`st.sidebar`): Contém todos os controles de configuração da simulação:
        *   Número de usuários e saldo inicial (desabilitados após o início da simulação).
        *   Configurações da casa e jogos (margem da casa, número de jogos por rodada).
        *   Configurações detalhadas para cada perfil de apostador (probabilidade de apostar, lambda da Poisson, percentuais de saldo para aposta), utilizando `st.expander` e widgets como `st.slider` e `st.number_input`.
        *   Validações para garantir que Min % < Max % do saldo.
        *   Botões "Iniciar / Próxima Rodada" e "Resetar Simulação".

5.  **Lógica da Simulação (dentro do `if st.button("▶️ Iniciar / Próxima Rodada")`):**
    *   Incrementa `rodada_atual`.
    *   Primeira Rodada: Inicializa a lista de `usuarios` com seus atributos (ID, nome, email, perfil, saldo inicial, etc.) e reseta estatísticas acumuladas.
    *   Lógica Principal da Rodada:
        1.  **Geração de Jogos:** Cria o número especificado de jogos, cada um com suas probabilidades reais e odds da casa.
        2.  **Usuários Fazem Apostas:** Itera sobre cada usuário:
            *   Decisão de Apostar: Verifica se o usuário decide apostar nesta rodada com base na probabilidade do seu perfil.
            *   Quantidade de Apostas: Se decidir apostar, determina quantas apostas fará usando `poisson_truncada_em_1()`.
            *   Criação das Apostas: Para cada aposta desejada:
                *   Calcula o `valor_aposta_calculado`.
                *   Escolhe aleatoriamente um jogo e um resultado para apostar.
                *   Registra a aposta com todos os seus detalhes (ID, usuário, jogo, valor, odd).
                *   Debita o valor do saldo do usuário e atualiza seu balanço e total apostado.
                *   Atualiza as estatísticas da rodada (total apostado, número de apostas, por perfil).
        3.  **Resolução dos Jogos:** Simula o resultado final de cada jogo.
        4.  **Liquidação das Apostas:** Itera sobre todas as apostas feitas na rodada:
            *   Verifica se a aposta foi vencedora comparando com o resultado do jogo.
            *   Se vencedora, calcula o `valor_ganho_bruto` (valor apostado \* odd) e o adiciona ao saldo e balanço do usuário, e atualiza os pagamentos da casa.
        5.  **Atualização Final da Rodada:**
            *   Arredonda saldos e balanços para 2 casas decimais e garante que o saldo não seja negativo.
            *   Calcula o GGR da rodada (total apostado - total pago).
            *   Calcula estatísticas de usuários (ativos, lucrativos, zerados, saldo médio, ativos por perfil).
            *   Armazena todas as estatísticas da rodada no `st.session_state.historico_casa`.
            *   Atualiza as estatísticas acumuladas da casa.
            *   Armazena os jogos e apostas da rodada nos respectivos históricos (`st.session_state.historico_jogos`, `st.session_state.historico_apostas`).

6.  **Painel Principal (Dashboard - `if st.session_state.simulacao_iniciada`):**
    *   Exibe os resultados e análises se a simulação tiver sido iniciada.
    *   Resultados da Rodada Atual (Métricas): Utiliza `st.columns` e `st.metric` para exibir as principais métricas da rodada em duas linhas (faturamento, pagamentos, lucro da casa; métricas de usuários).
    *   Análise Detalhada da Rodada:
        *   Duas colunas (`st.columns([1,2])`):
            *   Coluna 1: Tabela "Jogos da Rodada" (descrição, odds, resultado, volume apostado).
            *   Coluna 2: Tabela "Maiores Pagamentos" (top apostas vencedoras que mais custaram para a casa).
        *   Métricas de "Volume por Perfil" (Conservador, Moderado, Arriscado).
    *   Estatísticas Acumuladas da Casa (Métricas): Seis `st.metric` em uma linha para faturamento, pagamentos, lucro acumulado, margem de lucro, lucro médio/rodada, total de apostas acumuladas.
    *   Gráficos Acumulados:
        *   Evolução do Lucro da Casa (por rodada e acumulado) - `st.line_chart`.
        *   Faturamento vs. Pagamentos por rodada - `st.line_chart`.
        *   Evolução dos Usuários (% Lucrativos vs. % Zerados) - `st.line_chart`.
        *   Usuários Ativos por Perfil ao longo das rodadas - `st.line_chart`.
        *   Saldo Médio dos Usuários ao longo das rodadas - `st.line_chart`.
    *   Explorador de Rodadas Históricas (`st.expander`):
        *   `st.selectbox` para escolher uma rodada anterior.
        *   `st.tabs` para separar a visualização de "Jogos" e "Apostas" da rodada selecionada.
        *   Tabelas (`st.dataframe`) detalhadas para jogos e apostas, com formatação de colunas.
    *   Detalhes dos Usuários (`st.expander`):
        *   Tabela (`st.dataframe`) com dados de todos os usuários (nome, perfil, saldo, nº apostas, etc.).
    *   Histórico Individual do Usuário (`st.expander`):
        *   `st.selectbox` para escolher um usuário específico (ordenado por nome).
        *   Métricas individuais do usuário selecionado (total de apostas, total apostado/ganho, taxa de acerto, lucro/prejuízo).
        *   Tabela (`st.dataframe`) com todas as apostas do usuário selecionado.
        *   Gráfico (`st.line_chart`) da evolução do saldo do usuário selecionado ao longo das rodadas em que apostou.

### 2.3. Lógica Probabilística e Modelagem

O simulador emprega vários conceitos probabilísticos para modelar a aleatoriedade inerente aos jogos de azar e ao comportamento dos apostadores.

#### 2.3.1. Geração de Probabilidades de Jogos de Futebol

A função `gerar_probabilidades_futebol()` é responsável por criar um conjunto realista de probabilidades para os três resultados possíveis de uma partida de futebol: Vitória do Time da Casa (V), Empate (E) e Derrota do Time da Casa (D).

*   Probabilidade de Vitória (*P(V)*): Gerada a partir de uma distribuição uniforme ( U(0.05, 0.70) ). Isso significa que a probabilidade de vitória pode variar entre 5% e 70%, refletindo desde jogos muito desequilibrados até confrontos mais parelhos.
    ```
    [ P(V) \sim U(0.05, 0.70) ]
    ```
*   Probabilidade de Empate (*P(E)*): Gerada a partir de uma distribuição uniforme ( U(0.10, 0.25) ). Empates no futebol geralmente ocorrem com menor frequência do que vitórias ou derrotas, mas dentro de uma faixa relativamente estável.
    ```
    [ P(E) \sim U(0.10, 0.25) ]
    ```
*   Probabilidade de Derrota (*P(D)*): Calculada como o complemento das outras duas, para garantir que a soma das probabilidades seja 1 (ou 100%).
    ```
    [ P(D) = 1 - P(V) - P(E) ]
    ```
*   Validação e Normalização: Após a geração inicial, há uma verificação para garantir que (`P(D)` ≥ 0). Se, devido aos extremos das distribuições uniformes, (`P(D)`) se tornar negativa, a (`P(E)`) é reajustada para (`1 - P(V)`) e (`P(D)`) é definida como 0 (um cenário extremo e raro). Finalmente, todas as probabilidades são arredondadas para duas casas decimais e, se necessário, a (`P(D)`) é recalculada para assegurar que (`P(V) + P(E) + P(D) = 1.00`).

O resultado final é uma lista de três probabilidades, por exemplo, `[0.45, 0.30, 0.25]`, que representam as chances "reais" de cada resultado ocorrer.

#### 2.3.2. Cálculo das Odds da Casa

A função `calcular_odds_casa()` transforma as probabilidades reais em odds que serão oferecidas aos apostadores. Este processo inclui a incorporação da margem de lucro da casa (`margem_casa_global`).

1.  Fair Odds (Odds Justas): Para cada probabilidade real (*P<sub>real</sub>*) de um resultado, a odd justa (sem margem da casa) é o inverso da probabilidade:
    ```
    [ \text{Odd}{\text{justa}} = \frac{1}{P{\text{real}}} ]
    ```
    Por exemplo, se *P(V)* = 0.50, a odd justa para a vitória seria 1 / 0.50 = 2.00.

2.  Incorporação da Margem da Casa: A casa não oferece odds justas, pois precisa de uma margem para operar lucrativamente. A `margem_casa_global` (um percentual, por exemplo, 5% ou 0.05) é aplicada para reduzir o pagamento potencial, efetivamente inflando a probabilidade implícita nas odds.
    A odd da casa é calculada como:
    ```
    [ \text{Odd}{\text{casa}} = \text{Odd}{\text{justa}} \times (1 - \text{margem_casa_global}) ]
    ```
    Continuando o exemplo, com uma margem de 5%:
    ```
    [ \text{Odd}_{\text{casa}} = 2.00 \times (1 - 0.05) = 2.00 \times 0.95 = 1.90 ]
    ```
    Isso significa que, em vez de pagar R$2,00 para cada R$1,00 apostado em um evento com 50% de chance, a casa pagará R$1,90. A diferença é a margem da casa.

3.  Odd Mínima: Existe uma garantia de que a odd nunca será inferior a 1.01. Odds de 1.00 ou menos significariam que o apostador receberia menos do que apostou, mesmo ganhando, o que não é prático.

4.  Probabilidade Zero: Se uma probabilidade real for zero (evento impossível), uma odd muito alta (999.0) é atribuída como um placeholder, embora na prática tais eventos não devam ocorrer com a geração atual de probabilidades.

O conjunto de odds da casa `[Odd(V), Odd(E), Odd(D)]` é então usado para calcular os pagamentos das apostas.

#### 2.3.3. Simulação do Resultado do Jogo

A função `simular_resultado_jogo()` usa as probabilidades reais (não as odds da casa) para determinar o resultado de uma partida. Ela utiliza a função `numpy.random.choice()`, que permite escolher um item de uma lista com base em um conjunto de probabilidades associadas.

*   Input: Lista de resultados possíveis (e.g., ["Vitória", "Empate", "Derrota"]) e a lista de suas probabilidades reais (e.g., [0.45, 0.30, 0.25]).
*   Output: Uma string representando o resultado sorteado (e.g., "Empate").

Este método garante que, ao longo de muitas simulações, a frequência observada de cada resultado convirja para as probabilidades reais definidas para o jogo.

#### 2.3.4. Comportamento do Apostador: Decisão e Quantidade de Apostas

O comportamento de cada apostador é regido por parâmetros do seu perfil e por processos estocásticos.

1.  **Decisão de Apostar na Rodada:**
    *   Cada perfil (Conservador, Moderado, Arriscado) possui um parâmetro `prob_decidir_apostar` (e.g., Conservador: 0.60, Arriscado: 0.95).
    *   Em cada rodada, para cada usuário, um número aleatório (*R* ~ U(0, 1)) é gerado.
    *   Se *R* < `prob_decidir_apostar`, o usuário decide fazer apostas naquela rodada.

2.  **Quantidade de Apostas Desejadas (Poisson Truncada):**
    *   Se um usuário decide apostar, a quantidade de apostas que ele deseja fazer é determinada pela função `poisson_truncada_em_1()`. Esta função utiliza a Distribuição de Poisson.
    *   A Distribuição de Poisson, `P(k; λ) = (λ^k * e^(-λ)) / k!`, modela o número de vezes que um evento ocorre em um intervalo fixo de tempo ou espaço, dado uma taxa média de ocorrência (*λ*) (lambda).
    *   No nosso caso, (*λ*) é o parâmetro `lambda_poisson` do perfil do usuário (e.g., Conservador: 1.5, Arriscado: 3.5), representando a "média de apostas desejadas" por aquele perfil quando ele decide apostar.
    *   A modificação "truncada em 1" significa que a função só retorna valores (≥ 1). Se a Poisson gerar 0, um novo número é sorteado até que um valor positivo seja obtido. Isso garante que, se um usuário decide apostar, ele fará pelo menos uma aposta.
    *   O usuário então tentará fazer essa quantidade de apostas, limitado pelo seu saldo disponível e pelo valor mínimo de aposta.

#### 2.3.5. Cálculo do Valor da Aposta

A função `calcular_valor_aposta()` determina o montante que um usuário apostará em uma única aposta, seguindo uma lógica específica para equilibrar o comportamento do perfil com regras práticas de aposta:

1.  Saldo Insuficiente para Aposta Mínima: Se o saldo atual do usuário (`saldo_usuario`) for menor que `VALOR_APOSTA_MINIMA` (R$ 5,00) mas maior que zero, o usuário aposta todo o saldo restante.
    ```
    [ \text{Se } 0 < \text{saldo_usuario} < \text{VALOR_APOSTA_MINIMA} \rightarrow \text{valor_aposta} = \text{saldo_usuario} ]
    ```

2.  Geração Baseada no Perfil: Se o saldo for suficiente, o valor da aposta é inicialmente proposto com base em um percentual do saldo atual do usuário. Este percentual é sorteado de uma distribuição uniforme entre `perc_saldo_aposta_min` e `perc_saldo_aposta_max`, definidos no perfil do usuário.
    ```
    [ \text{perc_aposta} \sim U(\text{perc_min}, \text{perc_max}) ]
    ```
    ```
    [ \text{valor_proposto} = \text{saldo_usuario} \times \text{perc_aposta} ]
    ```
    Por exemplo, um perfil Conservador pode ter `perc_min` = 0.05 (5%) e `perc_max` = 0.15 (15%).

3.  Ajuste pelo Valor Mínimo: Se o `valor_proposto` for menor que `VALOR_APOSTA_MINIMA`, o valor da aposta é ajustado para `VALOR_APOSTA_MINIMA`.
    ```
    [ \text{Se } \text{valor_proposto} < \text{VALOR_APOSTA_MINIMA} \rightarrow \text{valor_final_aposta} = \text{VALOR_APOSTA_MINIMA} ]
    ```
    Caso contrário, `valor_final_aposta` = `valor_proposto`.

4.  Garantia de Não Exceder o Saldo: Finalmente, o valor da aposta é limitado ao saldo disponível do usuário.
    ```
    [ \text{valor_final_aposta} = \min(\text{valor_final_aposta}, \text{saldo_usuario}) ]
    ```

Todos os valores monetários são arredondados para duas casas decimais para evitar problemas de precisão de ponto flutuante.

#### 2.3.6. Seleção do Jogo e Resultado para Apostar

Quando um usuário decide fazer uma aposta específica:

*   Escolha do Jogo: Um jogo é selecionado aleatoriamente (`random.choice()`) da lista de jogos disponíveis na rodada atual.
*   Escolha do Resultado: Um dos três resultados possíveis para aquele jogo (Vitória, Empate, Derrota) é selecionado aleatoriamente (`random.randint(0, 2)`), com igual probabilidade para cada um dos três resultados. Não há "inteligência" do apostador em escolher o resultado mais provável; a escolha é puramente aleatória, refletindo um apostador não informado ou que aposta por impulso em qualquer opção disponível.

### 2.4. Gerenciamento de Estado e Interatividade

O **Streamlit** gerencia o estado da aplicação através do objeto `st.session_state`. Qualquer variável que precise persistir entre as interações do usuário (como cliques em botões, mudanças em sliders) deve ser armazenada em `st.session_state`.

*   Inicialização: No início da execução do script, verifica-se se as chaves essenciais (como `simulacao_iniciada`, `rodada_atual`, `usuarios`, etc.) existem em `st.session_state`. Se não existirem, são inicializadas com valores padrão.
*   Modificação: A lógica da simulação atualiza diretamente os valores em `st.session_state` (e.g., `st.session_state.rodada_atual += 1`, `st.session_state.usuarios[i]["saldo"] -= valor_aposta`).
*   Re-renderização: Após cada interação que modifica o `st.session_state` (como clicar no botão "Próxima Rodada"), o **Streamlit** re-executa o script `app.py` do início ao fim. Os valores em `st.session_state` são preservados, permitindo que a interface reflita o novo estado.

Os widgets interativos (sliders, botões, selectboxes) são vinculados a chaves no `st.session_state` ou seus valores são usados para atualizar o estado quando uma ação é disparada.

### 2.5. Precisão Numérica

Devido à natureza das transações financeiras, a precisão dos cálculos é crucial. Operações com números de ponto flutuante podem levar a pequenos erros de arredondamento que se acumulam ao longo do tempo.

Para mitigar isso, as seguintes medidas foram tomadas:

*   Arredondamento Consistente: Todos os valores monetários (saldos, valores de aposta, prêmios, balanços) são explicitamente arredondados para duas casas decimais (`round(valor, 2)`) após cada operação que possa alterar seu valor (subtração, adição, multiplicação).
*   Cálculo do Balanço Pessoal: O `balanco_pessoal` de um usuário é calculado como `round(saldo_atual - saldo_inicial, 2)` ao final de cada rodada para garantir consistência com o saldo atual, em vez de apenas acumular débitos e créditos que poderiam levar a desvios.
*   Valor Mínimo de Aposta: A regra do `VALOR_APOSTA_MINIMA` também ajuda a evitar apostas de valores excessivamente pequenos que poderiam exacerbar problemas de precisão.

## 📊 Funcionalidades Detalhadas e Interface do Usuário

### 3.1. Configurações da Simulação (Barra Lateral)

A barra lateral (`st.sidebar`) é o centro de controle da simulação, permitindo ao usuário ajustar os parâmetros antes de iniciar ou entre as rodadas.

*   Número de Usuários Iniciais: `st.number_input` para definir quantos apostadores participarão da simulação (padrão: 100). Este campo é desabilitado após a primeira rodada.
*   Saldo Inicial por Usuário (R$): `st.number_input` para o valor com que cada usuário começa (padrão: R$ 100). Desabilitado após a primeira rodada.
*   Margem da Casa nas Odds (%): `st.slider` para definir a margem de lucro da casa (0% a 20%, padrão: 5%). Este valor influencia diretamente as odds oferecidas.
*   Número de Jogos por Rodada: `st.number_input` para definir quantos jogos serão simulados em cada rodada (padrão: 5).

*   Comportamento dos Usuários (Perfis): Para cada um dos três perfis (Conservador, Moderado, Arriscado), um `st.expander` organiza os seguintes controles:
    *   Probabilidade de Decidir Apostar: `st.slider` (0.05 a 1.0) - A chance de o usuário deste perfil fazer apostas na rodada.
    *   Média de Apostas Desejadas (λ): `st.slider` (0.5 a 7.0) - O parâmetro lambda para a distribuição de Poisson truncada, que determina o número de apostas que o perfil tentará fazer.
    *   Min % Saldo / Max % Saldo: Dois `st.number_input` lado a lado (`st.columns`) para definir o intervalo percentual do saldo que será usado para calcular o valor de uma aposta individual. Uma validação (`st.warning`) é exibida se Min % ≥ Max %.

*   Botões de Ação:
    *   ▶️ Iniciar / Próxima Rodada: Botão principal que avança a simulação. É desabilitado se houver erros de configuração nos perfis (Min % ≥ Max %).
    *   🔄 Resetar Simulação: Reinicia todo o estado da simulação para os valores iniciais, permitindo começar uma nova simulação com os mesmos ou novos parâmetros da barra lateral (exceto as configurações de perfil, que são mantidas).

### 3.2. Dashboard Principal: Resultados e Análises

Quando a simulação está em andamento, o painel principal exibe uma riqueza de informações.

#### 3.2.1. Resultados da Rodada Atual
Exibidos no topo, logo abaixo do cabeçalho da rodada (`st.header`).

*   **Linha 1: Métricas da Casa/Operação da Rodada** (5 colunas - `st.metric`):
    1.  **Faturamento Rodada:** Total de dinheiro apostado na rodada atual.
    2.  **Pagamentos Rodada:** Total de dinheiro pago pela casa em prêmios na rodada atual.
    3.  **Lucro Rodada:** Faturamento da Rodada - Pagamentos da Rodada. Inclui um "delta" mostrando o percentual do lucro em relação ao faturamento da rodada.
    4.  **Nº Apostas Rodada:** Número total de apostas feitas na rodada atual.
    5.  **Valor Médio Apostado:** Faturamento da Rodada / Nº Apostas da Rodada.

*   **Linha 2: Métricas dos Usuários na Rodada** (5 colunas - `st.metric`):
    1.  **Total de Usuários:** Contagem total de usuários na simulação.
    2.  **Usuários Lucrativos:** Número de usuários cujo saldo atual é maior que o saldo inicial.
    3.  **Usuários Ativos:** Número de usuários com saldo > R$ 0,00.
    4.  **Usuários Falidos:** Número de usuários com saldo = R$ 0,00.
    5.  **Saldo Médio:** Média do saldo de todos os usuários.

#### 3.2.2. Análise Detalhada da Rodada (Substituiu "Desempenho por Perfil")
Esta seção fornece uma visão mais granular da rodada atual.

*   **Duas Colunas Principais** (`st.columns([1, 2])`):
    *   **Coluna 1: 🎮 Jogos da Rodada** (`st.dataframe`):
        *   Colunas: Jogo (descrição), Vitória (odd), Empate (odd), Derrota (odd), Resultado (final), Volume (total apostado naquele jogo).
        *   Permite ver rapidamente todos os jogos da rodada, suas odds, quem venceu e quanto dinheiro movimentaram.
    *   **Coluna 2: 💰 Maiores Pagamentos** (`st.dataframe`):
        *   Mostra as N principais apostas vencedoras que resultaram nos maiores pagamentos pela casa, onde N é o número de jogos na rodada (para manter uma altura de tabela semelhante à de jogos).
        *   Colunas: Usuário (nome), Perfil, Jogo, Aposta (resultado escolhido), Valor (apostado), Odd, Pago (prêmio), Status (✅/❌).
        *   Ajuda a identificar "grandes ganhos" individuais.

*   **Métricas de Volume por Perfil** (abaixo das tabelas, 3 colunas - `st.metric`):
    1.  **Volume Conservador:** Total apostado por usuários do perfil Conservador na rodada.
    2.  **Volume Moderado:** Total apostado por usuários do perfil Moderado na rodada.
    3.  **Volume Arriscado:** Total apostado por usuários do perfil Arriscado na rodada.

#### 3.2.3. Estatísticas Acumuladas da Casa
Localizada após a análise da rodada, esta seção mostra o desempenho financeiro da casa ao longo de todas as rodadas.

*   **Métricas Chave Acumuladas** (6 colunas - `st.metric`):
    1.  **Faturamento Acumulado:** Soma de todo o dinheiro apostado desde o início.
    2.  **Pagamentos Acumulado:** Soma de todos os prêmios pagos.
    3.  **Lucro Acumulado:** Faturamento Acumulado - Pagamentos Acumulado. O "delta" aqui é colorido (verde para lucro, vermelho para prejuízo) e mostra o valor absoluto do lucro/prejuízo, facilitando a visualização do desempenho financeiro da casa.
    4.  **Margem Lucro Acum. (%):** (Lucro Acumulado / Faturamento Acumulado) \* 100.
    5.  **Lucro Médio/Rodada:** Lucro Acumulado / Número de Rodadas.
    6.  **Total Apostas Acum.:** Número total de apostas feitas em todas as rodadas.

#### 3.2.4. Gráficos de Evolução Acumulada
Visualizações que mostram tendências ao longo do tempo (rodadas).

*   **Evolução do Lucro da Casa** (`st.line_chart`):
    *   Duas linhas: "Lucro na Rodada" (GGR de cada rodada individual) e "Lucro Acumulado" (GGR total até aquela rodada).
    *   Permite ver a volatilidade do lucro por rodada e a tendência geral.
*   **Faturamento vs. Pagamentos** (`st.line_chart`):
    *   Duas linhas: "Faturamento" e "Pagamentos" por rodada.
    *   Mostra a relação entre o dinheiro que entra e o dinheiro que sai a cada rodada.
*   **Evolução dos Usuários (%)** (`st.line_chart`):
    *   Duas linhas: "% Lucrativos" (percentual de usuários com saldo > inicial) e "% Zerados" (percentual de usuários com saldo = 0).
    *   Mostra como a "saúde financeira" da base de usuários evolui.
*   **Usuários Ativos por Perfil** (`st.line_chart`):
    *   Três linhas, uma para cada perfil (Conservador, Moderado, Arriscado), mostrando o número de usuários ativos (saldo > 0) de cada perfil ao longo das rodadas.
    *   Cores das linhas correspondem às cores definidas para os perfis.
*   **Saldo Médio dos Usuários** (`st.line_chart`):
    *   Uma linha mostrando a evolução do saldo médio de todos os usuários.

### 3.3. Ferramentas de Exploração de Dados (`st.expander`)

Estas seções expansíveis permitem uma análise mais profunda de dados históricos e individuais.

#### 3.3.1. Explorar Jogos e Apostas por Rodada

*   **Seletor de Rodada** (`st.selectbox`): Permite ao usuário escolher qualquer rodada anterior para análise. Por padrão, mostra a última rodada.
*   **Abas** (`st.tabs`): "🎮 Jogos" e "💰 Apostas"
    *   **Aba Jogos:** Exibe uma tabela (`st.dataframe`) com todos os detalhes dos jogos da rodada selecionada: ID, Descrição, Resultados Possíveis, Probabilidades Reais, Odds da Casa e Resultado Final.
    *   **Aba Apostas:**
        *   Métricas da rodada selecionada (Total de Apostas, Total Faturado, Total Pago, Apostas Vencedoras).
        *   Tabela (`st.dataframe`) com todas as apostas feitas na rodada selecionada. Colunas: Usuário (nome), Perfil, Jogo, Aposta (resultado), Valor, Odd, Ganhou?, Prêmio. Esta tabela mostra todas as apostas, não apenas um subconjunto.

#### 3.3.2. Detalhes dos Usuários

*   Exibe uma tabela (`st.dataframe`) com informações consolidadas de todos os usuários na simulação.
*   Colunas: Nome, Perfil, Saldo (atual), Nº de Apostas Feitas (total em todas as rodadas), Nº Rodadas C/ Aposta (em quantas rodadas o usuário fez pelo menos uma aposta), Total Faturado (quanto o usuário apostou no total, que é faturamento para a casa vindo dele), Balanço Pessoal (Saldo Atual - Saldo Inicial).
*   A tabela é útil para classificar e comparar o desempenho e atividade dos usuários.

#### 3.3.3. Histórico Individual do Usuário

Permite uma análise detalhada do histórico de um apostador específico.

*   **Seletor de Usuário** (`st.selectbox`): Lista todos os usuários (ordenados alfabeticamente por nome) para seleção.
*   **Estatísticas Pessoais** (5 colunas - `st.metric`): Para o usuário selecionado:
    1.  **Total de Apostas** (feitas por este usuário).
    2.  **Total Apostado** (soma de todos os valores apostados por ele).
    3.  **Total Ganho** (soma de todos os prêmios recebidos).
    4.  **Taxa de Acerto** ((Apostas Vencedoras / Total de Apostas) \* 100).
    5.  **Lucro/Prejuízo** (Total Ganho - Total Apostado).
*   **Histórico Completo de Apostas** (`st.dataframe`):
    *   Tabela com todas as apostas feitas pelo usuário selecionado, ordenadas da rodada mais recente para a mais antiga.
    *   Colunas: Rodada, Jogo, Aposta, Valor, Odd, Resultado (da aposta ✅/❌), Prêmio, Lucro (da aposta individual).
*   **Gráfico de Saldo por Rodada** (`st.line_chart`):
    *   Mostra a evolução do saldo do usuário selecionado ao final de cada rodada em que ele participou (ou seja, fez apostas ou teve seu saldo alterado por elas).
    *   O eixo Y representa o saldo e o eixo X as rodadas.

## 🛠️ Decisões de Design e Melhorias Futuras

### 4.1. Principais Decisões de Design

*   Simplicidade Inicial com `app.py` Único: Para facilitar o desenvolvimento rápido e o compartilhamento, comum em projetos **Streamlit**, optou-se por um único arquivo. Para projetos maiores, a modularização em múltiplos arquivos e classes seria mais apropriada.
*   Foco em Futebol (3 Resultados): Simplificou a lógica inicial de geração de jogos e odds. A estrutura permite expansão para outros esportes ou mercados.
*   Perfis de Apostador Baseados em Regras: Em vez de IA complexa, os perfis seguem regras claras e parâmetros estatísticos (probabilidade de apostar, Poisson para quantidade, percentual do saldo). Isso torna o comportamento deles compreensível e os efeitos de suas configurações, analisáveis.
*   Uso Intensivo de `st.session_state`: Essencial para a reatividade e persistência de dados em uma aplicação **Streamlit**.
*   Priorização da Visualização de Dados: O dashboard foi projetado para oferecer múltiplas perspectivas sobre os dados (métricas, tabelas, gráficos), permitindo uma análise rica.
*   Feedback Contínuo e Iterativo: O desenvolvimento seguiu um ciclo de implementação de funcionalidades, teste, feedback (baseado na observação do comportamento do simulador) e refatoração/correção.
*   Arredondamento para Precisão Financeira: A decisão de arredondar todos os valores monetários para duas casas decimais em cada etapa de cálculo foi crucial para evitar discrepâncias e garantir a integridade dos saldos e balanços.

### 4.2. Melhorias Futuras e Extensões Possíveis

O simulador atual é uma base sólida, mas existem diversas avenidas para expansão e aprimoramento:

*   Modelos de Apostador Mais Sofisticados:
    *   Introduzir "memória" ou aprendizado simples (e.g., apostar mais após uma vitória, ou mudar de estratégia após perdas).
    *   Permitir que apostadores escolham jogos/resultados com base nas odds (e.g., value betting) ou em "dicas" (probabilidades levemente distorcidas).
*   Novos Tipos de Esportes e Mercados de Apostas:
    *   Adicionar outros esportes (e.g., basquete, tênis) com suas próprias lógicas de resultado.
    *   Incluir mercados mais complexos (handicaps, totais, apostas combinadas).
*   Recursos Avançados da Casa de Apostas:
    *   Implementar um sistema de "cash out".
    *   Adicionar bônus de boas-vindas ou promoções de fidelidade.
    *   Simular limites de aposta por jogo ou por usuário.
*   Análise Estatística Mais Profunda:
    *   Testes de hipótese sobre a lucratividade de diferentes estratégias.
    *   Análise de sensibilidade dos lucros da casa em relação à sua margem.
    *   Detecção de padrões de apostas.
*   Melhorias na Interface e UX:
    *   Opção para exportar dados (CSV, Excel).
    *   Mais opções de personalização de gráficos.
    *   Um "modo tutorial" para guiar novos usuários pelas funcionalidades.
*   Otimização de Performance: Para simulações com um número muito grande de usuários ou rodadas, otimizações no processamento de dados podem ser necessárias (embora **Pandas** e **NumPy** já sejam bastante eficientes).
*   Modularização do Código: Refatorar o `app.py` em múltiplos módulos/classes para melhor organização e manutenibilidade à medida que o projeto cresce.
*   Testes Automatizados: Implementar testes unitários e de integração para garantir a robustez do código.

## 🏁 Conclusão

O Simulador de Casa de Apostas Avançado desenvolvido atingiu com sucesso seus objetivos primários de criar uma ferramenta interativa e educacional para modelar e analisar a dinâmica das apostas esportivas. Através de uma interface rica e configurável construída com **Streamlit**, os usuários podem explorar como diferentes perfis de apostadores interagem com um sistema de jogos e odds definido pela casa, e observar as consequências financeiras dessas interações.

A incorporação de modelos probabilísticos como a Distribuição de Poisson e a Uniforme, juntamente com uma lógica cuidadosa para o cálculo de valores de apostas e odds, confere um grau de realismo útil para a simulação. As extensas funcionalidades de dashboard, incluindo métricas em tempo real, gráficos de evolução e ferramentas de exploração histórica, fornecem insights valiosos tanto sobre o desempenho da casa quanto sobre o comportamento e o destino financeiro dos apostadores.

As decisões de design, como o foco na precisão numérica e a estrutura iterativa de desenvolvimento, foram fundamentais para a criação de uma aplicação funcional e confiável. Embora haja um vasto campo para melhorias e extensões futuras, o simulador, em seu estado atual, já serve como uma excelente plataforma para aprendizado, experimentação e demonstração dos complexos mecanismos que regem o mundo das apostas esportivas.
 