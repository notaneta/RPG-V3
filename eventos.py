import random, copy
from inimigos import boss_caverna, boss_montanhasgeladas, boss_floresta, inimigos_floresta, inimigos_caverna, boss_yeti, Bandido
from itens import poçoes
from combate import combatesys
from lore import dialogo, copia_heroi_dialogo, copia_heroi_dialogo2
from util import acampamento_ativo, set_acampamento, limpar_tela, Cores
import progresso

def acampamento(heroi):
    print("\nVocê monta um acampamento...\n")
    input("Pressione ENTER para continuar...\n")
    cura = heroi.vidamax * 0.30
    heroi.vida = int(min(heroi.vidamax, heroi.vida + cura))
    mana = heroi.manamax * 0.30
    heroi.mana = int(min(heroi.manamax, heroi.mana * mana))
    print(f"Você recuperou HP {int(cura)} e MP {int(mana)}")
    heroi.mostrar_status()
    input("Pressione ENTER para continuar...")
    teste = random.randint(1,10)
    if teste >= 3: # 70% de Chance de evento
        eventoaleatorio = random.choice([evento_bau, evento_erva, evento_emboscada, evento_fada, evento_fogueira, evento_tempestade, evento_livro, evento_pedagio_forcado, evento_assalto_noturno])
        eventoaleatorio(heroi) 

def evento_erva(heroi):
    from util import limpar_tela
    import random

    limpar_tela()
    print()
    print("  [EVENTO] Uma planta de aparência estranha cresce perto do acampamento.")
    print("           As folhas brilham levemente à luz da fogueira.")
    print()

    escolha = input("  Deseja comê-la?  [1] Sim  [2] Não  > ").strip()

    if escolha == "2":
        print("\n  Você decide não arriscar. A planta continua ali, indiferente.")
        input("  Pressione ENTER para continuar...")
        return

    if escolha != "1":
        print("\n  Comando inválido.")
        input("  Pressione ENTER para continuar...")
        return

    # Efeito aleatório
    efeito = random.choice(["cura", "veneno"])

    if efeito == "cura":
        # Cura escala com nível, com um pequeno bônus aleatório
        cura = random.randint(15, 25) + int(heroi.nivel * 1.5)
        vida_antes = heroi.vida
        heroi.vida = min(heroi.vidamax, heroi.vida + cura)
        curado_real = heroi.vida - vida_antes

        print(f"\n  A erva tinha propriedades curativas!")
        print(f"  Você recuperou {curado_real} de HP.")
        if curado_real < cura:
            print(f"  (Já estava com vida quase cheia — {cura - curado_real} de cura desperdiçados.)")

    else:
        # Veneno dói mais que a cura cura
        dano = random.randint(20, 35) + int(heroi.nivel * 1.8)
        heroi.vida = max(0, heroi.vida - dano)

        print(f"\n  A erva era venenosa!")
        print(f"  Você perdeu {dano} de HP.")

        # Alerta se o veneno for letal
        if heroi.vida <= 0:
            print(f"\n  O veneno foi forte demais...")
            # Se quiser, deixe o jogo tratar a morte aqui. Ex:
            # print("[GAME OVER]")
            # sys.exit()
        elif heroi.vida / heroi.vidamax < 0.25:
            print(f"\n  ⚠ Vida crítica: {heroi.vida}/{heroi.vidamax}")

    input("\n  Pressione ENTER para continuar...")

