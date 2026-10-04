import random, copy, sys
from combate import combateini, combatesys
from inimigos import boss_floresta, boss_caverna, inimigos_caverna, inimigos_floresta, inimigos_montanhasgeladas, boss_montanhasgeladas, inimigos_castelo, boss_castelo_do_caos, boss_abismo
from util import limpar_tela, Cores
from lore import boss_final_dialogo, dialogo_FINAL_verdadeiro
dialogo2_boss = False
import progresso

class Progressao:

    def __init__(self, nome, lista_inimigos, boss, proximo_cenario):
        self.nome = nome
        self.lista_inimigos = lista_inimigos
        self.boss = boss
        self.bossderrotado = False
        self.progresso = 0
        self.lutas_para_boss = 5
        self.boss_especial_derrotado = False
        self.proximo_cenario = proximo_cenario

    def __eq__(self, outro):
        if not isinstance(outro, Progressao):
            return NotImplemented
        return self.nome == outro.nome

    def __hash__(self):
        return hash(self.nome)

    def explorar(self, heroi):
        inimigoaleatório = copy.deepcopy(random.choice(self.lista_inimigos))
        combateini(heroi, inimigoaleatório)
        return
            
    def chamarboss(self, heroi):
        global dialogo2_boss
        if not self.bossderrotado and self.progresso >= self.lutas_para_boss:
            inimigo = copy.deepcopy(self.boss[0])
            inimigo.nome = f"{Cores.VERMELHO}{inimigo.nome}{Cores.RESET}"
            if  self == zona4_castelo_do_caos:
                boss_final_dialogo(heroi, inimigo)
            
            combatesys(heroi, inimigo)
            
            if progresso.final_verdadeiro and dialogo2_boss == False:
                dialogo_FINAL_verdadeiro(heroi, inimigo)
                dialogo2_boss = True

    def chamar_boss_especial(self, heroi):
        if heroi.zona_atual == zona4_castelo_do_caos:
            
            from eventos import evento_raid_vila_destruida
            evento_raid_vila_destruida(heroi)
            limpar_tela()
            heroi.focogen += 0.1
            print("Parabéns! Você venceu a luta e sua geração de Fúria aumentou em +0.5\n")
            heroi.vida = heroi.vidamax
            heroi.mana = heroi.manamax
            print("Seu HP e MP foram restaurados!\n")
            input("Pressione ENTER para continuar...")
            
            return  
        
        inimigo = copy.deepcopy(self.boss[1])
        inimigo.nome = f"{Cores.VERMELHO}{inimigo.nome}{Cores.RESET}"
        combatesys(heroi, inimigo)
        if inimigo.vida <= 0:
            limpar_tela()
            heroi.focogen += 0.3
            print("Parabéns! Você venceu a luta e sua geração de Fúria aumentou em +0.5")
            input("Pressione ENTER para continuar...")

            return

    def avançarjogo(self):
        self.progresso +=1


# 1. Zonas
zona5_abismo = Progressao("Abismo do Rei", None, boss_abismo, proximo_cenario=None)
zona4_castelo_do_caos = Progressao("Castelo do Caos", inimigos_castelo, boss_castelo_do_caos, proximo_cenario=zona5_abismo)   # Cavaleiros sombrios, etc /  final boss
zona3_montanhagelada = Progressao("Montanha Congelada", inimigos_montanhasgeladas, boss_montanhasgeladas, proximo_cenario=zona4_castelo_do_caos)   
zona2_caverna = Progressao("Caverna Sombria", inimigos_caverna, boss_caverna, proximo_cenario=zona3_montanhagelada)
zona1_floresta = Progressao("Floresta Verde", inimigos_floresta, boss_floresta, proximo_cenario=zona2_caverna)


zona_atual = zona1_floresta # nome, lista_inimigos, boss, proximo_cenario):
inimigos_acampamento = zona_atual.lista_inimigos  # Faz os inimigos do acampamento serem sempre baseados no local ondem você está, porém vou pensar ainda se eixo essa opção, pois pode ser chato ficar lutando toda hora
# Pensar se vai ter luta ou não no acampamento, para deixar mais dificil, ou não ter para ser menos repetitivo

def hud_mundo(heroi):
    from util import limpar_tela
    limpar_tela()

    L = 44  # largura dos separadores

    # ---------- Nome do herói ----------
    print(f"  {heroi.nome.upper()}")
    print("  " + "-" * L)

    # ---------- Status em duas colunas ----------
    print(f"  Vida    {heroi.vida:>3}/{heroi.vidamax:<3}"
          f"     Mana    {int(heroi.mana):>3}/{heroi.manamax:<3}")

    print(f"  Ataque  {heroi.ataque:<5}"
          f"       Defesa  {heroi.defesa:<5}")

    print(f"  Ouro    {heroi.ouro:<5}"
          f"       Nível   {heroi.nivel:<5}")

    print()

    # ---------- Área e progresso ----------
    progresso = heroi.zona_atual.progresso
    total     = heroi.zona_atual.lutas_para_boss

    preenchido = int((progresso / total) * 10) if total else 0
    barra = "#" * preenchido + "." * (10 - preenchido)

    print(f"  {heroi.zona_atual.nome}          "
          f"Progresso  [{barra}]  {progresso}/{total}")

    print()

    # ---------- Opções ----------
    print("  " + "-" * L)
    print("  [1] Explorar Zona")
    print("  [2] Ir para Próxima Zona  (avançar jogo)")
    print("  [0] Voltar ao Menu")
    print()

    return input("  Qual sua decisão? ")

