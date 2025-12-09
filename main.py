import os


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


# lògica de xifrat
def xifrar_missatge(): 
    print("\n--- CARREGANT ROTORS ---")

    r1 = carregar_rotor("Rotor1.txt")
    r2 = carregar_rotor("Rotor2.txt")
    r3 = carregar_rotor("Rotor3.txt")

    # per continuar els tres han de estar carregats bé
    if r1 and r2 and r3:
        print("[OK] Tots els rotors carregats correctament!")
        print(f"Rotor 1: {r1['permutacio']} (Notch: {r1['notch']})")
        print(f"Rotor 2: {r2['permutacio']} (Notch: {r2['notch']})")
        print(f"Rotor 3: {r3['permutacio']} (Notch: {r3['notch']})")
    else:
        print("[ERROR] No es pot continuar sense els rotors vàlids.")
    

def desxifrar_missatge():
    print("Has triat: Desxifrar missatge")
    # lògica de desxifrat

def editar_rotors():
    print("Has triat: Editar rotors")
    # configuració dels rotors

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