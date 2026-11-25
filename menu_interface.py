# pip install customtkinter

# ============================================================
# COMO ESSE ARQUIVO FUNCIONA (a regra de ouro)
#
# 1. MONTAR: cada tela é montada UMA vez, quando o programa abre.
#    Nessa hora ainda não existe herói, então os textos começam vazios.
#
# 2. ATUALIZAR: toda vez que uma tela aparece, mostrar_tela() chama a função
#    atualizar_<tela>(), que só troca o texto dos labels com .configure(...)
#    usando os dados de AGORA do herói.
#
# 3. O HERÓI GUARDA TUDO: onde ele está fica em jogador.zona_atual e
#    jogador.vila_atual (igual no V2). Nada de mundo.zona_atual / vilas.Vila_atual.
#    Assim, quando tiver o banco de dados, é só salvar o herói.
# ============================================================

import customtkinter as ctk
from copy import deepcopy

import combate_interface
import itens
import mundo
from heroi import Heroi
from itens import poçoes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

FONTE_TITULO = ("Impact", 28)
FONTE = ("Arial", 22)

jogador = None   # vira um Heroi quando o jogador digita o nome
telas = {}       # "nome da tela" -> frame
atualizadores = {}  # "nome da tela" -> função que atualiza os textos dela

janela = ctk.CTk()
janela.title("RPG V3")
janela.geometry("1920x1080")

itens_ferreiro = []

# ============================================================
# TROCA DE TELA
# ============================================================
def nova_tela(nome, atualizar=None):
    """Cria o frame da tela, registra no dicionário e (opcional) a função que atualiza ela."""
    frame = ctk.CTkFrame(janela)
    telas[nome] = frame
    if atualizar:
        atualizadores[nome] = atualizar
    return frame


def mostrar_tela(nome):
    for tela in telas.values():
        tela.pack_forget()  # esconde todas

    if nome in atualizadores and jogador is not None:
        atualizadores[nome]()  # refaz os textos com os valores de agora

    telas[nome].pack(fill="both", expand=True)  # mostra só a desejada


# ============================================================
# BARRA DE STATUS (aparece no menu, vila e área)
# ============================================================
def texto_status():
    zona = jogador.zona_atual
    return (f"{jogador.nome}  |  Nível {jogador.nivel}  |  "
            f"HP {int(jogador.vida)}/{jogador.vidamax}  |  MP {int(jogador.mana)}/{jogador.manamax}  |  "
            f"Ouro {jogador.ouro}\n"
            f"Vila: {jogador.vila_atual.nome}   •   Zona: {zona.nome}   •   "
            f"Progresso: {zona.progresso}/{zona.lutas_para_boss}")


# ============================================================
# TELA INICIAL
# ============================================================
def salvar_nome():
    global jogador
    nome = nome_input.get().strip()  # strip() tira espaços das pontas

    if not nome:  # nome vazio
        nome_input.configure(placeholder_text="Precisa digitar o seu nome!", placeholder_text_color="red")
        return

    jogador = Heroi(nome)
    mostrar_tela("menu")


tela_inicio = nova_tela("inicio")
ctk.CTkLabel(tela_inicio, text="Iniciar RPG V3", font=FONTE_TITULO).pack(pady=50)
nome_input = ctk.CTkEntry(tela_inicio, placeholder_text="Digite o seu nome", font=("Arial", 24), width=500, height=50)
nome_input.pack(pady=50)
ctk.CTkButton(tela_inicio, text="Iniciar", command=salvar_nome).pack(pady=10)


# ============================================================
# TELA DE MENU
# ============================================================
def atualizar_menu():
    label_menu_bemvindo.configure(text=f"Bem-vindo, {jogador.nome}!")
    label_menu_status.configure(text=texto_status())


