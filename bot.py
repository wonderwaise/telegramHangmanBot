from aiogram import Bot, Dispatcher, types, executor
import typing
from word_generator import get_random_word


bot = Bot(token='1071730588:AAH2OW_VPlB748GYXYeirm1h3h3wLvjFpbY')

dp = Dispatcher(bot=bot)
rus_alphabet = 'йцукенгшщзхъфывапролджэячсмитьбюё'
USERS_BASE = {}


def decorator(method):
    def wrapper(self, *args):
        result = method(self, *args)
        if self.mistake_counter >= 6:
            return self.end_game(0)
        elif '-' not in self.result:
            return self.end_game(1)
        return result
    return wrapper


def letter_check(text: str) -> typing.Union[int, str]:
    if len(text) > 1:
        return 'Ошибка длины!'
    elif text not in rus_alphabet:
        return 'Ошибка алфавита'
    else:
        return 0


def register_user(user: types.User):
    game_profile = Game(user.id)
    USERS_BASE[user.id] = game_profile
    return len(game_profile.word)


@dp.message_handler(commands=['play'])
async def play_command(message: types.Message):
    user = message.from_user
    if user not in USERS_BASE:
        length = register_user(user)
        await message.reply(f'Игра началась, слово загадано!\n'
                            f'Длина слова состовляет {length} символов. Успехов!', reply=False)
    else:
        await message.reply('Вы не можете начать игру так как уже начали ранее!')


def check_user_registration(user: types.User) -> int:
    if user.id in USERS_BASE:
        return 1
    else:
        return 0


@dp.message_handler()
async def on_message(message: types.Message):
    print(f'-- [MESSAGE] --\n'
          f'\t[TEXT] {message.text}\n'
          f'\t[AUTHOR] {message.from_user.full_name}, [ID] {message.from_user.id}\n'
          f'---------------')
    if not check_user_registration(message.from_user):
        await message.reply('Вы не начали игру. Для начала игры пропишите команду /play', reply=False)
    elif x := letter_check(message.text):
        await message.reply(x, reply=False)
    else:
        print('here')
        first, second = USERS_BASE[message.from_user.id].match_letter(message.text)
        await message.reply(f'{first}\n{second}', reply=False, parse_mode='HTML')


class Game:
    def __init__(self, user_id):
        self.id = user_id
        self.word = get_random_word()
        self.result = ['-' for _ in self.word]
        self.mistake_counter = 0
        self.called_letters = []
        self.state: int = 0
        print(f'[START GAME] word - {self.word}')

    @decorator
    def match_letter(self, let):
        if let in self.called_letters:
            return 'Внимание!', 'Вы уже называли эту букву, выберите другую'
        changes = False
        self.called_letters.append(let)
        for index, letter in enumerate(self.word):
            if letter == let:
                self.open_letter(index, let)
                changes = True
        if changes is False:
            self.mistake_counter += 1
            return 'Увы данной буквы нет в слове!', f'Счетчик ошибок: {self.mistake_counter} / 6'

        else:
            return 'Великолепно! Такая буква есть в слове', self.display_result()

    def display_result(self):
        """
        Отображает слово в котором открываются буквы
        """
        return ' '.join(self.result)

    def open_letter(self, index, letter):
        self.result[index] = letter

    def end_game(self, state: int):
        """
        Заканчивает игру, отображая сообщение о проигрыше или выигрыше
        """
        answers = {
            0: 'ошибок',
            1: 'ошибку',
            2: 'ошибки',
            3: 'ошибки',
            4: 'ошибки',
            5: 'ошибок',
            6: 'ошибок'
        }

        if state:
            USERS_BASE.pop(self.id)
            return (f'Победа!\nВы допустили <b>{self.mistake_counter} '
                    f'{answers.get(self.mistake_counter)}</b> и справились с задачей\n',
                    '\nДля начала следующей игры, вызовите команду /play снова.')

        else:
            USERS_BASE.pop(self.id)
            return (f'Проигрыш.\nЗагаданное слово было: <b>{self.word}</b>\n',
                    '\nДля начала следующей игры, вызовите команду /play снова.')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
