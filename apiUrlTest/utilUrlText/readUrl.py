#import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import time


#Definir el metodo para obtener solo el texto
from apiUrlTest.utilUrlText.Exceptions import CustomException


def getOnlyText(url:str,amount_words:int=5) :
    """
    Función que regresa un json con la información requerida por el usuario, en el caso ingresa una url y la cantidad de listar de las primeras n palabras que mas se
    repiten.
    :param url: dirección de la pagina web que el usuario quiere buscar
    :param amount_words: cantidad de palabras que el usuario desea
    :return: regresa el json.
    """
    #Obtener el texto de la pagina dada por paramentro
    try:
        Alltext = urlopen(url).read()
        beautiful_soup = BeautifulSoup(Alltext, features="html.parser")
    except:
        raise CustomException("Error al momento de recolectar la información de la URL "+url)
    #extraer todas las ocurriencias que sean script o style
    for script in beautiful_soup(["script", "style"]):
        script.extract()

    FilterText = beautiful_soup.get_text()

    #Conseguir el array sin los saltos de linea  y convirtiendo  todas las ocurrencias en lowercase para estandarizar los datos
    array=[a.replace("\n","").lower() for a in FilterText.split(" ")]
    #Eliminar aquellas posiciones en donde sea igual a vacio(ningun caracter) o si no es alfabetico
    array2=list(filter(lambda a: not(a == "" or not(a.isalpha())), array))


    #crear dataframe
    df = pd.DataFrame(columns=["Word","count"])
    df['Word'] = array2
    df=df.fillna(1)
    df = df.groupby(['Word'])['count'].sum().reset_index()
    newDf=df.sort_values(by=["count"],ascending=False)
    newDf.index = np.arange(1, len(newDf)+1)
    # ---------------------

    if(len(newDf.index)>amount_words):
        newDf=newDf.head(amount_words)

    returnJson = newDf.to_json(orient="index")
    parsed = json.loads(returnJson)
    return(parsed)


"""

 formas de llamar al metodo getOnlyText

var1="https://narrativabreve.com/2017/02/el-cuervo-allan-poe-en-estado-puro.html"
print("___________________________ LINE _____________")
print(json.dumps(getOnlyText(var1,1233333),indent=4))



var2="https://www.hola.com/"
print("___________________________ LINE _____________")
print(json.dumps(getOnlyText(var2),indent=4))


var3="https://en.wikipedia.org/wiki/History_of_the_United_States"
print("___________________________ LINE _____________")
print(json.dumps(getOnlyText(var3,12),indent=4))


"""