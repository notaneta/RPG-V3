from util import limpar_tela
from itens import poçoes, ferreiro_Amuletos_Ataque, ferreiro_Amuletos_Defesa, amuletos_ataque_exclusivos, amuletos_defesa_exclusivos, amuletos_mana_exclusivos, mago_amuletos_mana
from magias import listamagias
from magias import magias
from eventos import evento_vila_inical, evento_festival_da_neve, evento_pesca_vila, evento_raid_vila_destruida, evento_sombra

class Vilas:
    def __init__(self, nome, descricao, bossnecessario, proximavila, eventos=[]):
        self.nome = nome
        self.descricao = descricao
        self.bossnecessario = bossnecessario
        self.proximavila = proximavila
        # itens ou eventos
        self.eventos = eventos

    def vilamenu(self, heroi):
        while True:
            limpar_tela()

            print("╔" + "═" * 46 + "╗")
            print("║" + heroi.vila_atual.nome.upper().center(46) + "║")
            print("╚" + "═" * 46 + "╝")
            print()
            print(f"  Herói:  {heroi.nome}")
            print(f"  Ouro:   {heroi.ouro}")
            print()
            print("  " + "─" * 44)
            print("  [1]  Loja de Itens")
            print("  [2]  Ferreiro")
            print("  [3]  Estalagem          (restaura HP/MP)")
            print("  [4]  Status / Inventário")
            print("  [5]  Evento da Vila     (Disponivel apenas antes da luta do Chefe)")
            print("  [0]  Sair da Vila")
            print("  " + "─" * 44)
            print()
            escolha = input("  Qual sua decisão? ")

            if escolha == "1":
                menuloja(heroi)
            elif escolha == "2":
                ferreiro(heroi)
            elif escolha == "3":
                estalagem(heroi)
            elif escolha == "4":
                while True:
                    escolha2 = input("\n1 - Status Heroi\n2 - Inventário poções\n3 - Magias Aprendidas\n4 - Habilidades Aprendidas\n0 - Voltar\n")
                    if escolha2 == "1":
                        heroi.mostrar_status()
                        input("\nPressione ENTER para continuar...")
                        break

                    elif escolha2 == "2":
                        heroi.mostrar_inventario_pocoes()
                        input("\nPressione ENTER para continuar...")
                        break

                    elif escolha2 == "3":
                        heroi.mostrarmagias()
                        input("\nPressione ENTER para continuar...")
                        break

                    elif escolha2 == "4":
                        heroi.mostrarSkill()
                        input("\nPressione ENTER para continuar...")
                        break

                    elif escolha2 == "0":
                        break

            elif escolha == "5":
                heroi.vila_atual.eventos[0](heroi)
                return

            elif escolha == "0":
                print("\nSaindo da vila em direção à aventura...")
                break
            
# Vilas
vila5_finalverdadeiro = Vilas(None, None, None, None, None)
vila4_destruida = Vilas("Aldeia Destruida", "Aldeia que foi destruida", bossnecessario=4 , proximavila=1, eventos = [evento_sombra]) 
vila3_gelada = Vilas("Vila da Neve", "Uma humilde vila conhecida por usa temperatura gelada", bossnecessario=3, proximavila=vila4_destruida, eventos = [evento_festival_da_neve])
vila2_pescadores = Vilas("Porto Azul", "Vila de pescadores à beira do lago", bossnecessario=2, proximavila=vila3_gelada, eventos = [evento_pesca_vila])
vila_inicial = Vilas("Vila do vale verde", "Uma vila pacífica no bosque", bossnecessario=1, proximavila=vila2_pescadores, eventos = [evento_vila_inical])
Vila_atual = vila_inicial

from itens import poçoes, usaritem
from util import limpar_tela

