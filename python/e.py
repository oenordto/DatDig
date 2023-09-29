# Brukerhistorie e
#   En bruker skal kunne registrere seg i kunderegisteret.

import sqlite3
from sqlite3 import IntegrityError
import re
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "TogDB.db")

con = sqlite3.connect(db_path)

if (con.total_changes == 0):
    print("Databasen er tilkoblet!")
else:
    raise Exception("Noe gikke galt med databasetilkoblingen:/")

cursor = con.cursor()

print("Kunde må fylle inn:")

#Sjekker at input verdiene er på riktig format
while True:
    navn = input("Navn: ")
    if  not re.match("^[A-Za-zÆØÅæøå\- ]+$", navn):
        print("Ugyldig navn. Prøv igjen")
    else:
        break

while True:
    epost = input("Mail adresse: ")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", epost):
        print("Ugyldig mail adresse. Prøv igjen")
    else:
        break

while True:
    tlf = input("Telefonnummer: ")
    if not re.match(r"^\d{8}$", tlf):
        print("Ugyldig telefonnummer. Prøv igjen")
    else:
        break

#Legger til kunden i databasen så lenge epost og telefonnummer ikke allerede er registrert i databasen
try:
    rows = cursor.execute(
        ''' INSERT INTO Kunde VALUES (null, ?, ?, ?)''', [navn, epost, tlf]
    )
    con.commit()
    print("Hei " + navn + "!\nDu er nå regirstrert i kunderegisteret med mail adresse: " + epost + " og telefonnummer " + tlf)
except IntegrityError:
    print("Ops, epost eller telefonnummer er allerede registrert:/")

con.close()