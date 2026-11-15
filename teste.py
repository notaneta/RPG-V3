import customtkinter as ctk

janela = ctk.CTk()
janela.title("RPG V3")
janela.geometry("800x600")

texto = ctk.CTkLabel(janela, text="Olá")
texto.pack(pady=10)

def clicou():
    texto.configure(text="Você clicou!")
    botao.configure(text="Clicou!")

botao = ctk.CTkButton(janela, text="Clique aqui", command=clicou)
botao.pack()

janela.mainloop()

# Use o grid para a maioria dos projetos no CustomTkinter, pois ele oferece mais controle de alinhamento e organização em linhas e colunas.
# O pack serve apenas para empilhamentos lineares muito simples.