def evento_fada(heroi):
    from util import limpar_tela

    limpar_tela()
    print()
    print("  [EVENTO] Uma luz brilhante surge em volta... É uma fada?!")
    print("           Ela flutua, indiferente, à beira do acampamento.")
    print()

    escolha = input("  O que fazer?  [1] Aproximar  [2] Ignorar  > ").strip()

    if escolha == "2":
        print("\n  Você decide não se envolver. A luz desaparece sozinha.")
        input("  Pressione ENTER para continuar...")
        return

    if escolha != "1":
        print("\n  Comando inválido.")
        input("  Pressione ENTER para continuar...")
        return

    # Rolagem de 1 a 10
    # 1-4 → armadilha (40%)
    # 5   → nada (10%)
    # 6-10 → bênção (50%)
    teste = random.randint(1, 10)

    if teste >= 6:
        # ---- BÊNÇÃO ----
        bonus = 10 + int(heroi.nivel * 0.8)
        heroi.manamax += bonus
        heroi.mana = min(heroi.mana + bonus, heroi.manamax)

        limpar_tela()
        print()
        print("  A fada sorri.")
        input("  Pressione ENTER para continuar...")
        print("\n  Ela canaliza uma energia mágica em você antes de desaparecer.")
        print(f"  Seu MP máximo aumentou permanentemente em +{bonus}!")
        input("\n  Pressione ENTER para continuar...")

    elif teste >= 5:
        # ---- NADA ----
        limpar_tela()
        print()
        print("  A luz pisca... e some.")
        print("  Não era nada, apenas um reflexo do luar.")
        input("\n  Pressione ENTER para continuar...")

    else:
        # ---- ARMADILHA ----
        limpar_tela()
        print()
        print("  A fada se distorce... e revela sua verdadeira forma.")
        input("  Pressione ENTER para continuar...")
        print("\n  Era uma armadilha de um monstro das sombras!")
        print("  Você gasta energia para escapar antes que ele te alcance.")

        # Custo escala com o nível (mínimo 10, máximo 25% da mana atual)
        custo = min(heroi.mana, 10 + int(heroi.nivel * 0.8))
        if custo <= 0:
            # Sem mana: o monstro te acerta direto
            dano = random.randint(10, 20) + int(heroi.nivel * 1.5)
            heroi.vida = max(0, heroi.vida - dano)
            print(f"\n  Sem mana para se defender, você é atingido: -{dano} HP.")
        else:
            heroi.mana -= custo
            print(f"\n  Você perdeu {custo} de MP ao escapar.")

        if heroi.vida / heroi.vidamax < 0.25:
            print(f"\n  ⚠ Vida crítica: {heroi.vida}/{heroi.vidamax}")

        input("\n  Pressione ENTER para continuar...")
        
def evento_bau(heroi):
    from util import limpar_tela

    limpar_tela()
    print()
    print("  [EVENTO] Você encontra um baú velho enterrado perto da sua barraca.")
    print("           A madeira está apodrecida, mas o cadeado ainda parece intacto.")
    print()

    escolha = input("  Deseja abrir?  [1] Sim  [2] Não  > ").strip()

    if escolha == "2":
        print("\n  Você decide não arriscar. O baú continua enterrado.")
        input("  Pressione ENTER para continuar...")
        return

    if escolha != "1":
        print("\n  Comando inválido.")
        input("  Pressione ENTER para continuar...")
        return

    # Rolagem: 1-4 → armadilha (40%), 5-10 → tesouro (60%)
    sorte = random.randint(1, 10)

    if sorte >= 5:
        # ---- TESOURO ----
        ganho = random.randint(15, 30) + int(heroi.nivel * 3)
        heroi.ouro += ganho

        limpar_tela()
        print()
        print("  Você força o cadeado... e ele cede.")
        input("  Pressione ENTER para continuar...")
        print(f"\n  Dentro do baú, moedas antigas brilham à luz da fogueira.")
        print(f"  Você encontrou {ganho} de ouro!")
        input("\n  Pressione ENTER para continuar...")

    else:
        # ---- ARMADILHA ----
        dano = random.randint(8, 15) + int(heroi.nivel * 1.5)
        heroi.vida = max(0, heroi.vida - dano)

        limpar_tela()
        print()
        print("  Você força o cadeado...")
        input("  Pressione ENTER para continuar...")
        print(f"\n  Agulhas enferrujadas disparam do mecanismo!")
        print(f"  Você tomou {dano} de dano.")

        if heroi.vida <= 0:
            print("\n  O ferimento foi profundo demais...")
            # Aqui você pode chamar o game over, se quiser:
            # print("[GAME OVER]")
            # sys.exit()
        elif heroi.vida / heroi.vidamax < 0.25:
            print(f"\n  ⚠ Vida crítica: {heroi.vida}/{heroi.vidamax}")

        input("\n  Pressione ENTER para continuar...")

