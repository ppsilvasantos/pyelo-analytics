class Equipe:
    def __init__(self, nome, rating_inicial=1500):
        #Cria os atributos iniciais de cada equipe
        self.nome = nome
        self.rating_atual = rating_inicial
        self.historico_rating = [rating_inicial]
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        self.sequencia = []
    
    def atualizar_rating(self, novo_rating):
        pass
    
    def obter_resumo(self):
        linhas = []
        linhas.append(f"\n--- RELATÓRIO: {self.nome.upper()} ---")
        linhas.append(f"Rating Atual: {self.rating_atual:.2f}")
        
        # Acessa o max/min evitando erro se a lista estiver vazia
        if self.historico_rating:
            maior = max(self.historico_rating)
            menor = min(self.historico_rating)
        else:
            maior = self.rating_atual
            menor = self.rating_atual

        linhas.append(f"Melhor Elo: {maior:.2f}")
        linhas.append(f"Pior Elo: {menor:.2f}")
        
        total_jogos = self.vitorias + self.derrotas + self.empates
        linhas.append(f"Cartel: {self.vitorias}V - {self.empates}E - {self.derrotas}D (Total: {total_jogos})")
        linhas.append("-" * 30)

        return "\n".join(linhas)

    def obter_historico(self):
        return self.historico_rating

    def atualizar_rating(self, novo_rating):
        # Atualiza o rating atual e salva no histórico.
        self.rating_atual = novo_rating
        self.historico_rating.append(novo_rating)

    def adicionar_resultado(self, resultado):
        # Recebe 'V' (Vitória), 'D' (Derrota) ou 'E' (Empate). Atualiza contadores e sequência.
        self.sequencia.append(resultado)
        
        if resultado == "V":
            self.vitorias += 1
        elif resultado == "D":
            self.derrotas += 1
        elif resultado == "E":
            self.empates += 1