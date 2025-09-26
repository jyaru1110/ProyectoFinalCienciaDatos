# Proyecto Final de Ciencia de Datos

Este repositorio contiene un proyecto completo de ciencia de datos que implementa un pipeline end-to-end para análisis de datos y machine learning.

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

### Ejecutar el notebook

1. Inicia Jupyter Notebook:
```bash
jupyter notebook
```

2. Abre el archivo `proyecto_final_ciencia_datos.ipynb`

3. Ejecuta las celdas secuencialmente

## 📊 Características del Proyecto

### Análisis Implementado
- **Estadísticos descriptivos** completos
- **Visualizaciones** de distribuciones y correlaciones
- **Tests de hipótesis** estadísticas
- **Modelos de Machine Learning**:
  - Regresión Logística
  - Random Forest
  - SVM (Support Vector Machine)
  - K-Nearest Neighbors
  - Gradient Boosting

### Métricas de Evaluación
- Accuracy
- Validación cruzada
- Matriz de confusión
- Reportes de clasificación
- AUC-ROC Score

## 🔧 Estructura de Archivos

```
ProyectoFinalCienciaDatos/
│
├── proyecto_final_ciencia_datos.ipynb  # Notebook principal
├── requirements.txt                     # Dependencias del proyecto
├── README.md                           # Documentación
└── .gitignore                          # Archivos ignorados por git
```

## 📝 Notas

- El notebook incluye un dataset sintético para demostración
- Para usar tus propios datos, reemplaza la sección de carga de datos en el notebook
- Todos los códigos están documentados y comentados para facilitar la comprensión

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de seguir las mejores prácticas de ciencia de datos y documentar cualquier cambio.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
