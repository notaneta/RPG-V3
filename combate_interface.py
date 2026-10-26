"""Tela de combate do RPG V3 (customtkinter).

Fluxo:
    1. criar_tela_combate(frame)       -> monta os widgets (uma vez, na abertura)
    2. iniciar_combate(heroi, inimigo) -> preenche a tela com os dados (a cada combate)
    3. os botões chamam atacar(), abrir_magias(), etc.
"""
import random
from copy import deepcopy
from magias import listamagias, executar_magia
from habilidades import listahabilidades, executar_skill
import customtkinter as ctk


# ============================================================
# CONFIGURAÇÕES
# ============================================================
FONTE = ("Impact", 14)
POSICAO_PAINEL = dict(row=7, column=2, sticky="se", padx=20, pady=20)

# Cores das barras (cada cor mora em um lugar só)
COR_HP = "green"
COR_MP = "blue"
COR_FURIA = "orange"
COR_INIMIGO = "red"


# ============================================================
# ESTADO DO COMBATE
# ============================================================
jogador = None
inimigo = None

# Widgets: são criados em criar_tela_combate, mas ficam declarados aqui
# para as outras funções do arquivo poderem usar.
hp_heroi = hp_heroi_numero = None
hp_heroi_nome = hp_heroi = hp_heroi_numero = None
mp_heroi = mp_heroi_numero = None
furia_heroi = furia_heroi_numero = None
inimigo_nome = hp_inimigo = hp_inimigo_numero = None
historico = None
painel_botoes = painel_magias = None

## Listas de botões
botoes_magias = []
botao_skills = []
botoes_itens = []
lista_de_botoes = []   # botões de ação (para bloquear/liberar de uma vez)


# ============================================================
# INÍCIO DO COMBATE
# ============================================================
def iniciar_combate(heroi_recebido, inimigo_recebido):
    global jogador, inimigo
    jogador = heroi_recebido
    inimigo = deepcopy(inimigo_recebido)  # cópia, para não alterar o inimigo original

    criar_magia()
    criar_skill()
    criar_itens()

    limpar_historico()
    atualizar_tela()
    liberar_botoes()



# ============================================================
# ATUALIZAÇÃO DA TELA
# ============================================================
def atualizar_tela():
    # Herói também acrescentado agora vida max até 0, não fica negativa e além disso tem nome do jogador na tela
    hp_heroi_nome.configure(text=f"HP de {jogador.nome}")
    atualizar_barra(hp_heroi, jogador.vida, jogador.vidamax, COR_HP)
    hp_heroi_numero.configure(text=f"{max(0, int(jogador.vida))}/{jogador.vidamax}")
    atualizar_barra(mp_heroi, jogador.mana, jogador.manamax, COR_MP)
    mp_heroi_numero.configure(text=f"{max(0, int(jogador.mana))}/{jogador.manamax}")
    atualizar_barra(furia_heroi, jogador.foco, jogador.focomax, COR_FURIA)
    furia_heroi_numero.configure(text=f"{max(0, int(jogador.foco))}/{jogador.focomax}")

    # Inimigo (max(0, ...) evita vida negativa na tela)
    inimigo_nome.configure(text=inimigo.nome)
    atualizar_barra(hp_inimigo, inimigo.vida, inimigo.vidamax, COR_INIMIGO)
    hp_inimigo_numero.configure(text=f"{max(0, int(inimigo.vida))}/{inimigo.vidamax}")

def escrever_historico(mensagem):
    historico.configure(state="normal")   # libera para escrita
    historico.insert("end", "\n" + mensagem)
    historico.configure(state="disabled")  # trava de novo
    historico.see("end")


def limpar_historico():
    historico.configure(state="normal")
    historico.delete("0.0", "end")
    historico.insert("0.0", "Combate Iniciado!")
    historico.configure(state="disabled")


def bloquear_botoes():
    for botao in lista_de_botoes:
        botao.configure(state="disabled")


def liberar_botoes():
    for botao in lista_de_botoes:
        botao.configure(state="normal")

def verificar_fim(): # Verifica condições, se GAME OVER, ou recompensas
    global botao_continuar
    if jogador.vida <= 0:
        escrever_historico("Jogador Derrotado!")
        escrever_historico("GAME OVER")
        bloquear_botoes()
        botao_continuar = ctk.CTkButton(painel, text="continuar", command=fim_combate, font=FONTE)
        botao_continuar.grid(row=4, column=0, sticky="ew", pady=5)
        return True


    if inimigo.vida <= 0:

        jogador.ouro += inimigo.ouro
        jogador.xp += inimigo.xp

        escrever_historico("Inimigo Derrotado!")
        bloquear_botoes()
        botao_continuar = ctk.CTkButton(painel, text="Continuar", command=fim_combate)
        botao_continuar.grid(row=4, column=0, sticky="ew", pady=5)
        historico.configure(state="normal")  # libera para escrita
        historico.insert("end", "\n" + f"Você recebeu {inimigo.ouro} de ouro e {inimigo.xp} de XP!")
        historico.insert("end", "\n" + f"Seu ouro atual: {jogador.ouro}")

        historico.configure(state="disabled")  # trava de novo
        historico.see("end")

        calculo_combate = jogador.subirnivel()
        for item in calculo_combate:
            escrever_historico(item)

        escrever_historico(f"Seu XP: {jogador.xp} / {jogador.xplevel}")

        return True

