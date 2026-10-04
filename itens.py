# Poção de Cura
from util import Cores

class Pocao:
    def __init__(self, id, nome, cura, custo, quantidade, descricao, tipo="vida"):
        self.id = id
        self.nome = nome
        self.cura = cura
        self.custo = custo
        self.quantidade = quantidade
        self.descricao = descricao
        self.tipo = tipo   # "vida", "mana" ou "revive"

    def mostrar_item(self, id_item=None, ouro_jogador=None):
        # Cores
        cor = ""
        reset = ""
        if ouro_jogador is not None:
            cor = Cores.VERDE if ouro_jogador >= self.custo else Cores.CINZA
            reset = Cores.RESET

        # Efeito formatado conforme o tipo
        if self.tipo == "vida":
            efeito = f"+{self.cura:>3} HP"
        elif self.tipo == "mana":
            efeito = f"+{self.cura:>3} MP"
        else:  # revive
            efeito = " revive "

        prefixo = f"[{id_item:>2}] " if id_item is not None else ""
        print(f"{cor}{prefixo}{self.nome:<20} {efeito:<9} -- {self.custo:>3} ouro{reset}")
        # Descrição só quando é item especial (revive)
        if self.tipo == "revive":
            print(f"      {self.descricao}")

poçoes = [
    # --- Vida ---
    Pocao("1", "Poção Pequena",  35,  15, 1, "Cura uma pequena parte da vida"),
    Pocao("2", "Poção Média",    75,  35, 1, "Cura média da sua vida"),
    Pocao("3", "Poção Grande",  125,  45, 1, "Cura grande parte da sua vida"),
    Pocao("4", "Poção Élfica",  250, 100, 1, "Cura massiva. Item de fim de jogo."),
    Pocao("5", "Elixir do Caos",500, 220, 1, "Cura quase total. Reservado para o Rei do Caos."),

    # --- Mana ---
    Pocao("6", "Poção de Mana",  50,  40, 1, "Restaura 50 de MP",  tipo="mana"),
    Pocao("7", "Elixir de Mana",150, 120, 1, "Restaura 150 de MP", tipo="mana"),

    # --- Revive ---
    Pocao("8", "Pedra da Vida", 0, 350, 1, "Revive automaticamente com 50% da vida ao morrer (consumida ao usar)", tipo="revive"),
]

def usaritem(heroi):
    while True:
        print("Qual item do seu inventário usar?")
        heroi.mostrar_inventario_pocoes()
        escolha = input("Digite o número do item que deseja usar ou digite 0 para sair...")

        if escolha == "0":
            return

        if not escolha.isdigit():
            print("Digite apenas números!")
            input("Pressione ENTER para continuar...")
            continue

        indice = int(escolha) - 1

        if not (0 <= indice < len(heroi.inventario)):
            print("Item inválido.")
            input("Pressione ENTER para continuar...")
            continue

        item = heroi.inventario[indice]

        if item.quantidade <= 0:
            print("Este item não pode ser usado (quantidade zero).")
            input("Pressione ENTER para continuar...")
            return

        if item.tipo == "vida":
            curado = min(item.cura, heroi.vidamax - heroi.vida)
            heroi.vida += curado
            print(f"Você usou {item.nome} e recuperou {curado} de HP.")
        elif item.tipo == "mana":
            restaurado = min(item.cura, heroi.manamax - heroi.mana)
            heroi.mana += restaurado
            print(f"Você usou {item.nome} e recuperou {restaurado} de MP.")
        elif item.tipo == "revive":
            print("A Pedra da Vida só é ativada automaticamente ao morrer.")
            input("Pressione ENTER para continuar...")
            continue

        heroi.removeritem(item)
        input("Pressione ENTER para continuar...")
        return


class Amuletos_Ataque:
    def __init__(self, nome, descricao, dano, custo):
        self.nome = nome
        self.descricao = descricao
        self.dano = dano
        self.custo = custo

    def mostrar_item(self, id_item=None, ouro_jogador=None):
        cor = ""
        reset = ""
        if ouro_jogador is not None:
            cor = Cores.VERDE if ouro_jogador >= self.custo else Cores.CINZA
            reset = Cores.RESET

        prefixo = f"[{id_item:>2}] " if id_item is not None else ""
        print(f"{cor}{prefixo}{self.nome:<22} +{self.dano:>2} ATK   {self.custo:>3} ouro{reset}")
        print(f"      {self.descricao}")

    def comprar(self, heroi):
        heroi.ouro -= self.custo

    def equipar(self, heroi):
        heroi.ataque += self.dano

    def __str__(self):
        return self.nome


