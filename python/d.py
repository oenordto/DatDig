# Brukerhistorie d
#   Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
#   utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
#   returneres, sortert på tid.

# TODO: Skrive antagelse om 24 timers togruter

import sqlite3
import os.path
import datetime
import time

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


#Hvis input ikke sammsvarer med verdiene som ligger i databasen
#blir det forespurt en ny input fra bruker
while True:
    start_stasjon = input("Startstasjon: ")
    if (start_stasjon,) not in gyldige_stasjoner:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

while True:
    slutt_stasjon= input("Startstasjon: ")
    if (slutt_stasjon,) not in gyldige_stasjoner:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

#Hvis input ikke er på riktig format blir det forespurt en ny input fra bruker
while True:
    dato_avreise = input("Dato for avreise (yyyy-mm-dd): ")
    try:
        gyldig_format = bool(datetime.datetime.strptime(dato_avreise, '%Y-%m-%d'))
    except ValueError:
        gyldig_format = False

    if not gyldig_format:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

while True:
    klokkeslett_avreise = input("Tidligste klokkeslett for avreise: ")
    try:
        gyldig_format = time.strptime(klokkeslett_avreise, '%H:%M') 
    except ValueError:
        gyldig_format = False

    if not gyldig_format:
        print("Ugyldig klokkeslett. Prøv igjen")
    else:
        break

dato_pluss_en_dag = str(datetime.datetime.strptime(dato_avreise, '%Y-%m-%d').date() + datetime.timedelta(days = 1))

#Henter alle nattog fra databasen
togruterID_natt = cursor.execute(
    '''
    SELECT TogruteID FROM Togrute
    WHERE Avgang > Ankomst
    '''
).fetchall()

sortert_nattog = []

#Spørringen returnerer startstasjon og alle mellomstopp som er på togruten før midnatt
for ID in togruterID_natt:
    stopp_for_ID = []
    stopp_for_midtnatt = cursor.execute(
        '''
            SELECT * FROM
	        (
                SELECT TogruteID, TogruteNavn, Avgang, JernbanestasjonNavn FROM Togrute
                JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = Togrute.StartStasjon
	            WHERE TogruteID = ?

                UNION

                SELECT Togrute.TogruteID, TogruteNavn,  MS.Avgang, JernbanestasjonNavn  FROM Togrute
                JOIN MellomStopp  AS MS ON Togrute.TogruteID = MS.TogruteID
                JOIN Jernbanestasjon J ON J.JernbanestasjonID =  MS.JernbanestasjonID
	            Where MS.Avgang > Togrute.Avgang AND Togrute.TogruteID = ?
	        )
	        ORDER BY Avgang
            ''', [ID[0], ID[0]]
    ).fetchall()

    for stopp in stopp_for_midtnatt:
        stopp_for_ID.append(list(stopp))


    #Spørringen returnerer sluttstasjon og alle mellomstopp som er på togruten etter midnatt
    stopp_etter_midtnatt = cursor.execute(
        '''
        SELECT * FROM
        (
            SELECT Togrute.TogruteID, TogruteNavn,  MS.Avgang, JernbanestasjonNavn, Togrute.TogruteID  FROM Togrute
            JOIN MellomStopp  AS MS ON Togrute.TogruteID = MS.TogruteID
            JOIN Jernbanestasjon J ON J.JernbanestasjonID =  MS.JernbanestasjonID
            Where MS.Avgang < Togrute.Avgang AND Togrute.TogruteID = ?

            UNION

            SELECT TogruteID, TogruteNavn, Ankomst, JernbanestasjonNavn, Togrute.TogruteID FROM Togrute
            JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = Togrute.Sluttstasjon
            WHERE TogruteID = ?
        )
        ORDER BY Avgang
        ''', [ID[0], ID[0]]
    ).fetchall()

    for stopp in stopp_etter_midtnatt:
        stopp_for_ID.append(list(stopp))
    
    #Sortert liste med alle nattog og tilhørende mellomstopp.
    sortert_nattog.append(stopp_for_ID)


#Henter ID for alle nattog i den sorterte listen
for nattog in sortert_nattog:
    datoer = cursor.execute(
        '''
        SELECT Dato FROM Togruteforekomst
        WHERE TogruteID = ?
        ''',[nattog[0][0]]
    ).fetchall()

    #Beregner dato for til alle mellomstopp
    for dato in datoer:
        for stopp in nattog:
            if stopp[2] < nattog[0][2]:
                stopp.append(str(datetime.datetime.strptime(dato[0], '%Y-%m-%d').date() + datetime.timedelta(days = 1)))
            else:
                stopp.append(str(datetime.datetime.strptime(dato[0], '%Y-%m-%d').date()))

togruter_man_kan_ta = []


