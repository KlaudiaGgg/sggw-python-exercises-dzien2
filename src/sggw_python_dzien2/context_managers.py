
# Ćwiczenie praktyczne 1 - Context Manager


# 1. Logger
class Logger:

    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Koniec sekcji logowania")


# 2. FileWriter
class FileWriter:

    def __init__(self, sciezka):
        self.sciezka = sciezka

    def __enter__(self):
        self.plik = open(self.sciezka, "w", encoding="utf-8")
        return self.plik

    def __exit__(self, exc_type, exc_value, traceback):
        self.plik.close()

        if exc_type is not None:
            print(f"Błąd podczas zapisu: {exc_value}")

        return False


# 3. SafeDivision
class SafeDivision:

    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is ZeroDivisionError:
            print("Nie można dzielić przez zero")
            return True

        return False


# Testowanie klas
if __name__ == "__main__":

    # Test Logger
    with Logger():
        print("Wykonuję operację wewnątrz bloku")

    # Test FileWriter
    with FileWriter("test.txt") as plik:
        plik.write("Pierwszy zapis do pliku.")

    # Test FileWriter - obsługa wyjątku
    try:
        with FileWriter("test_error.txt") as plik:
            plik.write("Test wyjątku")
            raise ValueError("Przykładowy błąd")

    except ValueError:
        print("Wyjątek nie został stłumiony.")

    # Test SafeDivision
    with SafeDivision() as dzielenie:
        print(dzielenie.divide(10, 2))

    with SafeDivision() as dzielenie:
        dzielenie.divide(10, 0)

    print("Program działa dalej.")

