from word_generator import get_random_word


class Game:
    def __init__(self):
        self.word = get_random_word()
        self.result = ['-' for _ in self.word]
        self.mistake_counter = 0

    def match_letter(self, let):
        changes = False
        for index, letter in enumerate(self.word):
            if letter == let:
                self.open_letter(index, let)
                changes = True
        if changes is False:
            self.mistake_counter += 1
        else:
            self.display_result()

    def display_result(self):
        """
        Отображает слово в котором открываются буквы
        """
        print(' '.join(self.result))

    def open_letter(self, index, letter):
        self.result[index] = letter

    @staticmethod
    def request_letter() -> str:
        return input('Letter?\n')

    def end_game(self, state: int):
        """
        Заканчивает игру, отображая сообщение о проигрыше или выигрыше
        """
        if state:
            print('Победа')
        else:
            print('Проигрыш')

    def run(self):
        while 1:
            letter = self.request_letter()
            self.match_letter(letter)

            if '-' not in self.result:
                self.end_game(1)

            if self.mistake_counter == 6:
                self.end_game(0)
                break


if __name__ == '__main__':
    x = Game()
    x.run()
