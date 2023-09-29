# Brukerhistorie h
#   For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
#   reiser.

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

#Henter ut alle registrerte mail adresser i databasen
gyldige_mail_adresser = cursor.execute(
    '''
    SELECT Epost FROM Kunde
    '''
).fetchall()

#Sjekker at input er en registrert mail adresse i databasen
while True:
    epost = input("Skriv inn din mail: ")
    if (epost,) not in gyldige_mail_adresser:
        print(epost + " er ikke registrert i våre systemer. Prøv igjen")
    else:
        break

#Returnerer informasjon om alle fremtidige reiser til brukeren
rows = cursor.execute('''
    SELECT * FROM(
	SELECT  Kunde.Navn,  Epost,  KjopsDato, KjopsKlokkeslett, TogruteNavn, PlassNr, VognNr, Dato, J1.JernbanestasjonNavn  AS StartStasjon , J2.JernbanestasjonNavn  AS SluttstasjonStasjon , TogruteforekomstID, Avgang FROM Kunde
    NATURAL JOIN KundeOrdre
	NATURAL JOIN Billett
	NATURAL JOIN Togruteforekomst
	JOIN Togrute ON Togrute.TogruteID = Togruteforekomst.TogruteID
	JOIN Jernbanestasjon AS J1 ON J1.JernbanestasjonID = Billett.StartStasjon
	JOIN Jernbanestasjon AS J2 ON J2.JernbanestasjonID = Billett.SluttStasjon
    JOIN Vogn ON Billett.VognID = Vogn.VognID
    WHERE Epost = ?  AND (Togruteforekomst.Dato > date() OR Togruteforekomst.Dato = date() AND Avgang >= time())    
	)
	ORDER BY TogruteforekomstID  
    ''', [epost]).fetchall()

#Printer dataen på et fint format
if rows:
    print("Her er kjøpene du har gjort for fremtidige reiser:")
    for x in rows:
        print("+-------------------------------------------------------------+")
        print(" Navn: {:<4} \n Mail adresse: {:<20} \n Togrutenavn: {:<12} \n Kjøpsdato: {:<20} \n Kjøps klokkeslett: {:<12} \n Vogn nummer: {:<20} \n Plass nummer: {:<20} \n Start stasjon: {:<20} \n Slutt stasjon: {:<11} \n Dato for avreise: {:<20} \n Tid for avreise: {:<20}".format(x[0], x[1], x[4], x[2], x[3], x[6], x[5], x[8], x[9], x[7], x[11], "", "", "", "", "", "", "", "", "", "", ""))
        print("+-------------------------------------------------------------+")
else:
    print("Du har foreløpig ingen fremtidige reiser.")

con.close()