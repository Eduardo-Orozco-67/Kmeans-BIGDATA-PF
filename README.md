# Kmeans-BIGDATA-PF
Proyecto final de la materia Big Data 

# Dashboard de Segmentación de Consumidores de WallCityTap

¡Bienvenido al Dashboard de Segmentación de Consumidores de WallCityTap! Este proyecto proporciona un dashboard interactivo para analizar datos de consumidores e identificar insights clave utilizando el clustering de K-means y el Método del Codo.

## Descripción

El dashboard permite a los usuarios explorar los datos de los consumidores, segmentar clientes en clusters y analizar sus hábitos de gasto y preferencias. También proporciona métricas clave como el método de pago preferido y los consumidores potenciales de alto valor.

## Características

- **Filtros Interactivos**: Ajusta el rango de edad y selecciona métodos de pago para filtrar los datos de los consumidores.
- **Análisis de Clusters**: Visualiza la segmentación de consumidores utilizando clustering de K-means.
- **Visualización del Método del Codo**: Determina el número óptimo de clusters.
- **Métricas Clave**: Muestra el número de consumidores en línea, la edad promedio para métodos de pago específicos y los métodos de pago preferidos.
- **Consumidores Potenciales**: Identifica y describe a los consumidores de alto valor.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Eduardo-Orozco-67/Kmeans-BIGDATA-PF.git
   cd Kmeans-BIGDATA-PF

2. Instalamos las dependencias a usar
   ```bash
   pip install -r requirements.txt

3. Ejecucion del proyecto
   ```bash
    shiny run main.py
Abre tu navegador web y navega a http://127.0.0.1:8000.

## Componentes Clave

### Método del Codo

El Método del Codo ayuda a determinar el número óptimo de clusters (k) para el clustering de K-means al graficar la Suma de Cuadrados Dentro del Cluster (WCSS) contra el número de clusters. El punto de "codo" indica el valor óptimo de k.

### Clustering de K-means

El clustering de K-means se utiliza para segmentar a los consumidores en clusters basados en su edad, ingreso anual y puntaje de gasto. Los clusters ayudan a identificar patrones y comportamiento de los consumidores.

### Métricas del Dashboard

- **Número de Consumidores en Línea**: Muestra el número total de consumidores en línea.
- **Edad Promedio para Pago en Efectivo**: Muestra la edad promedio de los consumidores que usan efectivo.
- **Edad Promedio para Ingresos Altos**: Muestra la edad promedio de los consumidores con un ingreso anual mayor a $20,000.
- **Método de Pago Preferido**: Identifica el método de pago más frecuentemente utilizado entre los consumidores.
