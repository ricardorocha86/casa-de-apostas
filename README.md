# 🎲 Simulador de Casa de Apostas Avançado

## 📜 Descrição Geral

Este projeto é um **Simulador Interativo de Casa de Apostas Esportivas** desenvolvido em Python com a biblioteca Streamlit. Ele permite modelar o funcionamento de uma casa de apostas, analisar o comportamento de diferentes perfis de apostadores (Conservador, Moderado, Arriscado) e visualizar uma ampla gama de métricas financeiras e estatísticas de jogo em tempo real e de forma acumulada.

O objetivo principal é fornecer uma ferramenta dinâmica para entender os fatores que influenciam a lucratividade de uma casa de apostas, o impacto da margem da casa, e como diferentes estratégias de apostas afetam o saldo dos usuários ao longo do tempo.

## ✨ Principais Funcionalidades

*   **Perfis de Apostadores Configuráveis:**
    *   Três perfis distintos: Conservador, Moderado e Arriscado.
    *   Parâmetros ajustáveis por perfil:
        *   Probabilidade de decidir apostar em uma rodada.
        *   Média de apostas desejadas (usando Distribuição de Poisson Truncada em 1).
        *   Percentual mínimo e máximo do saldo a ser apostado.
*   **Simulação Realista de Jogos de Futebol:**
    *   Geração dinâmica de jogos com 3 resultados possíveis (Vitória, Empate, Derrota).
    *   Probabilidades de resultados geradas aleatoriamente dentro de faixas realistas.
    *   Cálculo de odds pela casa, incorporando uma margem de lucro configurável.
*   **Sistema de Apostas Detalhado:**
    *   Valor mínimo de aposta global (R$ 5,00).
    *   Lógica de cálculo do valor da aposta que considera:
        1.  Saldo do usuário vs. valor mínimo.
        2.  Valor proposto pelo perfil vs. valor mínimo.
        3.  Disponibilidade de saldo.
*   **Dashboard Interativo e Abrangente:**
    *   **Resultados da Rodada Atual:** Faturamento, Pagamentos, Lucro (com % do faturamento), Nº Apostas, Valor Médio Apostado, Total de Usuários, Usuários Lucrativos, Ativos, Falidos e Saldo Médio.
    *   **Análise Detalhada da Rodada:**
        *   Tabela de Jogos: Odds, resultado final, volume apostado por jogo.
        *   Maiores Pagamentos: Top apostas que mais custaram para a casa.
        *   Volume de apostas por perfil.
    *   **Estatísticas Acumuladas da Casa:** Faturamento, Pagamentos, Lucro (com delta colorido), Margem de Lucro (%), Lucro Médio/Rodada, Total de Apostas.
*   **Gráficos de Evolução:**
    *   Evolução do Lucro da Casa (lucro na rodada e acumulado).
    *   Faturamento vs. Pagamentos por rodada.
    *   Evolução dos Usuários (percentual de lucrativos vs. zerados).
    *   Evolução de Usuários Ativos por Perfil.
    *   Evolução do Saldo Médio dos Usuários.
*   **Explorador de Rodadas Históricas:**
    *   Seleção de qualquer rodada anterior para análise.
    *   Visualização detalhada dos jogos (odds, probabilidades, resultado).
    *   Visualização de todas as apostas da rodada selecionada (usuário, jogo, valor, odd, resultado, prêmio).
*   **Análise de Usuários:**
    *   Tabela detalhada com informações de cada usuário: Nome, Perfil, Saldo, Nº de Apostas, Nº Rodadas com Aposta, Total Faturado pela casa com o usuário, Balanço Pessoal.
    *   **Histórico Individual do Usuário:**
        *   Seleção de usuário por nome.
        *   Métricas pessoais: Total de apostas, total apostado, total ganho, taxa de acerto, lucro/prejuízo.
        *   Tabela com todas as apostas feitas pelo usuário selecionado.
        *   Gráfico da evolução do saldo do usuário ao longo das rodadas.
*   **Configurações Flexíveis:**
    *   Número de usuários iniciais e saldo inicial.
    *   Margem da casa nas odds.
    *   Número de jogos por rodada.
    *   Ajustes finos para cada perfil de apostador.

## 🛠️ Tecnologias Utilizadas

*   **Python 3.x**
*   **Streamlit:** Para a interface web interativa.
*   **Pandas:** Para manipulação e exibição de dados tabulares.
*   **NumPy:** Para cálculos numéricos e geração de números aleatórios.
*   **Matplotlib (implícito via Streamlit):** Para a geração de gráficos.
*   **Faker:** Para geração de nomes e e-mails fictícios para os usuários.

## 🚀 Como Executar

1.  Certifique-se de ter Python e pip instalados.
2.  Instale as dependências:
    ```bash
    pip install streamlit pandas numpy faker
    ```
3.  Navegue até o diretório do projeto onde o arquivo `app.py` está localizado.
4.  Execute o comando no terminal:
    ```bash
    streamlit run app.py
    ```
5.  A aplicação será aberta automaticamente no seu navegador web.

## 📂 Estrutura do Projeto

*   `app.py`: Contém todo o código da aplicação Streamlit, incluindo a lógica de simulação e a interface do usuário.
*   `Relatorio Resumido.md`: Este arquivo, fornecendo uma visão geral do projeto.
*   `Relatorio Longo.md`: Documentação técnica detalhada do projeto, explicando a arquitetura, funcionalidades, modelos probabilísticos e decisões de design.

## 🎯 Objetivo do Projeto

O simulador foi desenvolvido como uma ferramenta educacional e analítica para:
*   Demonstrar os mecanismos internos de uma casa de apostas.
*   Permitir a experimentação com diferentes parâmetros (margem da casa, comportamento do apostador).
*   Visualizar o impacto financeiro de diferentes cenários de apostas.
*   Oferecer uma plataforma para explorar conceitos de probabilidade e risco no contexto de apostas esportivas.

---
*Este resumo foi gerado com base na funcionalidade completa do aplicativo `app.py`.* 
