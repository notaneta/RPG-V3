class foco:
    def __init__(self,id, nome, dano, custo, requisito):
        self.id = id
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.requisito = requisito

    def mostrarskill(self):
        print(f"ID: {self.id} Habilidade: {self.nome}")
        print(f"Dano: {self.dano}")
        print(f"Uso de Fúria: {self.custo}")

def usarfoco(heroi, inimigo):
    if not heroi.habilidadesaprendidas:
        print("Você ainda não aprendeu nenhuma habilidade.")
        input("Pressione ENTER para continuar...")
        return False

    print("============ Habilidades ============")
    for skill in heroi.habilidadesaprendidas:
        skill.mostrarskill()
        print("-" * 20)

    try:
        escolha = input("Digite o N(ID) da habilidade que deseja usar, ou 0 para não fazer nada\n")
    except ValueError:
        print("Digite um número válido.")
        input("Pressione ENTER para continuar...")
        return False

    if escolha == 0:
        print("Você não faz nada...")
        input("Pressione ENTER para continuar...")
        return False

    for habilidade in heroi.habilidadesaprendidas:
        if habilidade.id == escolha:
            if heroi.foco >= habilidade.custo:
                heroi.foco -= habilidade.custo
                ataquefinal = max(1, habilidade.dano - inimigo.defesa)
                inimigo.vida -= ataquefinal
                print(f"Você causou {ataquefinal} de dano em {inimigo.nome}")
                print(f"Foco restante: {int(heroi.foco)}")
                input("Pressione ENTER para continuar...")
                return True
            else:
                print(f"Foco insuficiente. Você tem {int(heroi.foco)}, precisa de {habilidade.custo}.")
                input("Pressione ENTER para continuar...")
                return False
        else:
            print("ID da habilidade inválida")
            input("Pressione ENTER para continuar...")
            return False

listahabilidades = [
    # Id, Nome, Dano, Custo Foco, Nível
    foco("1", "Golpe Flamejante", 30, 25, 1),
    foco("2", "Corte Vorpal", 60, 40, 3),
    foco("3", "Lâmina do Dragão", 105, 60, 7),
    foco("4", "Impacto Símico", 150, 80, 12),
    foco("5", "Execução Divina", 210, 100, 18),
]

lista_habilidades_exclusivas = [
foco("3", "Corte Dimensional", 99, 100,"Após Derrotar um boss"),           # Será recebida após lutar contra 1 boss 
foco("9", "Multiplos Golpes", 10000, 100,"Oculto"),   # Magia secreta, comprada ou adquirida depois de certo requisito
]