def menumundo(heroi):   
    while True:
        limpar_tela()
        if heroi.zona_atual.progresso >= 5 and heroi.zona_atual.bossderrotado == False:
            print("Cuidado, a proxima luta será contra o CHEFE da área!")
            input("Pressione ENTER para continuar...")
            limpar_tela()

        opcao = hud_mundo(heroi)

        if opcao == "1" and heroi.zona_atual == zona5_abismo:
            heroi.zona_atual.progresso = 5
            print("A luta final irá começar, esteja preparado!")
            input("Pressione ENTER para continuar...")
            heroi.zona_atual.chamarboss(heroi)

        if opcao == "1":
            if heroi.zona_atual.bossderrotado == False:
                if heroi.zona_atual.progresso >= 5:
                    heroi.zona_atual.chamarboss(heroi)
                    heroi.zona_atual.bossderrotado = True
                    from database import salvar_heroi
                    salvar_heroi(heroi)
                    print("Jogo salvo automaticamente!")
                    input("Pressione ENTER para continuar...")
                    return

                else:
                    heroi.zona_atual.explorar(heroi)

            elif heroi.zona_atual.bossderrotado == True and heroi.zona_atual.progresso >= 6 and not heroi.zona_atual.boss_especial_derrotado:
                while True:
                    escolha = input("Você sente uma sensação estranha....\n[ALERTA][PERIGO] Algo MUITO PODEROSO parece estar vindo para lutar contra você!\n[1] - Lutar\n[2] - Sair\n")
                    if escolha == "1":
                        heroi.zona_atual.chamar_boss_especial(heroi)
                        heroi.zona_atual.boss_especial_derrotado = True
                        from database import salvar_heroi
                        salvar_heroi(heroi)
                        print("Jogo salvo automaticamente!")
                        input("Pressione ENTER para continuar...")
                        return

                    elif escolha == "2":
                        return

                    else:
                        print("Comando não existe...")
                        input("Pressione ENTER para continuar...")
                    
            else:
                print("Você já explorou a área e pode seguir em frente!")
                input("Pressione ENTER para continuar...")
            

        elif opcao == "2":
            if heroi.zona_atual.bossderrotado and heroi.zona_atual.proximo_cenario:
                while True:
                    escolha = input("Após sair da Área não poderá voltar...\n[1] - Mudar de Área\n[2] - Voltar\n")
                    if escolha == "1":

                        if heroi.zona_atual == zona5_abismo:
                            print("Você terminou o jogo e fez o final verdadeiro! Meus Parabéns!")
                            input("Pressione ENTER para continuar...\n")
                            print("Você terminou o jogo com esses Status:")
                            heroi.mostrar_status()
                            input("\nPressione ENTER para continuar...")

                            sys.exit()

                        if heroi.zona_atual == zona4_castelo_do_caos and progresso.final_verdadeiro:
                            heroi.zona_atual = heroi.zona_atual.proximo_cenario
                            heroi.vila_atual.nome = "Vila Indisponível" 
                            print(f"Você viajou para {heroi.zona_atual.nome}!")
                            input("Pressione ENTER para continuar...")
                            return

                        if heroi.zona_atual == zona4_castelo_do_caos:
                            if not progresso.final_verdadeiro:

                                print("Você terminou o jogo! Parabéns!")
                                input("Pressione ENTER para continuar...\n")
                                print("Você terminou o jogo com esses Status:")
                                heroi.mostrar_status()
                                input("\nPressione ENTER para continuar...")

                                # Fazer um ranking online de quem terminou mais forte / ou pontos acumulados e com os bosses derrotados 
                                sys.exit()

                        else:

                            heroi.zona_atual = heroi.zona_atual.proximo_cenario
                            heroi.vila_atual = (heroi.vila_atual.proximavila)
                            print(f"Você viajou para {heroi.zona_atual.nome}!")
                            input("Pressione ENTER para continuar...")
                            return

                    elif escolha == "2":
                        return

                    else:
                        print("Comando não existe...")
                        input("Pressione ENTER para continuar...")
            else:
                print("Explore a Zona primeiro")
                print("Você precisa derrotar o Boss desta zona para avançar!")
                input("Pressione ENTER para continuar...")

        elif opcao == "0":
            return
