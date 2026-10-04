import random
from lore import dialogo
texto_lobo = True
veneno = False
acabou_de_ativar = False
frase_golem = False
frase_sombra = False
frase_sombra2 = False

class Monstro:

    def __init__(self, nome, vida, ataque, ouro, xp):

        self.nome = nome
        self.vida = vida
        self.vidamax = vida
        self.ataque = ataque
        self.ouro = ouro
        self.xp = xp
        self.skill_stun = False

    def mostrar_status(self):
        print(f"============ INIMIGO ============")
        print(f"Nome: {self.nome}")
        print(f"Vida: {self.vida}/{self.vidamax}")
        print(f"Ataque: {self.ataque}")

    def atacar(self, heroi):            # Foco do heroi dento do ataque do inimigo para poder garantir que seja gerado caso atacar 2 vezes
            ataquefinal = max(1, self.ataque - heroi.defesa)
            heroi.vida -= ataquefinal
            print(f"\nO {self.nome} te ataca causando {ataquefinal} de dano")
            heroi.foco = min(100, heroi.foco + (random.randint(3, 6) + heroi.focogen * 0.07))
            input("\nPressione ENTER para continuar...\n")
        
class Inimigo(Monstro):
    def __init__(self, nome, vida, ataque, ouro, xp) : 
        super().__init__(nome, vida, ataque, ouro, xp) # Herdou os parametros de monstro
        self.defesa = 0
        self.defesa_magica = 0
        self.habilidade = None

    def usar_habilidade(self, heroi):
        pass

class Boss(Monstro):        # EXCLUSIVO DOS BOSSES POR HORA , defesa magica e defesa(ataque)
    def __init__(self, nome, vida, ataque, ouro, xp, habilidade, defesa) : 
        super().__init__(nome, vida, ataque, ouro, xp) 
        self.habilidade = habilidade
        self.defesa = defesa
        self.defesa_magica = 0
        self.habilidade_usada = False
        self.skill_stun = False

    def mostrar_status(self):
        print("============ INIMIGO ============")
        print(f"Nome: {self.nome}")
        print(f"Vida: {self.vida}/{self.vidamax}")
        print(f"Ataque: {self.ataque}")

    def atacar(self, heroi):
            ataquefinal = max(1, self.ataque - heroi.defesa)            # Foco do heroi dento do ataque do inimigo para poder garantir que seja gerado caso atacar 2 vezes
            heroi.vida -= ataquefinal
            print(f"\nO {self.nome} te ataca causando {ataquefinal} de dano")
            heroi.foco = min(100, heroi.foco + (random.randint(10, 14) + heroi.focogen * 1.02))
            input("\nPressione ENTER para continuar...")
    
    def usar_habilidade(self, heroi):
        if self.habilidade_usada == False:
            self.habilidade(heroi,self)

def slime_absorção(heroi, boss):
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.50:
        cura = random.randint(99, 110)
        boss.vida = min(boss.vidamax, boss.vida + cura)
        print("O Rei Slime absorveu a massa de outros slimes ao redor de si!")
        print(f"Rei Slime recuperou {cura} de HP!")
        input("\nPressione ENTER para continuar...")
        boss.habilidade_usada = True

def frenesi_lobo(heroi, boss):
    global texto_lobo
    if boss.vida <= boss.vidamax * 0.60 and texto_lobo == True:
        texto_lobo = False
        print(f"O {boss.nome} entrou em frenesi, e vai atacar 2 vezes por turno agora!")
        input("\nPressione ENTER para continuar...")
    if boss.vida <= boss.vidamax * 0.60:
        print(f"\n{boss.nome} está em frenesi")
        boss.atacar(heroi)

def golem_defesa_magica(heroi, boss):
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.40:
        print("O Golem se tornou ivulnerável a magias")
        print("Mas sua defesa física caiu o tornando vulnerável!")
        boss.defesa = 0
        boss.defesa_magica += 500
        input("\nPressione ENTER para continuar...")
        boss.habilidade_usada = True

def golem_defesa(heroi, boss):
    global frase_golem
    if not frase_golem:
        print(f"O {boss.nome} parece ser muito resistente a golpes físicos!")
        print("Você terá que pensar em algum modo de causar dano!")
        frase_golem = True
        input("\nPressione ENTER para continuar...")
     
def furia_dragão(heroi, boss):
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.40: # Vida abaixo de 40%
        print("O Dragão de gelo entrou em Fúria!")
        boss.ataque = int(boss.ataque * 1.40)
        print(f"Ataque aumentou para {boss.ataque}")
        boss.habilidade_usada = True
        input("\nPressione ENTER para continuar...")