class Amuletos_Defesa:
    def __init__(self, nome, descricao, defesa, custo):
        self.nome = nome
        self.descricao = descricao
        self.defesa = defesa
        self.custo = custo

    def mostrar_item(self, id_item=None, ouro_jogador=None):
        cor = ""
        reset = ""
        if ouro_jogador is not None:
            cor = Cores.VERDE if ouro_jogador >= self.custo else Cores.CINZA
            reset = Cores.RESET

        prefixo = f"[{id_item:>2}] " if id_item is not None else ""
        print(f"{cor}{prefixo}{self.nome:<22} +{self.defesa:>2} DEF   {self.custo:>3} ouro{reset}")
        print(f"      {self.descricao}")

    def comprar(self, heroi):
        heroi.ouro -= self.custo

    def equipar(self, heroi):
        heroi.defesa += self.defesa

    def __str__(self):
        return self.nome

class Amuletos_Mana:
    def __init__(self, nome, descricao, mana, custo):
        self.nome = nome
        self.descricao = descricao
        self.mana = mana
        self.custo = custo

    def mostrar_item(self, id_item=None, ouro_jogador=None):
        cor = ""
        reset = ""
        if ouro_jogador is not None:
            cor = Cores.VERDE if ouro_jogador >= self.custo else Cores.CINZA
            reset = Cores.RESET

        prefixo = f"[{id_item:>2}] " if id_item is not None else ""
        print(f"{cor}{prefixo}{self.nome:<22} +{self.mana:>2} MP   {self.custo:>3} ouro{reset}")
        print(f"      {self.descricao}")

    def comprar(self, heroi):
        heroi.ouro -= self.custo

    def equipar(self, heroi):
        heroi.manamax += self.mana

    def __str__(self):
        return self.nome


# ============================================================
# LISTAS
# ============================================================
ferreiro_Amuletos_Ataque = [
    Amuletos_Ataque("Amuleto do Aprendiz",  "Talismã simples dado a jovens guerreiros em seu primeiro treino.",  1,  20),
    Amuletos_Ataque("Amuleto do Garra",     "Pequeno talismã com dentes de fera que afia seus golpes.",          2,  35),
    Amuletos_Ataque("Amuleto do Caçador",   "Confeccionado com presas e penas, guia a mão do portador.",         3,  40),
    Amuletos_Ataque("Amuleto da Força",     "Esculpido em pedra rúnica, canaliza poder físico ao usuário.",      4,  45),
    Amuletos_Ataque("Amuleto da Fúria",     "Pulsa com a raiva contida de batalhas antigas.",                    5,  52),
    Amuletos_Ataque("Amuleto do Guerreiro", "Carrega a fúria de antigos combatentes das profundezas.",           6,  60),
    Amuletos_Ataque("Amuleto do Predador",  "Aumenta a precisão e a força de impacto em cada ataque.",           8,  80),
    Amuletos_Ataque("Amuleto do Berserker", "Enfeitiçado para ignorar a dor e golpear sem hesitar.",            10, 105),
    Amuletos_Ataque("Amuleto do Titã",      "Relíquia lendária que concede força devastadora e inigualável.",   12, 130),
    Amuletos_Ataque("Amuleto do Abismo",    "Forjado nas fissuras profundas, amplifica o impacto dos golpes.",  13, 170),
    Amuletos_Ataque("Amuleto do Caos",      "Energia sombria que dilacera qualquer armadura.",                  14, 210),
    Amuletos_Ataque("Amuleto do Vazio",     "Poder extraído do próprio abismo.",                                16, 320),
    Amuletos_Ataque("Amuleto da Ruína",     "Cada golpe carrega o eco de mil batalhas perdidas.",               20, 480),
    Amuletos_Ataque("Amuleto do Fim",       "O último artefato de guerra, forjado antes do silêncio eterno.",   25, 700),
]

