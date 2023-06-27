import sqlite3

class Pojisteny:
    def __init__(self, id, jmeno, prijmeni, vek, telefon):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.vek = vek
        self.telefon = telefon


    def __str__(self):
        return f"{self.jmeno}\t{self.prijmeni}\t{self.vek}\t{self.telefon}"


class Evidence:
    def __init__(self):
        self.conn = sqlite3.connect("pojisteni.db")
        self.vytvor_tabulku()

    def vytvor_tabulku(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pojisteni
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, jmeno TEXT, prijmeni TEXT, telefon TEXT, vek INTEGER)''')
        self.conn.commit()

    def pridej_pojisteneho(self):
        jmeno = input("Zadejte jméno pojistného: ")
        prijmeni = input("Zadejte příjmení: ")
        telefon = input("Zadejte telefonní číslo: ")
        vek = int(input("Zadejte věk: "))

        pojisteny = Pojisteny(None, jmeno, prijmeni, vek, telefon)
        self.insert_pojisteny(pojisteny)

        print("Data byla uložena. Pokračujte libovolnou klávesou...")

    def insert_pojisteny(self, pojisteny):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO pojisteni (jmeno, prijmeni, vek, telefon) VALUES (?, ?, ?, ?)",
                       (pojisteny.jmeno, pojisteny.prijmeni, pojisteny.vek, pojisteny.telefon))
        self.conn.commit()

    def vypis_pojistene(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, jmeno, prijmeni, vek, telefon FROM pojisteni")
        rows = cursor.fetchall()

        if not rows:
            print("Neexistují žádní pojistní.")

        for row in rows:
            pojisteny = Pojisteny(*row)
            print(pojisteny)

        input("Pokračujte libovolnou klávesou...")

    def vyhledej_pojisteneho(self):
        jmeno = input("Zadejte jméno pojistného: ")
        prijmeni = input("Zadejte příjmení: ")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pojisteni WHERE jmeno = ? AND prijmeni = ?", (jmeno, prijmeni))
        row = cursor.fetchone()

        if row:
            pojisteny = Pojisteny(*row)
            print(pojisteny)
        else:
            print("Pojistný nebyl nalezen.")

        input("Pokračujte libovolnou klávesou...")

    def __del__(self):
        self.conn.close()

def main():
    evidence = Evidence()

    while True:
        print("_________________________")
        print("Evidence pojistných")
        print("_________________________")
        print()
        print("Vyberte si akci:")
        print("1 - Přidat nového pojistného")
        print("2 - Vypsat všechny pojistné")
        print("3 - Vyhledat pojistného")
        print("4 - Konec")

        volba = input()

        if volba == "1":
            evidence.pridej_pojisteneho()
        elif volba == "2":
            evidence.vypis_pojistene()
        elif volba == "3":
            evidence.vyhledej_pojisteneho()
        elif volba == "4":
            break
        else:
            print("Neplatná volba. Zadejte prosím číslo od 1 do 4.")

if __name__ == "__main__":
    main()