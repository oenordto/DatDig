# Brukerhistorie g
#   Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute og kjøpe de billettene hen ønsker.
#       - Pass på at dere bare selger ledige plasser

import sqlite3
import os.path
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "TogDB.db")

con = sqlite3.connect(db_path)

# Sjekker om databasen er blitt koblet til riktig
if (con.total_changes == 0):
    print("Databasen er tilkoblet!")
else:
    raise Exception("Noe gikke galt med databasetilkoblingen:/")

cursor = con.cursor()

# Henter alle togruter i databasen og viser disse på et fint format
alle_togruter = cursor.execute(
    '''
    SELECT TogruteID, Togrutenavn FROM Togrute
    ORDER BY TogruteID
    '''
).fetchall()

print("Disse togrutene er registrert i vår database: ")
print("+------+------------------------------------------+")
print("| Tog  | Togrutenavn                              |")
print("+------+------------------------------------------+")
for togrute in alle_togruter:
    print("| {:<4} | {:<40} |".format(togrute[0], togrute[1]))
print("+------+------------------------------------------+")

# Henter de gyldige ID-ene for togruter, og spør bruker om ID
# til de har skrevet inn en gydlig en
gyldige_togruter = cursor.execute(
    '''
    SELECT TogruteID FROM Togrute
    '''
).fetchall()

print(gyldige_togruter)

while True:
    togrute = input("Hvilket tog ønsker du å reise med (skriv inn tallet): ")
    if not togrute.isdigit() or (int(togrute),) not in gyldige_togruter:
        print("Ugyldig togrute. Prøv igjen")
    else:
        break

# Samme prosedyre som det over, bare med hvor bruker ønsker å reise fra og til
gyldige_stasjoner = cursor.execute(
    '''
    SELECT jernbanestasjonNavn FROM Jernbanestasjon
    '''
).fetchall()

while True:
    startstasjon = input("Reiser fra: ")
    if (startstasjon,) not in gyldige_stasjoner:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

while True:
    sluttstasjon = input("Reiser til: ")
    if (sluttstasjon,) not in gyldige_stasjoner:
        print("Ugyldig stasjon. Prøv igjen")
    else:
        break

# Denne spørringen brukes til å sjekke om toget går over to datoer.
togrute_sjekk = cursor.execute(
    '''
    SELECT Avgang, Ankomst FROM Togrute
    WHERE TogruteID = ?
    ''', [togrute]
).fetchone()

# De to tilfellene (om et tog går over 1 eller 2 datoer) må håndteres ulikt
if togrute_sjekk[0] < togrute_sjekk[1]:
    # Første tilfellet er når toget går over kun 1 dato

    # Spørringen henter ut stasjonene for togruten i den rekkefølgen de blir besøkt
    rute_stopp = cursor.execute(
    '''
    SELECT * FROM
    (
        SELECT JernbanestasjonNavn, Avgang FROM Togrute
        JOIN Jernbanestasjon ON JernbanestasjonID = StartStasjon
        WHERE Togrute.TogruteID = ?

        UNION

        SELECT JernbanestasjonNavn, Ankomst FROM Togrute
        JOIN Jernbanestasjon ON JernbanestasjonID = SluttStasjon
        WHERE Togrute.TogruteID = ?

        UNION

        SELECT JernbanestasjonNavn, MellomStopp.Avgang FROM Togrute
        JOIN MellomStopp ON MellomStopp.TogruteID = Togrute.TogruteID
        JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = MellomStopp.JernbanestasjonID
        WHERE Togrute.TogruteID = ?
    )
        ORDER BY Avgang
    ''', [togrute, togrute, togrute]
    ).fetchall()

    # Finner index for stoppene i den sorterte listen over
    index_start = None
    index_stopp = None
    for stopp in rute_stopp:
        if stopp[0] == startstasjon:
            index_start = rute_stopp.index(stopp)
        if stopp[0] == sluttstasjon:
            index_stopp = rute_stopp.index(stopp)
    
    # Dersom togruten ikke er innom et av stoppene, eller er innom dem i feil
    # rekkefølge avsluttes programmet
    if index_start is None or index_stopp is None or index_stopp < index_start:
        print("Denne togruten går ikke denne strekningen")
        quit()
