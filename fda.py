from email.message import EmailMessage
import smtplib
from automata.fa.dfa import DFA
import re
from pathlib import Path
import os
import ssl


dfa = DFA(
    allow_partial=True,
    states={'A', 'B', 'C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','A1','A2','A0'},
    input_symbols={'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','_','.'},
    transitions={
        'A0': {'A':'A','B':'A','D':'A','E':'A','F':'A','G':'A','H':'A','I':'A','J':'A','K':'A','L':'A','N':'A','O':'A','P':'A','Q':'A','R':'A','S':'A','T':'A','U':'A','W':'A','X':'A','Y':'A','Z':'A','a':'A','b':'A','c':'A','d':'A','e':'A','f':'A','g':'A','h':'A','i':'A','j':'A','k':'A','l':'A','m':'A','n':'A','o':'A','p':'A','q':'A','r':'A','s':'A','t':'A','u':'A','v':'A','w':'A','x':'A','y':'A','z':'A','0':'A','1':'A','2':'A','3':'A','4':'A','5':'A','6':'A','7':'A','8':'A','9':'A','_':'A'},
        'A': {'A':'A','B':'A','D':'A','E':'A','F':'A','G':'A','H':'A','I':'A','J':'A','K':'A','L':'A','N':'A','O':'A','P':'A','Q':'A','R':'A','S':'A','T':'A','U':'A','W':'A','X':'A','Y':'A','Z':'A','a':'A','b':'A','c':'A','d':'A','e':'A','f':'A','g':'A','h':'A','i':'A','j':'A','k':'A','l':'A','m':'A','n':'A','o':'A','p':'A','q':'A','r':'A','s':'A','t':'A','u':'A','v':'A','w':'A','x':'A','y':'A','z':'A','0':'A','1':'A','2':'A','3':'A','4':'A','5':'A','6':'A','7':'A','8':'A','9':'A','_':'A', 'M' : 'B', 'C' : 'K', 'V' : 'V'},
        'B': {'o' : 'C'},
        'C': {'d' : 'D'},  
        'D': {'e' : 'E'},
        'E': {'l' : 'F'},
        'F': {'o' : 'G'},
        'G': {'.' : 'H'},
        'H': {'c' : 'I'},
        'I': {'s' : 'J'},
        'K': {'o' : 'L'},
        'L': {'n' : 'M'},
        'M': {'t' : 'N'},
        'N': {'r' : 'O'},
        'O': {'o' : 'P'},
        'P': {'l' : 'Q'},
        'Q': {'a' : 'R'},
        'R': {'d' : 'S'},
        'S': {'o' : 'T'},
        'T': {'r' : 'U'},
        'U': {'.' : 'H'},
        'V': {'i' : 'W'},
        'W': {'s' : 'X'},
        'X': {'t' : 'Y'},
        'Y': {'a' : 'Z'},
        'Z': {'.' : 'A1'},
        'A1': {'t' : 'A2'},
        'A2': {'s' : 'J'},
    },
    initial_state='A0',
    final_states={'J'}
)

def leerArchivo(file):
    with open(file) as f:
        lines = f.read().splitlines()
        return lines

def validador(cadena, origen):
    if dfa.accepts_input(cadena):
        return ""
    else:
        return "La cadena '" + str(cadena) + "', originada en " + str(origen) + ", es invalida (Verifique que "+ str(origen) +" no contiene alguna de las siguientes letras: 'M','V' o 'C'). Corrijalo de inmediato y vuelva a ejecutar el programa.\n"

def validarElementosEnAmbasListas(lista, carpeta):
    reporte = ""
    for elemento in lista:
        reporte += "El documento '" + elemento + "', que se encuentra en la carpeta '/" + str(carpeta) + "', no ha sido programado para ser creado.\n"
    return reporte

def faltaCrear(lista, carpeta):
    reporte = ""
    for elemento in lista:
        reporte += "Hace falta crear el documento '" + elemento + "', que se debera encontrar en la carpeta '/" + str(carpeta)+ ".\n"
    return reporte

def enviarCorreo(reporte):
    sender = "lorapemo@gmail.com"
    rec = "lorapemo@gmail.com"
    password = ""
    subject = "Reporte creación incorrecta"
    message= reporte

    em= EmailMessage()
    em['From']= sender
    em['To']= rec
    em['Subject']= subject
    em.set_content(message)

    context = ssl.create_default_context()  
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender,rec,em.as_string())
def main():
    reporte=""
    modelo = Path("Modelo")
    vista = Path("Vista")
    controlador = Path("Controlador")
    my_file= Path("Objetos_A_Crear.txt")
    filesModelo = []
    filesVista = []
    filesControlador = []

    print("Recuerde que en " + str(my_file) + " no debe de incluír ninguna de las siguientes letras: 'M', 'V', o 'C'.")

    for objeto in leerArchivo(my_file):
        filesModelo.append(objeto + "Modelo.cs" )
        filesVista.append(objeto + "Vista.ts" )
        filesControlador.append(objeto + "Controlador.cs" )
    for file in filesModelo:
        reporte += validador(file, my_file)
    for file in filesVista:
        reporte += validador(file, my_file)
    for file in filesControlador:
        reporte += validador(file, my_file)

    listDirVista = os.listdir(vista)
    lista = [x for x in listDirVista if x not in filesVista]
    reporte += validarElementosEnAmbasListas(lista, vista)
    lista = [x for x in filesVista if x not in listDirVista]
    reporte += faltaCrear(lista, vista)

    listDirModelo = os.listdir(modelo)
    lista = [x for x in listDirModelo if x not in filesModelo]
    reporte += validarElementosEnAmbasListas(lista, modelo)
    lista = [x for x in filesModelo if x not in listDirModelo]
    reporte += faltaCrear(lista, modelo)

    listDirControlador = os.listdir(controlador)
    lista = [x for x in listDirControlador if x not in filesControlador]
    reporte += validarElementosEnAmbasListas(lista, controlador)
    lista = [x for x in filesControlador if x not in listDirControlador]
    reporte += faltaCrear(lista, controlador)
    if reporte == "":
        print("Sin errores por reportar!")
    else:
        print("Un reporte con errores ha sido enviado a su correo.")
        enviarCorreo(reporte)

main()