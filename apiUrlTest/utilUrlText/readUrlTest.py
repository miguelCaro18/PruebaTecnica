#import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time



#Definir el metodo para obtener solo el texto
def getOnlyText(url:str) -> str:
    #Obtener el texto de la pagina dada por paramentro
    Alltext = urlopen(url).read()
    beautiful_soup = BeautifulSoup(Alltext, features="html.parser")

    #extraer todas las ocurriencias que sean script o style
    for script in beautiful_soup(["script", "style"]):
        script.extract()

    FilterText = beautiful_soup.get_text()

    #Conseguir el array sin los saltos de linea  y convirtiendo  todas las ocurrencias en lowercase para estandarizar los datos
    array=[a.replace("\n","").lower() for a in FilterText.split(" ")]
    #Eliminar aquellas posiciones en donde sea igual a vacio(ningun caracter) o si no es alfabetico
    array2=list(filter(lambda a: not(a == "" or not(a.isalpha())), array))
    print("------------------")
    print((array2))
    print("-------------TAMAÑO ES -----")
    print(len(array2))
    array3=array2.copy()

    # ---------------------  Comenzar WHILE
    t0 = time.time()
    palabras = {}
    while (True):
        if (array2[0] in palabras):
            palabras[array2[0]] += 1
        else:
            palabras[array2[0]] = 1
        del array2[0]
        if (len(array2) == 0):
            break
    ordenadas=sorted(palabras.items(), key=lambda x: x[1])
    t1 = time.time()

    # ---------------------




    # --------------------- Comenzar DATAFRAME
    t2 = time.time()
    df = pd.DataFrame(columns=["Word","count"])
    df['Word'] = array3
    df=df.fillna(1)
    df = df.groupby(['Word'])['count'].sum().reset_index()
    newDf=df.sort_values(by=["count"],ascending=False)
#    newDf=newDf.reset_index(drop=True)
    t3 = time.time()
    # ---------------------

    # ---------------------  Comenzar Prueba2
    t4 = time.time()
    palabras3={a: array3.count(a) for a in set(array3)}
    # palabras2 = {}
    # for i in set(array3):
    #     palabras2[i]=array3.count(i)

    ordenadas2=sorted(palabras3.items(), key=lambda x: x[1])
    t5 = time.time()

    # ---------------------


    print("TIEMPO TOMADO DEL WHILE ES ->",t1-t0)
    print("TIEMPO TOMADO DEL PANDAS  ES ->",t3-t2)
    print("TIEMPO TOMADO DEL PRUEBA2  ES ->", t5 - t4)


    print("El largo del WHILE es  ->",len(palabras))
    print("El largo del PANDAS es  ->",len(newDf.index))
    print("El largo del PRUEBA2 es  ->", len(palabras3))



    print("-----RESULTADO-----")
    print("DATAFRAME ____________________-")
    print(newDf.head())
    print("PALABRAS ____________________-")
    print(ordenadas)
    print("PRUEBA2 ____________________-")
    print(ordenadas2)


# #cantidad de texto = 2836 palabras encontradas
# TIEMPO TOMADO DEL WHILE ES -> 0.001041412353515625 MEJOR
# TIEMPO TOMADO DEL PANDAS  ES -> 0.004391670227050781
# TIEMPO TOMADO DEL PRUEBA2  ES -> 0.02381134033203125
getOnlyText("https://narrativabreve.com/2017/02/el-cuervo-allan-poe-en-estado-puro.html")


#cantidad de texto = 1738 palabras encontradas
# TIEMPO TOMADO DEL WHILE ES -> 0.0005414485931396484 MEJOR
# TIEMPO TOMADO DEL PANDAS  ES -> 0.0033659934997558594
# TIEMPO TOMADO DEL PRUEBA2  ES -> 0.010129451751708984
getOnlyText("https://www.hola.com/")


#cantidad de texto = 23275 palabras encontradas
# TIEMPO TOMADO DEL WHILE ES -> 0.03606104850769043
# TIEMPO TOMADO DEL PANDAS  ES -> 0.012851715087890625 MEJOR
# TIEMPO TOMADO DEL PRUEBA2  ES -> 0.7630164623260498
var2="https://en.wikipedia.org/wiki/History_of_the_United_States"
getOnlyText(var2)

#El mejor con mayor cantidad de palabras es pandas, para datos pequeños while