tela_menu = nova_tela("menu", atualizar_menu)
ctk.CTkLabel(tela_menu, text="Menu Principal", font=FONTE_TITULO).pack(pady=(50, 10))
label_menu_bemvindo = ctk.CTkLabel(tela_menu, text="", font=FONTE)
label_menu_bemvindo.pack(pady=10)
label_menu_status = ctk.CTkLabel(tela_menu, text="", font=("Arial", 18))
label_menu_status.pack(pady=20)
ctk.CTkButton(tela_menu, text="Aventurar", command=lambda: mostrar_tela("area")).pack(pady=10)
ctk.CTkButton(tela_menu, text="Visitar vila local", command=lambda: mostrar_tela("vila")).pack(pady=10)


# ============================================================
# TELA DA VILA
# ============================================================
def atualizar_vila():
    label_vila.configure(text=f"Você está na {jogador.vila_atual.nome}")
    label_vila_descricao.configure(text=jogador.vila_atual.descricao)
    label_vila_ouro.configure(text=f"Ouro: {jogador.ouro}")


tela_vila = nova_tela("vila", atualizar_vila)
label_vila = ctk.CTkLabel(tela_vila, text="", font=FONTE_TITULO)
label_vila.pack(pady=(50, 10))
label_vila_descricao = ctk.CTkLabel(tela_vila, text="", font=("Arial", 18))
label_vila_descricao.pack(pady=5)
label_vila_ouro = ctk.CTkLabel(tela_vila, text="", font=FONTE)
label_vila_ouro.pack(pady=20)
ctk.CTkButton(tela_vila, text="Ir a Loja do Mago", command=lambda: mostrar_tela("loja")).pack(pady=10)
ctk.CTkButton(tela_vila, text="Ir ao Ferreiro", command=lambda: mostrar_tela("ferreiro")).pack(pady=10)
ctk.CTkButton(tela_vila, text="Voltar", command=lambda: mostrar_tela("menu")).pack(pady=10)


# ============================================================
# TELA DA LOJA
# ============================================================
def comprar_pocao(pocao):
    """Compra a poção se o jogador tiver ouro suficiente."""
    if jogador.ouro < pocao.custo:
        label_loja_msg.configure(text=f"Ouro insuficiente! Você tem {jogador.ouro}, precisa de {pocao.custo}.",
                                 text_color="red")
        return

    jogador.ouro -= pocao.custo
    jogador.adicionar_pocoes(deepcopy(pocao))  # junta com a que já tem (soma quantidade)
    label_loja_msg.configure(text=f"Comprou {pocao.nome}!", text_color="green")
    atualizar_loja()


def atualizar_loja():
    label_loja_ouro.configure(text=f"Seu ouro: {jogador.ouro}")


tela_loja = nova_tela("loja", atualizar_loja)
ctk.CTkLabel(tela_loja, text="Loja do Mago", font=FONTE_TITULO).pack(pady=20)
label_loja_ouro = ctk.CTkLabel(tela_loja, text="", font=FONTE)
label_loja_ouro.pack(pady=5)
label_loja_msg = ctk.CTkLabel(tela_loja, text="", font=("Arial", 18))
label_loja_msg.pack(pady=5)


for pocao in poçoes:
    texto = f"{pocao.nome} — {pocao.custo} ouros\n{pocao.descricao}"
    ctk.CTkButton(tela_loja, text=texto, width=500,
                  command=lambda p=pocao: comprar_pocao(p)).pack(pady=5)  # p=pocao fixa o valor no lambda

ctk.CTkButton(tela_loja, text="Voltar", command=lambda: mostrar_tela("vila")).pack(pady=20)


# ============================================================
# TELA DO FERREIRO
# ============================================================
def atualizar_ferreiro():
    label_ferreiro_ouro.configure(text=f"Seu ouro: {jogador.ouro}")
    label_ferreiro_ouro_itens.configure(text=f"Seu ouro: {jogador.ouro}")


