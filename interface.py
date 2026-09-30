# pip install customtkinter
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

telas = {}

janela = ctk.CTk()
janela.title("RPG V3")
janela.geometry("1920x1080")

# def iniciar():
#     while True:
#         if nome is None:
#             print("Precisa digitar um nome antes!")
#             break
#
#         else:
#             print(f"Bem vindo! {nome}")
#
#             break

# texto = ctk.CTkLabel(janela, text="RPG V3")
#
# texto.pack(padx=10, pady=10)
#
#
# nome = ctk.CTkEntry(janela, placeholder_text="Digite Nome")
# nome.pack(padx=10, pady=10)
#
#
# botao = ctk.CTkButton(janela, text="Iniciar", command=lambda: mostrar_tela("menu"))
# botao.pack(padx=10, pady=10)


def mostrar_tela(nome):
    for tela in telas.values():
        tela.pack_forget()  # esconde todas
    telas[nome].pack(fill="both", expand=True)  # mostra só a desejada


#Telas
# --- Tela inicial ---
tela_inicio = ctk.CTkFrame(janela)
telas["inicio"] = tela_inicio
label_inicio = ctk.CTkLabel(tela_inicio, text="Iniciar RPG V3", font=("Impact", 24))
label_inicio.pack(pady=50)
nome1 = ctk.CTkEntry(tela_inicio, placeholder_text="Digite o seu nome", font=("Arial", 24), width=500, height=50)
nome1.pack(pady=50)
telas["inicio"] = tela_inicio
botao_iniciar = ctk.CTkButton(tela_inicio, text="Iniciar", command=lambda: mostrar_tela("menu"))
botao_iniciar.pack(pady=10)

jogador = nome1

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


mostrar_tela("inicio")





janela.mainloop()



