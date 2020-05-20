from random import choice


def get_file_data() -> list:
    with open('word_rus.txt', 'rt', encoding='utf-8') as file:
        return file.readlines()


def get_random_word() -> str:
    data = get_file_data()
    return choice(data).strip()

