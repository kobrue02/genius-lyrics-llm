import os

from datetime import date
from rs_exceptions import MissingInputException

class TrainingData:

    def __init__(self, dir: str) -> None:

        today = str(date.today())

        if dir.endswith('.txt'):
            self.text = open(dir, 'r').read() # should be simple plain text file
            self.filename = f"{dir.split('.')[0]}_{today}_rnn_output.txt"
        elif '/' in dir:
            self.text = self.__full_text(dir)
            self.filename = f"{dir.split('/')[1]}_{today}_rnn_output.txt"
        else:
            raise MissingInputException('You need to pass a text file or a plain text string.')

    def __full_text(self, dir):
        raw_text = ""
        for filename in os.listdir(dir):
            if filename.endswith('.txt'):
                with open(f'{dir}/{filename}', 'r', encoding='utf-8') as file:
                    cnt = file.read()
                    raw_text += cnt + "\n"
        return raw_text