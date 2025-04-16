# test_text_splitter.py
import sys
from pathlib import Path

# Añade la ruta del proyecto al sys.path
project_root = Path(__file__).resolve().parent.parent.parent  # Ajusta según tu estructura
sys.path.append(str(project_root))

from document_parser.parsing_strategies import (
    FixedSizeChunker,
    RecursiveChunker,
    MarkdownSplitter,
)

def test_splitters(text: str):
    splitters = {
        "FixedSizeChunker": FixedSizeChunker(chunk_size=256, chunk_overlap=20),
        "RecursiveChunker": RecursiveChunker(chunk_size=256, chunk_overlap=20),
        "MarkdownSplitter": MarkdownSplitter(chunk_size=256, chunk_overlap=20),
    }

    for name, splitter in splitters.items():
        print(f"\n--- {name} ---")
        chunks = splitter.split_text(text)
        print(f"Total chunks: {len(chunks)}")
        for i, chunk in enumerate(chunks, 1):
            print(f"\nChunk {i}:\n{chunk}\n{'-'*40}")

if __name__ == "__main__":
    sample_text = """
    Complex dynamics of lunar sighting, aiding in more reliable assessments. Furthermore, this study introduces a machine
    learning-based approach to classify crescent visibility conditions. Utilizing the Logistic Regression algorithm, the
    research achieves an impressive predictive accuracy of 98.83%, demonstrating the efficacy of data-driven methods in
    astronomical applications.
    By tuning the ODEH model based on Morocco’s historical observations and applying machine learning techniques,
    this research offers a robust and reliable framework for determining the start of the Hijri month. The integration of
    AI-driven analysis enhances predictive reliability and opens new avenues for refining astronomical criteria through
    data science innovations. The findings underscore the relevance of advanced computational techniques in addressing
    long-standing challenges in lunar calendar determination, setting the stage for further enhancements in predictive
    modeling and methodological refinement.
    2
    Related Works
    2.1
    Empirical Altitude–Azimuth Criteria
    The earliest methods rely on empirical relationships between the moon’s altitude and azimuth. Pioneered by Fother-
    ingham [4] and subsequently refined, Ilyas [5], and Fatoohi [6], these criteria are typically expressed as polynomial
    equations that define a threshold for visibility. Although simple and based on direct observational data, these models
    suffer from being overly static; they often fail to capture the variability in atmospheric conditions, observer differences,
    and geographical diversity. For instance, Ilyas’s criterion has been criticized for underestimating the human eye’s
    capability, thereby limiting its practical predictive power.
    2.2
    Lunar Cycle Analysis
    Another approach focuses on the statistical examination of lunar cycle patterns [7] [8]. These analyses explore the
    frequency of 29- versus 30-day months and compare the resulting patterns with observational data. While they provide
    insight into the broader calendrical implications of crescent sightings, their main shortcoming lies in the inherent
    variability of lunar cycles. Each cycle is unique because of factors like sun–moon declination differences, observer
    location, and atmospheric influences; thus, the lunar cycle approach is less reliable for predicting individual crescent
    sightings or for forming a robust calendrical criterion.
    2.3
    Arc of Vision Versus Arc of Light (Elongation) Criteria
    Modern calendrical systems have also adopted criteria based on a combination of the arc of vision (the altitude
    difference between the moon and the sun) and the arc of light (or elongation) [2]. These methods aim to eliminate
    false-positive sightings by setting a lower boundary that positive observations must exceed. Yet, their rigidity—often
    designed specifically to support a calendrical framework—can lead to cases where real, but borderline, observations are
    disregarded. In particular, the criteria can be too conservative, especially when distinguishing between naked-eye and
    optical-aided observations
    2.4
    Arc of Vision Versus Width Criteria
    Introduced by Bruin [9] and later adapted by researchers such as Yallop [10], Odeh [11], Qureshi [12], and Alrefay et al
    [13], these criteria extend the analysis by incorporating the lunar crescent’s width into the visibility equation. Although
    this method adds a valuable geometric dimension that can also predict observation windows, it is hampered by the
    difficulty in accurately predicting crescent visibility because the empirical conditions cannot reflect the actual crescent
    visibility in a country.
    2.5
    Lag Time–Based Criteria
    Lag time, the interval between sunset (or moonset) and the relevant lunar phase, has also been used as a predictor [14].
    While lag time is intuitively appealing (longer intervals are thought to correlate with easier visibility), its predictive
    power is undermined by low correlation coefficients and its sensitivity to observer latitude. In high-latitude regions, for
    example, the lunar crescent’s slanted path significantly alters lag time, rendering it less reliable as a sole or primary
    parameter in visibility criteria.
    Despite the notable advancements achieved by state-of-the-art methods, these techniques are fundamentally limited
    by their reliance on static, one-size-fits-all thresholds. Such rigidity hinders their ability to accommodate the inherent
    """
    test_splitters(sample_text)