def comprar_item_ferreiro(item, tipo):
    """Compra o amuleto e equipa. tipo é "ataque" ou "defesa"."""
    equipado = getattr(jogador, f"amuleto_{tipo}", None)  # None se ainda não equipou nenhum

    if equipado is not None and equipado.nome == item.nome:
        label_ferreiro_msg.configure(text=f"Você já está com {item.nome} equipado.", text_color="orange")
        return

    if jogador.ouro < item.custo:
        label_ferreiro_msg.configure(text=f"Ouro insuficiente! Você tem {jogador.ouro}, precisa de {item.custo}.",
                                     text_color="red")
        return

    jogador.ouro -= item.custo
    if tipo == "ataque":
        jogador.equipar_ataque(item)
    else:
        jogador.equipar_defesa(item)

    label_ferreiro_msg.configure(text=f"Comprou {item.nome}!", text_color="green")
    atualizar_ferreiro()


def criar_amuletos_ferreiro(tipo):
    for b in itens_ferreiro:
        b.destroy()
    itens_ferreiro.clear()

    if tipo == "ataque":
        lista = itens.ferreiro_Amuletos_Ataque
    else:
        lista = itens.ferreiro_Amuletos_Defesa

    for item in lista:
        texto = f"{item.nome} — {item.custo} ouros\n{item.descricao}"
        botao = ctk.CTkButton(
            tela_ferreiro_itens,
            text=texto,
            width=500,
            command=lambda item=item: comprar_item_ferreiro(item, tipo))
        botao.pack(pady=5)
        itens_ferreiro.append(botao)

    botao_voltar = ctk.CTkButton(
        tela_ferreiro_itens, text="Voltar",
        command=lambda: mostrar_tela("ferreiro"))
    botao_voltar.pack(pady=20)
    itens_ferreiro.append(botao_voltar)


def abrir_ferreiro(tipo):
    label_ferreiro_msg.configure(text="")
    criar_amuletos_ferreiro(tipo)
    mostrar_tela("ferreiro_itens")


tela_ferreiro = nova_tela("ferreiro", atualizar_ferreiro)
ctk.CTkLabel(tela_ferreiro, text="Ferreiro (em construção)", font=FONTE_TITULO).pack(pady=50)
label_ferreiro_ouro = ctk.CTkLabel(tela_ferreiro, text="", font=FONTE)
label_ferreiro_ouro.pack(pady=5)
ctk.CTkButton(tela_ferreiro, text="Amuleto de Ataque", command=lambda: abrir_ferreiro("ataque")).pack(pady=10)
ctk.CTkButton(tela_ferreiro, text="Amuleto de Defesa", command=lambda: abrir_ferreiro("defesa")).pack(pady=10)
ctk.CTkButton(tela_ferreiro, text="Voltar", command=lambda: mostrar_tela("vila")).pack(pady=10)

# a lista de amuletos fica nessa tela, os botões são criados em criar_amuletos_ferreiro
tela_ferreiro_itens = nova_tela("ferreiro_itens", atualizar_ferreiro)
label_ferreiro_ouro_itens = ctk.CTkLabel(tela_ferreiro_itens, text="", font=FONTE)
label_ferreiro_ouro_itens.pack(pady=5)
label_ferreiro_msg = ctk.CTkLabel(tela_ferreiro_itens, text="", font=("Arial", 18))
label_ferreiro_msg.pack(pady=5)