def evento_livro(heroi):
    from util import limpar_tela

    limpar_tela()
    print()
    print("  [EVENTO] Escondido entre as raízes de uma árvore próxima,")
    print("           você encontra um livro antigo, coberto de poeira.")
    print("           A capa traz símbolos que você não reconhece.")
    print()

    escolha = input("  Deseja folhear as páginas?  [1] Sim  [2] Não  > ").strip()

    if escolha == "2":
        print("\n  Você devolve o livro ao esconderijo. Algumas coisas melhor não tocar.")
        input("  Pressione ENTER para continuar...")
        return

    if escolha != "1":
        print("\n  Comando inválido.")
        input("  Pressione ENTER para continuar...")
        return

    # Rolagem: 1-3 → maldição (30%), 4-10 → benefício (70%)
    sorte = random.randint(1, 10)

    if sorte >= 4:
        # ---- BENEFÍCIO ----
        # Bônus escala com o nível, mas com teto pra não quebrar o jogo no fim
        bonus = min(2 + int(heroi.nivel * 0.4), 15)
        heroi.ataque += bonus

        limpar_tela()
        print()
        print("  Você abre o livro com cuidado...")
        input("  Pressione ENTER para continuar...")
        print(f"\n  As páginas revelam técnicas antigas de combate,")
        print(f"  diagramas de postura, formas de golpe que você nunca viu.")
        print(f"  Seu ATAQUE aumentou permanentemente em +{bonus}!")
        input("\n  Pressione ENTER para continuar...")

    else:
        # ---- MALDIÇÃO ----
        dano = 12 + int(heroi.nivel * 1.2)
        heroi.vida = max(0, heroi.vida - dano)

        limpar_tela()
        print()
        print("  Você abre o livro...")
        input("  Pressione ENTER para continuar...")
        print(f"\n  Uma névoa sombria emerge das páginas e atinge você!")
        print(f"  Você perdeu {dano} de HP.")

        if heroi.vida <= 0:
            print("\n  A maldição foi forte demais...")
            # Aqui você pode chamar o game over, se quiser:
            # print("[GAME OVER]")
            # sys.exit()
        elif heroi.vida / heroi.vidamax < 0.25:
            print(f"\n  ⚠ Vida crítica: {heroi.vida}/{heroi.vidamax}")

        input("\n  Pressione ENTER para continuar...")

def evento_fogueira(heroi):
    print("\n[EVENTO] A noite está tranquila. O som da fogueira acalma sua mente.")
    print("Você aproveita o tempo para afiar suas armas e refletir.")

    heroi.xp += 10
    print("Você ganhou +10 de XP pela meditação!")

    # Se o herói usa Foco, recupera Foco também
    if hasattr(heroi, "foco"):
        heroi.foco = min(heroi.focomax, heroi.foco + 20)
        print("Sua barra de FÚRIA irá começar com 20 pontos na proxima luta!")

    input("Pressione ENTER para continuar...")

def evento_emboscada(heroi):
    print("\n[EVENTO][ALERTA] Barulhos no mato! Um monstro emboscou seu acampamento! \nEle parece ter algo diferente dos demais da região!")
    escolha = input("O que fazer?\n[1]- Pegar a espada e lutar\n[2] - Apagar a fogueira e se esconder\n")

    if escolha == "1":
        print("Você se levanta rapidamente a tempo de repelir o ataque inicial!")
        input("\nPressione ENTER para continuar...")
        set_acampamento(False)
        inimigo = copy.deepcopy(random.choice(heroi.zona_atual.lista_inimigos))
        inimigo.ataque += 12
        combatesys(heroi, inimigo)
        print("Você recebeu 20 de Ouro e 20 de XP adicional da luta")
        heroi.ouro += 20
        heroi.xp += 20

        input("\nPressione ENTER para continuar...")
        set_acampamento(True)

    elif escolha == "2":
        teste = random.randint(1, 10)
        if teste > 4:
            print("Você apagou o fogo a tempo e o monstro passou direto!")
            input("\nPressione ENTER para continuar...")
        else:
            dano = 15
            heroi.vida -= dano
            print(f"Você tropeçou no escuro ao se esconder e tomou {dano} de dano!")
            input("\nPressione ENTER para continuar...")

