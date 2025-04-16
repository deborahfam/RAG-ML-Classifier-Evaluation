# Sistema de Evaluación de Prompts para Clasificación de Problemas de Machine Learning

Este proyecto proporciona herramientas para evaluar diferentes estrategias de prompting en la clasificación de problemas de Machine Learning utilizando un sistema RAG (Retrieval-Augmented Generation).

## Descripción

El sistema clasifica problemas de Machine Learning en tres categorías:
- **Clasificación**: Problemas donde se predice una categoría o clase.
- **Regresión**: Problemas donde se predice un valor numérico.
- **Clustering**: Problemas donde se busca agrupar datos similares sin etiquetas previas.

El proyecto permite comparar diferentes estrategias de prompting (zero-shot, one-shot, few-shot, chain-of-thought, etc.) para determinar cuál ofrece los mejores resultados para esta tarea de clasificación.

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/rag-ml-classifier-evaluation.git
cd rag-ml-classifier-evaluation
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tu clave API de OpenAI (opcional, el sistema puede funcionar en modo simulado):
```bash
export OPENAI_API_KEY=tu-clave-api
```

## Estructura del Proyecto

```
rag-ml-classifier-evaluation/
├── rag/
│   ├── prompts/
│   │   └── classification_prompts.py  # Estrategias de prompting
│   ├── retriever.py                   # Módulo de recuperación de contexto
│   ├── model.py                       # Módulo de interacción con LLM
│   ├── evaluate_prompts.py            # Script de evaluación
│   └── generate_sample_problems.py    # Generador de problemas de ejemplo
├── knowledge_base/                    # Base de conocimiento (documentos)
├── results/                           # Directorio para resultados
└── README.md                          # Este archivo
```

## Uso

### 1. Generar problemas de ejemplo

Genera un archivo con ejemplos de problemas de Machine Learning para evaluación:

```bash
python rag/generate_sample_problems.py -o datos/ml_problems.txt
```

Opciones:
- `--classification N`: Número de problemas de clasificación (defecto: 5)
- `--regression N`: Número de problemas de regresión (defecto: 5)
- `--clustering N`: Número de problemas de clustering (defecto: 5)
- `--ambiguous N`: Número de problemas ambiguos (defecto: 5)

### 2. Crear una base de conocimiento

Crea una base de conocimiento de ejemplo sobre Machine Learning:

```bash
python rag/retriever.py
```

Esto generará documentos de ejemplo en el directorio `knowledge_base/`.

### 3. Ejecutar la evaluación

Evalúa diferentes estrategias de prompting con los problemas de ejemplo:

```bash
python rag/evaluate_prompts.py datos/ml_problems.txt --output results/
```

Opciones:
- `--strategies strategy1 strategy2`: Especifica qué estrategias evaluar (por defecto: todas)

### 4. Analizar resultados

Los resultados se guardan en el directorio especificado:
- `results/all_results.json`: Todos los resultados en formato JSON
- `results/results_summary.csv`: Resumen en formato CSV
- Archivos individuales para cada problema y estrategia

## Estrategias de Prompting Disponibles

1. **Estándar** (`standard`): Prompt básico de clasificación.
2. **Zero-Shot** (`zero_shot`): Clasificación directa sin ejemplos.
3. **One-Shot** (`one_shot`): Clasificación con un solo ejemplo.
4. **Few-Shot** (`few_shot`): Clasificación con varios ejemplos.
5. **Chain-of-Thought** (`chain_of_thought`): Razonamiento paso a paso.
6. **Definición Directa** (`direct_definition`): Basado en definiciones.
7. **Preguntas Simples** (`simple_question`): Basado en preguntas clave.
8. **Template Matching** (`template_matching`): Comparación con plantillas.
9. **Checklist Básico** (`basic_checklist`): Lista de verificación.
10. **Análisis de Palabras Clave** (`keyword_analysis`): Análisis de términos clave.

## Ejemplo de uso completo

```bash
# Generar problemas de ejemplo
python rag/generate_sample_problems.py -o datos/ml_problems.txt --classification 3 --regression 3 --clustering 3

# Crear base de conocimiento
python rag/retriever.py

# Ejecutar evaluación con estrategias específicas
python rag/evaluate_prompts.py datos/ml_problems.txt --strategies zero_shot one_shot few_shot chain_of_thought --output results/experiment1/

# Ver resultados
cat results/experiment1/results_summary.csv
```

## Personalización

Puedes modificar los prompts en `rag/prompts/classification_prompts.py` para ajustar las estrategias o añadir nuevas.

Para usar tu propia base de conocimiento, coloca tus documentos en formato JSON en el directorio `knowledge_base/` con la siguiente estructura:

```json
{
  "title": "Título del documento",
  "content": "Contenido del documento...",
  "source": "Fuente (opcional)"
}
```

## Requisitos

- Python 3.7+
- pandas
- numpy
- requests
- tqdm

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
