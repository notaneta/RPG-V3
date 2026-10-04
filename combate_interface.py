import customtkinter as ctk

vidamaxheroi = 100
vidaheroi = 50
inimigovida = 50
inimigovidamax = 50

class Magias:       # Provisório para teste
    def __init__(self, nome, mana, dano):
        self.nome = nome
        self.mana = mana
        self.dano = dano

lista_magias = [
    Magias("Fogo", 10, 5),
    Magias("Gelo", 10, 5),
]

def atacar():
    global inimigovida
    dano = 5
    print(f"atacou e causou {dano}")
    mensagem = "Dano causado ao inimigo 5"
    escrever_historico(mensagem)
    inimigovida -= dano
    hp_inimigo.set(inimigovida/inimigovidamax)
    hp_inimigo_numero.configure(text=f"{inimigovida}/{inimigovidamax}")

def escrever_historico(mensagem):
    historico.configure(state="normal")
    historico.insert("end", "\n" + mensagem)
    historico.configure(state="disabled")
    historico.see("end")

def lancar_magia(magia):
    escrever_historico(f"{magia.nome} foi lançada!")

def magias():
    painel_botoes.grid_forget()
    painel_magias.grid(row=7, column=2, sticky="se", padx=20, pady=20)

def voltar():
    painel_magias.grid_forget()
    painel_botoes.grid(row=7, column=2, sticky="se", padx=20, pady=20)