def fim_combate():
    if inimigo.vida <= 0:
        botao_continuar.grid_forget()
        from menu_interface import mostrar_tela
        mostrar_tela("area")

    if jogador.vida <= 0:
        from menu_interface import  janela
        janela.destroy()  # Fecha janela Ao morrer

# ============================================================
# AÇÕES DO JOGADOR
# ============================================================
def atacar():
    dano = jogador.atacar_calculo(inimigo)  # tira a vida do inimigo e devolve o dano
    escrever_historico(f"Dano causado ao inimigo: {dano}")

    finalizar_acao_heroi()


def lancar_magia(magia):
    dano = executar_magia(jogador, inimigo, magia)
    if dano is None:
        escrever_historico("MP Insuficiente para a magia!")
        voltar()
        return
    else:
        escrever_historico(f"Você usou {magia.nome}!")
        escrever_historico(f"Dano causado ao inimigo: {dano}")

        finalizar_acao_heroi()


def lancar_skill(skill):
    dano = executar_skill(jogador, inimigo, skill)
    if dano is None:
        escrever_historico("Fúria Insuficiente para a habilidade!")
        voltar()
        return
    else:
        escrever_historico(f"Você usou {skill.nome}!")
        escrever_historico(f"Dano causado ao inimigo: {dano}")

        finalizar_acao_heroi()

def usar_item(item):
    from itens import executar_item
    resultado = executar_item(jogador, item)
    if item.tipo == "revive":
        escrever_historico(resultado)
        voltar()
    if item.tipo == "vida":
        escrever_historico(resultado)
    if item.tipo == "mana":
        escrever_historico(resultado)


def finalizar_acao_heroi():
    bloquear_botoes()
    atualizar_tela()
    voltar()
    if verificar_fim(): return
    historico.after(280, turno_inimigo) # Tempo para iniciar turno do inimigo


# ============================================================
# TURNO DO INIMIGO
# ============================================================
def turno_inimigo():
    # Provisório: o inimigo.atacar() original tem input() e congelaria a janela.
    # Melhorar a IA depois (sortear entre ataque e habilidade).
    dano = inimigo.atacar_calculo(jogador)
    escrever_historico(f"{inimigo.nome} causou {dano} de dano em você")
    atualizar_tela()
    liberar_botoes()
    if verificar_fim():
        return

# ============================================================
# TROCA DE PAINÉIS (AÇÕES <-> MAGIAS / SKILLS / ITENS)
# ============================================================
def abrir_magias():
    painel_botoes.grid_forget()
    painel_magias.grid(**POSICAO_PAINEL)

def abrir_skills():
    painel_botoes.grid_forget()
    painel_skills.grid(**POSICAO_PAINEL)

def abrir_itens():
    if botoes_itens == []:
        escrever_historico("Você não tem nenhum item!")
        return
    else:
        painel_botoes.grid_forget()
        painel_itens.grid(**POSICAO_PAINEL)


def voltar():
    painel_magias.grid_forget()
    painel_skills.grid_forget()
    painel_itens.grid_forget()
    painel_botoes.grid(**POSICAO_PAINEL)

# ============================================================
# CONSTRUÇÃO DA TELA (roda uma vez, na abertura do programa)
# ============================================================
def criar_tela_combate(tela_combate):  # recebe o frame, não cria janela
    tela_combate.grid_columnconfigure(2, weight=1)  # coluna elástica
    tela_combate.grid_rowconfigure(6, weight=1)     # linha elástica

    criar_lado_heroi(tela_combate)
    criar_lado_inimigo(tela_combate)
    criar_botoes(tela_combate)

def criar_barra(tela, nome, cor, linha):
    """Cria rótulo + barra + número. Devolve (rótulo, barra, numero)."""
    rotulo = ctk.CTkLabel(tela, text=nome, font=FONTE)
    barra = ctk.CTkProgressBar(tela, width=490, height=20, progress_color=cor)
    numero = ctk.CTkLabel(tela, text="", font=FONTE)
    barra.set(0)

    rotulo.grid(row=linha, column=0, sticky="nw", padx=5, pady=5)
    barra.grid(row=linha + 1, column=0, sticky="nw", padx=5, pady=5)
    numero.grid(row=linha + 1, column=1, sticky="nw", padx=0, pady=5)
    return rotulo, barra, numero

def atualizar_barra(barra, atual, maximo, cor):
    """Atualiza a barra. Com valor 0, pinta o preenchimento com a cor do fundo
    para sumir a ponta arredondada que o CTkProgressBar deixa na tela."""
    barra.set(max(0, atual) / maximo)
    if atual <= 0:
        barra.configure(progress_color=barra.cget("fg_color"))
    else:
        barra.configure(progress_color=cor)


