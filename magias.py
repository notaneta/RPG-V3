class magias:
    def __init__(self,id, nome, dano, custo, requisito):
        self.id = id
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.requisito = requisito

    def mostrarmagias(self):
        print(f"Dano: {self.dano}")
        print(f"Custo MP: {self.custo}")

def usarmagia(heroi, inimigo):
    if not heroi.magiasaprendidas:
        print("Você ainda não aprendeu nenhuma magia.")
        input("Pressione ENTER para continuar...")
        return False

    heroi.mostrarmagias()

    try:
        escolha = input("Digite o N* da magia que deseja usar, ou 0 para não fazer nada\n")
    except ValueError:
        print("Digite um número válido.")
        input("Pressione ENTER para continuar...")
        return False

    if escolha == 0:
        print("Você não faz nada...")
        input("Pressione ENTER para continuar...")
        return False

    for magia in heroi.magiasaprendidas:
        if magia.id == escolha:
            if heroi.mana >= magia.custo:
                heroi.mana -= magia.custo
                ataquefinal = max(1, magia.dano - inimigo.defesa_magica)
                inimigo.vida -= ataquefinal
                print(f"Você causou {ataquefinal} de dano em {inimigo.nome}")
                input("Pressione ENTER para continuar...")
                return True
            else:
                print("Você não tem MP suficiente.")
                input("Pressione ENTER para continuar...")
                return False
        else:
            print("ID da Magia inválida")
            input("Pressione ENTER para continuar...")
            return False

listamagias = [
    # Nome, Dano, Custo MP, Nível Requisito
    magias("1", "Chamas de Fogo", 22, 18, 2),
    magias("2", "Espinho de Gelo", 45, 30, 4),
    magias("3", "Bola de fogo", 75, 48, 6),
    magias("4", "Relâmpago Arcano", 115, 68, 10),
    magias("5", "Cometa Sombrio", 160, 95, 14),
]

magia_boss = [
    magias("3", "Chamas do Dragão", 99, 70, "Após Derrotar um boss"),           # Será recebida após lutar contra 1 boss
    magias("9", "Forma do Caos", 10000, 1, "Oculto"),   # Magia secreta, comprada ou adquirida depois de certo requisito
]
