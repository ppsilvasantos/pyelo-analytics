# 🏀 PyElo Analytics: Sports Prediction Engine

> **Projeto Final de Introdução à Ciência da Computação I - ICMC/USP**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Data Science](https://img.shields.io/badge/Data%20Science-Statistics-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

## 📄 Sobre o Projeto

O **PyElo Analytics** é um software desktop de análise esportiva desenvolvido para calcular ratings dinâmicos e prever probabilidades de vitória em partidas de Futebol e Basquete.

A principal motivação deste projeto foi unir os conceitos de **Programação Orientada a Objetos (POO)** com **Estatística Aplicada**, fugindo de escopos triviais para resolver um problema real de *Sports Analytics*.

O sistema processa bases de dados históricas (Brasileirão, NBA, etc.), calcula a força relativa das equipes e gera visualizações gráficas de desempenho.

---

## 🧠 Modelagem Matemática (O "Motor" do Sistema)

Apesar do nome "Elo Rating", o sistema utiliza um **algoritmo customizado** desenvolvido pela equipe. Diferente do Elo clássico do Xadrez, nosso modelo incorpora variáveis cruciais para esportes coletivos:

1.  **Fator Casa:** Ponderação estatística para a vantagem do time mandante.
2.  **Momentum (Sequência):** O algoritmo detecta sequências de vitórias ou derrotas (últimos 3 jogos), ajustando a probabilidade pré-jogo com base na "fase" do time.
3.  **Probabilidade Logística:** Cálculo da chance de vitória baseado no diferencial de rating entre as equipes.

---

## 📊 Funcionalidades

* **📈 Cálculo de Rating Histórico:** Processamento de milhares de partidas via arquivos CSV.
* **🎲 Simulador de Partidas:** Previsão probabilística (ex: *Time A tem 64% de chance de vitória*).
* **🖥️ Interface Gráfica (GUI):** Dashboard moderno com modo escuro (Dark Mode).
* **📉 Visualização de Dados:** Geração automática de gráficos de linha mostrando a evolução do time ao longo da temporada.
* **📋 Relatórios Estatísticos:** Exibição de métricas como "Melhor Elo", "Pior Elo" e Cartel (Vitórias/Empates/Derrotas).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Interface:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Modern UI)
* **Manipulação de Dados:** Pandas
* **Visualização:** Matplotlib
* **Imagens:** Pillow (PIL)

---

## 📂 Estrutura do Projeto

O código foi estruturado seguindo práticas de modularização:

* `interface.py`: Gerencia a GUI e a interação com o usuário.
* `simulador.py`: O "cérebro" lógico. Contém a classe `SimuladorElo` que processa os algoritmos.
* `equipe.py`: Modelo de classe que representa um Time (Objeto) e seus atributos estatísticos.
* `main.py`: Versão alternativa para execução via terminal (CLI).

---

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado.

1. **Clone o repositório:**
   ```
   git clone [https://github.com/ppsilvasantos/pyelo-analytics.git]
   cd pyelo-analytics
   
2. **Instale as dependências:**
   ```
   pip install -r requirements.txt
  
3. **Execute a aplicação:**
    ```
    python interface.py

---

## 🔮 Trabalhos Futuros

Como evolução do projeto, mapeamos as seguintes melhorias para versões futuras:

* **🕸️ Web Scraping Automatizado:** Substituir a importação manual de CSVs por *crawlers* (usando `BeautifulSoup` ou `Selenium`) para coletar resultados em tempo real de portais esportivos.
* **💰 Backtesting Financeiro:** Implementar um módulo para comparar as probabilidades do modelo contra as *odds* históricas de casas de apostas, calculando o ROI (Retorno sobre Investimento) teórico e validando a eficiência do algoritmo frente ao mercado.
* **🤖 Comparação com Machine Learning:** Integrar bibliotecas como *Scikit-Learn* para confrontar o desempenho do nosso Elo Customizado contra modelos de Classificação Supervisionada (ex: *Random Forest* ou *Regressão Logística*).
* **u, s, σ (Estatística Descritiva):** Refinar o modelo matemático implementando métricas de dispersão (desvio padrão) e médias móveis ponderadas para tratar a volatilidade do ranking em início de temporada.

---

## 👨‍💻 Autores

Projeto desenvolvido por discentes do curso de Estatística e Ciência de Dados e Ciência de Computação do ICMC-USP:

Pedro Paulo Silva Santos 

Vinicius Gonzalez

Julia Lopes Lamarchi

Docente: Prof. Matheus Machado dos Santos
