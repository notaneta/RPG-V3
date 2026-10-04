pip install pillow

from PIL import Image

img = Image.open("imagem.png") 

print(img.size) # Printa tamanho

img.show() # Abre a imagem com o visualizador do win

input("Aperte ENTER para continuar e mudar a resolução da IMAGEM")

img = img.resize((200, 200))

img.show()

img.save("nova_imagem.png") # Salva a iamgem modificada



# Exemplo com Tkinter

from tkinter import *
from PIL import Image, ImageTk

janela = Tk()

img = Image.open("imagem.png")
img = img.resize((200, 200))

foto = ImageTk.PhotoImage(img) # A foto é inserida dentro da variavel

label = Label(janela, image=foto) # Variavel é enviada no image=
label.pack()

janela.mainloop()


# CustomTKinter
import customtkinter as ctk
from PIL import Image

app = ctk.CTk()

imagem = ctk.CTkImage(light_image=Image.open("icone.png"), dark_image=Image.open("icone.png"), size=(100, 100))
# Dark Image e Light Image, São apenas para poder referenciar que em qualquer tema do APP ele será a mesma imagem.

label = ctk.CTkLabel(app, text="", image=imagem)

label.pack(pady=20)

app.mainloop()