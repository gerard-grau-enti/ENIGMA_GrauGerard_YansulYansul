import os

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


def guardar_fitxer(nom_fitxer, contingut):
    """
    Guardar text en el fitxer
    """
    try:
        with open(nom_fitxer, 'w') as f:
            f.write(contingut)
        print(f"[INFO] Guardat a {nom_fitxer}")
    except:
        print(f"[ERROR] No s'ha pogut guardar {nom_fitxer}")

def moure_rotors(r1, r2, r3):
    """
    Mou els rotors
    """
    # el rotor tres sempre es mou
    moure_r3 = True
    moure_r2 = False
    moure_r1 = False

    # busca on e´s el notch en entre el cero i el vint-i-cinc
    notch3 = ALFABET.find(r3['notch'])
    notch2 = ALFABET.find(r2['notch'])

    # si el rotor tres està en el notch, arrosega el segon
    if r3['pos'] == notch3:
        moure_r2 = True

    # si el rotor dos està en el notch, arrossega el primer i ha ell mateix
    if r2['pos'] == notch2:
        moure_r1 = True
        moure_r2 = True

    # executa els moviments sumant un i fent mòdul 26 per si passem de la z
    if moure_r3: r3['pos'] = (r3['pos'] + 1) % 26
    if moure_r2: r2['pos'] = (r2['pos'] + 1) % 26
    if moure_r1: r1['pos'] = (r1['pos'] + 1) % 26

def passar_pel_rotor(index_entrada, rotor, es_anada):
    """
    Calcula per quina lletra surt el senyal
    """
    desplacament = rotor['pos']

    if es_anada:
        # camí d'anada (entrada -> rotor)
        index_ajustat = (index_entrada + desplacament) % 26
        lletra = rotor['permutacio'][index_ajustat]
        index_brut = ALFABET.find(lletra)
        index_sortida = (index_brut - desplacament) % 26
        return index_sortida
    else:
        # camí de tornada (rotor -> entrada)
        index_ajustat = (index_entrada + desplacament) % 26
        lletra_alfabet = ALFABET[index_ajustat]
        pos_permutacio = rotor['permutacio'].find(lletra_alfabet)
        index_sortida = (pos_permutacio - desplacament) % 26
        return index_sortida

def carregar_rotor(nom_fitxer):
    """
    LLegeix un fitxer de rotor i retorna la seva configuració
    Retorna un diccionari amb 'permutacio' i 'notch' o None si falla
    """
    if not os.path.exists(nom_fitxer):
        print(f"[ERROR] El fitxer {nom_fitxer} no existeix. ")
        return None
    
    try:
        with open(nom_fitxer, 'r') as f:
            dades = f.readlines()

        if not dades:
            print(f"[ERROR] El fitxer {nom_fitxer} està buit. ")
            return None
        
        permutacio = dades[0].strip().upper()

        if len(permutacio) != 26 or not permutacio.isalpha():
            print(f"[ERROR] {nom_fitxer}: permutació incorrecta. Calen 26 lletres úniques A-Z. ")
            return None
        
        if len(dades) > 1:
            notch = dades[1].strip().upper()
        else:
            notch = 'Z'

        return {"permutacio": permutacio, "notch": notch}
    
    except Exception as e:
        print(f"[ERROR] Error llegint {nom_fitxer}: {e}")
        return None