# ============================================================
# TELA DA ÁREA (MUNDO)
# ============================================================
def atualizar_area():
    zona = jogador.zona_atual
    label_area.configure(text=f"Você está em: {zona.nome}")
    label_area_vila.configure(text=f"Vila mais próxima: {jogador.vila_atual.nome}")
    label_area_progresso.configure(text=f"Inimigos derrotados: {zona.progresso}/{zona.lutas_para_boss}")

    # Regra: o .configure() só muda o que você passa. O resto FICA como estava.
    # Por isso cada caso abaixo define o botão INTEIRO (texto, cor, comando, estado)
    # usando configurar_explorar(). Assim nada "vaza" de uma área para outra.
    inimigo, tipo = mundo.proxima_luta(jogador)
    if tipo is None:
        label_area_aviso.configure(text="Área concluída!", text_color="green")
        configurar_explorar("Concluído", estado="disabled")
    elif tipo == "boss":
        label_area_aviso.configure(text="Cuidado, a próxima luta será contra o CHEFE da área!", text_color="orange")
        configurar_explorar("Explorar")
    elif tipo == "especial":
        label_area_aviso.configure(text="Você já pode Viajar!", text_color="green")
        configurar_explorar("Explorar", comando=aviso)   # 1º clique só avisa (segredo)
    else:
        label_area_aviso.configure(text="")
        configurar_explorar("Explorar")

    botao_viajar.configure(state="normal" if mundo.pode_viajar(jogador) else "disabled")


def explorar():
    inimigo, tipo = mundo.proxima_luta(jogador)
    if inimigo is None:
        return

    def quando_terminar(venceu):
        if not venceu:
            janela.destroy()  # GAME OVER fecha o jogo (por enquanto)
            return
        mundo.registrar_vitoria(jogador, tipo)
        mostrar_tela("area")  # mostrar_tela já chama atualizar_area()

    combate_interface.iniciar_combate(jogador, inimigo, quando_terminar)
    mostrar_tela("combate")

def configurar_explorar(texto, cor=None, comando=None, estado="normal"):
    """Define TUDO do botão explorar de uma vez. Sem cor/comando = volta ao padrão."""
    botao_explorar.configure(text=texto,
                             text_color=cor or COR_TEXTO_PADRAO,
                             command=comando or explorar,
                             state=estado)


def aviso():
    # 2º clique (agora o comando é explorar) começa a luta contra o boss secreto
    configurar_explorar("[PERIGO] Algo MUITO PODEROSO está vindo...", cor="red", comando=explorar)


def viajar():
    if mundo.viajar_area(jogador):
        mostrar_tela("area")   # atualizar_area() já deixa o botão certo, não precisa mexer nele aqui


tela_area = nova_tela("area", atualizar_area)
label_area = ctk.CTkLabel(tela_area, text="", font=FONTE_TITULO)
label_area.pack(pady=(50, 10))
label_area_vila = ctk.CTkLabel(tela_area, text="", font=("Arial", 18))
label_area_vila.pack(pady=5)
label_area_progresso = ctk.CTkLabel(tela_area, text="", font=FONTE)
label_area_progresso.pack(pady=20)
label_area_aviso = ctk.CTkLabel(tela_area, text="", font=FONTE)
label_area_aviso.pack(pady=10)
label_area_aviso_2 = ctk.CTkLabel(tela_area, text="", font=FONTE)
label_area_aviso_2.pack(pady=10)

botao_explorar = ctk.CTkButton(tela_area, text="Explorar", command=explorar)
botao_explorar.pack(pady=10)
COR_TEXTO_PADRAO = botao_explorar.cget("text_color")  # guarda a cor original do tema para poder voltar nela
botao_viajar = ctk.CTkButton(tela_area, text="Viajar", command=viajar, state="disabled")
botao_viajar.pack(pady=10)
ctk.CTkButton(tela_area, text="Voltar", command=lambda: mostrar_tela("menu")).pack(pady=10)


# ============================================================
# TELA DE COMBATE
# ============================================================
tela_combate = nova_tela("combate")
combate_interface.criar_tela_combate(tela_combate)  # monta uma vez ao iniciar o programa


mostrar_tela("inicio")
# O janela.mainloop() fica só no main.py


# Trocar botões para grid, deixar na parte de baixo da tela
# criar / Interligar sistema de compra de itens dos ferreiros a botões
# Criar I.A do inimigo
# começar usar imagem com o pillow
# Criar menu de equipamentos, com sistema de equipar e remover
