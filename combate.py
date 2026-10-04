import random
import sys 
from util import limpar_tela, barra_hp, barra_mp, barra_furia, largura, acampamento_ativo, set_acampamento
from itens import usaritem
from magias import usarmagia, listamagias
from habilidades import usarfoco , listahabilidades

def combateini(heroi, inimigo):   # Heroi e inimigo dentro do parenteses, recebem os dados que foram enviados em ordem no parenteses do main

    while True:
        limpar_tela()
        print("======Um inimigo apareceu!======\n")
        inimigo.mostrar_status()
        escolha = input("\nQual sua decisão? \n[1] - Lutar\n[2] - Fugir (Chance de 50%)\n")
        if escolha == "1":
                combatesys(heroi, inimigo)          # Como o combateINI já recebeu os dados, aqui só peço para ele compartilhar os dados com a outra função
                return
        elif escolha == "2":
            testefugir = random.randint(1, 10) 
            if testefugir >= 5:
                print("Você fugiu com sucesso")
                input("Pressione ENTER para continuar...")
                break
            else:
                print("Você não conseguiu fugir e terá que lutar")
                input("Pressione ENTER para continuar...")
                combatesys(heroi, inimigo)
                return

def combatehud(heroi, inimigo): 
    print(f"{heroi.nome}")
    print(f"HP [{barra_hp(heroi.vida, heroi.vidamax)}] "f"{int(heroi.vida)}/{heroi.vidamax}")
    print(f"MP [{barra_mp(heroi.mana, heroi.manamax)}] "f"{int(heroi.mana)}/{heroi.manamax}")
    print(f"Fúria [{barra_furia(heroi.foco, heroi.focomax)}] "f"{int(heroi.foco)}/{heroi.focomax}")
    print(f"Ataque: {heroi.ataque}       Defesa: {heroi.defesa}")
    print("=" * largura)
    print(f"{inimigo.nome}")
    print(f"HP [{barra_hp(inimigo.vida, inimigo.vidamax)}] "f"{int(inimigo.vida)}/{inimigo.vidamax}")
    print(f"Ataque: {inimigo.ataque}")      # Posteriormente na proxima versão colocar na HUD a defesa dos monstros de cada um, pois vai ajudar a deixar o combate mais complexo, alguns melhores contra espada e outros contra magia


    if heroi.contador_gelo > 0:
        if heroi.contador_gelo == 1:
            print("\nVocê será paralisado no próximo turno!")
        else:
            print(f"\nTurnos até ser paralisado: {heroi.contador_gelo - 1}")
    elif heroi.contador_gelo == 0 and inimigo.skill_stun:
        print("\nVocê será paralisado agora!")

def combatesys(heroi, inimigo):
    while True:
        while heroi.vida > 0 and inimigo.vida > 0:
            limpar_tela()
            combatehud(heroi, inimigo)
            lutar = input("\n[1] - Atacar\n[2] - Lançar Magia\n[3] - Usar Item (Não passa o turno)\n[4] - Usar Habilidade\n")
            print("\nQual sua decisão?\n")
            turnojogador = False

            # Teste Stun

            if heroi.turnos_stun >= 1:
                print("Você ficou paralisado e não conseguiu agir nesse turno!")
                input("\nPressione ENTER para continuar...")
                heroi.turnos_stun -= 1
                turnojogador = True

            else:   # Sistema padrão escolhas jogador

                if lutar == '1':       
                    turnojogador = True
                    heroi.atacar(inimigo)
                    heroi.turnos_stun -= 1

                elif lutar == "2":
                    if heroi.mana >= 18:
                        turnojogador = usarmagia(heroi, inimigo)
                    else:
                        print("\nVocê precisa de pelo menos 25 de mana!")
                        input("\nPressione ENTER para continuar...")

                elif lutar == '3':
                    usaritem(heroi)

                elif lutar == "4":
                    if heroi.foco >= 25:
                        turnojogador = usarfoco(heroi, inimigo)

                    else:
                        print("\nVocê precisa de pelo menos 25 de fúria!")
                        input("\nPressione ENTER para continuar...")

            if turnojogador and inimigo.vida > 0:           # Comando de ataque inimigo dentro da classe dele
                inimigo.atacar(heroi)     # Foco do heroi é gerado no comando de atacar do inimigo / Assim caso a ação se repita, o foco gera também
                if inimigo.habilidade is not None:
                    for habilidade in inimigo.habilidade:
                        habilidade(heroi, inimigo)      # Habilidade só é executada caso a vida do boss esteja no nivel correto conforme ele mesmo dispor

        # Logica Game over

        else:
            if heroi.vida <= 0:
                # Procura Pedra da Vida no inventário
                pedra = next(
                    (item for item in heroi.inventario
                    if getattr(item, "tipo", None) == "revive" and item.quantidade > 0),
                    None)

                if pedra:
                    heroi.vida = heroi.vidamax // 2
                    heroi.removeritem(pedra)
                    print(f"\n[{pedra.nome}] brilha e se desfaz!")
                    print(f"Você revive com {heroi.vida}/{heroi.vidamax} de HP.")
                    input("Pressione ENTER para continuar...")
                    # Continua o combate: reentra no while
                    continue
                    
                else:
                    print("\nSeu HP foi reduzido a 0, Você perdeu...\n[GAME OVER]\n")

                    while True:
                        escolha3 = input("Continuar? (s/n)")
                        if escolha3 == "s":
                            from database import menu_principal 
                            menu_principal()
                        elif escolha3 == "n":
                            sys.exit()

                        else:
                            print("Comando invalido")

            # Logica vecer batalha 

            elif inimigo.vida <= 0:
                inimigo.skill_stun = False
                limpar_tela()

                print(f"\nVocê derrotou o inimigo e recebeu {inimigo.ouro} de OURO e {inimigo.xp} de XP")

                heroi.ouro += inimigo.ouro
                heroi.xp += inimigo.xp
                heroi.foco = 0

                input("\nPressione ENTER para continuar...\n")

                heroi.subirnivel(listahabilidades, listamagias)

                import progresso

                if progresso.avancar_jogo:
                    heroi.zona_atual.avançarjogo()

                # Evento acampamento
                if acampamento_ativo():
                    from eventos import acampamento

                    while True:
                        limpar_tela()
                        print("=" * 54)
                        print(f"ACAMPAMENTO".center(54))
                        print("=" * 54)
                        print("Depois da batalha, você encontra um local para acampar...")
                        print("[1] - Acampar (Restaura 30% HP/MP) Risco de evento")
                        print("[2] - Voltar")

                        escolha = input("\nOque fazer? ")

                        if escolha == "1":
                            acampamento(heroi)
                            return

                        elif escolha == "2":
                            return

                        else:
                            print("Opção invalida")
                            input("\nPressione ENTER para continuar...")

                return