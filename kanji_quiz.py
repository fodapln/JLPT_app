import polars as pl
import random as rd
import os
import sys

class KanjiQuiz:
    def __init__(self, csv_path="./Kanji_20240329_003023.csv"):
        self.csv_path = csv_path
        self.full_df = self.load_data()
        self.vidas_iniciais = 3

    def load_data(self):
        try:
            return pl.read_csv(self.csv_path, separator="|")
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.csv_path} não encontrado.")
            sys.exit(1)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def __limpar_ultima_linha(self):
        # Sobe uma linha e apaga
        sys.stdout.write('\033[F\033[K')
        sys.stdout.flush()

    def selecionar_nivel(self):
        self.clear_screen()
        print("Escolha o nível do JLPT que quer competir (1 a 5):")
        while True:
            nivel_input = input("Nível: ")
            if nivel_input.isdigit() and 1 <= int(nivel_input) <= 5:
                return int(nivel_input)

            self.__limpar_ultima_linha()
            print("Opção inválida. Tente novamente. 🥺", end="\r")

    def preparar_jogo(self, nivel):
        df_nivel = self.full_df.filter(pl.col("JLPT-test") == nivel)
        df_nivel = df_nivel.select(pl.col(
            'id', 'Kanji', 'Grade', 'JLPT-test',
            'Reading within Joyo', 'Reading beyond Joyo',
            'On within Joyo', 'Translation of On',
            'Kun within Joyo', 'Translation of Kun',
            'English', 'Portugues'
        ))

        self.kanji_df = df_nivel
        lista_de_ids = df_nivel["id"].to_list()
        self.lista_aleatoria = rd.sample(lista_de_ids, len(lista_de_ids))
        self.vidas = self.vidas_iniciais
        self.feedback = []

    def rodada(self):
        # Separa um kanji
        current_id = self.lista_aleatoria[0]
        kanji_linha_escolhido = self.kanji_df.filter(pl.col('id') == current_id)

        kanji_escolhido = kanji_linha_escolhido.item(0, 'Kanji')
        traducao_escolhida = kanji_linha_escolhido.item(0, 'Portugues')

        print(f"Você tem {self.vidas} vidas!")
        print("Escolha a tradução correspondente ao kanji!")
        print(f"\n--- {kanji_escolhido} ---\n")

        # Separa outras 3 escolhas
        outros_kanjis = self.kanji_df.filter(pl.col('id') != current_id)
        num_escolhas = min(3, outros_kanjis.height)
        kanji_linha_escolhas = outros_kanjis.sample(num_escolhas)

        kanji_quiz = kanji_linha_escolhido.vstack(kanji_linha_escolhas)

        lista_possibilidades = kanji_quiz["Portugues"].to_list()
        lista_possibilidades = rd.sample(lista_possibilidades, len(lista_possibilidades))

        for idx, item in enumerate(lista_possibilidades):
            print(f"{idx + 1} - {item}")

        while True:
            escolha = input("Escolha uma opção: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(lista_possibilidades):
                break
            self.__limpar_ultima_linha()
            print("Opção inválida. 🥺")

        if lista_possibilidades[int(escolha) - 1] == traducao_escolhida:
            print('\nAcertou Miseravi! 🎉')
            self.lista_aleatoria.pop(0)
        else:
            print(f'\nErrado! A resposta certa era {kanji_escolhido} - {traducao_escolhida}.')
            self.feedback.append([kanji_escolhido, traducao_escolhida])
            self.vidas -= 1

        print('Aperte enter para continuar')
        input()

    def run(self):
        while True:
            nivel = self.selecionar_nivel()
            self.preparar_jogo(nivel)

            while len(self.lista_aleatoria) > 0 and self.vidas > 0:
                self.clear_screen()
                print(f"Nível JLPT N{nivel} - Faltam {len(self.lista_aleatoria)} kanjis!")
                self.rodada()

            self.clear_screen()
            if self.vidas == 0:
                print("Game Over! Você perdeu todas as suas vidas.")
            else:
                print("Parabéns! Você completou todos os kanjis deste nível!")

            if self.feedback:
                print("\nKanjis que você errou:")
                for kanji, traducao in self.feedback:
                    print(f"{kanji} - {traducao}")

            print("\nDeseja jogar novamente? (y/n)")
            again = ""
            while again not in ["y", "n"]:
                again = input().lower()
            if again == "n":
                print("Obrigado por jogar!")
                break

if __name__ == "__main__":
    quiz = KanjiQuiz()
    quiz.run()