def evento_assalto_noturno(heroi):
    print("\n[EVENTO OBRIGATÓRIO] Você acorda assustado com um barulho ao lado do seu saco de dormir!")
    print("Um ladrão sorrateiro aproveitou seu sono profundo para cortar sua bolsa de moedas!")

    if heroi.ouro > 0:
        # Rouba entre 10 e 25 moedas (ou todo o ouro se tiver menos)
        perda = random.randint(10, 25)
        ouro_roubado = min(heroi.ouro, perda)
        heroi.ouro -= ouro_roubado
        print(f"O ladrão foge rapidamente para a escuridão da noite gargalhando!")
        print(f"Você perdeu {ouro_roubado} de ouro!")
    else:
        print("O ladrão mexeu nos seus bolsos, mas como você não tinha ouro, ele só te deu um chute e fugiu!")
        heroi.vida -= 10

    input("\nPressione ENTER para continuar...")

def evento_pedagio_forcado(heroi):
    print("\n[EVENTO OBRIGATÓRIO] Três bandidos armados cercam a sua fogueira!")
    print("Líder dos Bandidos: 'Acampando em nossas terras sem pagar a taxa?'")

    # O valor do pedágio também sobe com o nível do herói
    valor_pedagio = heroi.nivel * 15
    print(f"Eles exigem {valor_pedagio} moedas de ouro para deixar você passar a noite em paz.")
    print(f"Seu Ouro atual: {heroi.ouro}")

    print(f"\n[1] - Pagar o pedágio ({valor_pedagio} Ouro)")
    print("[2] - Recusar e LUTAR!")

    escolha = input("\nQual a sua escolha?\n")

    if escolha == "1":
        if heroi.ouro >= valor_pedagio:
            heroi.ouro -= valor_pedagio
            print("\nLíder dos Bandidos: 'Sábia escolha. Tenha uma boa noite de sono... enquanto pode.'")
            print(f"Você pagou {valor_pedagio} de ouro.")
        else:
            print("\nLíder dos Bandidos: 'Você não tem ouro suficiente?! Então vai pagar com a própria VIDA!'")
            input("\nPressione ENTER para puxar sua arma...")
            _iniciar_luta_pedagio(heroi)
    else:
        print("\nVocê se recusa a pagar e desembainha sua arma!")
        input("\nPressione ENTER para iniciar a batalha...")
        _iniciar_luta_pedagio(heroi)

    input("\nPressione ENTER para continuar...")

def _iniciar_luta_pedagio(heroi):
    set_acampamento(False)

    inimigo = copy.deepcopy(Bandido[0])

    # Multiplicadores de atributo baseados no Nível do Herói:
    # Ajuste os valores base (ex: 25 de HP e 4 de Dano por nível) conforme o balanceamento do seu jogo
    inimigo.vidamax = heroi.nivel * 25
    inimigo.vida = inimigo.vidamax
    inimigo.ataque = heroi.nivel * 4
    inimigo.defesa = heroi.nivel * 2

    # Ajusta o ganho de recompensa proporcional ao nível
    inimigo.ouro = heroi.nivel * 12
    inimigo.xp = heroi.nivel * 20

    print(f"\n O Líder Bandido (Nível {heroi.nivel}) se prepara para atacar!")
    print(f"Status do Inimigo -> HP: {inimigo.vida} | Ataque: {inimigo.ataque} | Defesa: {inimigo.defesa}")
    input("\nPressione ENTER para começar o combate...")

    combatesys(heroi, inimigo)
    set_acampamento(True)
    
def evento_tempestade(heroi):
    print("\n[EVENTO OBRIGATÓRIO] O tempo vira bruscamente e uma tempestade severa atinge seu acampamento!")
    print("Sua tenda é levada pelo vento e a chuva gelada destrói sua fogueira.")

    dano_tempestade = random.randint(8, 15)
    heroi.vida = max(1, heroi.vida - dano_tempestade)  # Evita matar instantaneamente

    print(f"Você passa a noite no frio extremo e perde {dano_tempestade} de HP.")

    # Perda de Mana pela exaustão
    if heroi.mana >= 10:
        heroi.mana = max(0, heroi.mana - 10)
        print("Sua energia mágica foi desgastada (-10 de MP).")

    input("\nPressione ENTER para continuar...")

