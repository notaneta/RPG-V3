# pip install customtkinter
from logging import disable

import customtkinter as ctk
import combate_interface
from heroi import Heroi
jogador = None
import random
from copy import deepcopy
import inimigos

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

telas = {}

janela = ctk.CTk()
janela.title("RPG V3")
janela.geometry("1920x1080")


def mostrar_tela(nome):
    for tela in telas.values():
        tela.pack_forget()  # esconde todas
    telas[nome].pack(fill="both", expand=True)  # mostra só a desejada
    atualizar_area_vila_progresso()

def salvar_nome():
    global jogador  # "vou mexer no jogador de fora, não criar um novo"
    nome = nome_input.get().strip()  # strip() tira espaços das pontas
    print(nome)

    if not nome:  # nome vazio
        nome_input.configure(placeholder_text="Precisa digitar o seu nome!", placeholder_text_color="red")
        print("Digite um nome!")
        return

    jogador = Heroi(nome)
    mostrar_tela("menu")

#Telas
# --- Tela inicial ---
tela_inicio = ctk.CTkFrame(janela)
telas["inicio"] = tela_inicio
label_inicio = ctk.CTkLabel(tela_inicio, text="Iniciar RPG V3", font=("Impact", 24))
label_inicio.pack(pady=50)
nome_input = ctk.CTkEntry(tela_inicio, placeholder_text="Digite o seu nome", font=("Arial", 24), width=500, height=50)
nome_input.pack(pady=50)
telas["inicio"] = tela_inicio
botao_iniciar = ctk.CTkButton(tela_inicio, text="Iniciar", command=salvar_nome)
botao_iniciar.pack(pady=10)

# --- Tela de Menu ---
tela_menu = ctk.CTkFrame(janela)
telas["menu"] = tela_menu

label_menu = ctk.CTkLabel(tela_menu, text="Menu Principal", font=("Arial", 24))
label_menu.pack(pady=50)

label_menu = ctk.CTkLabel(tela_menu, text="bem vindo", font=("Arial", 24))
botao_area = ctk.CTkButton(tela_menu, text="Aventurar", command=lambda: mostrar_tela("area"))
botao_area.pack(pady=10)
botao_vila = ctk.CTkButton(tela_menu, text="Visitar vila local", command=lambda: mostrar_tela("vila"))
botao_vila.pack(pady=10)

import vilas

# --- Tela da Vila ---
tela_vila = ctk.CTkFrame(janela)
telas["vila"] = tela_vila

label_vila = ctk.CTkLabel(tela_vila, text=f"Você está na {vilas.Vila_atual.nome}", font=("Arial", 24))   # Fazer a loja da vila, e as opções dela
label_vila.pack(pady=50)

botao_loja = ctk.CTkButton(tela_vila, text="Ir a Loja do Mago", command=lambda: mostrar_tela("loja"))
botao_loja.pack(pady=10)
botao_ferreiro = ctk.CTkButton(tela_vila, text="Ir ao Ferreiro", command=lambda: mostrar_tela("ferreiro"))
botao_ferreiro.pack(pady=10)
botao_voltar = ctk.CTkButton(tela_vila, text="Voltar", command=lambda: mostrar_tela("menu"))
botao_voltar.pack(pady=10)

# --- Tela Loja ---

tela_loja = ctk.CTkFrame(janela)
telas["loja"] = tela_loja

botao_loja = ctk.CTkButton(tela_loja, text="Comprar Poções", command=lambda: mostrar_tela("loja"))
botao_loja.pack(pady=10)

botao_voltar = ctk.CTkButton(tela_loja, text="Voltar", command=lambda: mostrar_tela("vila"))
botao_voltar.pack(pady=10)

# --- Tela Ferreiro ---

tela_ferreiro = ctk.CTkFrame(janela)
telas["ferreiro"] = tela_ferreiro

botao_voltar = ctk.CTkButton(tela_ferreiro, text="Voltar", command=lambda: mostrar_tela("vila"))
botao_voltar.pack(pady=10)

def abrir_combate(inimigoaleatório):
    combate_interface.iniciar_combate(jogador, inimigoaleatório)
    mostrar_tela("combate")

# --- Tela do Mundo ---

import mundo # Importa o .py completo para prevenir atualizações
tela_area = ctk.CTkFrame(janela)
telas["area"] = tela_area

label_area = ctk.CTkLabel(tela_area, text=f"Você está em: {mundo.zona_atual.nome}", font=("Arial", 24))
label_area.pack(pady=50)
label_area_progresso = ctk.CTkLabel(tela_area, text=f"Inimigos derrotados: {mundo.zona_atual.progresso}", font=("Arial", 24))
label_area_progresso.pack(pady=50)

def atualizar_area_vila_progresso():
    # Chamada toda vez que uma tela é mostrada: refaz os textos com os valores de agora
    label_area.configure(text=f"Você está em: {mundo.zona_atual.nome}")
    label_area_progresso.configure(text=f"Inimigos derrotados: {mundo.zona_atual.progresso}")
    label_vila.configure(text=f"Você está na {vilas.Vila_atual.nome}")

    if mundo.zona_atual.progresso >= 7:
        botao_explorar.configure(text="Explorar", state="disabled")
        botao_voltar.configure(state="enabled", command = lambda: viajar_area(jogador))


from mundo import  iniciar_exploracao
botao_explorar = ctk.CTkButton(tela_area, text="Explorar", command=iniciar_exploracao) #  Adaptar a função de explorar do RPG
botao_explorar.pack(pady=10)

from mundo import viajar_area
botao_prosseguir = ctk.CTkButton(tela_area, text="Viajar", state="disabled") # Viaja para a proxima area
botao_prosseguir.pack(pady=10)


botao_voltar = ctk.CTkButton(tela_area, text="Voltar", command=lambda: mostrar_tela("menu"))
botao_voltar.pack(pady=10)


# --- Tela de Combate ---
tela_combate = ctk.CTkFrame(janela)
telas["combate"] = tela_combate
combate_interface.criar_tela_combate(tela_combate)  # monta uma vez ao ser iniciado o programa




mostrar_tela("inicio")





# Trocar botões para grid, deixar na parte de baixo da tela
# Interligar interface de luta com os valores reais do heroi e do inimigo. (valores do inimigo, tem que ser definido/randomizado antes de ser mandado os dados para a interface)
# criar / Interligar sistema de compra de itens das lojas e ferreiros a butôes
# Interligar sistema de progressão a interface
# Criar I.A do inimigo
# começar usar imagem com o pillow

# Criar menu de equipamentos, com sistema de equipar e remover

janela.mainloop()