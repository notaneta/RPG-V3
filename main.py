from menu_interface import janela

janela.mainloop()


# Prox Passo
# Vilas , itens, lojas, história, habilidades dos bosses

# Poção não é removida do inventário, botão do item não é removido
# Poção pode ser usada com vida max, e não cura nada
# Vida não sobre quando usa poção, falta atualizar a tela

# Viajar ainda não funciona
# Teste # 1 colocar as telas dentro de funções, chamando os modulos.py
# Motivo do meu teste ( Suspeito que o problema vem por que o JOGADOR/ HEROI ainda não foi definido na hora que o jogo inicia
# Causando assim um erro , pois ele afirma que ainda não foi definido nada, já a função, ela pode ser executada depois, quando o já tem os dados do heroi)
# Funciona mas o jogo quebra kkkkkkkkkkkkkkkkkkkkkkkk
#
    # Esse teste também vai tentar me ajudar a deixar mais organizado

# Defesa do RPG V2 atualizado funciona
# Mecanica de geração de foco removida quando skill é usada foi adicionado, conforme atualização do RPG V2

# Ferreiro passou a funcionar porém falta retirar os itens que foram comprados, não irei fazer o menu nesse RPG ainda kkkkkkkkkkkkkkkkkkkkkkkkk

# Mensagem tem que sair colorida para destacar no historico, ver se existe essa opção
# Jogo fecha ao Morrer, resolver isso

# Teste de fazer em funções funcionou
# Video mais organizando meu arquivo e depois mostrando que consegui arrumar muita coisa

# Viajar continua travado mesmo com a progressão do heroi em +6
# botão configure estava para o voltar e não o viajar

# Mesmo ao existir item no inventário, o mesmo não é mostrado / Corrigir
# Bug por que eu esqueci de fazer botoes_itens.append(botao) , esqueci de trocar o painel_skills e fiz append na lista errada
# Na tentativa de adicionar os bosses e progressão de area quebrei o contador de progressão e sua atualização de novo, mas não foi muito dificil de resolver
# Era só chamar a função de atualizar que acabei removendo e depois chamar o contador +1 cada vez que derrotava um inimigo

# Quase perdi boa parte do meu projeto porque ainda sou bem lerdo pra usar o git, mas entendi só depois que o branch serve para dividir o projeto em partes
# Assim separando as partes funcionais e evitando quebrar o codigo

# Nova mecanica
# Pet que ajuda o heroi nas batalhas, o mesmo a depender do pet pode curar o heroi, ajudar a atacar, ou buffar ele.
# O pet tem HP se o mesmo chegar a 0 ele desmaia na luta e só volta após o final da luta com 1 de HP.

# Novas Magias
# Magia do vento e magia de velocidade, a do vento pode atrasar o turno do inimigo,
# enquanto a de velocidade ajuda a ter chances de desviar do inimgio


# Sprite - Histórias aparecem em cima deles, eles conversando textinho me cima
# Log de combate