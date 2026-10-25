class foco:
    def __init__(self, id, nome, dano, custo, requisito):
        self.id = id
        self.nome = nome
        self.dano = dano
        self.custo = custo
        self.requisito = requisito

    def mostrarskill(self, numero=None):
        prefixo = f"[{numero}] " if numero is not None else f"ID: {self.id} "
        print(f"{prefixo}Habilidade: {self.nome}")
        print(f"Dano: {self.dano}")
        print(f"Uso de Fúria: {self.custo}")


def usarfoco(heroi, inimigo):
    if not heroi.habilidadesaprendidas:
        print("Você ainda não aprendeu nenhuma habilidade.")
        input("Pressione ENTER para continuar...")
        return False

    print("============ Habilidades ============")
    for i, skill in enumerate(heroi.habilidadesaprendidas, start=1):
        skill.mostrarskill(i)
        print("-" * 20)

    escolha = input("Digite o N* da habilidade que deseja usar, ou 0 para não fazer nada\n").strip()

    if escolha == "0":
        print("Você não faz nada...")
        input("Pressione ENTER para continuar...")
        return False

    if not escolha.isdigit():
        print("Digite um número válido.")
        input("Pressione ENTER para continuar...")
        return False

    indice = int(escolha) - 1

    if not (0 <= indice < len(heroi.habilidadesaprendidas)):
        print("Habilidade inválida.")
        input("Pressione ENTER para continuar...")
        return False

    habilidade = heroi.habilidadesaprendidas[indice]

    if heroi.foco < habilidade.custo:
        print(f"Foco insuficiente. Você tem {int(heroi.foco)}, precisa de {habilidade.custo}.")
        input("Pressione ENTER para continuar...")
        return False

    heroi.foco -= habilidade.custo
    ataquefinal = max(1, habilidade.dano - inimigo.defesa)
    inimigo.vida -= ataquefinal
    print(f"Você causou {ataquefinal} de dano em {inimigo.nome}")
    print(f"Foco restante: {int(heroi.foco)}")
    input("Pressione ENTER para continuar...")
    return True

def executar_skill(heroi, inimigo, skill):
    if heroi.foco >= skill.custo:
        heroi.foco -= skill.custo
        danofinal = max(1, skill.dano - inimigo.defesa_magica)
        inimigo.vida -= danofinal
    else:
        danofinal = None
    return danofinal


listahabilidades = [
    # Id, Nome, Dano, Custo Foco, Nível
    foco("1", "Golpe Flamejante", 30, 25, 1),
    foco("2", "Corte Vorpal", 60, 40, 3),
    foco("3", "Lâmina do Dragão", 105, 60, 7),
    foco("4", "Impacto Sísmico", 150, 80, 12),
    foco("5", "Execução Divina", 210, 100, 18),
]

lista_habilidades_exclusivas = [
    foco("10", "Corte Dimensional", 99, 100, "Após Derrotar um boss"),  # Recebida após derrotar 1 boss
    foco("11", "Multiplos Golpes", 10000, 100, "Oculto"),               # Secreta, adquirida depois de certo requisito
]