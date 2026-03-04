import polars as pl
import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import json
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

class responseModel(BaseModel):
    kanjiMeaning: str
    word1: str
    reading1: str
    translation1: str
    word2: str
    reading2: str
    translation2: str
    word3: str
    reading3: str
    translation3: str


def traduzir_kanji(kanji):

    response = client.responses.parse(
        model="gpt-4o-mini-2024-07-18",
        input=[
            {"role": "system",
            "content": """Take the kanji and translate it to Portuguese in 1 or 2 words max.
            Also, fill the examples with words that use this kanji, how to read them and translate them to Brazilian Portuguese.
            Example for kanji "日": {"kanjiMeaning": "Dia, Sol",
            "word1": "日曜日",
            "reading1": "にちようび",
            "translation1": "domingo",
            "word2": "日本",
            "reading2": "にほん",
            "translation2": "Japão"}"""},
            {
                "role": "user",
                "content": kanji
            },
        ],
        text_format=responseModel,
    )
    # Extrai o JSON da resposta
    event = response.output_parsed
    print(event)
    try:
        return event
    except Exception:
        return ""

def main():
    kanji_df = pl.read_csv("JLPT_app\\Kanji_20240329_003023-Chatgpt.csv", separator="|")
    kanji_list = kanji_df["Kanji"].to_list()

    # Inicializa listas para cada atributo
    kanjiMeaning_list = []
    word1_list = []
    reading1_list = []
    translation1_list = []
    word2_list = []
    reading2_list = []
    translation2_list = []
    word3_list = []
    reading3_list = []
    translation3_list = []

    # Para salvar incrementalmente
    output_json = []
    output_csv_path = "JLPT_app\\Kanji_Traduzido.csv"
    output_json_path = "JLPT_app\\Kanji_Traduzido.json"

    for idx, kanji in enumerate(kanji_list):
        obj_kanji = traduzir_kanji(kanji)
        if obj_kanji:
            kanjiMeaning_list.append(obj_kanji.kanjiMeaning)
            word1_list.append(obj_kanji.word1)
            reading1_list.append(obj_kanji.reading1)
            translation1_list.append(obj_kanji.translation1)
            word2_list.append(obj_kanji.word2)
            reading2_list.append(obj_kanji.reading2)
            translation2_list.append(obj_kanji.translation2)
            word3_list.append(obj_kanji.word3)
            reading3_list.append(obj_kanji.reading3)
            translation3_list.append(obj_kanji.translation3)
        else:
            kanjiMeaning_list.append("")
            word1_list.append("")
            reading1_list.append("")
            translation1_list.append("")
            word2_list.append("")
            reading2_list.append("")
            translation2_list.append("")
            word3_list.append("")
            reading3_list.append("")
            translation3_list.append("")

        # Salva incrementalmente no JSON
        output_json.append({
            "Kanji": kanji,
            "GPT-PT-BR": kanjiMeaning_list[-1],
            "word1": word1_list[-1],
            "reading1": reading1_list[-1],
            "translation1": translation1_list[-1],
            "word2": word2_list[-1],
            "reading2": reading2_list[-1],
            "translation2": translation2_list[-1],
            "word3": word3_list[-1],
            "reading3": reading3_list[-1],
            "translation3": translation3_list[-1],
        })
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(output_json, f, ensure_ascii=False, indent=2)

        # Salva incrementalmente no CSV
        temp_df = pl.DataFrame({
            "Kanji": kanji_list[:idx+1],
            "GPT-PT-BR": kanjiMeaning_list,
            "word1": word1_list,
            "reading1": reading1_list,
            "translation1": translation1_list,
            "word2": word2_list,
            "reading2": reading2_list,
            "translation2": translation2_list,
            "word3": word3_list,
            "reading3": reading3_list,
            "translation3": translation3_list,
        })
        temp_df.write_csv(output_csv_path, separator="|")

if __name__ == "__main__":
    main()