def criar_lado_heroi(tela):
    global hp_heroi_nome, hp_heroi, hp_heroi_numero
    global mp_heroi, mp_heroi_numero
    global furia_heroi, furia_heroi_numero

# O _ é a convenção do Python para “recebi esse valor, mas não vou usar”. O MP e a Fúria não precisam mudar de texto, então jogam o rótulo fora.
    hp_heroi_nome, hp_heroi, hp_heroi_numero = criar_barra(tela, "HP", COR_HP, linha=0)
    _, mp_heroi, mp_heroi_numero = criar_barra(tela, "MP", COR_MP, linha=2)
    _, furia_heroi, furia_heroi_numero = criar_barra(tela, "Fúria", COR_FURIA, linha=4)


def criar_lado_inimigo(tela):
    global inimigo_nome, hp_inimigo, hp_inimigo_numero, historico, painel

    painel = ctk.CTkFrame(tela, fg_color="transparent")
    painel.grid(row=0, column=2, rowspan=6, sticky="ne", padx=20, pady=5)
    painel.grid_columnconfigure(0, weight=1)

    inimigo_nome = ctk.CTkLabel(painel, text="", font=FONTE)
    hp_inimigo = ctk.CTkProgressBar(painel, width=490, height=20, progress_color=COR_INIMIGO)
    hp_inimigo_numero = ctk.CTkLabel(painel, text="", font=FONTE)
    historico = ctk.CTkTextbox(painel, height=200)

    hp_inimigo.set(0)
    historico.configure(state="disabled")  # somente leitura

    inimigo_nome.grid(row=0, column=0, sticky="e", pady=5)
    hp_inimigo.grid(row=1, column=0, sticky="e", pady=5)
    hp_inimigo_numero.grid(row=2, column=0, sticky="e", pady=5)
    historico.grid(row=3, column=0, sticky="ew", pady=5)


def criar_botoes(tela):
    global painel_botoes, painel_magias, painel_skills, painel_itens

    painel_botoes = ctk.CTkFrame(tela, fg_color="transparent")
    painel_magias = ctk.CTkFrame(tela, fg_color="transparent")
    painel_skills = ctk.CTkFrame(tela, fg_color="transparent")
    painel_itens = ctk.CTkFrame(tela, fg_color="transparent")
    painel_botoes.grid(**POSICAO_PAINEL)  # o painel de magias começa escondido

    # Botões de ação: (texto, função). None = ainda sem ação.
    acoes = [
        ("Atacar", atacar),
        ("Mágias", abrir_magias),
        ("Habilidades", abrir_skills),
        ("Itens", abrir_itens),
    ]

    lista_de_botoes.clear()
    for linha, (texto, comando) in enumerate(acoes):
        botao = ctk.CTkButton(painel_botoes, text=texto, command=comando)
        botao.grid(row=linha, column=0, sticky="e", pady=5)
        lista_de_botoes.append(botao)


def criar_magia():
    for b in botoes_magias:
        b.destroy()
    botoes_magias.clear()

    for linha, magia in enumerate(jogador.magiasaprendidas):
        botao = ctk.CTkButton(painel_magias, text=magia.nome, command=lambda m=magia: lancar_magia(m))
        botao.grid(row=linha, column=0, sticky="nw", padx=5, pady=5)

    botao_voltar = ctk.CTkButton(painel_magias, text="Voltar", command=voltar)
    botao_voltar.grid(row=len(jogador.magiasaprendidas), column=0, sticky="nw", padx=5, pady=5)
    botoes_magias.append(botao_voltar)


def criar_skill():
    for b in botao_skills:
        b.destroy()
    botao_skills.clear()

    for linha, skill in enumerate(jogador.habilidadesaprendidas):
        botao = ctk.CTkButton(painel_skills, text=skill.nome, command=lambda m=skill: lancar_skill(m))
        botao.grid(row=linha, column=0, sticky="nw", padx=5, pady=5)

    botao_voltar = ctk.CTkButton(painel_skills, text="Voltar", command=voltar)
    botao_voltar.grid(row=len(jogador.habilidadesaprendidas), column=0, sticky="nw", padx=5, pady=5)
    botao_skills.append(botao_voltar)


def criar_itens():
    for b in botoes_itens:
        b.destroy()
    botoes_itens.clear()

    for linha, item in enumerate(jogador.inventario):
        botao = ctk.CTkButton(painel_skills, text=item.nome, command=lambda m=item: usar_item(m))
        botao.grid(row=linha, column=0, sticky="nw", padx=5, pady=5)

    botao_voltar = ctk.CTkButton(painel_itens, text="Voltar", command=voltar)
    botao_voltar.grid(row=len(jogador.inventario), column=0, sticky="nw", padx=5, pady=5)
    botao_skills.append(botao_voltar)