ferreiro_Amuletos_Defesa = [
    Amuletos_Defesa("Amuleto do Couro",      "Tira de couro curtido, primeira proteção de todo aventureiro.",     1,  18),
    Amuletos_Defesa("Amuleto da Proteção",   "Encantamento simples que repele pequenos impactos.",                3,  30),
    Amuletos_Defesa("Amuleto do Escudeiro",  "Feito para quem ainda aprende a aparar golpes.",                    4,  40),
    Amuletos_Defesa("Amuleto da Casca",      "Feito com madeira sagrada enrijecida contra impactos.",             5,  50),
    Amuletos_Defesa("Amuleto do Bastião",    "Cria uma barreira sutil que reduz o dano de acertos diretos.",      9,  80),
    Amuletos_Defesa("Amuleto do Muro",       "Pedra viva entrelaçada, sustenta o corpo contra investidas.",      11,  95),
    Amuletos_Defesa("Amuleto do Guardião",   "Forjado com rocha subterrânea, fortifica o corpo do herói.",       14, 110),
    Amuletos_Defesa("Amuleto do Colosso",    "Peso e resistência de uma montanha em miniatura.",                 16, 135),
    Amuletos_Defesa("Amuleto Inabalável",    "Relíquia congelada que absorve os golpes mais violentos.",         18, 160),
    Amuletos_Defesa("Amuleto do Abismo",     "Blindagem densa como as pressões do fundo do mar.",                20, 210),
    Amuletos_Defesa("Amuleto do Caos",       "Proteção forjada no próprio caos.",                                22, 260),
    Amuletos_Defesa("Amuleto do Vazio",      "Blindagem absoluta do abismo.",                                    26, 400),
    Amuletos_Defesa("Amuleto da Eternidade", "Nada o corrói, nada o quebra, nada o atravessa.",                  30, 600),
]

# ---- Exclusivos (chave = nome legível da vila) ----
amuletos_ataque_exclusivos = {
    "Vila do vale verde": [],
    "Porto Azul": [
        Amuletos_Ataque("[Exclusivo] Bênção do Abismo", "Amuleto raro das profundezas.", 12, 200),
    ],
    "Vila da Neve": [
        Amuletos_Ataque("[Exclusivo] Coração de Gelo", "Pulsa com o frio eterno.", 24, 350),
    ],
    "Aldeia Destruida": [
        Amuletos_Ataque("[Exclusivo] Selo do Caos",  "Energia proibida do castelo.", 42, 600),
        Amuletos_Ataque("[Exclusivo] Marca do Caos", "O último poder antes do fim.", 65, 950),
    ],
}

amuletos_defesa_exclusivos = {
    "Vila do vale verde": [],
    "Porto Azul": [
        Amuletos_Defesa("[Exclusivo] Escudo das Profundezas", "Rocha viva que protege.", 12, 200),
    ],
    "Vila da Neve": [
        Amuletos_Defesa("[Exclusivo] Manto Glacial", "Congela o impacto.", 24, 350),
    ],
    "Aldeia Destruida": [
        Amuletos_Defesa("[Exclusivo] Égide Sombria",    "Barreira do caos.", 42, 600),
        Amuletos_Defesa("[Exclusivo] Coração do Vazio", "Nada te atinge.",  65, 950),
    ],
}

mago_amuletos_mana = [
    Amuletos_Mana("Amuleto do Aprendiz Arcano", "Cristal opaco que guarda o primeiro fio de magia.",           5,  25),
    Amuletos_Mana("Amuleto da Fonte",           "Pequena nascente encantada, sempre a fluir.",                 8,  40),
    Amuletos_Mana("Amuleto do Cristal",         "Cristal puro que armazena energia mágica lentamente.",       12,  60),
    Amuletos_Mana("Amuleto do Estudioso",       "Feito para quem passa noites debruçado sobre grimórios.",    16,  85),
    Amuletos_Mana("Amuleto do Sábio",           "Runas antigas sussurram segredos ao portador.",              22, 120),
    Amuletos_Mana("Amuleto do Arcano",          "Concentra mana como um redemoinho silencioso.",              30, 175),
    Amuletos_Mana("Amuleto do Éter",            "Toca o plano invisível de onde toda magia nasce.",           40, 260),
    Amuletos_Mana("Amuleto do Infinito",        "Círculo sem fim, mana sem fim, preço sem fim.",              55, 400),
]

amuletos_mana_exclusivos = {
    "Vila do vale verde": [],
    "Porto Azul": [
        Amuletos_Mana("[Exclusivo] Pérola das Profundezas", "Pulsa com a maré e devolve mana ao portador.",       18, 220),
    ],
    "Vila da Neve": [
        Amuletos_Mana("[Exclusivo] Núcleo Glacial", "Frio eterno condensado em mana pura.",                            35, 380),
    ],
    "Aldeia Destruida": [
        Amuletos_Mana("[Exclusivo] Selo Arcano do Caos", "Mana corrompida que ainda obedece a um mestre.",       55, 650),
        Amuletos_Mana("[Exclusivo] Lágrima do Vazio",    "Vazia e infinita, dá mana em troca da alma.",         80, 1000),
    ],
}