#Luker ut togruter som går motsatt veg eller som ikke passer til dato spesifikasjonene
for togrute in sortert_nattog:
    teller = 0
    midlertidig = []
    for stopp in togrute:
        for i in range(len(stopp) -4 ):
            if (start_stasjon in stopp and ((stopp[4 + i] == dato_avreise and stopp[2] >= klokkeslett_avreise)  or
                                             stopp[4 + i] == str(datetime.datetime.strptime(dato_avreise, '%Y-%m-%d').date() + datetime.timedelta(days = 1)) )  ):
                teller = 1
                midlertidig.append([stopp[0], stopp[1], stopp[2], stopp[3], stopp[4+i], stopp[4]])
            if  slutt_stasjon in stopp and teller == 1:
                for element in midlertidig:
                    togruter_man_kan_ta.append(element)
                midlertidig = []
                teller = 0

#Returnerer alle togruter som ikke er et nattog 
togruter_dag = cursor.execute(
    '''
         SELECT * FROM
 (
	SELECT TogruteforekomstID, TogruteNavn, Avgang, JernbanestasjonNavn,  Togruteforekomst.Dato, Togrute.TogruteID FROM Togrute
    NATURAL JOIN Togruteforekomst
    JOIN Jernbanestasjon ON JernbanestasjonID = StartStasjon
    WHERE Togrute.Avgang<Togrute.Ankomst AND ((Togruteforekomst.Dato = ? AND Avgang > ?) or Togruteforekomst.Dato = ? )

    UNION

    SELECT TogruteforekomstID, TogruteNavn, Ankomst, JernbanestasjonNavn, Togruteforekomst.Dato, Togrute.TogruteID FROM Togrute
    NATURAL JOIN Togruteforekomst
    JOIN Jernbanestasjon ON JernbanestasjonID = SluttStasjon
    WHERE Togrute.Avgang<Togrute.Ankomst AND ((Togruteforekomst.Dato = ? AND Ankomst > ?) or Togruteforekomst.Dato = ? )

    UNION

    SELECT TogruteforekomstID, TogruteNavn, MellomStopp.Avgang, JernbanestasjonNavn, Togruteforekomst.Dato, Togrute.TogruteID FROM Togrute
    NATURAL JOIN Togruteforekomst
    JOIN MellomStopp ON MellomStopp.TogruteID = Togrute.TogruteID
    JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = MellomStopp.JernbanestasjonID
    WHERE Togrute.Avgang<Togrute.Ankomst AND ((Togruteforekomst.Dato = ? AND MellomStopp.Avgang > ?) or Togruteforekomst.Dato = ? )
)
	ORDER BY TogruteforekomstID, TogruteNavn, Avgang
 
    ''', [dato_avreise, klokkeslett_avreise, dato_pluss_en_dag, 
          dato_avreise, klokkeslett_avreise, dato_pluss_en_dag,
            dato_avreise, klokkeslett_avreise, dato_pluss_en_dag]
).fetchall()

#Legger alle dag-togrutene inn i en dictonary
dict = {}
for stopp in togruter_dag:
    liste = [stopp[3], stopp[2]]
    if not stopp[0] in dict: 
        dict[stopp[0]] = [liste]
    elif not stopp[3] in dict[stopp[0]] :
         dict[stopp[0]].append(liste)
    else:
        pass 

#Luker ut togruter som går motsatt veg
element_liste = []
id_liste = []
for key, value in dict.items():
    for element in value:  
        element_liste.append(element[0])   
        if start_stasjon in element_liste and slutt_stasjon in element_liste:
            if element_liste.index(start_stasjon) < element_liste.index(slutt_stasjon):
                id_liste.append(key)
                break
    element_liste.clear()

#Legger alle togruter med all info inn i ny liste
ny_liste = []
for id in id_liste:
    for togrute in togruter_dag:
        if togrute[0] == id and togrute[3] == start_stasjon:
            ny_liste.append(togrute)
            break

#Merger nattog med dagtogene
for element in ny_liste:
    togruter_man_kan_ta.append(element)

#Sorterer togruter_man_kan_ta etter dato og avgangstid
sortert_liste = sorted(togruter_man_kan_ta, key=lambda x: (x[4], x[2]))

#Printer ut dataen i sortert_liste på et fint og leselig format
if sortert_liste:
    print("Tog-ruter fra {} til {}:".format(start_stasjon, slutt_stasjon))
    print("+------+--------------+--------------+------------+------------+")
    print("| Tog  | Fra stasjon  | Til stasjon  | Dato       | Avgangstid |")
    print("+------+--------------+--------------+------------+------------+")
    for x in sortert_liste:
        print("| {:<4} | {:<12} | {:<12} | {:<10} | {:<10} |".format(x[5], x[3], slutt_stasjon, x[4], x[2]))
    print("+------+--------------+--------------+------------+------------+")
else:
    print("Det er ingen tog som går fra {} til {} på dette tidspunktet".format(start_stasjon, slutt_stasjon))

con.close()