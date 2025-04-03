import os
import time
from urllib.parse import quote_plus
import urllib.request
import xml.etree.ElementTree as ET

def get_arxiv_papers(start=0, max_results=100):
    """Fetch papers específicos de clasificación, clustering y regresión"""
    base_url = 'http://export.arxiv.org/api/query?'
    
    # Filtro especializado para los 3 problemas
    query = (
        "(cat:cs.LG OR cat:stat.ML) "  # Categorías base
        "AND ("
        # "all:\"classification\" OR "    # Clasificación
        # "all:\"clustering\" OR "       # Clustering
        # "all:\"regression\" OR "        # Regresión
        "all:\"supervised learning\" OR "
        "all:\"unsupervised learning\""
        ") "
        "ANDNOT (all:\"ethics\" OR all:\"bias\" OR all:\"fairness\")"  # Exclusiones
    )
    
    encoded_query = quote_plus(query)
    url = f'{base_url}search_query={encoded_query}&start={start}&max_results={max_results}&sortBy=submittedDate'
    
    try:
        with urllib.request.urlopen(url) as response:
            return parse_xml(response.read().decode('utf-8'))
    except Exception as e:
        print(f"API Error: {e}")
        return None
    finally:
        time.sleep(3)

def parse_xml(xml_content):
    """Parse XML con detección del tipo de problema"""
    root = ET.fromstring(xml_content)
    namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('atom:entry', namespaces):
        paper_id = entry.find('atom:id', namespaces).text.split('/')[-1]
        title = entry.find('atom:title', namespaces).text.strip().lower()
        summary = entry.find('atom:summary', namespaces).text.strip().lower()
        
        # Detectar tipo de problema
        problem_type = detect_problem_type(title, summary)
        
        papers.append({
            'id': paper_id,
            'title': title,
            'problem_type': problem_type,
            'links': {link.get('title'): link.get('href') 
                      for link in entry.findall('atom:link', namespaces)
                      if link.get('title') in ['pdf']},
            'published': entry.find('atom:published', namespaces).text
        })
    return papers

def detect_problem_type(title, summary):
    """Clasifica el paper en los 3 tipos de problemas"""
    keywords = {
        'classification': ['classification', 'classify', 'supervised'],
        'clustering': ['clustering', 'cluster', 'unsupervised'],
        'regression': ['regression', 'regress', 'continuous']
    }
    
    for problem, terms in keywords.items():
        if any(term in title or term in summary for term in terms):
            return problem
    return 'other'

def download_pdfs(papers, base_folder='ml_problems'):
    """Descarga organizada por tipo de problema"""
    for paper in papers:
        if not paper['links'].get('pdf'):
            continue
            
        # Crear subcarpeta por tipo de problema
        folder = os.path.join(base_folder, paper['problem_type'])
        os.makedirs(folder, exist_ok=True)
        
        # Nombre de archivo descriptivo
        filename = f"{paper['id']}_{paper['problem_type']}.pdf"
        filepath = os.path.join(folder, filename)
        
        try:
            with urllib.request.urlopen(paper['links']['pdf']) as response:
                with open(filepath, 'wb') as f:
                    f.write(response.read())
            print(f"Descargado [{paper['problem_type']}]: {paper['title'][:50]}...")
        except Exception as e:
            print(f"Error en {paper['id']}: {str(e)[:30]}")

if __name__ == '__main__':
    papers = get_arxiv_papers(max_results=150)  # Más papers para cubrir los 3 temas
    
    if papers:
        download_pdfs(papers)
        print("\nResumen:")
        counts = {'classification': 0, 'clustering': 0, 'regression': 0}
        for p in papers:
            if p['problem_type'] in counts:
                counts[p['problem_type']] += 1
        for k, v in counts.items():
            print(f"- {k.capitalize()}: {v} papers")
    else:
        print("No se encontraron papers")