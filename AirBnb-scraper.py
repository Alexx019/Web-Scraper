import re
import requests
import csv
from colorama import Fore

#colores para la consola
color_name = Fore.WHITE
color_ciudad = Fore.MAGENTA
color_precio = Fore.BLUE
color_valoracion = Fore.CYAN
color_amarillo = Fore.YELLOW
color_verde = Fore.GREEN
color_rojo = Fore.RED
reset_color = Fore.RESET

#sacamos el contenido de la página web
website = 'https://www.airbnb.es/s/London--United-Kingdom/homes?adults=1&place_id=ChIJdd4hrwug2EcRmSrV3Vo6llI&refinement_paths%5B%5D=%2Fhomes'
resultado = requests.get(website)
content = resultado.text

#la información de cada lugar está entre:
#"__typename":"StaySearchResult" y "__typename":"StaySearchResult"

#sacamos bloques de texto con esa información
patron = r'__typename":"StaySearchResult"[\w\W]*?"__typename":"StaySearchResult"'
bloques = re.findall(patron, str(content))
    
#cada bloque tiene la info del nombre del lugar, la ciudad, el precio, etc

#el nombre del lugar está entre "name":" y ",
patron_nombre = r'"name":"[\w\W]*?",'

#la ciudad está entre "title":" y ",
patron_ciudad = r'"title":"[\w\W]*?",'

#el precio está entre "price":" y ",
patron_precio = r'"price":"[\w\W]*?",'

#la valoración media está entre "avgRatingLocalized": y ",
patron_valoracion = r'"avgRatingLocalized":"[\w\W]*?",'

#para cada bloque, sacamos el nombre, la ciudad, el precio y la valoración media
for i in bloques:
    nombre = re.findall(patron_nombre, i)
    ciudad = re.findall(patron_ciudad, i)
    precio = re.findall(patron_precio, i)
    valoracion = re.findall(patron_valoracion, i)
    
    #solo permitimos un resultado por bloque
    nombre = nombre[0:1]
    ciudad = ciudad[0:1]
    precio = precio[0:1]
    valoracion = valoracion[0:1]
    
    #quitamos las comillas y el "name":""
    for j in nombre:
        str = j.replace('"name":"', '')
        str = str.replace('",', '')
        
        #quitamos las , para que no haya problemas con el csv
        str = str.replace(',', '')
        nombre = str
        
        print (color_name + "Nombre: ", str + reset_color)
        fila = str + ", "
    
    #quitamos las comillas y el "title":""
    for j in ciudad:
        str = j.replace('"title":"', '')
        str = str.replace('",', '')
        
        #quitamos las , para que no haya problemas con el csv
        str = str.replace(',', '')
        
        #evitamos que sea "Desglose del precio"
        if str != "Desglose del precio":
            print (color_ciudad + "Ciudad: ", str + reset_color)
            fila = fila + str + ", "
        
    #quitamos las comillas y el "price":""    
    for j in precio:
        str = j.replace('"price":"', '')
        str = str.replace('",', '')
        
        #quitamos las , para que no haya problemas con el csv
        str = str.replace(',', '')
        
        print (color_precio + "Precio: ", str + reset_color)
        fila = fila + str + ", "
    
    #quitamos las comillas y el "avgRatingLocalized":""
    for j in valoracion:
        str = j.replace('"avgRatingLocalized":"', '')
        str = str.replace('",', '')
        
        #quitamos las , para que no haya problemas con el csv
        str = str.replace(',', '\'')
        
        print (color_valoracion + "Valoración: ", str + reset_color)
        fila = fila + str + ", "
    
    print (color_amarillo + "----------------------------------------")
    print ("----------------------------------------" + reset_color)
    
    #abrirmos el fichero csv y sacamos la lista de nombres
    with open("airbnb.csv", "r") as fichero:
        lector = csv.reader(fichero, delimiter = ",")
        lista = [f[0] for f in lector]
    
    #si el nombre del lugar no está en el fichero, lo añadimos
    if nombre not in lista:
        fichero = open("airbnb.csv", "a")
        
        #escribimos la fila en el fichero
        fichero.write(fila + "\n")  
        print (color_verde + nombre + " Añadido al fichero" + reset_color)
    else:
        print (color_rojo + nombre + " Ya está en el fichero" + reset_color)
    
    print ("\n")
        
