import random
import os


class Hangman:
    def __init__(self, words_list, cheating=False):
        self.cls()
        self.password = random.choice(words_list).upper()
        self.n_password = ["_"] * len(self.password)
        # Gdy cheating jest ustawiony na True gra wyświetla hasło
        self.cheating = cheating

        # W przypadku podania przez gracza hasła składającego sie z kilku słów oddzielonych od siebie " " lub "-"
        # gra automatycznie pokazuje je w ukrytym haśle
        index = [i for i, x in enumerate(self.password) if x in [" ", "-"]]
        if index:
            for i in index:
                self.n_password[i] = " "

        self.life = 0
        self.info = ""
        self.used = []
        self.game()

    # funkcja czyszcząca terminal działa w systemie windows i linux
    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    # funkcja odpowiedzialna za wyświetlanie oktualnego poziomu żyć gracza
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

    # funkcja odpowiedzalna za pobieranie litery od gracza oraz sprawdzenie jej poprawności.
    # funkcja przyjmuje tylko pojedyńczą literę, która nie była jeszcze wykorzystana.
    # Poprawne litery są zwracane, w przypadku błędu zwracany jest False, który w game() oznacza wywołanie continue
    # co skutkuje ponownym wywołanie funkcji typing().
    def typing(self):
        # wyświetlanie komunikatu błednego wprowadzenia litery.
        # w przypadku braku błędu komunikat jest pusty ("")
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
            # po w pisaniu flagi -c lub --cheating wyświetlane będzie zgadywane hasło
            if self.cheating:
                print(self.password)

            # Wyświetlanie liczby szans w formie grafik, zakodowanego hasła na które są nanoszone odgadnięte litery oraz
            # wykorzystane litery
            self.draw()
            print(" ".join(self.n_password))
            if self.used:
                print(self.used)

            # pobieranie liter od gracza w przypadku niepoprawnego wprowadzenia char przyjmuje wartość False co
            # zaczyna nową pętlę.
            char = self.typing()
            if not char:
                continue

            # sprawdzanie indeksu na jakim znajduje się ta litera w haśle i podmienianie w zakodowanym haśle.
            # Gdzy nie ma takiej litery w haśle liczba żyć sie zwiększa o jeden
            index = [i for i, x in enumerate(self.password) if x == char]
            if index:
                for i in index:
                    self.n_password[i] = char
            else:
                self.life += 1

            # Gra kończy sie gdy liczba żyć równa się 6 lub gracz odgadł całe hasło
            if self.life == 6 or "".join(self.n_password) == self.password:
                break

        # wyowałnie wyświetlania wyników
        self.result()

    # wyświetlanie wyników
    # rysunek oznaczający liczbę żle podanch liter, oraz komunikat o wygranej lub przegranej
    # wraz z hasłem jakie zgadywał
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
    # pakiet argparse pozwala dodać funkcje flag do programu
    import argparse

    ap = argparse.ArgumentParser()
    # flaga do podania pliku z hasłami
    ap.add_argument("-i", "--input", required=False,
                    help="""Ścieżka do pliku z słowami.
                    Każde słowo w pliku musi być w osobnej linii.
                    """)
    # wybranie tego parametru pokazuje wylosowane hasło (przydatne tylko w celach pokazowych)
    ap.add_argument("-c", "--cheating", action='store_true', required=False,
                    help="""Pokazuje wylosowane hasło
                        """)
    # pozwala podać własne hasło do gry w wisielca
    ap.add_argument("-w", "--word", required=False,
                    help="Podaj swoje hasło do gry w wisielca.")

    # odczytywanie podanych flag i uruchamianie gry w wielca
    args = vars(ap.parse_args())

    words = ["pies", "kot", "szynszyla", "mysz"]

    if args["word"]:
        words = [args["word"], args["word"]]

    if args["input"]:
        with open(args["input"], "r") as f:
            ff = f.readlines()
        words = [i.strip().upper() for i in ff]

    Hangman(words, args["cheating"])
