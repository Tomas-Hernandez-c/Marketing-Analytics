#Netflix analysis
import pandas as pd
df = pd.read_csv("C:/Users/tohec/Desktop/netflix_titles.csv")

#Evaluación de los datos faltantes
print("Valores nulos por columna:")
print(df.isnull().sum())

#Evaluación de las filas duplicadas
print("Filas duplicadas:", df.duplicated().sum())

#Tipos de datos de las columnas
print("Tipos de datos:")
print(df.dtypes)

# Reemplazar los valores nulos en 'director', 'cast' y 'country' con 'Unknown'
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

# Eliminar filas con valores nulos en 'rating', 'duration' y 'data_added'
df = df.dropna(subset=['rating', 'duration', 'date_added'])

print(df.isnull().sum())

#Cantidad de filas y columnas
print("Cantidad de filas y columnas:", df.shape)

#Nombre de las variables (columnas)
print("Variables incluidas:", df.columns.tolist())

#Rango de fechas de cuándo se ingresó la información
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df_clean = df.dropna(subset=['date_added'])
fecha_mas_antigua_date_added = df_clean['date_added'].min()
print(fecha_mas_antigua_date_added)

fecha_mas_reciente_date_added =df_clean['date_added'].max()
print(fecha_mas_reciente_date_added)

#Rango de fechas de cuándo se lanzó el contenido
fecha_mas_antigua_release_year = df_clean['release_year'].min()
print(fecha_mas_antigua_release_year)
fecha_mas_reciente_release_year = df_clean['release_year'].max()
print(fecha_mas_reciente_release_year)

# Filtrar los TV Shows
tv_shows = df[df['type'] == 'TV Show']

# Filtrar las Movies
movies = df[df['type'] == 'Movie']

# Función para extraer duración en minutos para Movies
def extraer_duracion_minutos(duracion):
    if 'min' in str(duracion):
        # Extraer el número de minutos
        minutos = int(''.join(filter(str.isdigit, str(duracion))))
        return minutos

# Aplicar la función a las Movies
# Filtrar las Movies y hacer una copia para evitar el warning
movies = df[df['type'] == 'Movie'].copy()

# Aplicar la función a las Movies de manera segura con .loc
movies.loc[:, 'duracion_minutos'] = movies['duration'].apply(extraer_duracion_minutos)

# Función para extraer cantidad de temporadas para TV Shows
def extraer_temporadas(duracion):
    if 'Season' in str(duracion):
        # Extraer el número de temporadas
        temporadas = int(''.join(filter(str.isdigit, str(duracion))))
        return temporadas

# Aplicar la función a los TV Shows
# Filtrar los TV Shows y hacer una copia para evitar el warning
tv_shows = df[df['type'] == 'TV Show'].copy()

# Aplicar la función a los TV Shows de manera segura con .loc
tv_shows.loc[:, 'num_temporadas'] = tv_shows['duration'].apply(extraer_temporadas)

# Descripción estadística para las Movies
descripcion_movies = movies['duracion_minutos'].describe()

# Descripción estadística para los TV Shows
descripcion_tv_shows = tv_shows['num_temporadas'].describe()

# Mostrar las descripciones
print("Descripción estadística para Movies:")
print(descripcion_movies)

print("\nDescripción estadística para TV Shows:")
print(descripcion_tv_shows)

import seaborn as sns
import matplotlib.pyplot as plt

# Filtrar y asegurarse de tener las columnas correctas para Movies y TV Shows
movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()

# Para las Movies, asegurarse de que la duración esté en minutos
movies['duracion_minutos'] = movies['duration'].apply(extraer_duracion_minutos)

# Para los TV Shows, asegurarse de que la duración sea el número de temporadas
tv_shows['num_temporadas'] = tv_shows['duration'].apply(extraer_temporadas)

# Crear el DataFrame para el boxplot combinando las columnas
# Unificar ambos DataFrames y mantener el tipo de contenido
movies['tipo'] = 'Movie'
tv_shows['tipo'] = 'TV Show'

# Combinar ambos DataFrames en uno solo
boxplot_data = pd.concat([movies[['tipo', 'duracion_minutos']], tv_shows[['tipo', 'num_temporadas']].rename(columns={'num_temporadas': 'duracion_minutos'})])

# Crear el boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='tipo', y='duracion_minutos', data=boxplot_data)
plt.title('Distribución de Duración de Movies y TV Shows')
plt.xlabel('Tipo')
plt.ylabel('Duración (minutos o temporadas)')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Filtrar los datos de Movies y TV Shows
movies = df[df['type'] == 'Movie'].copy()
tv_shows = df[df['type'] == 'TV Show'].copy()

# Para las Movies, asegurarse de que la duración esté en minutos
movies['duracion_minutos'] = movies['duration'].apply(extraer_duracion_minutos)

# Para los TV Shows, asegurarse de que la duración sea el número de temporadas
tv_shows['num_temporadas'] = tv_shows['duration'].apply(extraer_temporadas)

# Crear los subgráficos
plt.figure(figsize=(14, 6))

# Primer subgráfico: Boxplot de Movies
plt.subplot(1, 2, 1)
sns.boxplot(x='duracion_minutos', data=movies)
plt.title('Duración de Movies')
plt.xlabel('Duración en Minutos')

# Segundo subgráfico: Boxplot de TV Shows
plt.subplot(1, 2, 2)
sns.boxplot(x='num_temporadas', data=tv_shows)
plt.title('Duración de TV Shows')
plt.xlabel('Número de Temporadas')

plt.tight_layout()  # Ajustar el espaciado entre los subgráficos
plt.show()

df.to_csv('base_datos_modificada.csv', index=False)