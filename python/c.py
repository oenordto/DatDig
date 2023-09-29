# Brukerhistorie c
#   For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.

import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "TogDB.db")

con = sqlite3.connect(db_path)

# Sjekker om databasen er blitt koblet til riktig
if (con.total_changes == 0):
    print("Databasen er tilkoblet!")
else:
    raise Exception("Noe gikke galt med databasetilkoblingen:/")

cursor = con.cursor()

#Henter alle jernbanestasjon navn som ligger i databasen
gyldige_stasjoner = cursor.execute(
    '''
    SELECT jernbanestasjonNavn FROM Jernbanestasjon
    '''
).fetchall()

gyldige_dager = cursor.execute(
    '''
    SELECT Ukedag FROM Ukedag
    '''
).fetchall()

#Hvis input ikke sammsvarer med verdiene som ligger i databasen
#blir det forespurt en ny input fra bruker
while True:
    jernbanestasjon = input("Skriv in jernbanestasjon: ")
    if (jernbanestasjon,) not in gyldige_stasjoner:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

while True:
    dag = input("Skriv in dag: ")
    if (dag,) not in gyldige_dager:
        print("Ugyldig dag. Prøv igjen")
    else:
        break

#Spørringen returnerer alle togruter som er innom den jernbanestasjonen på den gitte dagen
rows = cursor.execute('''
    SELECT TogruteID, TogruteNavn FROM Togrute AS T
    NATURAL JOIN Togrute_Delstrekning AS TD
    NATURAL JOIN Delstrekning AS D
    JOIN Jernbanestasjon AS J ON J.JernbanestasjonID = D.Stasjon1
    NATURAL JOIN Togrute_Ukedag as TU
    NATURAL JOIN Ukedag
    WHERE Ukedag = ? AND JernbanestasjonNavn = ?
    UNION
    SELECT TogruteID, TogruteNavn FROM Togrute AS T
    NATURAL JOIN Togrute_Delstrekning AS TD
    NATURAL JOIN Delstrekning AS D
    JOIN Jernbanestasjon AS J ON J.JernbanestasjonID = D.Stasjon2
    NATURAL JOIN Togrute_Ukedag as TU
    NATURAL JOIN Ukedag
    WHERE Ukedag = ? AND JernbanestasjonNavn = ?
    ''', [dag, jernbanestasjon, dag, jernbanestasjon]).fetchall()

#Printer ut dataen som returneres fra databasen på et fint og leselig format
if rows:
    print("Disse togrutene er innom {} på {}er.".format(jernbanestasjon, dag.lower()))
    print("+------+------------------------------------------+")
    print("| Tog  | Togrutenavn                              |")
    print("+------+------------------------------------------+")
    for row in rows:
        print("| {:<4} | {:<40} |".format(row[0], row[1]))
    print("+------+------------------------------------------+")
else:
    print("Det er ingen togruter innom {} på {}er.".format(jernbanestasjon, dag.lower()))

con.close()