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
    # el rotor u sempre es mou primer
    moure_r1 = True
    moure_r2 = False
    moure_r3 = False

    # busca on e´s el notch en entre el cero i el vint-i-cinc
    notch1 = ALFABET.find(r1['notch'])
    notch2 = ALFABET.find(r2['notch'])

    # si el rotor u està en el notch, arrosega el segon
    if r1['pos'] == notch1:
        moure_r2 = True

    # si el rotor dos està en el notch, arrossega el rotor tres
    if r2['pos'] == notch2:
        moure_r3 = True

    # executa els moviments sumant un i fent mòdul 26 per si passem de la z
    if moure_r1: r1['pos'] = (r1['pos'] + 1) % 26
    if moure_r2: r2['pos'] = (r2['pos'] + 1) % 26
    if moure_r3: r3['pos'] = (r3['pos'] + 1) % 26

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

        # nomes pot tenir vint-i-sis lletres i nomes de l'a a la z
        if len(permutacio) != 26 or not permutacio.isalpha():
            print(f"[ERROR] {nom_fitxer}: permutació incorrecta. Calen 26 lletres úniques A-Z. ")
            return None
        
        # si no s'especifica notch, el notch sera z
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

    # guarda el fitxer
    guardar_fitxer("Xifrat.txt", resultat_final)
    
    # resultat en pantalla despres de xifrar
    num_lletres = len(resultat)
    num_grups = len(resultat_final.split())

    # mostra el numero de lletres i grups per pantalla
    print(f'[OK] Missatge xifrat a "Xifrat.txt" ({num_lletres} lletres, {num_grups} grups de 5)')
    

def desxifrar_missatge():
    print("Has triat: Desxifrar missatge")
    xifrar_missatge(pregunta="Escriu el missatge xifrat: ")


def editar_rotors():
    print("\n--- EDITAR ROTORS ---")
    print("1. Modificar Rotor 1")
    print("2. Modificar Rotor 2")
    print("3. Modificar Rotor 3")
    print("4. Tornar enrere")
    """
    Modifica els rotors
    """

    # pregunta quin rotor volem modificar
    opcio = input("Quin rotor vols canviar? ")

    # depenent de l'opcio seleccionada modificarem un roto o un altre, o en el cas quatre tornarem enrrere
    nom_rotor = ""
    if opcio == "1":
        nom_rotor = "Rotor1.txt"
    elif opcio == "2":
        nom_rotor = "Rotor2.txt"
    elif opcio == "3":
        nom_rotor = "Rotor3.txt"
    elif opcio == "4":
        return
    else:
        print("[ERROR] Opció incorrecta.")
        return
    
    print(f"Atenció: Estàs a punt de canviar la configuració de {nom_rotor}")

    # demana la nova permutacio per al rotor sel·leccionat
    print("Escriu la nova permutació (26 lletres seguides i sense repetir-se):")
    perm = input("> ").upper().strip()

    # valida que son vint-i-sis lletres
    if len(perm) != 26 or not perm.isalpha():
        print("[ERROR] Han de ser 26 lletres exactes de la A a la Z.")
        return
    
    # valida que no hi ha cap lletra repetida
    if len(set(perm)) != 26:
        print("[ERROR] No poden haver-hi lletres repetides.")
        return
    
    # demana el notch
    notch = input("Escriu la lletra del Notch: ").upper().strip()
    if len(notch) != 1 or notch not in ALFABET:
        print("[AVÍS] Notch invàlid, es posarà 'Z'.")
        notch = "Z"

    # sobrescriu el rotor
    contingut = f"{perm}\n{notch}"
    guardar_fitxer(nom_rotor, contingut)
    print(f"[OK] {nom_rotor} actualitzat correctament.")


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