else:
    # Andre tilfellet er når toget går over 2 datoer

    rute_stopp = []

    # Henter stoppene toget er innom før midnatt i sortert rekkefølge 
    stopp_for_midnatt = (cursor.execute(
        '''
            SELECT * FROM
	        (
                SELECT JernbanestasjonNavn, Avgang FROM Togrute
                JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = Togrute.StartStasjon
	            WHERE TogruteID = ?

                UNION

                SELECT JernbanestasjonNavn,  MS.Avgang FROM Togrute
                JOIN MellomStopp  AS MS ON Togrute.TogruteID = MS.TogruteID
                JOIN Jernbanestasjon J ON J.JernbanestasjonID =  MS.JernbanestasjonID
	            Where MS.Avgang > Togrute.Avgang AND Togrute.TogruteID = ?
	        )
	        ORDER BY Avgang
        ''',[togrute, togrute]
    ).fetchall())
    
    # Henter stoppene toget er innom etter midnatt i sortert rekkefølge 
    stopp_etter_midnatt = cursor.execute(
        '''
        SELECT * FROM
        (
            SELECT JernbanestasjonNavn,  MS.Avgang FROM Togrute
            JOIN MellomStopp  AS MS ON Togrute.TogruteID = MS.TogruteID
            JOIN Jernbanestasjon J ON J.JernbanestasjonID =  MS.JernbanestasjonID
            Where MS.Avgang < Togrute.Avgang AND Togrute.TogruteID = ?

            UNION

            SELECT JernbanestasjonNavn, Ankomst FROM Togrute
            JOIN Jernbanestasjon ON Jernbanestasjon.JernbanestasjonID = Togrute.Sluttstasjon
            WHERE TogruteID = ?
        )
        ORDER BY Avgang
        ''', [togrute, togrute]
    ).fetchall()
    
    # Setter de to listene med sorterte stopp sammen for å få en fullstendig og sortert liste med stopp
    for row in stopp_for_midnatt:
        rute_stopp.append(row)
    for row in stopp_etter_midnatt:
        rute_stopp.append(row)
    
    # Samme sjekk som for det andre tilfellet.
    index_start = None
    index_stopp = None
    for stopp in rute_stopp:
        if stopp[0] == startstasjon:
            index_start = rute_stopp.index(stopp)
        if stopp[0] == sluttstasjon:
            index_stopp = rute_stopp.index(stopp)
    
    if index_start is None or index_stopp is None or index_stopp < index_start:
        print("Denne togruten går ikke denne strekningen")
        quit()

# Finner alle avgangsdatoer for togruten som er blitt oppgitt
avgangs_datoer = list(cursor.execute(
    '''
    SELECT DISTINCT dato FROM Togruteforekomst
    WHERE TogruteID = ?
    ''', [togrute]
    ).fetchall())

# Finner når togruten som bruker har oppgitt går fra startstasjonen som bruker har oppgitt.
avgang_startstasjon = cursor.execute(
    '''
    SELECT Avgang FROM (
	SELECT J.JernbanestasjonNavn, Avgang, TogruteID FROM Jernbanestasjon AS J
    JOIN Togrute ON J.JernbanestasjonID = StartStasjon

    UNION
    SELECT J.JernbanestasjonNavn, Ankomst, TogruteID FROM Jernbanestasjon AS J
    JOIN Togrute ON J.JernbanestasjonID = SluttStasjon

    UNION
    SELECT J.JernbanestasjonNavn, Avgang, TogruteID FROM Jernbanestasjon AS J
    JOIN mellomStopp ON J.JernbanestasjonID = MellomStopp.JernbanestasjonID
	)
	WHERE JernbanestasjonNavn = ? and TogruteID = ?
    ''', [startstasjon, togrute]
).fetchone()


