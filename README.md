# Proyecto Final de Ciencia de Datos

## 📋 Contenido del Proyecto

El proyecto está estructurado en 5 etapas principales:

1. **Extracción de Datos**: Registro de dimensiones iniciales del dataset
2. **Limpieza de Datos**: Documentación y tratamiento de valores nulos, duplicados e inconsistencias
3. **Análisis Exploratorio de Datos (EDA)**: Distribuciones, frecuencias, estadísticos descriptivos y visualizaciones
4. **Análisis Estadístico**: Planteamiento y evaluación de hipótesis estadísticas
5. **Machine Learning**: Entrenamiento de cinco modelos de ML y evaluación de desempeño

## 🚀 Cómo usar este proyecto

### Requisitos previos

Este proyecto utiliza `uv` para gestionar el entorno de Python. Si no tienes `uv` instalado, puedes instalarlo siguiendo las instrucciones en [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/).

### Configuración del entorno

```bash
uv sync --locked
```

### Agregar el kernel de Jupyter

Para que el entorno esté disponible como kernel en Jupyter, ejecuta:

```bash
uv run python -m ipykernel install --user --name 'pr_ciencia_datos' --display-name "Proyecto Ciencia de Datos"
```