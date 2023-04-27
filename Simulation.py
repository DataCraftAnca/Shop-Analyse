import pandas as pd
import numpy as np
import random
from itertools import product


anzahl = 10
startspielstaende = list(product([i for i in range(40)],[i for i in range(40)]))
print(startspielstaende)
risikos = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
spielstaerke_team_a = 0.6
spielstaerke_team_b = 0.3

ergebnisse = []


for startspielstand in startspielstaende:
    print(f"startspielstand ist {startspielstand}")
    for risiko in risikos:
        print(f"risiko ist {risiko}")
        for spiel in range(anzahl):
            print(f"spiel nr ist {spiel}")
            an_der_reihe = random.sample(["team_a", "team_b"], 1)[0]
            team_a_score = startspielstand[0]
            team_b_score = startspielstand[1]
            while max(team_a_score, team_b_score)<21 or abs(team_a_score - team_b_score) <2:
                print(f"punkte a {team_a_score}", f"punkte b {team_b_score}")
                if an_der_reihe == "team_a":
                    angriffsball = np.random.normal(spielstaerke_team_a, 0.1 + risiko) #würde tausend Bälle mit Spielstärke (Mittelpunkt) mu und Risiko (Streuung) sigma generieren
                else:
                    angriffsball = np.random.normal(spielstaerke_team_b,0.1 + risiko)
                rallye = True
                i=0
                #print(i)
                while rallye == True:
                    i+=1
                    #print(i)
                    #print(angriffsball)
                    if angriffsball < 0: #AUS
                        if an_der_reihe == "team_a":
                            an_der_reihe = "team_b"
                        else:
                            an_der_reihe = "team_a"
                        #print("aus")
                        rallye = False
                    else: # DRIN
                        if an_der_reihe == "team_a":
                            if angriffsball > spielstaerke_team_b + 0.2:
                                team_a_score +=1
                                rallye = False
                            else: # ball nicht stark genung für punkt. Rallye geht weiter, anderes team an der reihe
                               an_der_reihe = "team_b"
                        else:#team_b muss dran sein
                            if angriffsball > spielstaerke_team_a + 0.2:
                                team_b_score +=1
                                rallye = False
                            else: #ball nicht stark genung für punkt. Rallye geht weiter, anderes team an der reihe
                                an_der_reihe = "team_a"
                    if an_der_reihe == "team_a":
                        angriffsball = np.random.normal(spielstaerke_team_a, 0.1 + risiko)
                    else:
                        angriffsball = np.random.normal(spielstaerke_team_b, 0.1 + risiko)
            if team_a_score > team_b_score:
                ergebnisse.append([1, risiko, startspielstand[0],startspielstand[1]])
            else:
                ergebnisse.append([0, risiko, startspielstand[0],startspielstand[1]])
df = pd.DataFrame(ergebnisse, columns= ["team_a_gewonnen", "risiko", "startspielstand_a","startspielstand_b"])
print(df)


import openpyxl
df.to_excel("simulation.xlsx")




