# ENIGMA_GrauGerard_YansulYansul

**Descripció**

Aquesta programa simula una versio simplificada de la màquina enigma. Aquest programa permet a l'usuari xifrar i desxifrar missatges utilitzant tres rotors. Funciona a taravés del terminal i té dos arxius diferents per guardar els resultatas. El projecte s'ha creat per practicar la programació en Python i entendre com funciona la xifratge basat en rotors.

**Estructura del projecte**

- main.py : aquest fitxer conté el programa i el menú de visualització per a l'usuario.
- Rotor1.txt, Rotor2.txt, Rotor3.txt : aquest fitxer contenen la permutació de lletres i les entrades de cada rotor.
- Missatge.txt : Emmagatzema el missatge original sense espais abans de l'encriptció
- Xifrat.txt: Emmagatzema el missatge xifrat agrupat en blocs de cinc lletres
- Missatge_desxifrat.txt: emmagatzema el mitssatge desxifrat.

**Com funciona el programa**

El programa encripta cada lletra del missatge. Per a cada lletra, els rotors giren i el senyal passa a través del tres rotors en ordre. Després, el senyal passa per un reflector i torna a fer girar els rotors en ordre invers. Com que els rotor giren, la xifratge canvia cada lletra.
Per desxifrar un missatge, s'ha de utilitzar la mateixa configuració del rotor i la posició inicial.

**Com executar el programa**

En primer lloc, assegureu-vos que teniu installat Python al vostre ordinador. A continuació, obriu la terminal al fitxer del projecte i executeu el programa amb "main.py" i un menú apareixerá a la pantalla.

**Opcions del menú**

El programa mostra un menú amb quatre opcions:
- **Xifrar missatge:** permeti a l'usuario introduir un missatge i una configuració inicial del rotor i el missatge xifrat s'emmagatzema a Xifrat.txt
- **Desxifrar missatge:** Això desxifra el missatge emmagatzemat a Xifrat.txt utilitzant la mateixa configuració  inicial. El resultat mostrat a la pantalla es guardarà a Mitssatge_desxifrat.txt
- **Editar rotors:** permet a l'usuari modificar la permutació del rotor i la posició de les entrades manualment.
- **Sortir**: tancar el programa


**Configuració del rotor**

Cada rotor es defineix per una permutació de 26 lletres majúscules (A-Z) i una lletra de tall que controla quan el següent rotor gira.
