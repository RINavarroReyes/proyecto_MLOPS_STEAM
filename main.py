from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from collections import Counter

app =FastAPI()

df = pd.read_json('datasets/df_limpio.json', lines=True)

#http://127.0.0.1:8000

@app.get("/getGenero/{anio}")
def genero(anio: str):
    # Filtrar el DataFrame para obtener solo las filas del año dado
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Unir todas las listas de géneros en una sola lista
    all_genres = [genre for genres_list in filtered_df['genres'] for genre in genres_list]
    # Contar la frecuencia de cada género en la lista
    genre_counts = Counter(all_genres)
    # Obtener los N géneros más repetidos
    top_genres = genre_counts.most_common(5)
    # Devolver los géneros como una lista
    return {'Lista de generos mas comunes': [genre for genre, count in top_genres]}

@app.get("/getJuegos/{anio}")
def juegos(anio: str):
    # Filtrar el DataFrame para obtener solo las filas del año dado
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Extraer los nombres de los juegos para las filas filtradas y guardarlos en una lista
    games_list = filtered_df['app_name'].tolist()
    # Devolver la lista con los nombres de los juegos
    return {'Lista de juegos': games_list}

@app.get("/getSpecs/{anio}")
def specs(anio: str):
    # Filtrar el DataFrame para obtener solo las filas del año dado
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Unir todas las listas de géneros en una sola lista
    all_specs = [spec for specs_list in filtered_df['specs'] for spec in specs_list]
    # Contar la frecuencia de cada género en la lista
    spec_counts = Counter(all_specs)
    # Obtener los N géneros más repetidos
    top_specs = spec_counts.most_common(5)
    # Devolver los géneros como una lista
    return {'Lista de aspectos que mas se repiten': [spec for spec, count in top_specs]}    

@app.get("/getEarlyacces/{anio}")
def earlyacces(anio: str):
    # Filtrar el DataFrame para obtener solo las filas del año dado
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Contar el número de videojuegos con "early access" (valor True) en la columna 'early_access'
    early_access_count = filtered_df['early_access'].sum()
    # Devolver el número de videojuegos con "early access"
    return {'Numero de Earlyacces': str(early_access_count)}


lista_sentiments = ['Mixed', 'Very Positive', 'Positive', 'Mostly Positive','Mostly Negative', 'Overwhelmingly Positive', 'Negative', 'Very Negative', 'Overwhelmingly Negative']

@app.get("/getSentiment/{anio}")
def sentiment(anio: str):
    # Filtrar el DataFrame para obtener solo las filas del año dado
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Utilizar value_counts para obtener la cantidad de ocurrencias de cada valor en la columna 'sentiment'
    sentiment_counts = filtered_df['sentiment'].value_counts()
    # Filtrar los resultados para obtener solo los valores de sentiments de la lista
    filtered_sentiments_counts = sentiment_counts[sentiment_counts.index.isin(lista_sentiments)]
    # Convertir el resultado a un diccionario
    sentiments_dict = filtered_sentiments_counts.to_dict()
    return {'Analisis de sentimiento': sentiments_dict}

@app.get("/getMetascore/{anio}")
def metascore(anio: str):
    filtered_df = df[df['anio_lanzamiento'] == anio]
    # Convertir los valores de la columna 'metascore' a valores numéricos (float)
    filtered_df['metascore'] = pd.to_numeric(filtered_df['metascore'], errors='coerce')
    # Ordenar las filas por el metascore de mayor a menor
    sorted_df = filtered_df.sort_values(by='metascore', ascending=False)
    # Seleccionar las 5 primeras filas con los metascores más altos para ese año
    top_5_metascores = sorted_df.head(5)
    top_5_juegos = top_5_metascores['app_name'].tolist()
    return {'Top 5 de juegos con mayor metascore': top_5_juegos}

#print(genero('2019'))
#print(juegos('2017'))
#print(specs('2017'))
#print(earlyacces('2017'))
#print(sentiment('2017'))
#print(metascore('2017'))