def casulo_sombrio(heroi, boss):
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.30: # Vida abaixo de 50%
        print(f"A {boss.nome} se envolveu em uma teia gigante.\nA defesa dela aumentou em +15 mas o ataque dela diminuiu em -15")
        boss.ataque -= 15
        boss.defesa += 15
        boss.habilidade_usada = True

def veneno_ancestral(heroi, boss):  # Teste de veneno 
    teste = random.randint(1, 10)
    global veneno
    if not boss.habilidade_usada and boss.vida <= boss.vidamax * 0.50:
        print("A aranha se enfureceu e seus ataques causarão veneno agora!")

    if teste >= 5 and heroi.turnos_veneno == 0 and boss.vida <= boss.vidamax * 0.50:
        heroi.turnos_veneno = 3
        print(f"{heroi.nome} foi envenenado por 3 turnos!")
        input("\nPressione ENTER para continuar...\n")
        veneno = True

    if veneno == True:
        dano = random.randint(20, 30)
        heroi.vida -= dano
        print(f"{heroi.nome} recebeu {dano} de dano do veneno...")
        input("\nPressione ENTER para continuar...\n")
        heroi.turnos_veneno -= 1
        print(f"Turnos restante até acabar veneno {heroi.turnos_veneno}")
        input("\nPressione ENTER para continuar...\n")

def tempestade_Glacial(heroi, boss):
    # Ativação
    if not boss.habilidade_usada and boss.vida <= boss.vidamax * 0.50:
        print("Ymir usou TEMPESTADE GLACIAL.")
        print("Ymir congela o campo de batalha.")
        input("\nPressione ENTER para continuar...\n")
        print("Ele irá te congelar de 3 em 3 turnos, causando dano e te deixando paralisado por 1 turno...")
        input("\nPressione ENTER para continuar...\n")
        heroi.contador_gelo = 3   # 3 turnos até o stun
        boss.habilidade_usada = True
        boss.skill_stun = True
        return

    if not boss.skill_stun:
        return

    # Turno do stun
    if heroi.contador_gelo == 0:
        dano = random.randint(10, 24)
        heroi.vida -= dano
        heroi.turnos_stun = 1
        heroi.contador_gelo = 3   # reinicia o ciclo
        print(f"{heroi.nome} recebeu {dano} e ficou paralisado devido ao frio...")
        input("\nPressione ENTER para continuar...\n")
        return

    # Contagem regressiva
    heroi.contador_gelo -= 1

def eco_dos_mortos(heroi, boss):    # Termnar habilidade boss
    global acabou_de_ativar
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.50:
        dialogo(f"\n{boss.nome}: Interessante...\nHá séculos ninguém era capaz de me ferir.")
        input("\nPressione ENTER para continuar...\n")
        dialogo(f"\n{boss.nome}: Mas isso não muda nada! O mundo continuará apodrecendo!\n")
        print("Os espíritos invocados irão te atacar de 3 em 3 turnos causando dano adicional de 10% do dano recebido e paralisado por 1 turno.")
        input("\nPressione ENTER para continuar...\n")
        heroi.contador_gelo = 4
        boss.habilidade_usada = True

    if heroi.contador_gelo == 0:
        print("\nOs espiritos invocados atacam!")
        dano = boss.ataque * 0.10
        heroi.vida -= dano
        heroi.turnos_stun += 1
        heroi.contador_gelo  = 4
        print(f"Você recebeu {dano} de dano dos espiritos e ficou paralisando")
        acabou_de_ativar = True
        
    if heroi.contador_gelo > 0 and acabou_de_ativar == False:      # Abaixo de 3* turnos, sem stun e sem dano
        heroi.turnos_stun = 0
        heroi.contador_gelo  -= 1

    acabou_de_ativar = False

def lamento_final(heroi, boss): 
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.30:
        print(f"\n{boss.nome}: Você não é nada")
        print(f"{boss.nome} usou Lamento Final .")
        cura = boss.vidamax * 0.40
        boss.vida = cura
        print(f"\n{boss.nome} teve a vida recuperada em {cura}")
        boss.ataque += 30
        print(f"\n{boss.nome} teve o ataque aumentado em 30")
        input("\nPressione ENTER para continuar...\n")

