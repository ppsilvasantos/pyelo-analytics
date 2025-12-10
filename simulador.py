from equipe import Equipe
import pandas as pd
import matplotlib.pyplot as plt

class SimuladorElo:
    def __init__(self, esporte):
        #Inicia a instância do simulador
        self.esporte = esporte
        self.times = {}
        self.df = None
            


    def carregar_dados(self, arquivo):
        # Apaga os dados antigos
        self.times = {} 
        self.df = None
        # Lê o arquivo
        dados = pd.read_csv(arquivo)

        # Limpa os nomes das colunas
        colunas_dados = [nome.strip().upper() for nome in dados.columns]

        # Aplica os nomes limpos ao dataframe e confere a formatação
        dados.columns = colunas_dados

        colunas_esperadas = ["TIME A", "TIME B", "PLACAR A", "PLACAR B"]
        for coluna in colunas_esperadas:
            if coluna not in colunas_dados:
                print(f"Erro: {coluna} não foi encontrada no dataset.")
                raise KeyError("Arquivo CSV com formatação incorreta.")
            
        # Limpeza de dados
        dados['TIME A'] = dados['TIME A'].str.strip().str.title()
        dados['TIME B'] = dados['TIME B'].str.strip().str.title()
        
        self.df = dados

        #Acessa os times únicos
        times_a = set(self.df['TIME A'])
        times_b = set(self.df['TIME B'])
        todos_os_times = times_a.union(times_b)

        #Usa a classe equipe para criar os dados de cada time.
        for time in todos_os_times:
            self.times[time] = Equipe(time)

    def consultar_time(self, nome):

        # Limpa o nome para consulta
        nome = nome.strip().title()

        # Verifica se o nome está entre as equipes carregadas e retorna a consulta
        if nome in self.times:
            equipe = self.times[nome]
            return equipe.obter_resumo()
        else:
            return f"Erro: {nome} não foi encontrado."
        
    def calcular_novos_ratings(self, jogo):

        # Cálculos matemáticos
        def sequencia_vitorias(ultimos_jogos):
            if ultimos_jogos == "VVV":
                sequencia = 9
            elif ultimos_jogos == "VVE" or ultimos_jogos == "VEV" or ultimos_jogos == "EVV":
                sequencia = 7
            elif ultimos_jogos == "VVD" or ultimos_jogos == "VDV" or ultimos_jogos == "DVV":
                sequencia = 6
            elif ultimos_jogos == "VEE" or ultimos_jogos == "EVE" or ultimos_jogos == "EEV":
                sequencia = 5
            elif ultimos_jogos == "VDE" or ultimos_jogos == "VED" or ultimos_jogos == "EDV" or ultimos_jogos == "EVD" or ultimos_jogos == "DVE" or ultimos_jogos == "DEV":
                sequencia = 4
            elif ultimos_jogos == "VDD" or ultimos_jogos == "DVD" or ultimos_jogos == "DDV" or ultimos_jogos == "EEE":
                sequencia = 3
            elif ultimos_jogos == "DEE" or ultimos_jogos == "EDE" or ultimos_jogos == "EED":
                sequencia = 2
            elif ultimos_jogos == "EDD" or ultimos_jogos == "DED" or ultimos_jogos == "DDE":
                sequencia = 1
            elif ultimos_jogos == "DDD":
                sequencia = 0
            return sequencia
        
        objeto_a = self.times[jogo["TIME A"]]
        objeto_b = self.times[jogo["TIME B"]]

        esporte = self.esporte

        ultimos_jogos_a = objeto_a.sequencia[-3:]
        ultimos_jogos_b = objeto_b.sequencia[-3:]
        uja = "".join(ultimos_jogos_a)
        ujb = "".join(ultimos_jogos_b)

        sequencia_a = 0
        sequencia_b = 0
        if len(ultimos_jogos_a) >= 3:
            sequencia_a = sequencia_vitorias(uja)

        if len(ultimos_jogos_b) >= 3:
            sequencia_b = sequencia_vitorias(ujb)

        if esporte == "futebol":

            rating_time_a = float(objeto_a.rating_atual)
            rating_time_b = float(objeto_b.rating_atual)

            time_a_ganhou = False
            time_b_ganhou = False
            empate = False

            if jogo["PLACAR A"] > jogo["PLACAR B"]:
                time_a_ganhou = True
            elif jogo["PLACAR B"] < jogo["PLACAR A"]:
                time_b_ganhou = True
            else:
                empate = True

            fator_casa_sequencia_a = (1.1*rating_time_a)*((sequencia_a/9)+1) - rating_time_a*(0.85*sequencia_a/9)
            fator_casa_sequencia_b = (0.9*rating_time_b)*((sequencia_b/9)+1) - rating_time_b*(0.76*sequencia_b/9)

            if rating_time_a > rating_time_b:
                probabilidade_a = (1.2*fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_b = 1 - probabilidade_a
            elif rating_time_b > rating_time_a:
                probabilidade_b = 1.2*(fator_casa_sequencia_b) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_a = 1 - probabilidade_b
            else:
                probabilidade_a = (fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_b = 1 - probabilidade_a
            
            if time_a_ganhou:
                if probabilidade_a >= 0.5:
                    mult_a = 1 + (1-probabilidade_a)/10
                    mult_b = 1 - (mult_a - 1)
                    rating_atualizado_time_a = rating_time_a * mult_a
                    rating_atualizado_time_b = rating_time_b * mult_b
                elif probabilidade_a < 0.5:
                    mult_a = 1 + 1.5*(1-probabilidade_a)/10
                    mult_b = 1 - (mult_a - 1)
                    rating_atualizado_time_a = rating_time_a * mult_a
                    rating_atualizado_time_b = rating_time_b * mult_b

                objeto_a.atualizar_rating(rating_atualizado_time_a)
                objeto_a.adicionar_resultado("V")
                objeto_b.atualizar_rating(rating_atualizado_time_b)
                objeto_b.adicionar_resultado("D")
                
            elif time_b_ganhou:
                if probabilidade_b >= 0.5:
                    mult_b = 1 + (1.1*(1-probabilidade_b)/10)
                    mult_a = 1 - (mult_b - 1)
                    rating_atualizado_time_b = rating_time_b * mult_b
                    rating_atualizado_time_a = rating_time_a * mult_a
                elif probabilidade_b < 0.5:
                    mult_b = 1 + 1.5*(1.1*((1-probabilidade_b)/10))
                    mult_a = 1 - (mult_b - 1)
                    rating_atualizado_time_b = rating_time_b * mult_b
                    rating_atualizado_time_a = rating_time_a * mult_a
                
                objeto_a.atualizar_rating(rating_atualizado_time_a)
                objeto_a.adicionar_resultado("D")
                objeto_b.atualizar_rating(rating_atualizado_time_b)
                objeto_b.adicionar_resultado("V")

            else:
                if probabilidade_a >= 0.5:
                    mult_b = 1 + 1.1*((1-probabilidade_b)/10)
                    mult_a = 1 - (mult_b - 1)
                    rating_atualizado_time_b = rating_time_b * mult_b
                    rating_atualizado_time_a = rating_time_a * mult_a
                else:
                    mult_a = 1 + (1-probabilidade_a)/20
                    mult_b = 1 - (mult_a - 1)
                    rating_atualizado_time_a = rating_time_a * mult_a
                    rating_atualizado_time_b = rating_time_b * mult_b

                objeto_a.atualizar_rating(rating_atualizado_time_a)
                objeto_a.adicionar_resultado("E")
                objeto_b.atualizar_rating(rating_atualizado_time_b)
                objeto_b.adicionar_resultado("E")
        
        else:

            rating_time_a = float(objeto_a.rating_atual)
            rating_time_b = float(objeto_b.rating_atual)

            time_a_ganhou = False
            time_b_ganhou = False

            if jogo["PLACAR A"] > jogo["PLACAR B"]:
                time_a_ganhou = True
            else:
                time_b_ganhou = True

            fator_casa_sequencia_a = (1.1*rating_time_a)*((sequencia_a/9)+1) - rating_time_a*(0.85*sequencia_a/9)
            fator_casa_sequencia_b = (0.9*rating_time_b)*((sequencia_b/9)+1) - rating_time_b*(0.76*sequencia_b/9)

            if rating_time_a > rating_time_b:
                probabilidade_a = (1.2*fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_b = 1 - probabilidade_a
            elif rating_time_b > rating_time_a:
                probabilidade_b = 1.2*(fator_casa_sequencia_b) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_a = 1 - probabilidade_b
            else:
                probabilidade_a = (fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_b = 1 - probabilidade_a
            
            if time_a_ganhou:
                if probabilidade_a >= 0.5:
                    mult_a = 1 + (1-probabilidade_a)/10
                    mult_b = 1 - (mult_a - 1)
                    rating_atualizado_time_a = rating_time_a * mult_a
                    rating_atualizado_time_b = rating_time_b * mult_b
                elif probabilidade_a < 0.5:
                    mult_a = 1 + 1.5*(1-probabilidade_a)/10
                    mult_b = 1 - (mult_a - 1)
                    rating_atualizado_time_a = rating_time_a * mult_a
                    rating_atualizado_time_b = rating_time_b * mult_b

                objeto_a.atualizar_rating(rating_atualizado_time_a)
                objeto_a.adicionar_resultado("V")
                objeto_b.atualizar_rating(rating_atualizado_time_b)
                objeto_b.adicionar_resultado("D")
                
            else:
                if probabilidade_b >= 0.5:
                    mult_b = 1 + (1.1*(1-probabilidade_b)/10)
                    mult_a = 1 - (mult_b - 1)
                    rating_atualizado_time_b = rating_time_b * mult_b
                    rating_atualizado_time_a = rating_time_a * mult_a
                elif probabilidade_b < 0.5:
                    mult_b = 1 + 1.5*(1.1*((1-probabilidade_b)/10))
                    mult_a = 1 - (mult_b - 1)
                    rating_atualizado_time_b = rating_time_b * mult_b
                    rating_atualizado_time_a = rating_time_a * mult_a
                
                objeto_a.atualizar_rating(rating_atualizado_time_a)
                objeto_a.adicionar_resultado("D")
                objeto_b.atualizar_rating(rating_atualizado_time_b)
                objeto_b.adicionar_resultado("V")
      
    def processar_temporada(self):
        linhas = []

        linhas.append("Processando temporada...")

        for indice, jogo in self.df.iterrows():
            self.calcular_novos_ratings(jogo)

        linhas.append("Temporada processada!")

        return linhas
    
    def obter_ranking_final(self):
        # Verifica se existem times carregados
        if not self.times:
            return "Nenhum time carregado!"
        else:
            linhas = []
            linhas.append("RANKING ATUAL (DECRESCENTE POR ELO)\n")
            # Acessa os times únicos
            lista_times = list(self.times.values())

            # Ordena por ordem decrescente com o desempate na ordem alfabética
            times_ordenados = sorted(lista_times, key = lambda time: (-time.rating_atual, time.nome))

            # Escreve o cabeçalho
            linhas.append(f"{'POS':<5} {'TIME':<25} {'RATING':<10}")
            linhas.append("-" * 40)

            for i, time in enumerate(times_ordenados, 1):
                # Retorna as informações de cada time
                linhas.append(f"{i:<5} {time.nome:<25} {time.rating_atual:.2f}")
                
            return "\n".join(linhas)
        
    def salvar_ranking(self, arquivo_saida):
        # Verifica se há times carregados
        if not self.times:
            print("Erro: Não há dados carregados para salvar.")
            return
        else:
            print(f"Salvando ranking em '{arquivo_saida}'...")

            # Acessa os times únicos
            lista_times = list(self.times.values())

            # Ordena por ordem decrescente com o desempate na ordem alfabética
            ranking_ordenado = sorted(lista_times, key=lambda t: (-t.rating_atual, t.nome))
            try:
                # Abre o arquivo para Escrita ('w' = write)
                with open(arquivo_saida, 'w') as arquivo:
                    
                    # Escreve o Cabeçalho
                    arquivo.write("Posicao,Time,Elo\n")
                    
                    # Escreve as linhas
                    for i, equipe in enumerate(ranking_ordenado, 1):
                        linha = f"{i},{equipe.nome},{equipe.rating_atual:.2f}\n"
                        arquivo.write(linha)
                
                print(f"Sucesso! Ranking salvo em '{arquivo_saida}'.")
            
            except Exception as e:
                print(f"Erro ao salvar arquivo: {e}")

    def obter_ranking_historico(self, rodada):
        # Verifica se há times carregados
        if not self.times:
            return "Erro: nenhum time carregado."
        else:

            # Verifica se a rodada é válida
            try:
                indice = int(rodada)
                if indice < 0:
                    return "Entrada inválida, digite um número positivo."
            except ValueError:
                return "Entrada inválida, digite um número inteiro."
            
            linhas = []
            linhas.append(f"\n--- RANKING HISTÓRICO (Após {indice} jogos/rodadas) ---")
            temp = []

            for time in self.times.values():
                hist = time.obter_historico()

                # Caso a rodada seja maior do que o número de jogos do time, acessa o último rating registrado
                if len(hist) <= indice:
                    rating_rodada = hist[-1]
                else:
                    rating_rodada = hist[indice]

                temp.append((time, rating_rodada))

            # Ordena por ordem decrescente com o desempate na ordem alfabética
            ranking_ordenado = sorted(temp, key=lambda x: (-x[1], x[0].nome))

        # Escreve o cabeçalho
        linhas.append(f"{'POS':<5} {'TIME':<25} {'RATING':<10}")
        linhas.append("-" * 40)
        
        # Escreve as kinhas
        for i, item in enumerate(ranking_ordenado, 1):
            equipe = item[0]
            rating = item[1]
            linhas.append(f"{i:<5} {equipe.nome:<25} {rating:.2f}")
        
        linhas.append("-" * 40)
        return "\n".join(linhas)

    def plotar_evolucao_time(self, nome):
        # Limpa o nome para busca
        nome = nome.strip().title()

        # Verifica se o nome está nos times carregados
        if nome not in self.times:
            print(f"Erro {nome} não encontrado.")
            return
        else:
            time = self.times[nome]
            dados = time.obter_historico()

            print(f"Gerando gráfico para {time.nome}...")

            plt.figure(figsize=(10, 6)) # Cria uma janela de 10x6
            plt.plot(dados, marker='o', linestyle='-', label=time.nome) # Plota o gráfico
            plt.title(f"Evolução do Elo: {time.nome}")
            plt.xlabel("Partidas Jogadas")
            plt.ylabel("Rating Elo")
            plt.grid(True) # Grade no fundo
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.legend()   # Legenda com o nome do time

            plt.show()
            return

    def plotar_comparacao_times(self, nome_time_a, nome_time_b):
        # Limpa os nomes para busca
        nome_time_a = nome_time_a.strip().title()
        nome_time_b = nome_time_b.strip().title()

        # Verifica se os nomes estão nos times carregados
        if nome_time_a not in self.times:
            print(f"Erro {nome_time_a} não encontrado.")
        elif nome_time_b not in self.times:
            print(f"Erro {nome_time_b} não foi encontrado.")
        else:
            time_a = self.times[nome_time_a]
            time_b = self.times[nome_time_b]

            hist_a = time_a.obter_historico()
            hist_b = time_b.obter_historico()

            print(f"Gerando comparação: {time_a.nome} x {time_b.nome}...")

            plt.figure(figsize=(10, 6)) # Cria uma janela 10 x 6

            # Plota os gráficos
            plt.plot(hist_a, marker='o', linestyle='-', label=time_a.nome)
            plt.plot(hist_b, marker='x', linestyle='--', label=time_b.nome)

            plt.title(f"Comparação de Elo: {time_a.nome} vs {time_b.nome}")
            plt.xlabel("Partidas Jogadas")
            plt.ylabel("Rating Elo")
            plt.grid(True)
            plt.legend() # Mostra qual cor é qual time
            
            plt.show()
            return

    def carregar_elos_prontos(self, arquivo):
        # Limpa os dados antigos
        self.times = {} 
        self.df = None
        linhas = []
        # Lê o arquivo
        dados = pd.read_csv(arquivo)
                
        # Limpa os nomes das colunas 
        colunas_dados = [nome.strip().upper() for nome in dados.columns]
        
        # Aplica os nomes limpos ao dataframe e confere a formatação
        dados.columns = colunas_dados 

        colunas_esperadas = ["TIME", "ELO"]
        for coluna in colunas_esperadas:
            if coluna not in colunas_dados:
                linhas.append(f"Erro: {coluna} não foi encontrada no dataset.")
                raise KeyError("Arquivo CSV com formatação incorreta.")
        
        # Limpa os dados
        dados["TIME"] = dados["TIME"].str.strip().str.title()
        
        # Converte os elos para inteiros
        dados["ELO"] = pd.to_numeric(dados["ELO"], errors='coerce').fillna(1500).astype(int)

        self.df = dados 

        # Atualiza o dicionário
        self.times = {} # Limpa o dicionário anterior

        for index, linha in dados.iterrows():
            nome_time = linha["TIME"]
            rating = linha["ELO"]
            
            # Cria a equipe e guarda
            self.times[nome_time] = Equipe(nome_time, rating_inicial=rating)
            
        linhas.append("Elos carregados com sucesso!")

        return "\n".join(linhas)

    def prever_partida(self, mandante, visitante):
        mandante = mandante.strip().title()
        visitante = visitante.strip().title()
        # Validação, Impede simular Time A vs Time A
        if mandante == visitante:
            print("Erro: Selecione dois times diferentes!")
            return
        

        # Recupera os objetos Equipe
        equipe_a = self.times[mandante]
        equipe_b = self.times[visitante]

        rating_time_a = equipe_a.rating_atual
        rating_time_b = equipe_b.rating_atual

        # Cálculo de Probabilidade (sem considerar empate)
        def sequencia_vitorias(ultimos_jogos):
            if ultimos_jogos == "VVV":
                sequencia = 9
            elif ultimos_jogos == "VVE" or ultimos_jogos == "VEV" or ultimos_jogos == "EVV":
                sequencia = 7
            elif ultimos_jogos == "VVD" or ultimos_jogos == "VDV" or ultimos_jogos == "DVV":
                sequencia = 6
            elif ultimos_jogos == "VEE" or ultimos_jogos == "EVE" or ultimos_jogos == "EEV":
                sequencia = 5
            elif ultimos_jogos == "VDE" or ultimos_jogos == "VED" or ultimos_jogos == "EDV" or ultimos_jogos == "EVD" or ultimos_jogos == "DVE" or ultimos_jogos == "DEV":
                sequencia = 4
            elif ultimos_jogos == "VDD" or ultimos_jogos == "DVD" or ultimos_jogos == "DDV" or ultimos_jogos == "EEE":
                sequencia = 3
            elif ultimos_jogos == "DEE" or ultimos_jogos == "EDE" or ultimos_jogos == "EED":
                sequencia = 2
            elif ultimos_jogos == "EDD" or ultimos_jogos == "DED" or ultimos_jogos == "DDE":
                sequencia = 1
            elif ultimos_jogos == "DDD":
                sequencia = 0
            return sequencia
        
        esporte = self.esporte

        ultimos_jogos_a = equipe_a.sequencia[-3:]
        ultimos_jogos_b = equipe_b.sequencia[-3:]
        uja = "".join(ultimos_jogos_a)
        ujb = "".join(ultimos_jogos_b)

        sequencia_a = 0
        sequencia_b = 0
        if len(ultimos_jogos_a) >= 3:
            sequencia_a = sequencia_vitorias(uja)

        if len(ultimos_jogos_b) >= 3:
            sequencia_b = sequencia_vitorias(ujb)

        fator_casa_sequencia_a = (1.1*rating_time_a)*((sequencia_a/9)+1) - rating_time_a*(0.85*sequencia_a/9)
        fator_casa_sequencia_b = (0.9*rating_time_b)*((sequencia_b/9)+1) - rating_time_b*(0.76*sequencia_b/9)

        if rating_time_a > rating_time_b:
                probabilidade_a = (1.2*fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
                probabilidade_b = 1 - probabilidade_a
        elif rating_time_b > rating_time_a:
            probabilidade_b = 1.2*(fator_casa_sequencia_b) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
            probabilidade_a = 1 - probabilidade_b
        else:
            probabilidade_a = (fator_casa_sequencia_a) / (fator_casa_sequencia_a + fator_casa_sequencia_b)
            probabilidade_b = 1 - probabilidade_a

        # Caso o esporte seja futebol, calcula a chance de emapte
        chance_empate = 0
        if  self.esporte == "futebol":
            diferenca = abs(rating_time_a - rating_time_b)
            chance_empate = 0.28 * (2.718 ** - (diferenca / 500))

        # Converte para porcentagem 
        pct_a = (probabilidade_a - (chance_empate / 2)) * 100
        pct_b = (probabilidade_b - (chance_empate / 2)) * 100
        chance_empate = chance_empate * 100

        # Define quem é o favorito teórico
        if pct_a > pct_b:
            favorito = f"Favorito: {mandante}"
        else:
            favorito = f"Favorito: {visitante}"

        # Monta o Texto Final
        print(
            f"{mandante} ({rating_time_a:.0f})  vs  {visitante} ({rating_time_b:.0f})\n"
            f"---------------------------------------\n"
            f"Probabilidades:\n"
            f"{mandante}: {pct_a:.2f}%\n"
            f"{visitante}: {pct_b:.2f}%\n"
            f"Empate: {chance_empate:.2f}%\n"
            f"[{favorito}]"
        )

 