while True:
    dato = input("Dato: ")
    # Ordner dato (gjør om fra datoen bruker skal ta tog, til datoen toget starter å gå)
    # dersom bruker tar et tog fra en stasjon toget er på etter midnatt.
    if avgang_startstasjon[0] < togrute_sjekk[0]:
        dato = (datetime.datetime.strptime(dato, '%Y-%m-%d').date() - datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
    if (dato,) not in avgangs_datoer:
        print("Ugyldig dato for denne strekningen. Prøv igjen")
    else:
        break

# Henter vognene for bruker sin togrute
vogner = cursor.execute(
    '''
    SELECT TogruteNavn, VognNr, AntallSovekupeer, AntallStolrader, AntallSeter FROM Togrute
    NATURAL JOIN Vogn
    LEFT OUTER JOIN Sovevogn ON Sovevogn.VognID = Vogn.VognID
    LEFT OUTER JOIN Sittevogn ON Sittevogn.VognID = Vogn.VognID
    WHERE Togrute.TogruteID = ?
    ORDER BY VognNr
    ''', [togrute]
    ).fetchall()

# Henter billetter for bruker sin togruteforekomst
billetter = cursor.execute(
    '''
    SELECT J1.JernbanestasjonNavn,  J2.JernbanestasjonNavn, AntallSovekupeer, VognNr, PlassNr FROM Billett
    JOIN Togruteforekomst ON Billett.TogruteforekomstID = Togruteforekomst.TogruteforekomstID
    JOIN Togrute ON Togrute.TogruteID = Togruteforekomst.TogruteID
    JOIN Jernbanestasjon AS J1 ON Billett.StartStasjon = J1.JernbanestasjonID
    JOIN Jernbanestasjon AS J2 ON Billett.Sluttstasjon = J2.JernbanestasjonID
	JOIN Vogn ON Vogn.VognID = Billett.VognID
	LEFT OUTER JOIN Sovevogn ON Sovevogn.VognID = Vogn.VognID
    LEFT OUTER JOIN Sittevogn ON Sittevogn.VognID = Vogn.VognID
    WHERE Togrute.TogruteID = ? AND Togruteforekomst.dato = ?
    ''', [togrute, dato]
).fetchall()

# Finner vi alle plasser (De som er bestilt og de som er ledige)
alle_sitte_billetter = []
alle_sove_billetter = []
for vogn in vogner:
    if (vogn[2]== None):
        for stasjon in rute_stopp:
            for i in range (1, vogn[4] + 1):
                alle_sitte_billetter.append(["sitteplass", vogn[1], i, stasjon[0]])
    else:
        for i in range(1, vogn[2]*2 + 1):
            alle_sove_billetter.append(["soveplass", vogn[1], i])

# Finner alle plasser som er blitt bestilt
bestilte_sitte_billetter = []
bestilte_sove_billetter = []
for billett in billetter:
    if(billett[2] == None):
        billett_startstasjon = billett[0]
        billett_sluttstasjon = billett[1]
        test = False
        for stasjon in rute_stopp:
            if (test or stasjon[0] == billett_startstasjon):
                if (stasjon[0] == billett_sluttstasjon):
                    break
                else:
                    bestilte_sitte_billetter.append(["sitteplass", billett[3], billett[4], stasjon[0]])
                    test = True
    else:
        bestilte_sove_billetter.append(["soveplass", billett[3], billett[4]])

# Fjerner alle bestilte sitteplasser fra alle_sitte_billetter
for billett in bestilte_sitte_billetter:
    alle_sitte_billetter.remove(billett)

# Fjerner alle bestilte soveplass fra alle_sove_billetter
for bestilt_billett in bestilte_sove_billetter:
    if bestilt_billett in alle_sove_billetter:
        alle_sove_billetter.remove(bestilt_billett)
        # Dersom en seng er tatt skal hele kupeen være opptatt.
        if bestilt_billett[2] % 2 == 1:
            alle_sove_billetter.remove([bestilt_billett[0], bestilt_billett[1], bestilt_billett[2] + 1])
        else:
            alle_sove_billetter.remove([bestilt_billett[0], bestilt_billett[1], bestilt_billett[2] - 1])

# okkuperer_setet er alle stasjonen der setet må være ledig for at bruker skal kommer seg hele veien
okkuperer_setet = []
test = False
for stasjon in rute_stopp:
    if(test or startstasjon == stasjon[0]):
        if stasjon[0] == sluttstasjon:
            break
        okkuperer_setet.append(stasjon[0])
        test = True

# Finner alle ledige plasser for reisen til bruker
ledige_seter = []
ledige_soveplasser = []
for vogn in vogner:
    if vogn[2] == None:
        for i in range (1, vogn[4] + 1):
            for stasjon in okkuperer_setet:
                entry = ["sitteplass", vogn[1], i, stasjon]
                if entry not in alle_sitte_billetter:
                    break
                if okkuperer_setet[-1] == stasjon:
                    ledige_seter.append([vogn[1], i,])
    else:
        for billett in alle_sove_billetter:
            ledige_soveplasser.append([billett[1], billett[2]])

# Dersom det ikke er noen ledige plasser er toget fullt og programmet avsluttes
if len(ledige_seter) < 1 and len(ledige_soveplasser) < 1:
    print("Det er ingen ledige seter:/")
    quit()

# Skriver ut de ledige setene
if len(ledige_seter) > 0:
    print("De ledige setene er: ")
    for plass in ledige_seter:
        print("Vogn:" + str(plass[0]) + "\tSete:" + str(plass[1]))

# Skriver ut de ledige soveplassene
if len(ledige_soveplasser) > 0:
    print("De ledige soveplassene er: ")
    for plass in ledige_soveplasser:
        print("Vogn: " + str(plass[0]) + "\tSeng: " + str(plass[1]))

# Nå kan bruker bestille billettene bruker ønsker
bestilte_billetter = []
while True:
    while True:
        vogn = input("Ønsket vogn: ")
        sete = input("Ønsket plass: ")
        try:
            bestilling = [int(vogn), int(sete)]
            if (bestilling in ledige_seter or bestilling in ledige_soveplasser):
                break
            else:
                print("Plassen var ugyldig, opptatt eller allerede reservert av deg.")
        except:
            print("Du må gi kun tall. Prøv igjen")
    
    bestilte_billetter.append(bestilling)

    if bestilling in ledige_seter:
        ledige_seter.remove(bestilling)
    if bestilling in ledige_soveplasser:
        ledige_soveplasser.remove(bestilling)

    user_input = input("Ønsker du å kjøpe flere billetter?(y/n)")
    while user_input not in ["y", "n"]:
        print("Denne inputen var ugyldig. Prøv på nytt.")
        user_input = input("Ønsker du å kjøpe flere billetter?(y/n)")
    if user_input == "n":
        break

# Henter epostene som er registrert i databasen
gyldige_eposter = cursor.execute(
'''
    SELECT Epost FROM Kunde
'''
).fetchall()

print(gyldige_eposter[0])

# Før kjøpet blir registrert trenger vi å vite hvilken bruker det er som bestiller dette
while True:
    epost = input("Før vi gjennomfører bestillingen trenger vi din e-post: ")
    if epost not in gyldige_eposter[0]:
            print("Denne emaile er ikke registrert i vårt system. Prøv igjen")
    else:
        break

# Finner kunden tilhørende mailaddressen
kunde = cursor.execute(
'''
    SELECT KundeNr FROM Kunde
    WHERE epost = ?
''', [epost]
).fetchone()

# Oppretter KundeOrdren
cursor.execute(
''' 
INSERT INTO KundeOrdre VALUES (null, date(), time(), ?)
''', [kunde[0]])
con.commit()

# Alle spørringene under er informasjon vi trenger for å opprette billetter i databasen
ordrenr = cursor.execute(
    '''
    SELECT max(OrdreNr) From KundeOrdre
    '''
).fetchone()

togruteforekomstID = cursor.execute(
    '''
    SELECT TogruteforekomstID FROM Togruteforekomst
    WHERE dato = ? AND togruteID = ?
    ''', [dato, togrute]
).fetchone()

startstasjonID = cursor.execute(
    '''
    SELECT JernbanestasjonID FROM Jernbanestasjon
    WHERE JernbanestasjonNavn = ?
    ''', [startstasjon]
).fetchone()

sluttstasjonID = cursor.execute(
    '''
    SELECT JernbanestasjonID FROM Jernbanestasjon
    WHERE JernbanestasjonNavn = ?
    ''', [sluttstasjon]
).fetchone()

# Legger til alle de bestilte bilettene i databasen
for billett in bestilte_billetter:
    vognID = cursor.execute(
    '''
    SELECT VognID FROM Vogn
    Natural JOIN Togrute 
    WHERE TogruteID = ? and VognNr = ?
    ''', [togrute, billett[0]]
    ).fetchone()

    cursor.execute(
    ''' 
    INSERT INTO Billett VALUES (null, ?, ?, ?, ?, ?, ?)
    ''', [billett[1], vognID[0], ordrenr[0], togruteforekomstID[0], startstasjonID[0], sluttstasjonID[0]])

    con.commit()
con.close()

print("Dine billetter er bestilt:)")