def evento_mercador(heroi): # AINDA N DECIDI O TANTO QUE CURA
    print("\n[EVENTO] Um mercador ambulante senta ao lado da sua fogueira!")
    print(f"Ele oferece uma Poção Especial que faz (decidir ainda quanto cura, ou oque faz) e custa {custo}.") # Modificar
    custo = 15
    escolha = input("Deseja comprar?\n[1] - Sim\n[2] - Não\n")
    if escolha == "1":
        if heroi.ouro >= custo: # Preço do item
            heroi.ouro -= custo     # Quanto tira
            heroi.vida = min(heroi.vidamax, heroi.vida + 50)
            print("Você comprou e tomou a poção! E ")       # modificar
            input("\nPressione ENTER para continuar...")
        else:
            print("Você não tem ouro suficiente...")
            input("\nPressione ENTER para continuar...")
    else:
        print("O mercador deseja boa sorte e vai embora.")
        input("\nPressione ENTER para continuar...")

def evento_vila_inical(heroi): # Competição de Lenhadores Provavelmente 2* evento da vila / Se o ataque do jogador for maior que X ele ganha a disputa, ganhando ouro e XP 
    while progresso.flags_eventos["evento1_concluido"] == False:
        print("[EVENTO] Você vê que a guilda de aventureiros está reunindo caçadores para participar de uma caça a monstros elites!")
        escolha = input("Você pode: \n[1] - Participar\n[2] - Não Participar\n") 

        if escolha == "1":
            progresso.avancar_jogo = False
            set_acampamento(False) 
            print("Você terá que lutar contra 3 inimigos seguidos")
            inimigo = copy.deepcopy(inimigos_floresta[1])
            inimigo.nome = f"{Cores.AMARELO}{"Slime Elite"}{Cores.RESET}"
            inimigo.ataque += 10
            inimigo.ouro = 20
            inimigo.xp = 15
            combatesys(heroi, inimigo)
            print("Um dos aventureiros te entrega um item.")
            input("\nPressione ENTER para continuar...")
            heroi.adicionar_pocoes(poçoes[1])
            input("\nPressione ENTER para continuar...")

            inimigo = copy.deepcopy(inimigos_floresta[0])
            inimigo.nome = f"{Cores.AMARELO}{"Goblin Elite"}{Cores.RESET}"
            inimigo.ataque += 10
            inimigo.ouro = 20
            inimigo.xp = 15
            combatesys(heroi, inimigo)
            print("Outro aventureiro te entrega um item.")
            input("Pressione ENTER para continuar...\n")
            heroi.adicionar_pocoes(poçoes[1])
            input("\nPressione ENTER para continuar...")


            inimigo = copy.deepcopy(inimigos_floresta[3])
            inimigo.nome = f"{Cores.AMARELO}{"Urso Ancião de Elite"}{Cores.RESET}"
            inimigo.ataque += 10
            inimigo.ouro = 30
            inimigo.xp = 30
            combatesys(heroi, inimigo)
            print("Parabéns você derrotou todos os inimigos, a guilda te recompensou com 60 de ouro")
            print("Voc6e recebeu 60 de XP devido as lutas")
            progresso.flags_eventos["evento1_concluido"] = True
            set_acampamento(True)
            progresso.avancar_jogo = True
            input("\nPressione ENTER para continuar...")
            return


        elif escolha == "2":
            return
            
    else:
        print("O evento já foi concluido")
        input("Pressione ENTER para continuar...")
        return
    
