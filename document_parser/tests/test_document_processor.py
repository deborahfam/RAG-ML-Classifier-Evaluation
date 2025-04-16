# test_document_processor.py
from document_processor import DocumentProcessor
from chunking_strategies import (
    FixedLengthStrategy, OverlappingStrategy,
    SentenceBasedStrategy, ParagraphBasedStrategy,
    TokenBasedStrategy
)

if __name__ == '__main__':
    sample_text = (
        "Complex dynamics of lunar sighting, aiding in more reliable assessments. Furthermore, this study introduces a machine "
        "learning-based approach to classify crescent visibility conditions. Utilizing the Logistic Regression algorithm, the "
        "research achieves an impressive predictive accuracy of 98.83%, demonstrating the efficacy of data-driven methods in "
        "astronomical applications.\n"
        "By tuning the ODEH model based on Morocco’s historical observations and applying machine learning techniques, "
        "this research offers a robust and reliable framework for determining the start of the Hijri month. The integration of "
        "AI-driven analysis enhances predictive reliability and opens new avenues for refining astronomical criteria through "
        "data science innovations. The findings underscore the relevance of advanced computational techniques in addressing "
        "long-standing challenges in lunar calendar determination, setting the stage for further enhancements in predictive "
        "modeling and methodological refinement.\n"
        "2\n"
        "Related Works\n"
        "2.1\n"
        "Empirical Altitude–Azimuth Criteria\n"
        "The earliest methods rely on empirical relationships between the moon’s altitude and azimuth. Pioneered by Fotheringham "
        "and subsequently refined by Ilyas and Fatoohi, these criteria are typically expressed as polynomial equations that define "
        "a threshold for visibility. Although simple and based on direct observational data, these models suffer from being overly "
        "static; they often fail to capture the variability in atmospheric conditions, observer differences, and geographical diversity. "
        "For instance, Ilyas’s criterion has been criticized for underestimating the human eye’s capability, thereby limiting its practical "
        "predictive power.\n"
        "2.2\n"
        "Lunar Cycle Analysis\n"
        "Another approach focuses on the statistical examination of lunar cycle patterns. These analyses explore the frequency of 29- versus "
        "30-day months and compare the resulting patterns with observational data. While they provide insight into the broader calendrical "
        "implications of crescent sightings, their main shortcoming lies in the inherent variability of lunar cycles. Each cycle is unique "
        "because of factors like sun–moon declination differences, observer location, and atmospheric influences; thus, the lunar cycle "
        "approach is less reliable for predicting individual crescent sightings or for forming a robust calendrical criterion.\n"
        "2.3\n"
        "Arc of Vision Versus Arc of Light (Elongation) Criteria\n"
        "Modern calendrical systems have also adopted criteria based on a combination of the arc of vision (the altitude difference between "
        "the moon and the sun) and the arc of light (or elongation). These methods aim to eliminate false-positive sightings by setting a "
        "lower boundary that positive observations must exceed. Yet, their rigidity—often designed specifically to support a calendrical "
        "framework—can lead to cases where real, but borderline, observations are disregarded. In particular, the criteria can be too "
        "conservative, especially when distinguishing between naked-eye and optical-aided observations.\n"
        "2.4\n"
        "Arc of Vision Versus Width Criteria\n"
        "Introduced by Bruin and later adapted by researchers such as Yallop, Odeh, Qureshi, and Alrefay et al., these criteria extend the "
        "analysis by incorporating the lunar crescent’s width into the visibility equation. Although this method adds a valuable geometric "
        "dimension that can also predict observation windows, it is hampered by the difficulty in accurately predicting crescent visibility "
        "because the empirical conditions cannot reflect the actual crescent visibility in a country.\n"
        "2.5\n"
        "Lag Time–Based Criteria\n"
        "Lag time, the interval between sunset (or moonset) and the relevant lunar phase, has also been used as a predictor. While lag time "
        "is intuitively appealing (longer intervals are thought to correlate with easier visibility), its predictive power is undermined by "
        "low correlation coefficients and its sensitivity to observer latitude. In high-latitude regions, for example, the lunar crescent’s "
        "slanted path significantly alters lag time, rendering it less reliable as a sole or primary parameter in visibility criteria.\n"
        "Despite the notable advancements achieved by state-of-the-art methods, these techniques are fundamentally limited by their reliance "
        "on static, one-size-fits-all thresholds. Such rigidity hinders their ability to accommodate the inherent..."
    )

    # Definir las estrategias disponibles
    strategies = {
        "fixed": FixedLengthStrategy(chunk_size=2000),
        "overlap": OverlappingStrategy(chunk_size=2000, overlap=10),
        "sentence": SentenceBasedStrategy(max_chunk_size=2000),
        "paragraph": ParagraphBasedStrategy(),
        "token": TokenBasedStrategy(chunk_tokens=10, step_tokens=5)
    }

    # Instanciar el processor con una estrategia inicial
    processor = DocumentProcessor(strategy=strategies["fixed"])
    print("Chunks con estrategia FixedLengthStrategy:")
    for chunk in processor.process_document(sample_text):
        print("->", chunk)
    print("="*60)

    # Cambiamos a estrategia OverlappingStrategy
    processor.set_strategy(strategies["overlap"])
    print("Chunks con estrategia OverlappingStrategy:")
    for chunk in processor.process_document(sample_text):
        print(" ")
        print("->", chunk)
    print("="*60)

    # Estrategia basada en oraciones
    processor.set_strategy(strategies["sentence"])
    print("Chunks con estrategia SentenceBasedStrategy:")
    for chunk in processor.process_document(sample_text):
        print(" ")
        print("->", chunk)
    print("="*60)

    # Estrategia basada en párrafos
    processor.set_strategy(strategies["paragraph"])
    print("Chunks con estrategia ParagraphBasedStrategy:")
    for chunk in processor.process_document(sample_text):
        print(" ")
        print("->", chunk)
    print("="*60)

    # Estrategia basada en tokens con ventana deslizante
    processor.set_strategy(strategies["token"])
    print("Chunks con estrategia TokenBasedStrategy:")
    for chunk in processor.process_document(sample_text):
        print(" ")
        print("->", chunk)
