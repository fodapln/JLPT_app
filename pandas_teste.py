import polars as pl
import random as rd
import os
import sys
from time import sleep
class main():
    def __init__(self):
        #Lê o dataframe
        kanji = pl.read_csv("JLPT_app\Kanji_20240329_003023.csv",separator="|")

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
                                'Translation of Kun',
                                'English',
                                'Portugues'
                                ))
        #Separa os ids do nível selecionado
        lista_de_ids = kanji["id"].to_list()
        self.lista_de_ids = lista_de_ids
        self.vidas = 3
        self.kanji = kanji
        self.feedback =[]
        self.lista_aleatoria = rd.sample(lista_de_ids,len(lista_de_ids))
        self.game()

    def __limpar_ultima_linha(self):
    # Sobe uma linha e apaga
        sys.stdout.write('\033[F\033[K')
        sys.stdout.flush()


    def rodada(self):

        #Separa um kanji
        kanji_linha_escolhido = self.kanji.filter(pl.col('id') == self.lista_aleatoria[0])

        kanji_escolhido = kanji_linha_escolhido.item(0,'Kanji')
        traducao_escolhida = kanji_linha_escolhido.item(0,'Portugues')
        print(f"""Você tem {self.vidas} vidas!
Escolha a tradução correspondente ao kanji!""")
        print(kanji_escolhido)

        #Separa outras 3 escolhas
        kanji_linha_escolhas = self.kanji.filter(pl.col('id') != self.lista_aleatoria[0]).sample(3)

        # print(kanji_escolhas)
        kanji_quiz = kanji_linha_escolhido.vstack(kanji_linha_escolhas)
        n=0
        lista_possibilidades = []
        for row in kanji_quiz.rows(named=True):

            lista_possibilidades.append(kanji_quiz.item(n,'Portugues'))
            n+=1
        lista_possibilidades = rd.sample(lista_possibilidades,len(lista_possibilidades))

        for id, item in enumerate(lista_possibilidades):
            print(id + 1, ' - ', item)
        while True:
            escolha = input("Escolha uma opção [1-4]: ")
            if escolha in {'1', '2', '3', '4'}:
                break                  # ok, sai do loop 😎
            
            self.__limpar_ultima_linha()      # some com a entrada inválida
            print("Opção inválida. Tente um número de 1 a 4. 🥺")

        if lista_possibilidades[int(escolha) - 1] == traducao_escolhida:
            print('Acertou Miseravi')
            self.lista_aleatoria.pop(0)
            print('Aperte enter para continuar')
            input()
        else: 
            print(f'A resposta certa era {kanji_escolhido} - {traducao_escolhida}!')
            print(f'Vamos tentar outra vez, aperte enter pra continuar!')
            input()
            self.feedback.append([kanji_escolhido,traducao_escolhida])
            self.vidas = self.vidas - 1
    def game(self):
        while len(self.lista_aleatoria) != 0:
            os.system('cls')
            print(f"Faltam ainda {len(self.lista_aleatoria)} kanjis!")
            if self.vidas == 0:
                break
            self.rodada()
        if self.vidas < 1:
            os.system('cls')
            print("Você errou esses kanjis!")
            print(f"{self.feedback[0][0]} - {self.feedback[0][1]}")
            print(f"{self.feedback[1][0]} - {self.feedback[1][1]}")
            print(f"{self.feedback[2][0]} - {self.feedback[2][1]}")
            print("Você perdeu todas as vezes, deseja jogar novamente? y/n")
            y = "a"
            while str.lower(y) not in ["y","n"]:
                y = input()
            if y == "y":
                main()
            else:
                print("Obrigado por jogar!")

        else:
            # os.system('cls')
            if self.vidas < 3:
                print("Você errou esses kanjis!")
                for n in enumerate(self.feedback):
                    print(f"{n[1][0]} - {n[1][1]}")
            print('Você fechou o jogo! Tente em uma dificuldade mais difícil da proxima vez!')


main()
