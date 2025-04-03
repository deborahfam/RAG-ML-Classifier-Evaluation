import os
import time
import random
from scholarly import scholarly
from bs4 import BeautifulSoup
import requests

# Configuración de user-agents y proxies (necesario para evitar bloqueos)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
]

HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://scholar.google.com/'
}

def get_google_scholar_papers(search_terms, max_papers=30):
    papers = []
    
    for term in search_terms:
        print(f"Buscando: {term}")
        search_query = scholarly.search_pubs(f'machine learning "{term}" -ethics -bias -fairness')
        
        try:
            for _ in range(max_papers // len(search_terms)):
                paper = next(search_query)
                paper_detail = process_paper(paper)
                if paper_detail:
                    papers.append(paper_detail)
                time.sleep(random.uniform(2, 5))  # Evitar detección
        except StopIteration:
            continue
        except Exception as e:
            print(f"Error en {term}: {str(e)[:50]}")
    
    return papers

def process_paper(paper):
    """Extrae metadatos y detecta tipo de problema"""
    title = paper.get('bib', {}).get('title', '').lower()
    abstract = paper.get('bib', {}).get('abstract', '').lower()
    
    problem_type = detect_problem_type(title + " " + abstract)
    
    return {
        'title': title,
        'problem_type': problem_type,
        'url_pdf': get_pdf_link(paper),
        'year': paper.get('bib', {}).get('pub_year')
    }

def detect_problem_type(text):
    keywords = {
        'classification': ['classification', 'classify', 'supervised'],
        'clustering': ['clustering', 'cluster', 'unsupervised'],
        'regression': ['regression', 'regress', 'continuous']
    }
    
    for problem, terms in keywords.items():
        if any(term in text for term in terms):
            return problem
    return 'other'

def get_pdf_link(paper):
    """Intenta obtener enlace PDF desde las menciones"""
    if 'eprint_url' in paper:
        return paper['eprint_url']
    
    # Búsqueda alternativa en la página del paper
    session = requests.Session()
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
    
    try:
        resp = session.get(paper['pub_url'], headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        pdf_link = soup.find('a', {'href': True, 'type': 'application/pdf'})
        return pdf_link['href'] if pdf_link else None
    except:
        return None

def download_pdfs(papers, base_folder='scholar_papers'):
    """Descarga con rotación de user-agent y manejo de errores"""
    session = requests.Session()
    
    for paper in papers:
        if not paper['url_pdf'] or paper['problem_type'] == 'other':
            continue
            
        folder = os.path.join(base_folder, paper['problem_type'])
        os.makedirs(folder, exist_ok=True)
        
        filename = f"{paper['year']}_{paper['title'][:30].replace(' ', '_')}.pdf"
        filepath = os.path.join(folder, filename)
        
        try:
            session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
            response = session.get(paper['url_pdf'], headers=HEADERS, timeout=15)
            
            if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Descargado: {paper['title'][:50]}...")
            else:
                print(f"Formato inválido: {paper['title'][:30]}")
                
            time.sleep(random.uniform(5, 10))  # Critical para evitar bloqueos
            
        except Exception as e:
            print(f"Error descargando {paper['title'][:30]}: {str(e)[:30]}")

if __name__ == '__main__':
    # Búsqueda específica
    search_terms = [
        "classification problem", 
        "clustering algorithm", 
        "regression analysis"
    ]
    
    papers = get_google_scholar_papers(search_terms, max_papers=30)
    
    if papers:
        download_pdfs(papers)
        print("\nResumen descargas:")
        types = set(p['problem_type'] for p in papers)
        for t in types:
            count = len([p for p in papers if p['problem_type'] == t])
            print(f"- {t}: {count}")
    else:
        print("No se encontraron papers")