import os.path

while True:
    print("Trykk enter hvis du vil avslutte programmet.")
    userstory = input("Hvilken brukerhistorie ønsker du å utføre? (c, d, e, g eller h): ")

    if len(userstory.strip()) == 0: 
        break

    if userstory in ["c", "d", "e", "g", "h"]: 
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        exec(open(os.path.join(BASE_DIR, userstory + ".py")).read())
    else:
        print("Beklager, brukerhistorien du oppga var ikke gyldig:/")