def menuloja(heroi):

    nome_vila = heroi.vila_atual.nome
    exclusivos_mana = amuletos_mana_exclusivos.setdefault(nome_vila, [])

    while True:
        limpar_tela()

        print(f"Heroi: {heroi.nome}  |  Ouro: {heroi.ouro}")
        print("=" * 54)
        print("LOJA DO MAGO".center(54))
        print("=" * 54)
        print("1 - Comprar Poções")
        print("2 - Comprar amuletos")
        print("0 - Sair da loja")

        escolha = input("\nQual sua decisão? ")

        if escolha == "0":
            print("Você saiu da loja...")
            input("Pressione ENTER para continuar...")
            return

        if escolha == "1":
        # ---------- COMPRAR POÇÕES ----------
            while True:
                limpar_tela()

                # Separa por categoria preservando a ordem original
                vida      = [p for p in poçoes if p.tipo == "vida"]
                mana      = [p for p in poçoes if p.tipo == "mana"]
                especiais = [p for p in poçoes if p.tipo == "revive"]

                print(f"Heroi: {heroi.nome}  |  Ouro: {heroi.ouro}")
                print("=" * 54)
                print("LISTA DE POÇÕES".center(54))
                print("=" * 54)

                # --- Vida ---
                print("-------------- POÇÕES DE VIDA --------------")
                for i, p in enumerate(vida, start=1):
                    p.mostrar_item(i, heroi.ouro)
                print()

                # --- Mana ---
                print("-------------- POÇÕES DE MANA --------------")
                offset = len(vida)
                for i, p in enumerate(mana, start=1):
                    p.mostrar_item(offset + i, heroi.ouro)
                print()

                # --- Especiais ---
                if especiais:
                    print("------------- ITENS ESPECIAIS --------------")
                    offset += len(mana)
                    for i, p in enumerate(especiais, start=1):
                        p.mostrar_item(offset + i, heroi.ouro)
                    print()

                print("=" * 54)
                escolha2 = input("Digite o ID do item para comprar (0 = sair): ").strip()

                if escolha2 == "0":
                    print("Você saiu da seção de compras...")
                    input("Pressione ENTER para continuar...")
                    break

                if not escolha2.isdigit():
                    print("\nDigite apenas números.")
                    input("Pressione ENTER para continuar...")
                    continue

                # Reconstrói a lista completa na mesma ordem da HUD
                todos = vida + mana + especiais
                indice = int(escolha2) - 1

                if not (0 <= indice < len(todos)):
                    print("\nItem não existente.")
                    input("Pressione ENTER para continuar...")
                    continue

                item = todos[indice]

                if heroi.ouro < item.custo:
                    print(f"\nVocê não tem ouro suficiente. Precisa de {item.custo} e tem {heroi.ouro}.")
                    input("Pressione ENTER para continuar...")
                    continue

                heroi.ouro -= item.custo
                heroi.adicionar_pocoes(item)   # adicionar_pocoes já faz deepcopy

                print(f"\nVocê comprou {item.nome} por {item.custo} de ouro.")
                print(f"Seu novo ouro é {heroi.ouro}.")
                input("Pressione ENTER para continuar...")

        if escolha == "2":
            while True:
                
                lista_global = mago_amuletos_mana
                lista_exclusiva = exclusivos_mana
                categoria = "AMULETOS DE MANA"

                lista = lista_global + lista_exclusiva   # só para exibição

                print(f"Heroi: {heroi.nome}  |  Ouro: {heroi.ouro}")
                print("=" * 54)
                print(categoria.center(54))
                print("=" * 54)

                if not lista:
                    print("\nNenhum amuleto disponível nesta vila.")
                    input("Pressione ENTER para continuar...")
                    return

                mostrar_lista_amuletos(lista, heroi)

                print("=" * 54)
                escolha2 = input("Digite o ID do amuleto para comprar (0 = sair): ").strip()

                if escolha2 == "0":
                    print("Você saiu da loja...")
                    input("Pressione ENTER para continuar...")
                    break

                if not escolha2.isdigit():
                    print("\nDigite apenas números.")
                    input("Pressione ENTER para continuar...")
                    continue

                indice = int(escolha2) - 1

                if not (0 <= indice < len(lista)):
                    print("\nItem não existente.")
                    input("Pressione ENTER para continuar...")
                    continue

                amuleto = lista[indice]

                if amuleto.custo > heroi.ouro:
                    print(f"\nVocê não tem ouro suficiente. Precisa de {amuleto.custo} e tem {heroi.ouro}.")
                    input("Pressione ENTER para continuar...")
                    continue

                amuleto.comprar(heroi)
                amuleto.equipar(heroi)

                if escolha == "1":
                    print(f"\nVocê comprou {amuleto.nome}! Novo MP: {heroi.manamax}")

                # Remove do lugar de origem de verdade, não da lista temporária
                if amuleto in lista_global:
                    lista_global.remove(amuleto)
                elif amuleto in lista_exclusiva:
                    lista_exclusiva.remove(amuleto)

                input("Pressione ENTER para continuar...")

            
