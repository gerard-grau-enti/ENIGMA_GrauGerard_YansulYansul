def xifrar_missatge():
    print("Has triat: Xifrar missatge")
    # lògica de xifrat

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