def ultima_resistencia(heroi, boss): 
    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.30:
        print(f"\n{boss.nome}: Não!\nEu me recuso a desaparecer!\nSe o mundo deseja o caos...\nEntão eu me tornarei o próprio caos!")
        print(f"{boss.nome} usou ULTIMA RESISTENCIA.")
        cura = boss.vidamax * 0.20
        boss.vida = cura
        print(f"\n{boss.nome} teve a vida recuperada em {cura}")
        input("\nPressione ENTER para continuar...\n")
    "Recebe uma cura de emergência de 20% do HP total e dobra seu ataque"

def copia_magias(heroi, boss):
    
    magia = random.randint(1,10)
    if magia >= 7:  # Chance de 40 % de não usar magia
        print(f"\n{boss.nome} está carregando ataque mágico.")
        input("\nPressione ENTER para continuar...")
        return

    if magia >= 5:
        print(f"\n{boss.nome} usou magia BOLA DE FOGO")
        input("\nPressione ENTER para continuar...")
        heroi.vida -= 75
        print("\nVocê recebeu 75 de dano!")
        input("\nPressione ENTER para continuar...")

        return

    elif magia >= 3:
        print(f"\n{boss.nome} usou magia RELAMPAGO ARCANO")
        input("\nPressione ENTER para continuar...")
        heroi.vida -= 115
        print("\nVocê recebeu 115 de dano!")
        input("\nPressione ENTER para continuar...")

        return

    elif magia >= 1:
        print(f"\n{boss.nome} usou magia COMETA SOMBRIO")
        input("\nPressione ENTER para continuar...")
        heroi.vida -= 160
        print("\nVocê recebeu 160 de dano!")
        input("\nPressione ENTER para continuar...")

        return
    
def execuçao_sombria(heroi, boss):
    global frase_sombra, frase_sombra2

    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.65 and not frase_sombra:
        dialogo(f"{boss.nome}: Você acha que chegou até aqui por mérito próprio?")
        print(f"\n[ALERTA] {boss.nome} está carregando sua fúria!")
        input("\nPressione ENTER para continuar...")
        frase_sombra = True

    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.55 and not frase_sombra2:
        dialogo(f"{boss.nome}: Diga-me...\nQuantos monstros você matou para ser chamado de herói?")
        print(f"\n[ALERTA] {boss.nome} está com sua fúria completa!")
        print("\n[ALERTA][CUIDADO] Um golpe muito forte está para vir!")
        input("\nPressione ENTER para continuar...")
        frase_sombra2 = True

    if boss.habilidade_usada == False and boss.vida <= boss.vidamax * 0.40:
        print(f"\n{boss.nome} usou Habilidade EXECUÇÃO SOMBRIA")
        input("\nPressione ENTER para continuar...")
        dano = max(1, heroi.defesa - 225) 
        heroi.vida -= dano
        print("\nVocê recebeu 225 de dano!")
        input("\nPressione ENTER para continuar...")
        boss.habilidade_usada = True
  

# ============================================================
# ZONA 1 — FLORESTA (Nv 1-4)
# ============================================================
inimigos_floresta = [
    # nome, vida, ataque, xp, ouro
    Inimigo("Goblin",         random.randint(85, 100),  random.randint(15, 19), random.randint(24, 32),  random.randint(16, 24)),
    Inimigo("Slime",          random.randint(95, 115),  random.randint(13, 17), random.randint(20, 28),  random.randint(14, 20)),
    Inimigo("Aranha Gigante", random.randint(90, 110),  random.randint(17, 21), random.randint(28, 36),  random.randint(20, 28)),
    Inimigo("Lobo Selvagem",  random.randint(105, 125), random.randint(19, 23), random.randint(32, 42),  random.randint(22, 30)),
    Inimigo("Urso Ancião",    random.randint(150, 180), random.randint(24, 28), random.randint(50, 65),  random.randint(35, 48)),
]

boss_floresta = [
    Boss("Rei Slime",
         random.randint(370, 380),
         random.randint(40, 50),
         random.randint(70, 80),
         random.randint(50, 60),
         [slime_absorção],
         defesa=0),

    Boss("Lobo Superior",
         random.randint(460, 470),
         random.randint(48, 56),
         random.randint(70, 80),
         random.randint(45, 55),
         [frenesi_lobo],
         defesa=0),
]


# ============================================================
# ZONA 2 — CAVERNA (Nv 5-9)
# ============================================================
inimigos_caverna = [
    Inimigo("Rato das Profundezas", random.randint(190, 230), random.randint(30, 36), random.randint(65, 85),  random.randint(45, 60)),
    Inimigo("Besouro Blindado",     random.randint(240, 290), random.randint(34, 42), random.randint(80, 100), random.randint(55, 72)),
    Inimigo("Slime de Pedra",       random.randint(215, 260), random.randint(32, 38), random.randint(72, 92), random.randint(50, 66)),
    Inimigo("Escorpião Gigante",    random.randint(225, 275), random.randint(38, 46), random.randint(85, 108), random.randint(60, 78)),
    Inimigo("Orc",                  random.randint(290, 350), random.randint(42, 52), random.randint(105, 135), random.randint(75, 95)),
]

