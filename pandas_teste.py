import polars as pl
import random as rd
import os
import time
def main():
    #Lê o dataframe
    kanji = pl.read_csv("Kanji_20240329_003023.csv",separator="|")

    #Separa somente os kanjis do teste e as colunas que vou usar
    os.system('cls')
    # print("Escolha o nível do JLPT que quer competir, de 1 a 5, sendo 5 o primeiro nível:")
    # nivel = input()
    kanji = kanji.filter(pl.col("JLPT-test") == 5)
    kanji = kanji.select(pl.col('id',
                            'Kanji',
                            'Grade',
                            'JLPT-test', 
                            'Reading within Joyo', 
                            'Reading beyond Joyo', 
                            'On within Joyo', 
                            'Translation of On', 
                            'Kun within Joyo',
                            'Translation of Kun'
                            ))
    #Separa os ids do nível selecionado
    lista_de_ids = kanji["id"].to_list()
    def game(lista_de_ids):
        #aleatoriza a ordem dos ids
        lista_aleatoria = rd.sample(lista_de_ids,len(lista_de_ids))

        #Separa um kanji
        kanji_linha_escolhido = kanji.filter(pl.col('id') ==lista_aleatoria[0])

        kanji_escolhido = kanji_linha_escolhido.item(0,'Kanji')
        traducao_escolhida = kanji_linha_escolhido.item(0,'Translation of On')
        print(kanji_escolhido)

        #Separa outras 3 escolhas
        kanji_linha_escolhas = kanji.filter(pl.col('id') != lista_aleatoria[0]).sample(3)

        # print(kanji_escolhas)
        kanji_quiz = kanji_linha_escolhido.vstack(kanji_linha_escolhas)

        n=0
        lista_possibilidades = []
        for row in kanji_quiz.rows(named=True):
            lista_possibilidades.append(kanji_quiz.item(n,'Translation of On'))
            n+=1

        lista_possibilidades = rd.sample(lista_possibilidades,len(lista_possibilidades))

        for id, item in enumerate(lista_possibilidades):
            print(id, ' - ', item.split())
        escolha = 5
        while int(escolha) < 0 or int(escolha) > 3:
            escolha = input()

        if lista_possibilidades[int(escolha)] == traducao_escolhida:
            print('Acertou Miseravi')
            lista_de_ids.pop(0)
        else: 
            print('Sabe de nada inocente')
        time.sleep(1)
    while len(lista_de_ids) != 0:
        os.system('cls')
        game(lista_de_ids)

    print('Você fechou o jogo!')


main()