def evento_pesca_vila(heroi): 
    
    while progresso.flags_eventos["evento2_concluido"] == False:
        print("[EVENTO] Você ficou sabendo que a vila tem um local famoso de pesca por perto...")
        escolha = input("Você pode: \n[1] - Pescar\n[2] - Não Pescar\n") 
        if escolha == "1":
            print("\nVocê resolveu pescar.")
            dialogo("...")
            dialogo("...")
            sorte = random.randint(0,10)

            if sorte == 10:
                print(f"De 0 a 10, sua sorte foi {sorte}, parabéns!")
                input("Pressione ENTER para continuar...")
                print("Você encontrou uma poção GRANDE e mais 30 ouros!")
                input("Pressione ENTER para continuar...")
                print("Com isso se sentiu muito animado e devido a isso ganhou mais 10+ XP")
                input("Pressione ENTER para continuar...")
                heroi.xp += 10
                heroi.ouro += 30
                heroi.adicionar_pocoes(poçoes[2])
                progresso.flags_eventos["evento2_concluido"] = True
                return
            
            elif sorte >= 7:
                print(f"De 0 a 10, sua sorte foi {sorte}!")
                input("Pressione ENTER para continuar...")
                print("Você encontrou 15 ouros!")
                input("Pressione ENTER para continuar...")
                print("Com isso se sentiu muito animado e devido a isso ganhou +5 XP")
                input("Pressione ENTER para continuar...")
                heroi.xp += 5
                heroi.ouro += 30
                progresso.flags_eventos["evento2_concluido"] = True
                return

            elif sorte >= 4:
                print(f"De 0 a 10, sua sorte foi {sorte}!")
                input("\nPressione ENTER para continuar...")
                print("Você não conseguiu pescar nada.")
                print("Você se motiva a pensar que a proxima vez será melhor, e recebe +5 de XP! ")
                input("\nPressione ENTER para continuar...")
                heroi.xp += 5
                progresso.flags_eventos["evento2_concluido"] = True
                return


            elif sorte >= 1:
                print(f"De 0 a 10, sua sorte foi {sorte}!")
                input("\nPressione ENTER para continuar...")
                print("Durante a pesca, um inimigo tenta te atacar, você desvia e não tem escolha a não ser lutar!")
                inimigoaleatório = copy.deepcopy(random.choice(inimigos_caverna))
                combatesys(heroi, inimigoaleatório)
                progresso.flags_eventos["evento2_concluido"] = True
                return

            elif sorte == 0:
                print(f"De 0 a 10, sua sorte foi {sorte}, que azar!")
                print("Enquanto pescava, você se distraiu e tentaram te roubar!")
                if heroi.ouro > 10:
                    heroi.ouro -= 10
                    print("Você perdeu 10 de ouro.")
                    input("\nPressione ENTER para continuar...")
                    

                else:
                    print("Como você não tinha ouro, nada aconteceu.")
                    input("\nPressione ENTER para continuar...")

                progresso.flags_eventos["evento2_concluido"] = True
                return





        elif escolha == "2":
            return
            
    else:
        print("O evento já foi concluido")
        input("Pressione ENTER para continuar...")
        return

def evento_festival_da_neve(heroi):

    from mundo import zona_atual

    while progresso.flags_eventos["evento3_concluido"] == False and zona_atual.bossderrotado == False:
        limpar_tela()

        print("[EVENTO ]FESTIVAL DA NEVE")
        print("As Montanhas Geladas estão em festa!\nE você pode participar dos 3 eventos!")
        print("[1] - Guerra de Bola de Neve")
        print("[2] - Competição de Patinação")
        print("[3] - Explorar a Floresta Congelada")
        print("[0] - Sair")
        escolha = input("\nEscolha: ")
        # Guerra de Bola de Neve
        if escolha == "1" and progresso.flags_eventos["participou"] == False:
            print("\nVocê participa da Guerra de Bola de Neve!")

            teste = random.randint(1, heroi.defesa)

            if teste >= 15:
                ouro = random.randint(40, 80)
                heroi.ouro += ouro

                print(f"Vitória! Você ganhou {ouro} de ouro.")
                input("Pressione ENTER para continuar...")
                progresso.flags_eventos["participou"] = True
            else:
                print("Você foi atingido por várias bolas de neve e perdeu a competição!")
                input("Pressione ENTER para continuar...")
                progresso.flags_eventos["participou"] = True
        

        # Patinação
        elif escolha == "2" and progresso.flags_eventos["participou1"] == False:

            print("\nVocê entra na competição de patinação!")
            teste = random.randint(1, 10)

            if teste >= 5:
                xp = random.randint(30, 60)
                heroi.xp += xp

                print(f"Excelente apresentação! Você ganhou {xp} XP.")
                input("Pressione ENTER para continuar...")
                progresso.flags_eventos["participou1"] = True
            else:
                print("Você escorregou e caiu na neve.")
                input("Pressione ENTER para continuar...")
                progresso.flags_eventos["participou1"] = True

        # Área secreta com chance de boss
        elif escolha == "3" and progresso.flags_eventos["participou2"] == False:

            print("\nVocê segue uma trilha estranha na floresta congelada...")
            input("Pressione ENTER para continuar...")

            if random.randint(1, 100) <= 25:  # 25% de chance
                print("\nUm rugido ecoa pela montanha!")
                input("Pressione ENTER para continuar...")
                print("Um Yeti Lendário apareceu e vai lutar contra você!")
                input("Pressione ENTER para continuar...")

                boss = boss_yeti

                combatesys(heroi, boss)
                print("\nVocê derrotou o Yeti Lendário!")
                print("Você recebeu o artefato:")
                print("Coração de Gelo Ancestral")
                print("+15 Defesa")
                heroi.defesa += 15
                progresso.flags_eventos["participou2"] = True
                dialogo("Moradores : Incrível!\nMoradores : O monstro das lendas foi derrotado!\nO Festival da Neve nunca mais será o mesmo...")
                input("Pressione ENTER para continuar...")

            else:
                print("Você encontra apenas uma bela paisagem congelada.")
                ouro = random.randint(20, 50)
                heroi.ouro += ouro
                print(f"Você encontrou {ouro} de ouro abandonado.")
                input("Pressione ENTER para continuar...")
                progresso.flags_eventos["participou2"] = True
                

        elif escolha == "0":
            break

        elif progresso.flags_eventos["participou"] and progresso.flags_eventos["participou1"] and progresso.flags_eventos["participou2"]:
            progresso.flags_eventos["evento3_concluido"] = True
            print("Você já participou de todos os eventos")
            input("Pressione ENTER para continuar...")

        elif progresso.flags_eventos["participou"] or progresso.flags_eventos["participou1"] or progresso.flags_eventos["participou2"]:
            print("Você já participou dessa escolha do evento")
            input("Pressione ENTER para continuar...")

        else:
            print("Escolha inválida.")
            input("Pressione ENTER para continuar...")

    else:       
        print("O evento já foi concluido")
        input("Pressione ENTER para continuar...")
        return

