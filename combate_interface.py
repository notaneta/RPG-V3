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


# ============================================================
# ESTADO DO COMBATE
# ============================================================
jogador = None
inimigo = None
botoes_magias = []
botao_skills = []
lista_de_botoes = []   # botões de ação (para bloquear/liberar de uma vez)

# Widgets: são criados em criar_tela_combate, mas ficam declarados aqui
# para as outras funções do arquivo poderem usar.
hp_heroi = hp_heroi_numero = None
hp_heroi_nome = hp_heroi = hp_heroi_numero = None
mp_heroi = mp_heroi_numero = None
furia_heroi = furia_heroi_numero = None
inimigo_nome = hp_inimigo = hp_inimigo_numero = None
historico = None
painel_botoes = painel_magias = None

# ============================================================
# INÍCIO DO COMBATE
# ============================================================
def iniciar_combate(heroi_recebido, inimigo_recebido):
    global jogador, inimigo
    jogador = heroi_recebido
    inimigo = deepcopy(inimigo_recebido)  # cópia, para não alterar o inimigo original

    criar_magia()
    criar_skill()

    limpar_historico()
    atualizar_tela()
    liberar_botoes()



# ============================================================
# ATUALIZAÇÃO DA TELA
# ============================================================
def atualizar_tela():
    # Herói também acrescentado agora vida max até 0, não fica negativa e além disso tem nome do jogador na tela
    hp_heroi_nome.configure(text=f"HP de {jogador.nome}")
    hp_heroi.set(max(0, jogador.vida) / jogador.vidamax)
    hp_heroi_numero.configure(text=f"{max(0, int(jogador.vida))}/{jogador.vidamax}")
    mp_heroi.set(jogador.mana / jogador.manamax)
    mp_heroi_numero.configure(text=f"{int(jogador.mana)}/{jogador.manamax}")
    furia_heroi.set(jogador.foco / jogador.focomax)
    furia_heroi_numero.configure(text=f"{int(jogador.foco)}/{jogador.focomax}")

    # Inimigo (max(0, ...) evita vida negativa na tela)
    inimigo_nome.configure(text=inimigo.nome)
    hp_inimigo.set(max(0, inimigo.vida) / inimigo.vidamax)
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
        from menu_interface import telas, mostrar_tela
        mostrar_tela("vila")

    if jogador.vida <= 0:
        from menu_interface import  janela
        janela.destroy()  # Fecha janela Ao morrer

# ============================================================
# AÇÕES DO JOGADOR
# ============================================================
def atacar():
    bloquear_botoes()  # evita clicar de novo durante o turno do inimigo
    dano = jogador.atacar_calculo(inimigo)  # tira a vida do inimigo e devolve o dano
    escrever_historico(f"Dano causado ao inimigo: {dano}")
    atualizar_tela()
    if verificar_fim():    # Verifica primeiro se inimigo tem vida para continuar combate
        return
    historico.after(0, turno_inimigo)  # sem parênteses: agenda para daqui 1 s  colocar dps dnv 800


def lancar_magia(magia):
    dano = executar_magia(jogador, inimigo, magia)
    if dano is None:
        escrever_historico("MP Insuficiente para a magia!")
        return
    else:
        escrever_historico(f"Você usou {magia.nome}!")
        escrever_historico(f"Dano causado ao inimigo: {dano}")
        atualizar_tela()
        voltar()
        bloquear_botoes()
        verificar_fim()
        turno_inimigo()


def lancar_skill(skill):
    dano = executar_skill(jogador, inimigo, skill)
    if dano is None:
        escrever_historico("MP Insuficiente para a magia!")
        return
    else:
        escrever_historico(f"Você usou {skill.nome}!")
        escrever_historico(f"Dano causado ao inimigo: {dano}")
        atualizar_tela()
        voltar_skills()
        bloquear_botoes()
        verificar_fim()
        turno_inimigo()


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
# TROCA DE PAINÉIS (AÇÕES <-> MAGIAS)
# ============================================================
def abrir_magias():
    painel_botoes.grid_forget()
    painel_magias.grid(**POSICAO_PAINEL)


def voltar():
    painel_magias.grid_forget()
    painel_botoes.grid(**POSICAO_PAINEL)

