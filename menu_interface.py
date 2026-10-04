# pip install customtkinter

import customtkinter as ctk
import combate_interface
from heroi import Heroi
jogador = None

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

def salvar_nome():
    global jogador  # "vou mexer no jogador de fora, não criar um novo"
    nome = nome_input.get().strip()  # strip() tira espaços das pontas
    print(nome)

    if not nome:  # nome vazio
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
botao_vila = ctk.CTkButton(tela_menu, text="Vilas", command=lambda: mostrar_tela("vila"))
botao_vila.pack(pady=10)
botao_combate = ctk.CTkButton(tela_menu, text="Combate", command=lambda: mostrar_tela("combate"))
botao_combate.pack(pady=10)

# --- Tela da Vila ---
tela_vila = ctk.CTkFrame(janela)
telas["vila"] = tela_vila

label_vila = ctk.CTkLabel(tela_vila, text="Você está na Vila de:", font=("Arial", 24))
label_vila.pack(pady=50)

botao_ferreiro = ctk.CTkButton(tela_vila, text="Ir ao Ferreiro", command=lambda: mostrar_tela("ferreiro"))
botao_ferreiro.pack(pady=10)
botao_voltar = ctk.CTkButton(tela_vila, text="Voltar", command=lambda: mostrar_tela("menu"))
botao_voltar.pack(pady=10)

tela_ferreiro = ctk.CTkFrame(janela)
telas["ferreiro"] = tela_ferreiro

botao_voltar = ctk.CTkButton(tela_ferreiro, text="Voltar", command=lambda: mostrar_tela("vila"))
botao_voltar.pack(pady=10)

# --- Tela da Mundo ---
tela_area = ctk.CTkFrame(janela)
telas["area"] = tela_area

label_area = ctk.CTkLabel(tela_area, text=f"Você está na área: ", font=("Arial", 24))
label_area.pack(pady=50)

# botao_Explorar = ctk.CTkbutton(tela_area, text="Explorar", command=iniciar_exploração) #  Adaptar a função de explorar do RPG
# botao_Explorar.pack(pady=10)
#
# botao_prosseguir = ctk.CTkbutton(tela_area, text="Seguir em frente")
# botao_prosseguir.pack(pady=10)

botao_voltar = ctk.CTkButton(tela_area, text="Voltar", command=lambda: mostrar_tela("menu"))
botao_voltar.pack(pady=10)


# --- Tela de Combate ---
tela_combate = ctk.CTkFrame(janela)
telas["combate"] = tela_combate
combate_interface.criar_tela_combate(tela_combate)  # monta uma vez



mostrar_tela("inicio")

# Testar se chamar tela combate funcionou
# Botões magias sendo criados
# Ver se salva o nome digitado do heroi 

# Trocar botões para grid, deixar na parte de baixo da tela
# Interligar interface de luta com os valores reais do heroi e do inimigo. (valores do inimigo, tem que ser definido/randomizado antes de ser mandado os dados para a interface)
# criar / Interligar sistema de compra de itens das lojas e ferreiros a butôes
# Interligar sistema de progressão a interface
# Criar I.A do inimigo
# começar usar imagem com o pillow

# Criar menu de equipamentos, com sistema de equipar e remover

janela.mainloop()



