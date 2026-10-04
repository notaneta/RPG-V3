from util import limpar_tela
from habilidades import listahabilidades
from copy import deepcopy

class Personagem:

    def __init__(self, nome, vida, ataque, defesa, mana, ouro, nivel, xp, xplevel, foco):

        self.nome = nome
        self.vida = vida
        self.vidamax = vida
        self.ataque = ataque
        self.defesa = defesa
        self.mana = mana
        self.manamax = mana
        self.ouro = ouro
        self.nivel = nivel
        self.xp = xp
        self.xplevel = xplevel
        self.foco = foco
        self.focomax = 100
        self.focogen = 0.02        # Gerador de furia aumenta conforme derrota chefes ou eventos rolam, ou até mesmo lugar para aumentar
        # O inventário vazio, é uma lista de objetos
        self.inventario = []
        self.magiasaprendidas = []
        self.habilidadesaprendidas=[listahabilidades[0]]
        self.turnos_veneno = 0
        self.contador_gelo = 0
        self.turnos_stun = 0

    def mostrar_status(self):
        print(f"============ {self.nome.upper()} ============")
        print(f"Vida: {int(self.vida)}/{self.vidamax}   Mana: {int(self.mana)}/{self.manamax}")
        print(f"Ataque: {self.ataque}      Defesa: {self.defesa}")
        print(f"Ouro: {self.ouro}        Nível: {self.nivel}")    

    def subirnivel(self, listahabilidades, listamagias): 
        from habilidades import listahabilidades
        from magias import listamagias
        while self.xp >= self.xplevel:
            self.vidamax = int(self.vidamax * 1.06)
            self.vida = min(self.vidamax, self.vida + self.vidamax * 0.50)      # Recupera vida 40% ao subir de level
            self.manamax = int(self.manamax * 1.10)
            self.mana += min(self.manamax, self.mana + self.manamax * 0.50)      # Recupera mana 40% ao subir de level
            self.ataque = int(self.ataque * 1.07)
            self.defesa += 1
            self.xp -= self.xplevel
            self.nivel += 1
            self.xplevel = int(self.xplevel * 1.30)

            limpar_tela()
            print(f"\nParabéns você subiu para o nivel {self.nivel}!")
            print(f"Você teve seu HP e MP restaurado em 40%")
            input("\nPressione ENTER para continuar...")
            for skill in listahabilidades:
                if skill.requisito <= self.nivel and skill not in self.habilidadesaprendidas:   # Para cada SKILL que o requisito estiver acima ou igual o nivel do heroi, adicionar ela para o heroi
                    self.aprenderhabilidade(skill)        
                    input("\nPressione ENTER para continuar...\n")
            for magia in listamagias:
                if magia.requisito <= self.nivel and magia not in self.magiasaprendidas:  # Além disso verifica se a magia ou skill já não foi aprendida, para evitar duplicidade
                    self.aprendermagia(magia)
                    input("\nPressione ENTER para continuar...\n")
                                
            self.mostrar_status()
            input("\nPressione ENTER para continuar...")
        
    def adicionar_pocoes(self, novo_item):
        for item in self.inventario:
            if item.nome == novo_item.nome:
                item.quantidade += novo_item.quantidade
                print(f"O item {novo_item.nome} foi adicionado no seu inventário.")
                return
        self.inventario.append(deepcopy(novo_item))
        print(f"\nNovo item obtido: {novo_item.nome}!")


    def removeritem(self, item_removido):
        for item in self.inventario:
            if item is item_removido:
                item.quantidade -= 1
                if item.quantidade <= 0:
                    self.inventario.remove(item)
                return

    def equipar_ataque(self, amuleto):
        self.amuleto_ataque = amuleto
        print(f"{amuleto.nome} equipado (Ataque +{amuleto.dano}).")

    def equipar_defesa(self, amuleto):
        self.amuleto_defesa = amuleto
        print(f"{amuleto.nome} equipado (Defesa +{amuleto.defesa}).")

    def mostrar_inventario_pocoes(self):   
        """Exibe todos os itens que o personagem possui."""
        print(f"\n========== INVENTÁRIO DE {self.nome.upper()} ==========")
        if not self.inventario:
            print("Seu inventário está vazio.")
            print("==========================================")
            return
        for i, item in enumerate(self.inventario, start=1):
            print(
                f"{i} - {item.nome:<18} | Qtd: x{item.quantidade:<2} | Cura: {item.cura}")

        print("==========================================")

    def aprendermagia(self, nova_magia):
        self.magiasaprendidas.append(nova_magia)
        print(f"\nNova Magia aprendida: {nova_magia.nome}!")

    def mostrarmagias(self):   
        """Exibe todas as magias que o personagem possui."""
        print(f"\n========== MAGIAS DE {self.nome.upper()} ==========")
        if not self.magiasaprendidas:
            print("Você não tem nenhuma magia.")
            print("==========================================")
            return
        for i, magia in enumerate(self.magiasaprendidas, start=1):
            print(
                f"{i} - {magia.nome:<18} | Dano: {magia.dano:<2} | MP {magia.custo}")

        print("==========================================")

    def aprenderhabilidade(self, nova_habilidade):
        self.habilidadesaprendidas.append(nova_habilidade)
        print(f"\nNova Habilidade Aprendida: {nova_habilidade.nome}!")

    def mostrarSkill(self):   
        """Exibe todas as habilidade que o personagem possui."""
        print(f"\n========== HABILIDADES DE {self.nome.upper()} ==========")
        if not self.habilidadesaprendidas:
            print("Você não tem nenhuma habilidade.")
            print("==========================================")
            return
        for i, skill in enumerate(self.habilidadesaprendidas, start=1):
            print(
                f"{i} - {skill.nome:<18} | Dano: {skill.dano:<2} | Fúria: {skill.custo}")

        print("==========================================")

    def atacar(self, inimigo):
        ataquefinal = max(1, self.ataque - inimigo.defesa)
        inimigo.vida -= ataquefinal
        print(f"\nVoce ataca o {inimigo.nome} com sua espada e causa {ataquefinal} de dano.")
        input("\nPressione ENTER para continuar...")
    

class Heroi(Personagem):
    def __init__(self, nome):   #  nome, vida 180, ataque 13, defesa 7, mana 30, ouro 30, nivel 1, xp 0, xplevel 40 , foco 0):
        super().__init__(nome, 170, 13, 7, 30, 30, 1, 0, 40, 0) # Herdou os parametros de personagem / Aqui já configuro os status inicias também
        from vilas import vila_inicial
        self.vila_atual = vila_inicial
        import mundo  
        self.zona_atual = mundo.zona1_floresta

