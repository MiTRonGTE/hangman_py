import random
import os

class hangman:
    def __init__(self, words_list, cheating=False):
        self.cls()
        self.password = random.choice(words_list).upper()
        self.n_password = ["_"] * len(self.password)
        self.cheating = cheating
        self.life = 0
        self.info = ""
        self.used = []
        self.game()

    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw(self):
        graphics = [
            "",
            r"""
      /|\  
     /_|_\
     """,
            r"""
       |
       |
       |
       |
      /|\  
     /_|_\
    """,
            r"""
       _______
       |/
       |
       |
       |
      /|\  
     /_|_\
    """,
            r"""
       _______
       |/    |
       |    (?)
       |
       |
      /|\  
     /_|_\
    """,
            r"""
       _______
       |/    |
       |    (?)
       |    /|\
       |
      /|\  
     /_|_\
    """,
            r"""
       _______
       |/    |
       |    (?)
       |    /|\
       |    / \
      /|\  
     /_|_\
    """]
        print(graphics[self.life])

    def typing(self):
        print(self.info)
        char = input("Zgadnij litere: ").upper()

        if len(char) == 1 and \
                char.isalpha() and \
                char not in self.used:
            self.info = ""
            self.used.append(char)
            return char

        else:
            if char in self.used:
                self.info = f"Już użyłeś: {char}"
            elif len(char) == 0:
                self.info = ""
            elif len(char) > 1:
                self.info = "Wpisz tylko jedną litere"
            elif not char.isalpha():
                self.info = f"{char} nie jest literą"
            else:
                self.info = "nieznany błąd :("
        return False

    def game(self):
        while True:
            self.cls()
            if self.cheating:
                print(self.password)

            self.draw()
            print("".join(self.n_password))

            if self.used:
                print(self.used)

            char = self.typing()
            if not char:
                continue

            # sprawdzanie indeksu na jakim znajduje się ta litera w hasle
            index = [i for i, x in enumerate(self.password) if x == char]
            if index:
                for i in index:
                    self.n_password[i] = char
            else:
                self.life += 1

            if self.life == 6 or "".join(self.n_password) == self.password:
                break

        self.result()

    def result(self):
        self.cls()
        self.draw()
        if self.life < 6 and "".join(self.n_password) == self.password:
            print(f"Wygrałeś!!!\n"
                  f"twoim hasłem jest: {self.password}")
        else:
            print(f"Przegrałeś :(\n"
                  f"twoim hasłem było: {self.password}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--input", required=False,
                    help="""Ścieżka do pliku z słowami.
                    Każde słowo w pliku musi być w osobnej linii.
                    """)

    ap.add_argument("-c", "--cheating", action='store_true', required=False,
                    help="""Pokazuje wylosowane hasło
                        """)

    args = vars(ap.parse_args())

    try:
        with open(args["input"], "r") as f:
            ff = f.readlines()
        words = [i.strip().upper() for i in ff]
    except:
        print("podany plik nie istnieje")
        input("Wciśnij Enter by zakończyć")
        exit()

    hangman(words, args["cheating"])
