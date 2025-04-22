from prompt_engineer import PromptEngineer
from services.context_fetcher import fetch_context_from_query

mock_query_embedding = [0.1] * 768  # Sustituye con tu lógica real
query = "I need to predict customer churn based on their usage patterns"

# Obtener contexto
context = fetch_context_from_query(mock_query_embedding)

# Ejecutar prompt engineer
engineer = PromptEngineer()
results = engineer.evaluate_all_strategies(query, context)

# Mostrar resultados
for result in results:
    print(engineer.format_response(result))
    print("-" * 50)