def evento_sombra(heroi):

    from mundo import zona_atual
    print("[PERIGO] Um espelho quebrado chama sua atenção...")

    escolha = input("\n[1] - Aproximar-se\n[2] - Sair\n")

    if escolha == "1" and progresso.flags_eventos["evento4_concluido"] == False and zona_atual.bossderrotado == False:
        from inimigos import boss_castelo_do_caos
        sombra = copy.deepcopy(boss_castelo_do_caos[1])
        sombra.nome = f"Sombra de {heroi.nome}"
        sombra.vida += 150
        sombra.vidamax += 150
        sombra.ataque = int(heroi.ataque * 1.10)

        copia_heroi_dialogo(heroi, sombra)

        combatesys(heroi, sombra)

        copia_heroi_dialogo2(heroi, sombra)
        progresso.final_verdadeiro = True
        progresso.flags_eventos["evento4_concluido"] = True
        progresso.final_verdadeiro = True

    else:
        return

def evento_raid_vila_destruida(heroi):

    while progresso.flags_eventos["evento5_concluido"] == False:
        from progresso import item_raid_vila
        print("[EVENTO][PERIGO!] Você escuta alguns aldeões aflitos, parece que alguns monstros MUITO fortes estão prestes a tentar invadir a vila...")
        input("Pressione ENTER para continuar...")
        item_raid_vila
        set_acampamento(False)
        print("Você fica para lutar...")
        input("Pressione ENTER para continuar...")
        chefe = boss_floresta[0]
        chefe.vida += 500
        chefe.ataque += 30 
        chefe.nome = f"{Cores.AMARELO}{chefe.nome}{Cores.RESET}"
        combatesys(heroi, chefe)        # Já inicia sistema de luta, evitando poder fugir da luta e evitando re-ligar o acampamento 
        chefe = boss_caverna[0]
        chefe.vida += 500
        chefe.ataque += 30 
        chefe.nome = f"{Cores.AMARELO}{chefe.nome}{Cores.RESET}"
        combatesys(heroi, chefe)
        chefe.vida += 500
        chefe.ataque += 30 
        chefe.nome = f"{Cores.AMARELO}{chefe.nome}{Cores.RESET}"
        chefe = boss_montanhasgeladas[0]
        combatesys(heroi, chefe)
            # Recompensa do jogador é ativada dentro da verificação do ferreiro
        progresso.item_raid_vila = True
        set_acampamento(True)
        progresso.flags_eventos["evento5_concluido"] = True

    else:
        print("O evento já foi concluido")
        input("Pressione ENTER para continuar...")
        return