def criar_tela_combate(tela_combate):  # recebe o frame, não cria janela
    global hp_inimigo, hp_inimigo_numero, historico, painel_botoes, painel_magias

    hp_heroi_nome = ctk.CTkLabel(tela_combate, text="HP", font=("Impact", 14))
    hp_heroi = ctk.CTkProgressBar(tela_combate, width=490, height=20, progress_color="green")
    hp_heroi_numero = ctk.CTkLabel(tela_combate, text="30/50", font=("Impact", 14))
    hp_heroi.set(vidaheroi/vidamaxheroi)
    hp_heroi_numero.configure(text=f"{vidaheroi}/{vidamaxheroi}")

    mp_heroi_nome = ctk.CTkLabel(tela_combate, text="MP", font=("Impact", 14))
    mp_heroi = ctk.CTkProgressBar(tela_combate, width=490, height=20, progress_color="blue")
    mp_heroi_numero = ctk.CTkLabel(tela_combate, text="50/50", font=("Impact", 14))
    mp_heroi.set(50/50)
    mp_heroi_numero.configure(text=f"{50}/{50}")

    furia_heroi_nome = ctk.CTkLabel(tela_combate, text="Fúria", font=("Impact", 14))
    furia_heroi = ctk.CTkProgressBar(tela_combate, width=490, height=20, progress_color="orange")
    furia_heroi_numero = ctk.CTkLabel(tela_combate, text="0/100", font=("Impact", 14))
    furia_heroi.set(0/100)
    furia_heroi_numero.configure(text=f"{0}/{100}")

    hp_heroi_nome.grid(row=0, column=0, sticky="nw", padx=5, pady=5)
    hp_heroi.grid(row=1, column=0, padx=5, sticky="nw", pady=5)
    hp_heroi_numero.grid(row=1, column=1, sticky="nw", padx=0, pady=5)

    mp_heroi_nome.grid(row=2, column=0, sticky="nw", padx=5, pady=0)
    mp_heroi.grid(row=3, column=0, sticky="nw", padx=5, pady=20)
    mp_heroi_numero.grid(row=3, column=1, sticky="nw", padx=0, pady=5)

    furia_heroi_nome.grid(row=4, column=0, sticky="nw", padx=5, pady=5)
    furia_heroi.grid(row=5, column=0, sticky="nw", padx=5, pady=5)
    furia_heroi_numero.grid(row=5, column=1, sticky="nw", padx=0, pady=5)

    # Direita da Tela

    tela_combate.grid_columnconfigure(2, weight=1)

    painel_inimigo = ctk.CTkFrame(tela_combate, fg_color="transparent")

    inimigo_nome = ctk.CTkLabel(painel_inimigo, text="Goblin", font=("Impact", 14))
    hp_inimigo = ctk.CTkProgressBar(painel_inimigo, width=490, height=20, progress_color="red")
    hp_inimigo_numero = ctk.CTkLabel(painel_inimigo, text="50/50", font=("Impact", 14))
    hp_inimigo.set(inimigovida/inimigovidamax)
    hp_inimigo_numero.configure(text=f"{inimigovida}/{inimigovidamax}")

    historico = ctk.CTkTextbox(painel_inimigo, height=200)
    historico.insert("0.0", "Combate Iniciado!")
    historico.configure(state="disabled")

    tela_combate.grid_rowconfigure(6, weight=1)  # linha elástica
    painel_botoes = ctk.CTkFrame(tela_combate, fg_color="transparent")

    painel_magias = ctk.CTkFrame(tela_combate, fg_color="transparent")

    botao_ataque = ctk.CTkButton(painel_botoes, text="Atacar", command=atacar)
    botao_magia = ctk.CTkButton(painel_botoes, text="Mágias", command=magias)
    botao_habilidade = ctk.CTkButton(painel_botoes, text="Habilidades")
    botao_item = ctk.CTkButton(painel_botoes, text="Itens")

    # Painel fica no canto superior direito da tela
    painel_inimigo.grid(row=0, column=2, rowspan=6, sticky="ne", padx=20, pady=5)
    painel_botoes.grid(row=7, column=2, sticky="se", padx=20, pady=20)

    # Dentro do painel (grid próprio)
    painel_inimigo.grid_columnconfigure(0, weight=1)

    inimigo_nome.grid(row=0, column=0, sticky="e", pady=5)
    hp_inimigo.grid(row=1, column=0, sticky="e", pady=5)
    hp_inimigo_numero.grid(row=2, column=0, sticky="e", pady=5)

    historico.grid(row=3, column=0, sticky="ew", pady=5)

    botao_ataque.grid(row=4, column=0, sticky="e", pady=5)
    botao_magia.grid(row=5, column=0, sticky="e", pady=5)
    botao_habilidade.grid(row=6, column=0, sticky="e", pady=5)
    botao_item.grid(row=7, column=0, sticky="e", pady=5)

    # Botões das magias: criados UMA vez, aqui no final
    for indice, item in enumerate(lista_magias):
        botao = ctk.CTkButton(painel_magias, text=item.nome,
                              command=lambda m=item: lancar_magia(m))
        botao.grid(row=indice, column=0, sticky="nw", padx=5, pady=5)

    botao_voltar = ctk.CTkButton(painel_magias, text="Voltar", command=voltar)
    botao_voltar.grid(row=len(lista_magias), column=0, sticky="nw", padx=5, pady=5)


# Ideia interessante que posso usar depois, para algo, que necessitar quebrar/destruir o widget, porém a melhor execução
# seria ocultar esse painel de comandos e mostrar o de magias por cima.

            # def salvar_config_teste(widget, *atributos):
            #     return {attr: widget.cget(attr) for attr in atributos}
            #
            # def magias_teste_destruir():
            #     original = salvar_config_teste(botao_magia, "text", "fg_color", "hover_color", "command")
            #     botao_magia_1 = ctk.CTkButton(painel_botoes, text="Bola de fogo")
            #     botao_magia_1.grid(row=0, column=0, sticky="", padx=5, pady=5)
            #     botao_magia.configure(fg_color="black", command=lambda: desativar_magias(botao_magia_1, original))
            #     return
            #
            # def desativar_magias_teste_destruir(botao_magia_1,original):
            #     botao_magia.configure(**original)
            #     botao_magia_1.destroy()


# def mostrar_tela_combate(nome, telas):
#
#     for tela in telas.values():
#         tela.pack_forget()  # esconde todas
#     telas[nome].pack(fill="both", expand=True)  # mostra só a desejada



    # Esquerda da Tela




# Tela inicial

# mostrar_tela_combate("combate")
#
# janela.mainloop()