boss_caverna = [
    Boss("Golem Ancestral",
         random.randint(560, 570),
         random.randint(72, 82),
         random.randint(150, 160),
         random.randint(110, 120),
         [golem_defesa, golem_defesa_magica],
         defesa=80),

    Boss("Aranha Rainha das Profundezas",
         random.randint(69, 700),
         random.randint(92, 102),
         random.randint(160, 170),
         random.randint(120, 130),
         [casulo_sombrio, veneno_ancestral],
         defesa=0),
]


# ============================================================
# ZONA 3 — MONTANHAS GELADAS (Nv 10-14)
# ============================================================
inimigos_montanhasgeladas = [
    Inimigo("Águia Gigante",    random.randint(340, 410), random.randint(56, 68), random.randint(130, 165), random.randint(100, 130)),
    Inimigo("Espírito do Gelo", random.randint(370, 450), random.randint(62, 76), random.randint(145, 185), random.randint(115, 150)),
    Inimigo("Slime de Gelo",    random.randint(420, 510), random.randint(60, 74), random.randint(165, 205), random.randint(130, 170)),
    Inimigo("Líder Goblin",     random.randint(470, 580), random.randint(70, 86), random.randint(185, 235), random.randint(150, 195)),
    Inimigo("Líder Orc",        random.randint(540, 660), random.randint(80, 98), random.randint(215, 270), random.randint(175, 230)),
]

boss_montanhasgeladas = [
    Boss("Dragão de Gelo",
         random.randint(800, 880),
         random.randint(140, 150),
         random.randint(290, 300),
         random.randint(240, 250),
         [furia_dragão],
         defesa=0),

    Boss("Ymir, o Gigante de Gelo",
         random.randint(1220, 1230),
         random.randint(158, 168),
         random.randint(300, 310),
         random.randint(250, 260),
         [tempestade_Glacial],
         defesa=0),
]


# ============================================================
# ZONA 4 — CASTELO DO CAOS (Nv 15-20)
# ============================================================
inimigos_castelo = [
    Inimigo("Espectro do Castelo",  random.randint(430, 530), random.randint(92, 112), random.randint(230, 290), random.randint(190, 240)),
    Inimigo("Bruxo do Caos",        random.randint(455, 560), random.randint(100, 120), random.randint(245, 305), random.randint(200, 255)),
    Inimigo("Cavaleiro Corrompido", random.randint(500, 620), random.randint(85, 105),  random.randint(260, 320), random.randint(215, 270)),
    Inimigo("Executor das Ruínas",  random.randint(630, 770), random.randint(108, 132), random.randint(310, 380), random.randint(255, 325)),
    Inimigo("Guardião do Caos",     random.randint(700, 850), random.randint(120, 148), random.randint(360, 445), random.randint(295, 375)),
]

boss_castelo_do_caos = [
    Boss(
        "Rei do Caos",
        random.randint(1600, 1700),
        random.randint(220, 240),
        random.randint(550, 560),
        random.randint(270, 280),
        [ultima_resistencia],
        defesa=0
    ),
    Boss(
        "???",                       # boss especial (raid)
        random.randint(1900, 2250),
        random.randint(175, 210),
        random.randint(1500, 1900),
        random.randint(1300, 1700),
        [execuçao_sombria, copia_magias],
        defesa=0
    ),
]


# ============================================================
# ZONA 5 — ABISMO (Nv 20+)
# ============================================================
boss_abismo = [
    Boss(
        "Ultimo Rei",
        random.randint(3000, 3100),
        random.randint(260, 310),
        random.randint(4000, 5000),
        random.randint(3500, 4500),
        [lamento_final, eco_dos_mortos],
        defesa=0
    ),
]


# ============================================================
# EXTRAS
# ============================================================
Bandido = [
    Inimigo("Bandido",
            random.randint(38, 48),
            random.randint(32, 38),
            random.randint(22, 32),
            random.randint(22, 30))
]

boss_yeti = Boss(
    "Ymir, o Gigante de Gelo",
    random.randint(1680, 1920),
    random.randint(125, 148),
    random.randint(950, 1200),
    random.randint(850, 1100),
    [tempestade_Glacial],
    defesa=0
)