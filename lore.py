import time

def dialogo(texto):

    for letra in texto:

        print(letra, end="", flush=True)

        if letra in [".", "!", "?"]:
            time.sleep(0.3)     # Pausa automatica nos pontos.
        else:
            time.sleep(0.03)

    print()


def boss_final_dialogo(heroi, boss):

    from combate import set_acampamento

    set_acampamento(False)

    print("\nVocê atravessa o salão do trono.")
    print("O castelo está completamente silencioso.")
    input("Pressione ENTER para continuar...\n")

    print("No fundo do salão, uma figura está sentada em um enorme trono negro.")
    input("Pressione ENTER para continuar...\n")

    dialogo("??? Então... finalmente chegou.")
    dialogo("Derrotou meus generais.")
    dialogo("Sobreviveu às montanhas geladas.")
    dialogo("E chegou até aqui acreditando que eu sou a origem de todo esse caos.")
    dialogo("Mas você ainda não compreendeu a verdade deste mundo.")

    escolha = input(
        "\n1 - Quem é você?"
        "\n2 - Eu vim acabar com isso."
        "\nO que fazer?\n"
    )

    if escolha == "1":

        dialogo("Rei do Caos: Eu sou aquele que tentou lutar contra aquilo que deveriamos apenas aceitar.")

        dialogo("Rei do Caos: E paguei o preço por isso.")

        dialogo("Rei do Caos: Monstros?\nGuerras?\nDestruição?")

        dialogo("Rei do Caos: Tudo isso é apenas consequência.")

        dialogo("Rei do Caos: Do caos que sempre esteve dentro das pessoas.")

    elif escolha == "2":

        dialogo("Rei do Caos: Tão determinado...")

        dialogo("Rei do Caos: Mas você irá apenas falhar como os outros.")

    input("Pressione ENTER para continuar...\n")

    print("O Rei do Caos se levanta lentamente.")
    print("Uma energia sombria começa a envolver o salão.")
    print("A luta vai começar!")
    
    input("Pressione ENTER para continuar...\n")


def copia_heroi_dialogo(heroi, boss):

    print("Um espelho quebrado chama sua atenção.")
    print("Você vê seu reflexo...")
    print("Mas ele não imita seus movimentos.")
    input("Pressione ENTER para continuar...\n")

    print("A imagem sorri.")
    print("Então atravessa o espelho.")
    print("Uma versão distorcida de você surge diante dos seus olhos.")
    input("Pressione ENTER para continuar...\n")

    dialogo(f"{boss.nome}: Finalmente...")
    dialogo(f"{boss.nome}: Eu estava esperando por você.")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{heroi.nome}: Quem é você?")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{boss.nome} Você.")
    dialogo(f"{boss.nome} Ou aquilo que existe dentro de você.")

    input("Pressione ENTER para continuar...\n")

    print("A sombra ergue a mão.")
    print("Uma energia negra começa a envolver o salão.")
    input("Pressione ENTER para continuar...\n")

    dialogo(f"{boss.nome} O Rei me chamou de monstro.")
    dialogo(f"{boss.nome} Mas ele nunca entendeu...")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{boss.nome} Eu não fui criada para destruir a si mesmo.")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{boss.nome}: Fui criada para libertá-lo.")

    input("Pressione ENTER para continuar...\n")
    input("Pressione ENTER para continuar...\n")


def copia_heroi_dialogo2(heroi, boss):

    print("A sombra começa a desaparecer.")
    print("Você respira aliviado.")
    input("Pressione ENTER para continuar...\n")

    dialogo(f"{heroi.nome}: Acabou...")

    input("Pressione ENTER para continuar...\n")

    dialogo("Sombra: Não...")
    dialogo("Sombra: Agora começou.")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{heroi.nome}: O quê?")

    input("Pressione ENTER para continuar...\n")

    dialogo("Sombra: Você realmente acreditou que eu era o inimigo?")

    input("Pressione ENTER para continuar...\n")

    print("A sombra olha para o castelo.")
    input("Pressione ENTER para continuar...\n")

    dialogo("Sombra: Eu era apenas a chave.")

    input("Pressione ENTER para continuar...\n")

    dialogo(f"{heroi.nome}: Chave...?")

    input("Pressione ENTER para continuar...\n")

    dialogo(
        "Sombra: O Rei não queria que você me derrotasse."
    )

    dialogo(
        "Sombra: Ele precisava que você me derrotasse."
    )

    input("Pressione ENTER para continuar...\n")

    dialogo(
        "Sombra: Porque somente alguém capaz de superar "
        "a própria sombra poderia quebrar o selo."
    )

    input("Pressione ENTER para continuar...\n")

    dialogo("Sombra: E você acabou de fazer isso.")

    print("A energia negra começa a deixar o corpo da sombra.")
    print("Ela se transforma em uma espécie de chave de energia.")
    input("Pressione ENTER para continuar...\n")
    input("Pressione ENTER para continuar...\n")

def dialogo_FINAL_verdadeiro(heroi, boss):

    dialogo(f"{heroi.nome} Agora o mundo está em paz...")

    input("Pressione ENTER para continuar...\n")

    print("Uma energia explode pelo salão.")
    print("O castelo inteiro começa a tremer.")
    input("Pressione ENTER para continuar...\n")

    print("Por alguns segundos, tudo fica em silêncio.")
    input("Pressione ENTER para continuar...\n")

    print("Então...")
    print("Uma risada ecoa pelo castelo.")
    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: Finalmente.")

    input("Pressione ENTER para continuar...\n")

    print("O herói olha para trás.")
    print("O Rei do Caos está diante do trono.")
    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: Você abriu a prisão.")

    input("Pressione ENTER para continuar...\n")

    print("As paredes do castelo começam a rachar.")
    print("Uma enorme energia negra surge do interior do trono.")
    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: Eu nunca fui o verdadeiro caos.")

    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: Eu era apenas suas correntes.")

    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: E agora...")

    print("Uma enorme explosão de energia negra toma conta do salão.")
    input("Pressione ENTER para continuar...\n")

    dialogo("Rei do Caos: Ele está livre.")

    input("Pressione ENTER para continuar...\n")

    print("O castelo inteiro é consumido pela energia sombria.")
    print("Um enorme portal se abre diante de você.")
    input("Pressione ENTER para continuar...\n")

    print("Você sabe que não há mais como voltar atrás.")
    print("Para acabar com o caos, terá que atravessar o portal.")

    input("Pressione ENTER para continuar...\n")

    print("Nova área desbloqueada!")
    print("Abismo\n")
    input("Pressione ENTER para continuar...\n")
