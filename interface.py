from simulador import SimuladorElo
import customtkinter as ctk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image
import os

# Configurações Globais de Aparência
ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("dark-blue")


# Define uma nova classe mas mantendo as funções da classe customtkinter
class InterfaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações Básicas da Janela
        self.title("PyElo Analytics")
        self.geometry("900x600")

        # Inicia o simulador ainda vazio 
        self.simulador = None 

        # Configuração do Grid
        # Coluna 0 = Menu Lateral | Coluna 1 = Conteúdo Principal
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu_lateral()
        self.criar_area_conteudo()

    def limpar_conteudo(self):
            # Remove todos os widgets da área da direita para desenhar uma nova tela
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

    def acao_plotar_evolucao(self):
        # Pega o nome
        time_escolhido = self.menu_grafico_time.get()
        
        # Chama o simulador (o matplotlib ja abre uma janela por padrão)
        self.simulador.plotar_evolucao_time(time_escolhido)

    def acao_gerar_relatorio(self):
        # Pega o nome do time selecionado
        nome_time = self.menu_stats_time.get()

        # Chama o simulaor
        relatorio = self.simulador.consultar_time(nome_time)

        # Exibe na tela
        self.textbox_stats.delete("0.0", "end") # Limpa anterior
        self.textbox_stats.insert("end", relatorio)

    def acao_plotar_comparacao(self):
        # Pega os nomes
        time_a = self.menu_grafico_a.get()
        time_b = self.menu_grafico_b.get()

        # Verificação
        if time_a == time_b:
            messagebox.showwarning("Atenção", "Selecione times diferentes para comparar.")
            return

        # Chama o simulador (o matplotlib ja abre uma janela por padrão)
        self.simulador.plotar_comparacao_times(time_a, time_b)

    def acao_confirmar_esporte(self):
        # Recupera o que o usuário escolheu (futebol ou basquete)
        esporte_selecionado = self.var_esporte.get()

        # Atualiza a instância do simulador
        self.simulador = SimuladorElo(esporte_selecionado)

        # Feedback Visual (Aviso de sucesso)
        messagebox.showinfo("Sucesso", f"Sessão iniciada para: {esporte_selecionado.upper()}.\nCarregue o seu arquivo em 'Carregar Arquivo'")

        # Destrava o botão de "Carregar arquivo"
        self.btn_carregar.configure(state="normal")

    def acao_selecionar_arquivo(self):
        # Abre a janela do sistema para escolher arquivo e Filtra para mostrar CSVs
        caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo de partidas", filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")] )

        # Se o usuário escolheu algo (não cancelou)
        if caminho_arquivo:
            # Limpa o que estava escrito na caixa
            self.entry_arquivo.delete(0, "end")
            # Escreve o caminho novo na caixa
            self.entry_arquivo.insert(0, caminho_arquivo)

    def acao_exibir_ranking_tela(self):
        # Chama o simulador para pegar o texto do ranking
        texto_ranking = self.simulador.obter_ranking_final()
        
        # Joga na tela
        self.textbox_ranking.delete("0.0", "end")
        self.textbox_ranking.insert("end", texto_ranking)

    def acao_salvar_ranking_arquivo(self):
        # Abre a janela do Windows para o usuário escolher onde salvar e com que nome
        caminho_arquivo = filedialog.asksaveasfilename(title="Salvar Ranking como...", defaultextension=".csv",filetypes=[("Arquivo CSV", "*.csv")])

        # 2. Se o usuário cancelou (não escolheu nada)
        if not caminho_arquivo:
            return

        # 3. Chama o backend para salvar
        try:
            self.simulador.salvar_ranking(caminho_arquivo)
            
            messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{caminho_arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo.\nErro: {e}")

    def acao_simular_partida(self):
        # Recupera os nomes selecionados nos menus
        nome_time_a = self.menu_time_a.get()
        nome_time_b = self.menu_time_b.get()

        # 2. Validação, Impede simular Time A vs Time A
        if nome_time_a == nome_time_b:
            self.lbl_resultado_simulacao.configure(text="Erro: Selecione dois times diferentes!", text_color="red")
            return

        # Recupera os objetos Equipe do simulador 
        equipe_a = self.simulador.times[nome_time_a]
        equipe_b = self.simulador.times[nome_time_b]

        rating_time_a = equipe_a.rating_atual
        rating_time_b = equipe_b.rating_atual

        # Cálculos Matemáticos
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
        
        esporte = self.simulador.esporte

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

        chance_empate = 0
        # Caso o esporte seja futebol, calcula a chance de empate
        if  self.var_esporte.get() == "futebol":
            diferenca = abs(rating_time_a - rating_time_b)
            chance_empate = 0.28 * (2.718 ** - (diferenca / 500))

        # Converte para porcentagem 
        pct_a = (probabilidade_a - (chance_empate / 2)) * 100
        pct_b = (probabilidade_b - (chance_empate / 2)) * 100
        chance_empate = chance_empate * 100

        # Define quem é o favorito teórico
        if pct_a > pct_b:
            favorito = f"Favorito: {nome_time_a}"
            cor_destaque = "green" 
        else:
            favorito = f"Favorito: {nome_time_b}"
            cor_destaque = "orange"

        # Monta o Texto Final
        texto_resultado = (
            f"{nome_time_a} ({rating_time_a:.0f})  vs  {nome_time_b} ({rating_time_b:.0f})\n"
            f"---------------------------------------\n"
            f"Probabilidades:\n"
            f"{nome_time_a}: {pct_a:.2f}%\n"
            f"{nome_time_b}: {pct_b:.2f}%\n"
            f"Empate: {chance_empate:.2f}%\n"
            f"[{favorito}]"
        )

        # Exibe na Label de resultado
        self.lbl_resultado_simulacao.configure(text=texto_resultado, text_color="white")
    
    def atualizar_dica_arquivo(self, valor_escolhido):
        if valor_escolhido == "Histórico de Partidas":
            self.lbl_dica.configure(text="Colunas esperadas: TIME A, TIME B, PLACAR A, PLACAR B")
        else:
            self.lbl_dica.configure(text="Colunas esperadas: TIME, ELO")

    def acao_exibir_ranking_rodada_tela(self):
        # Recupera a rodada escolhida
        try:
            rodada = int(self.entry_rodada.get())
        except ValueError:
            self.textbox_rankingr.insert("0.0", "Erro: Digite um número!\n")
            

        # Chama o simulador para pegar o texto do ranking
        texto_ranking = self.simulador.obter_ranking_historico(rodada)
        
        # Joga na tela
        self.textbox_rankingr.delete("0.0", "end")
        self.textbox_rankingr.insert("end", texto_ranking)

    def acao_processar_arquivo(self):
        # Pega o nome do arquivo
        nome_arquivo = self.entry_arquivo.get()

        # Verificação
        if not nome_arquivo:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return

        # Verifica qual modo o usuário escolheu no botão segmentado
        modo_atual = self.seg_modo.get()

        self.textbox_log.delete("0.0", "end")
        self.textbox_log.insert("end", f"Modo: {modo_atual}\nLendo arquivo '{nome_arquivo}'...\n")

        try:
            if modo_atual == "Histórico de Partidas":
                # MODO 1: Calcula o Elo do zero
                self.simulador.carregar_dados(nome_arquivo)
                self.textbox_log.insert("end", "Arquivo lido. Calculando Elos...\n")
                self.simulador.processar_temporada()
                self.textbox_log.insert("end", "Cálculos finalizados!\n\n")
                texto = "As opções 'Estatísticas', 'Simular' e 'Visualizar Gráficos' foram liberadas!"
                self.textbox_log.insert("end", texto)
                
                # Destrava os botões de simular, visualizar gráficos e estatísticas do time
                self.btn_simular.configure(state="normal")
                self.btn_graficos.configure(state="normal")
                self.btn_stats.configure(state="normal")

            else:
                # MODO 2: Carrega Elos prontos 
                # Chama a função específica do simulador.py
                self.simulador.carregar_elos_prontos(nome_arquivo)
                self.textbox_log.insert("end", "Elos carregados!\n\n")
                texto = "A opção 'Simular' foi liberadas!"
                self.textbox_log.insert("end", texto)
                self.btn_simular.configure(state="normal")
                self.btn_graficos.configure(state="disabled")
                self.btn_stats.configure(state="disabled")



        except FileNotFoundError:
            self.textbox_log.insert("end", "ERRO: Arquivo não encontrado.")
            messagebox.showerror("Erro", "Arquivo não encontrado.")
        except KeyError as e:
             self.textbox_log.insert("end", f"ERRO: Colunas incorretas.\n{e}")
             messagebox.showerror("Erro de Formatação", f"As colunas do CSV estão erradas para este modo.\n\nDetalhe: {e}")
        except Exception as e:
            self.textbox_log.insert("end", f"ERRO CRÍTICO: {e}")
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        # Exceto erros (semelhante ao main.py)
        except FileNotFoundError:
            messagebox.showerror("Erro", f"O arquivo '{nome_arquivo}' não foi encontrado.\nVerifique se ele está na mesma pasta.")
            self.textbox_log.insert("end", "ERRO: Arquivo não encontrado.")
        
        except KeyError as e:
            messagebox.showerror("Erro de Formatação", f"As colunas do CSV estão erradas.\n{e}")
            self.textbox_log.insert("end", "ERRO: Colunas inválidas.")

        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")
            self.textbox_log.insert("end", f"ERRO CRÍTICO: {e}")

    def criar_menu_lateral(self):
            # Cria o Frame do Menu (botões)
            self.frame_menu = ctk.CTkFrame(self, width=200, corner_radius=0)
            self.frame_menu.grid(row=0, column=0, sticky="nsew")

            # Título do Projeto
            self.lbl_nome = ctk.CTkLabel(self.frame_menu, text="PyElo Analytics", font=ctk.CTkFont(size=20, weight="bold"))
            self.lbl_nome.grid(row=0, column=0, padx=20, pady=(20, 10))

            # Botões de Navegação
            # Botão Início
            self.btn_inicio = ctk.CTkButton(self.frame_menu, text="Início", command=self.mostrar_inicio, font=("Arial", 20, "bold"))
            self.btn_inicio.grid(row=1, column=0, padx=20, pady=10)

            # Botão Carregar arquivo (Começa desativado até escolher o esporte)
            self.btn_carregar = ctk.CTkButton(self.frame_menu, text="Carregar arquivo", state="disabled",command=self.mostrar_carregar, font=("Arial", 14, "bold"))
            self.btn_carregar.grid(row=2, column=0, padx=20, pady=10)

            # Botão de consultar estatística do time (Começa destravado até carregar um dataframe)
            self.btn_stats = ctk.CTkButton(self.frame_menu, text="Estatísticas", state="disabled", command=self.mostrar_estatisticas, font=("Arial", 14, "bold"))
            self.btn_stats.grid(row=3, column=0, padx=20, pady=10)

            # Botão Simular (Começa desativado até carregar um dataframe)
            self.btn_simular = ctk.CTkButton(self.frame_menu, text="Simular", state="disabled", command=self.mostrar_simular, font=("Arial", 14, "bold"))
            self.btn_simular.grid(row=4, column=0, padx=20, pady=10)

            # Botão de visualizar gráficos (Começa destravado até carregar um dataframe)
            self.btn_graficos = ctk.CTkButton(self.frame_menu, text="Visualizar Gráficos", state="disabled", command=self.mostrar_graficos, font=("Arial", 14, "bold"))
            self.btn_graficos.grid(row=5, column=0, padx=20, pady=10)

    def criar_area_conteudo(self):
        # Cria o Frame Principal
        self.frame_conteudo = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_conteudo.grid(row=0, column=1, sticky="nsew")

        try:
            # Carrega a logo do ICMC
            img_original = Image.open("logo_icmc.jpg")
            logo_ctk = ctk.CTkImage(light_image=img_original, dark_image=img_original, size=(400, 200)) 
            
            lbl_logo = ctk.CTkLabel(self.frame_conteudo, text="", image=logo_ctk)
            lbl_logo.pack(pady=(20, 10))
        except Exception as e:
            # Caso a imagem não seja encontrada, mostra apenas texto para não travar
            pass
        # Informações da Disciplina
        ctk.CTkLabel(self.frame_conteudo, text="SSC0801 - Introdução à Ciência de Computação I", font=("Arial", 16, "bold")).pack(pady=2)
        ctk.CTkLabel(self.frame_conteudo, text="Docente: Prof. Matheus Machado dos Santos", font=("Arial", 14)).pack(pady=2)

        # INTEGRANTES DO GRUPO
        # Frame para agrupar os nomes
        frame_integrantes = ctk.CTkFrame(self.frame_conteudo, fg_color="transparent")
        frame_integrantes.pack(pady=15)

        ctk.CTkLabel(frame_integrantes, text="Integrantes:", font=("Arial", 12, "bold")).pack()
        ctk.CTkLabel(frame_integrantes, text="Pedro Paulo Silva Santos ").pack()
        ctk.CTkLabel(frame_integrantes, text="Vinicius Gonzalez").pack()
        ctk.CTkLabel(frame_integrantes, text="Julia Lopes Lamarchi").pack()

        # Linha divisória visual
        ctk.CTkFrame(self.frame_conteudo, height=2, width=400, fg_color="gray").pack(pady=15)

    def mostrar_inicio(self):
        # Apaga o que estiver na tela da direita (caso você esteja voltando de outra tela)
        self.limpar_conteudo()

        # Título da Tela
        lbl_titulo = ctk.CTkLabel(self.frame_conteudo, text="Bem-vindo ao PyElo Analytics", font=ctk.CTkFont(size=24, weight="bold"))
        lbl_titulo.pack(pady=(40, 20)) # 40px em cima, 20px embaixo

        lbl_instrucao = ctk.CTkLabel(self.frame_conteudo, text="Selecione o esporte para esta sessão:", font=ctk.CTkFont(size=16))
        lbl_instrucao.pack(pady=10)

        # 3. Variável de Controle: guarda "futebol" ou "basquete". O valor inicial é futebol.
        self.var_esporte = ctk.StringVar(value="futebol")

        # Botões de Opção 
        # Ambos usam a mesma variable. Isso faz com que só um possa ser marcado por vez.
        rb_futebol = ctk.CTkRadioButton(self.frame_conteudo, text="Futebol", variable=self.var_esporte, value="futebol")
        rb_futebol.pack(pady=10)

        rb_basquete = ctk.CTkRadioButton(self.frame_conteudo, text="Basquete", variable=self.var_esporte, value="basquete")
        rb_basquete.pack(pady=10)

        # Botão de Confirmar
        btn_confirmar = ctk.CTkButton(self.frame_conteudo, text="Iniciar Sessão",command=self.acao_confirmar_esporte)
        btn_confirmar.pack(pady=30)

    def mostrar_carregar(self):
        self.limpar_conteudo()

        # Título
        lbl = ctk.CTkLabel(self.frame_conteudo, text="Carregar Arquivo", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=20)

        # Seletor de Modo
        lbl_modo = ctk.CTkLabel(self.frame_conteudo, text="Qual o tipo do seu arquivo?")
        lbl_modo.pack(pady=(10, 5))

        self.seg_modo = ctk.CTkSegmentedButton(self.frame_conteudo, values=["Histórico de Partidas", "Elos Já Prontos"], command=self.atualizar_dica_arquivo)
        self.seg_modo.set("Histórico de Partidas") # Valor padrão
        self.seg_modo.pack(pady=5)
        
        # Dica visual sobre as colunas (Muda conforme o botão acima)
        self.lbl_dica = ctk.CTkLabel(self.frame_conteudo, text="Colunas esperadas: TIME A, TIME B, PLACAR A, PLACAR B", text_color="gray")
        self.lbl_dica.pack(pady=5)

        # Campo de texto 
        self.entry_arquivo = ctk.CTkEntry(self.frame_conteudo, placeholder_text="Nenhum arquivo selecionado", width=400)
        self.entry_arquivo.pack(pady=(10, 5))

        # Botão para abrir o Explorer
        btn_escolher = ctk.CTkButton(self.frame_conteudo, text="📂 Selecionar Arquivo .CSV", command=self.acao_selecionar_arquivo, fg_color="gray", hover_color="#444")
        btn_escolher.pack(pady=5)

        # Botão de Ação
        btn_processar = ctk.CTkButton(self.frame_conteudo, text="💾 Carregar e Processar", command=self.acao_processar_arquivo, fg_color="green", hover_color="darkgreen")
        btn_processar.pack(pady=10)

        # Área de Texto para Resultados
        lbl_log = ctk.CTkLabel(self.frame_conteudo, text="Log de Processamento:")
        lbl_log.pack(pady=(20, 5))

        self.textbox_log = ctk.CTkTextbox(self.frame_conteudo, width=500, height=300, font=("Courier New", 12))
        self.textbox_log.pack(pady=10)

    def mostrar_simular(self):
        # Limpa o conteúdo anterior
        self.limpar_conteudo()

        # Título
        lbl = ctk.CTkLabel(self.frame_conteudo, text="Simulador de Resultados", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=10)

        # 1. Verificação de Segurança (Se não tiver times)
        if not self.simulador or not self.simulador.times:
            lbl_erro = ctk.CTkLabel(self.frame_conteudo, ext="Erro: Nenhum time carregado.\nCarregue um CSV na aba 'Carregar arquivo' primeiro.", text_color="red")
            lbl_erro.pack(pady=50)
            return

        aba_partida = self.frame_conteudo
        
        lista_times = sorted(list(self.simulador.times.keys()))

        # Cria as listas suspensas para seleção de equipes
        ctk.CTkLabel(aba_partida, text="Mandante:").pack(pady=5)
        self.menu_time_a = ctk.CTkOptionMenu(aba_partida, values=lista_times)
        self.menu_time_a.pack(pady=5)

        ctk.CTkLabel(aba_partida, text="X", font=("Arial", 16, "bold")).pack(pady=5)

        ctk.CTkLabel(aba_partida, text="Visitante:").pack(pady=5)
        self.menu_time_b = ctk.CTkOptionMenu(aba_partida, values=lista_times)
        
        # Por padrão a lista suspensa começa selecionada no primeiro time, para evitar Time x Time como placeholder setamos o menu B para o segundo time
        if len(lista_times) > 1:
            self.menu_time_b.set(lista_times[1])
        
        self.menu_time_b.pack(pady=5)


        ctk.CTkButton(aba_partida, text="🆚 Prever Vencedor", command=self.acao_simular_partida, fg_color="green").pack(pady=20)
        
        self.lbl_resultado_simulacao = ctk.CTkLabel(aba_partida, text="")
        self.lbl_resultado_simulacao.pack(pady=5)

    def mostrar_graficos(self):
        # Limpa o conteúdo anterior
        self.limpar_conteudo()

        # Título
        lbl = ctk.CTkLabel(self.frame_conteudo, text="Visualização Gráfica", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=10)

        # Criação das ABAS
        self.tab_graficos = ctk.CTkTabview(self.frame_conteudo, width=600, height=400)
        self.tab_graficos.pack(pady=10)

        self.tab_graficos.add("Evolução Individual")
        self.tab_graficos.add("Comparação Direta")

        # Preparando a lista de times
        lista_times = sorted(list(self.simulador.times.keys()))

        # ABA 1: EVOLUÇÃO (Um time)
        aba_evo = self.tab_graficos.tab("Evolução Individual")

        ctk.CTkLabel(aba_evo, text="Selecione o time para ver histórico:").pack(pady=20)
        
        # Cria lista suspensa
        self.menu_grafico_time = ctk.CTkOptionMenu(aba_evo, values=lista_times)
        self.menu_grafico_time.pack(pady=10)

        # Botão de ação
        ctk.CTkButton(aba_evo, text="📈 Gerar Gráfico", command=self.acao_plotar_evolucao, fg_color="blue").pack(pady=20)


        # ABA 2: COMPARAÇÃO (Dois times)
        # Título
        aba_comp = self.tab_graficos.tab("Comparação Direta")

        # Cria as listas suspensas
        ctk.CTkLabel(aba_comp, text="Time A:").pack(pady=5)
        self.menu_grafico_a = ctk.CTkOptionMenu(aba_comp, values=lista_times)
        self.menu_grafico_a.pack(pady=5)

        ctk.CTkLabel(aba_comp, text="X", font=("Arial", 16, "bold")).pack(pady=5)

        ctk.CTkLabel(aba_comp, text="Time B:").pack(pady=5)
        self.menu_grafico_b = ctk.CTkOptionMenu(aba_comp, values=lista_times)

        # (Mesma lógica do "mostrar_simular):
        # Por padrão a lista suspensa começa selecionada no primeiro time, para evitar Time x Time como placeholder setamos o menu B para o segundo time
        if len(lista_times) > 1: self.menu_grafico_b.set(lista_times[1]) 
        self.menu_grafico_b.pack(pady=5)

        # Botão de ação
        ctk.CTkButton(aba_comp, text="Comparar Gráficos", command=self.acao_plotar_comparacao, fg_color="purple").pack(pady=20)

    def mostrar_estatisticas(self):
        # Limpa o conteúdo anterior
        self.limpar_conteudo()

        # Título
        lbl = ctk.CTkLabel(self.frame_conteudo, text="Central de Estatísticas", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=20)

        # Criação das Abas
        self.tab_stats = ctk.CTkTabview(self.frame_conteudo, width=650, height=450)
        self.tab_stats.pack(pady=10)

        self.tab_stats.add("Ranking Final")
        self.tab_stats.add("Ranking por Rodada")
        self.tab_stats.add("Análise Individual")

        # Menu de Ranking final
        aba_rank = self.tab_stats.tab("Ranking Final")

        # Botão para atualizar/ver a lista na tela
        btn_ver_rank = ctk.CTkButton(aba_rank, text="🔄 Exibir Ranking Atualizado", command=self.acao_exibir_ranking_tela, fg_color="teal", hover_color="#00695c")
        btn_ver_rank.pack(pady=10)

        # Caixa de texto para mostrar o ranking
        self.textbox_ranking = ctk.CTkTextbox(aba_rank, width=500, height=250, font=("Courier New", 12))
        self.textbox_ranking.pack(pady=5)

        # Linha divisória
        ctk.CTkFrame(aba_rank, height=2, fg_color="gray").pack(fill="x", pady=15, padx=50)

        # Botão de salvar
        lbl_save = ctk.CTkLabel(aba_rank, text="Exportar dados:")
        lbl_save.pack(pady=2)

        self.btn_salvar_csv = ctk.CTkButton(aba_rank, text="💾 Salvar Ranking em .CSV", command=self.acao_salvar_ranking_arquivo, fg_color="green", hover_color="darkgreen")
        self.btn_salvar_csv.pack(pady=5)

        # Menu de Ranking por rodada
        aba_rankr = self.tab_stats.tab("Ranking por Rodada")

        # Botão para selecionar rodada
        self.entry_rodada = ctk.CTkEntry(aba_rankr, placeholder_text="Qual Rodada?", width=200)
        self.entry_rodada.pack(pady=10)

        # Botão confirmar
        btn_confirmar = ctk.CTkButton(aba_rankr, text="🔄 Ver Ranking", command=self.acao_exibir_ranking_rodada_tela, fg_color="teal").pack(pady=20)

        # Caixa de texto para mostrar o ranking
        self.textbox_rankingr = ctk.CTkTextbox(aba_rankr, width=500, height=250, font=("Courier New", 12))
        self.textbox_rankingr.pack(pady=5)

        # Linha divisória
        ctk.CTkFrame(aba_rankr, height=2, fg_color="gray").pack(fill="x", pady=15, padx=50)


        # Menu de Análise individual
        aba_indv = self.tab_stats.tab("Análise Individual")        
        lista_times = sorted(list(self.simulador.times.keys()))

        lbl_select = ctk.CTkLabel(aba_indv, text="Selecione a equipe para análise:")
        lbl_select.pack(pady=(10, 5))

        # Cria as listas suspensas
        self.menu_stats_time = ctk.CTkOptionMenu(aba_indv, values=lista_times)
        self.menu_stats_time.pack(pady=5)

        # Botão de Consultar
        btn_consultar = ctk.CTkButton(aba_indv, text="🔄 Gerar Relatório", command=self.acao_gerar_relatorio, fg_color="teal", hover_color="#00695c")
        btn_consultar.pack(pady=20)

        # Área de Texto para o Resultado
        # Usamos uma fonte monoespaçada (Courier) para que os números fiquem alinhados
        self.textbox_stats = ctk.CTkTextbox(aba_indv, width=400, height=300, font=("Courier New", 14))
        self.textbox_stats.pack(pady=10)

if __name__ == "__main__":
    app = InterfaceApp()  # Cria a instância janela

    app.mainloop()        # Mantém a janela aberta num loop infinito 