# llògica de xifrat
def xifrar_missatge(pregunta="Escriu el missatge: "): 
    print("\n--- CARREGANT ROTORS ---")
    """
    Xifra els missatges
    """

    # carrega els fitxers
    r1 = carregar_rotor("Rotor1.txt")
    r2 = carregar_rotor("Rotor2.txt")
    r3 = carregar_rotor("Rotor3.txt")

    if not (r1 and r2 and r3):
        print("[ERROR] No es pot continuar sense els rotors vàlids.")
        return
    
    # demana la configuracio inicial
    inici = input("Configuració inicial (ex: AAA): ").upper().replace(" ", "")
    if len(inici) != 3:
        inici = "AAA"
        print("Format incorrecte. Es fara servir AAA.")
    
    # afegeix la posició inicial als diccionaris
    r1['pos'] = ALFABET.find(inici[0])
    r2['pos'] = ALFABET.find(inici[1])
    r3['pos'] = ALFABET.find(inici[2])

    # demana el missatge
    missatge = input(pregunta).upper()

    # guarda el missatge sense espais
    missatge_net = ""
    for c in missatge:
        if c in ALFABET:
            missatge_net += c
    guardar_fitxer("Missatge.txt", missatge_net)

    resultat = ""

    # bucle principal lletra per lletra
    for lletra in missatge_net:
        # gira rotors
        moure_rotors(r1, r2, r3)

        # passa les lletres a numero
        idx = ALFABET.find(lletra)

        # circuit d'anada r3 -> r2 -> r1
        idx = passar_pel_rotor(idx, r3, True)
        idx = passar_pel_rotor(idx, r2, True)
        idx = passar_pel_rotor(idx, r1, True)

        # reflector
        lletra_ref = REFLECTOR_B[idx]
        idx = ALFABET.find(lletra_ref)

        # circuit de tornada
        idx = passar_pel_rotor(idx, r1, False)
        idx = passar_pel_rotor(idx, r2, False)
        idx = passar_pel_rotor(idx, r3, False)

        # guarda resultat
        resultat += ALFABET[idx]

    # agrupa en grups de cinc lletres
    resultat_final = ""
    comptador = 0
    for lletra in resultat:
        resultat_final += lletra
        comptador += 1
        if comptador == 5:
            resultat_final += " "
            comptador = 0
    
    print(f"\nMISSATGE XIFRAT: {resultat_final}")
    guardar_fitxer("Xifrat.txt", resultat_final)

def desxifrar_missatge():
    print("Has triat: Desxifrar missatge")
    xifrar_missatge(pregunta="Escriu el missatge xifrat: ")


def editar_rotors():
    print("\n--- CREAR NOU ROTOR ---")
    """
    Genera un nou rotor
    """

    # demana el nom del nou rotor
    nom_nou_rotor = input("Nom del nou rotor (ex: Rotor4.txt): ")
    if not nom_nou_rotor.endswith(".txt"):
        nom_nou_rotor += ".txt"

    # demana la permutacio
    print("Escriu les 26 lletres de l'alfabet desordenades (totes juntes):")
    perm = input("> ").upper().strip()

    # comprovacio de que hi han vint-i-sis lletres
    if len(perm) != 26 or not perm.isalpha():
        print ("[ERROR] Han de ser 26 lletres exactes.")
        return
    
    # comprovacio de que no hi ha lletres repetides
    if len(set(perm)) != 26:
        print("[ERROR] No pots repetir lletres.")
        return
    
    # demana el notch
    notch = input("Escriu la lletra del Notch: ").upper().strip()
    if len(notch) != 1 or notch not in ALFABET:
        print("[AVÍS] Notch incorrecte, s'usarà 'Z' per defecte.")
        notch = "Z"
    
    # guarda el fitxer
    contingut = f"{perm}\n{notch}"
    guardar_fitxer(nom_nou_rotor, contingut)
    print(f"[ÈXIT] Rotor creat correctament: {nom_nou_rotor}")

def mostrar_menu():
    continuar = True
    while continuar:
        print("\n--- MÀQUINA ENIGMA ---")
        print("1. Xifrar missatge")
        print("2. Desxifrar missatge")
        print("3. Editar rotors")
        print("4. Sortir")
        
        opcio = input("Tria una opció: ")

        if opcio == "1":
            xifrar_missatge()
        elif opcio == "2":
            print("Per desxifrar, introdueix la mateixa configuració i el text xifrat.")
            desxifrar_missatge()
        elif opcio == "3":
            editar_rotors()
        elif opcio == "4":
            print("Adéu!")
            continuar = False
        else:
            print("Opció incorrecta. Torna-ho a provar.")

# programa inici
if __name__ == "__main__":
    mostrar_menu()