def estalagem(heroi):
    while True:
        custo = int(12 + heroi.nivel * 1.05)
        while True:
            escolha = input(f"Ao chegar na estalagem, você tem a opção de:\n1 - Pagar {custo} para descansar(Cura total)\n0 - Sair\n")
            if escolha == "1":
                if heroi.ouro >= custo:
                    heroi.ouro -= custo
                    heroi.vida = heroi.vidamax
                    heroi.mana = heroi.manamax
                    print("\nVocê descansou na estalagem e curou HP e MP total!")
                    input("\nPressione ENTER para continuar...")   
                    return
                else:
                    print("Você não tem ouro suficiente!")
                    input("\nPressione ENTER para continuar...")
                    return

            elif escolha == "0":
                return
            

def mostrar_lista_amuletos(lista, heroi, offset=0):
    """Mostra uma lista de amuletos formatada, com numeração contínua a partir de offset."""
    for i, amuleto in enumerate(lista, start=offset + 1):
        amuleto.mostrar_item(i, heroi.ouro)
    print()

def ferreiro(heroi):
    while True:
        limpar_tela()

        nome_vila = heroi.vila_atual.nome
        exclusivos_ataque = amuletos_ataque_exclusivos.setdefault(nome_vila, [])
        exclusivos_defesa = amuletos_defesa_exclusivos.setdefault(nome_vila, [])

        print(f"Heroi: {heroi.nome}  |  Ouro: {heroi.ouro}")
        print("=" * 54)
        print(f"FERREIRO — {nome_vila}".center(54))
        print("=" * 54)
        print("1 - Melhorar Ataque")
        print("2 - Melhorar Defesa")
        print("0 - Sair do Ferreiro")

        escolha = input("\nQual sua decisão? ")

        if escolha == "0":
            return

        if escolha not in ("1", "2"):
            print("Comando não existente.")
            input("Pressione ENTER para continuar...")
            continue

        while True:
            limpar_tela()

            if escolha == "1":
                lista_global = ferreiro_Amuletos_Ataque
                lista_exclusiva = exclusivos_ataque
                categoria = "AMULETOS DE ATAQUE"
            else:
                lista_global = ferreiro_Amuletos_Defesa
                lista_exclusiva = exclusivos_defesa
                categoria = "AMULETOS DE DEFESA"

            lista = lista_global + lista_exclusiva   # só para exibição

            print(f"Heroi: {heroi.nome}  |  Ouro: {heroi.ouro}")
            print("=" * 54)
            print(categoria.center(54))
            print("=" * 54)

            if not lista:
                print("\nNenhum amuleto disponível nesta vila.")
                input("Pressione ENTER para continuar...")
                return

            mostrar_lista_amuletos(lista, heroi)

            print("=" * 54)
            escolha2 = input("Digite o ID do amuleto para comprar (0 = sair): ").strip()

            if escolha2 == "0":
                print("Você saiu do ferreiro...")
                input("Pressione ENTER para continuar...")
                break

            if not escolha2.isdigit():
                print("\nDigite apenas números.")
                input("Pressione ENTER para continuar...")
                continue

            indice = int(escolha2) - 1

            if not (0 <= indice < len(lista)):
                print("\nItem não existente.")
                input("Pressione ENTER para continuar...")
                continue

            amuleto = lista[indice]

            if amuleto.custo > heroi.ouro:
                print(f"\nVocê não tem ouro suficiente. Precisa de {amuleto.custo} e tem {heroi.ouro}.")
                input("Pressione ENTER para continuar...")
                continue

            amuleto.comprar(heroi)
            amuleto.equipar(heroi)

            if escolha == "1":
                print(f"\nVocê comprou {amuleto.nome}! Novo ataque: {heroi.ataque}")
            else:
                print(f"\nVocê comprou {amuleto.nome}! Nova defesa: {heroi.defesa}")

            # Remove do lugar de origem de verdade, não da lista temporária
            if amuleto in lista_global:
                lista_global.remove(amuleto)
            elif amuleto in lista_exclusiva:
                lista_exclusiva.remove(amuleto)

            input("Pressione ENTER para continuar...")