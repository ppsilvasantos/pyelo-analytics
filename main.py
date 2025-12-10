from simulador import SimuladorElo

def main():
    print("Bem vindo(a) ao PyElo Analytics!")
    print()
    print("Para começarmos, selecione o esporte para essa sessão:")
    print("Digite '1' - Futebol")
    print("Digite '2' - Basquete")
    print("Digite 'sair' - encerrar o programa.")

    esporte = ""
        
    while esporte not in ["1", "2", "sair"]:
        esporte = input().strip().lower()

        if esporte == "sair":
            print("Encerrando o programa...")
            return
        elif esporte == "1":
            modo_esporte = "futebol"
            print("Você selecionou o futebol.")
        elif esporte == "2":
            modo_esporte = "basquete"
            print("Você selecionou o basquete.")
        else:
             print("Digite uma opção válida.")

    simulador = SimuladorElo(modo_esporte)

    while True: 
        print("Selecione uma das opções abaixo:")
        print("Digite '1' - Tenho uma base de dados de jogos disputados (Gerar Elo).")
        print("Digite '2' - Tenho uma base de dados de ratings (Simular).")
        print("Digite 'sair' - encerrar o programa.")
        opcao = input().lower().strip()

        if opcao == "1":
            print("Você selecionou a opção para Gerar Elo.")
            print()
            print("A base de dados de jogos disputados deve cumprir os seguintes requisitos:")
            print("Estar no formato '.csv'.")
            print("Possuir as colunas EXATAS: TIME A | TIME B | PLACAR A | PLACAR B")
            print("TIME A = Time mandante, TIME B = Time visitante, PLACAR A = Pontos/gols time mandante, PLACAR B = Pontos/gols time visitante.")
            print("As linhas devem estar em ordem crescente da data das partidas.")
            print()
            arquivo = input("Digite o nome do arquivo com a base de dados: ")
            try:
                simulador.carregar_dados(arquivo)
                print(f"Arquivo '{arquivo}' carregado com sucesso!")
                print(f"Times encontrados:")
                for time in simulador.times.keys():
                    print(time)
                for linha in simulador.processar_temporada():
                    print(linha)
                print()
                while True:
                    print("Qual a próxima ação?")
                    print("Digite '1' - Obter ranking final.")
                    print("Digite '2' - Obter ranking de determinada rodada.")
                    print("Digite '3' - Plotar histórico de evolução de determinado time.")
                    print("Digite '4' - Plotar histórico de evolução de dois times")
                    print("Digite '5' - Obter estatísticas de determinado time.")
                    print("Digite '6' - Simular partida entre duas equipes.")
                    print("Digite '7' - Salvar arquivo com os ratings.")
                    print("Digite 'voltar' - Voltar ao menu principal.")

                    opcao = input().lower().strip()

                    if opcao == "1":
                        print(simulador.obter_ranking_final())
                    elif opcao == "2":
                        rodada = input("Qual a rodada desejada? ")
                        print(simulador.obter_ranking_historico(rodada))
                    elif opcao == "3":
                        equipe = input("Qual a equipe desejada? ")
                        if equipe.title() not in simulador.times:
                            print(f"Erro: {equipe} não encontrada!")
                            continue
                        simulador.plotar_evolucao_time(equipe)
                    elif opcao == "4":
                        equipe_a = input("Qual a primeira equipe? ")
                        equipe_b = input("Qual a segunda equipe? ")
                        if equipe_a.title() not in simulador.times:
                            print(f"Erro: {equipe_a} não foi encontrada!")
                            continue
                        elif equipe_b.title() not in simulador.times:
                            print(f"Erro: {equipe_b} não foi encontrada!")
                            continue
                        simulador.plotar_comparacao_times(equipe_a, equipe_b)
                    elif opcao == "5":
                        equipe = input("Qual a equipe desejada? ")
                        if equipe not in simulador.times:
                            print(f"Erro: {equipe} não foi encontrada!")
                            continue
                        print(simulador.consultar_time(equipe))
                    elif opcao == "6":
                        equipe_a = input("Qual a primeira equipe? ")
                        equipe_b = input("Qual a segunda equipe? ")
                        if equipe_a.title() not in simulador.times:
                            print(f"Erro: {equipe_a} não foi encontrada!")
                            continue
                        elif equipe_b.title() not in simulador.times:
                            print(f"Erro: {equipe_b} não foi encontrada!")
                            continue
                        simulador.prever_partida(equipe_a, equipe_b)
                    elif opcao == "7":
                        arquivo = input("Qual o nome do arquivo à ser criado? ")
                        simulador.salvar_ranking(arquivo)
                    elif opcao == "voltar":
                        break
                    else:
                        print(f"{opcao} não é uma ação válida.")

            except FileNotFoundError:
                print(f"\nERRO: Arquivo '{arquivo}' não encontrado.")
                print("Verifique o nome e se ele está na mesma pasta do main.py. Lembre-se de adicionar '.csv' ao fim.")
            
            except KeyError:
                print("\nERRO: O arquivo não tem as colunas esperadas.")
                print("Verifique se as colunas são 'Time A', 'Time B', 'Placar A', 'Placar B'.")
            
            except Exception as e:
                print(f"\nOcorreu um erro inesperado: {e}")

        elif opcao == "2":
            print("Você selecionou a opção para Simular.")
            print()
            print("A base de dados de jogos disputados deve cumprir os seguintes requisitos:")
            print("Estar no formato '.csv'.")
            print("Possuir as colunas EXATAS: TIME | ELO")
            print("TIME = Nome do time, ELO = Valor do Elo do time")
            print()
            arquivo = input("Digite o nome do arquivo com a base de dados: ")
            try:
                print(simulador.carregar_elos_prontos(arquivo))
                print(f"Arquivo '{arquivo}' carregado com sucesso!")
                print(f"Times encontrados:")
                for time in simulador.times.keys():
                    print(time)
            except FileNotFoundError:
                print(f"\nERRO: Arquivo '{arquivo}' não encontrado.")
                print("Verifique o nome e se ele está na mesma pasta do main.py. Lembre-se de adicionar '.csv' ao fim.")
            
            except KeyError:
                print("\nERRO: O arquivo não tem as colunas esperadas.")
                print("Verifique se as colunas são 'Time', 'Elo'.")
            
            except Exception as e:
                print(f"\nOcorreu um erro inesperado: {e}")

            while True:
                print("Qual a próxima ação?")
                print("Digite '1' - Simular uma partida entre dois times.")
                print("Digite 'voltar' - Voltar ao menu principal.")

                opcao = input().strip().lower()

                if opcao == "1":
                    equipe_a = input("Qual a equipe mandante? ")
                    equipe_b = input("Qual a equipe visitante? ")
                    if equipe_a not in simulador.times:
                        print(f"Erro: {equipe_a} não foi encontrada!")
                        continue
                    elif equipe_b not in simulador.times:
                        print(f"Erro: {equipe_b} não foi encontrada!")
                        continue

                    print(f"Simulando partida entre {equipe_a} e {equipe_b}...")
                    simulador.prever_partida(equipe_a, equipe_b)
                elif opcao == "sair":
                    break
                else:
                    print(f"{opcao} não é uma ação válida.")


        elif opcao == "sair":
            print("Encerrando o programa...")
            break

if __name__ == "__main__":
    main()