def abrir_skills():
    painel_botoes.grid_forget()
    painel_botoes.grid(**POSICAO_PAINEL)


def voltar_skills():
    painel_skills.grid_forget()
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


def criar_lado_heroi(tela):
    global hp_heroi_nome, hp_heroi, hp_heroi_numero
    global mp_heroi, mp_heroi_numero
    global furia_heroi, furia_heroi_numero

# O _ é a convenção do Python para “recebi esse valor, mas não vou usar”. O MP e a Fúria não precisam mudar de texto, então jogam o rótulo fora.
    hp_heroi_nome, hp_heroi, hp_heroi_numero = criar_barra(tela, "HP", "green", linha=0)
    _, mp_heroi, mp_heroi_numero = criar_barra(tela, "MP", "blue", linha=2)
    _, furia_heroi, furia_heroi_numero = criar_barra(tela, "Fúria", "orange", linha=4)


def criar_lado_inimigo(tela):
    global inimigo_nome, hp_inimigo, hp_inimigo_numero, historico, painel

    painel = ctk.CTkFrame(tela, fg_color="transparent")
    painel.grid(row=0, column=2, rowspan=6, sticky="ne", padx=20, pady=5)
    painel.grid_columnconfigure(0, weight=1)

    inimigo_nome = ctk.CTkLabel(painel, text="", font=FONTE)
    hp_inimigo = ctk.CTkProgressBar(painel, width=490, height=20, progress_color="red")
    hp_inimigo_numero = ctk.CTkLabel(painel, text="", font=FONTE)
    historico = ctk.CTkTextbox(painel, height=200)

    hp_inimigo.set(0)
    historico.configure(state="disabled")  # somente leitura

    inimigo_nome.grid(row=0, column=0, sticky="e", pady=5)
    hp_inimigo.grid(row=1, column=0, sticky="e", pady=5)
    hp_inimigo_numero.grid(row=2, column=0, sticky="e", pady=5)
    historico.grid(row=3, column=0, sticky="ew", pady=5)


def criar_botoes(tela):
    global painel_botoes, painel_magias, painel_skills

    painel_botoes = ctk.CTkFrame(tela, fg_color="transparent")
    painel_magias = ctk.CTkFrame(tela, fg_color="transparent")
    painel_skills = ctk.CTkFrame(tela, fg_color="transparent")
    painel_botoes.grid(**POSICAO_PAINEL)  # o painel de magias começa escondido

    # Botões de ação: (texto, função). None = ainda sem ação.
    acoes = [
        ("Atacar", atacar),
        ("Mágias", abrir_magias),
        ("Habilidades", abrir_skills),
        ("Itens", None),
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




def criar_skill():
    for b in botao_skills:
        b.destroy()
    botao_skills.clear()

    for linha, skill in enumerate(jogador.habilidadesaprendidas):
        botao = ctk.CTkButton(painel_skills, text=skill.nome, command=lambda m=skill: usar_skill(m))
        botao.grid(row=linha, column=0, sticky="nw", padx=5, pady=5)

    botao_voltar = ctk.CTkButton(painel_skills, text="Voltar", command=voltar)
    botao_voltar.grid(row=len(jogador.habilidadesaprendidas), column=0, sticky="nw", padx=5, pady=5)
# ============================================================
# IDEIAS PARA DEPOIS
# ============================================================
# Quando precisar quebrar/destruir um widget, a melhor execução seria ocultar o
# painel de comandos e mostrar o de magias por cima (como está acima).
#
# def salvar_config_teste(widget, *atributos):
#     return {attr: widget.cget(attr) for attr in atributos}
#
# def magias_teste_destruir():
#     original = salvar_config_teste(botao_magia, "text", "fg_color", "hover_color", "command")
#     botao_magia_1 = ctk.CTkButton(painel_botoes, text="Bola de fogo")
#     botao_magia_1.grid(row=0, column=0, sticky="", padx=5, pady=5)
#     botao_magia.configure(fg_color="black", command=lambda: desativar_magias(botao_magia_1, original))
#
# def desativar_magias_teste_destruir(botao_magia_1, original):
#     botao_magia.configure(**original)
#     botao_magia_1.destroy()