import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time
import os

BASE_URL = 'https://www1.ufrgs.br/PortalEnsino/graduacaoprocessoseletivo/DivulgacaoDadosChamamento'
SISU = 'S'
VESTIBULAR = 1
MAX_RETRIES = 3

types_dict = {
    'vest': VESTIBULAR,
    'sisu': SISU
}

def get_data(url, form_data, retries=MAX_RETRIES, backoff_factor=2):
    for attempt in range(retries):
        try:
            response = requests.post(url, data=form_data, timeout=10)
            if response.status_code == 200:
                return response
            else:
                print(f"Attempt {attempt+1}/{retries}: Received status {response.status_code}. Retrying...")
        except requests.RequestException as e:
            print(f"Attempt {attempt+1}/{retries}: Request failed due to {e}. Retrying...")

        time.sleep(backoff_factor ** attempt)  

    return None 
 
def get_courses_from_html(url, form_data): 
    options_dict = {}
    response = get_data(url, form_data)

    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        select_element = soup.find(id="selectCurso")

        if not select_element: 
            return
        
        for option in select_element.find_all("option"):
            value = option.get("value")
            text = option.text.strip()
            if value:
                options_dict[value] = text

    return options_dict
        

def get_courses_data():
    url = f"{BASE_URL}/carregaCursos"
    years = list(range(2016, 2026))
    data = {'data': []}

    for year in years:
        form_vest = {
            "anoSelecao": year,
            "sequenciaSelecao": VESTIBULAR,
        }

        form_sisu = {
            "anoSelecao": year,
            "sequenciaSelecao": SISU,
        }

        vest_data = get_courses_from_html(url, form_vest)
        sisu_data = get_courses_from_html(url, form_sisu)

        for key in vest_data.keys():
            data['data'].append({
                'year': year,
                'type': 'vest',
                'course_code': key,
                'course_name': vest_data[key] 
            })
        
        for key in sisu_data.keys():
            data['data'].append({
                'year': year,
                'type': 'sisu',
                'course_code': key,
                'course_name': sisu_data[key] 
        })

        print(year)
    
    return data

def get_candidates_data(year, type ,course_code):
    url = f"{BASE_URL}/carregaDadosDivulgacao"
    form_data = {
        'anoSelecao': year,
        'sequenciaSelecao': type,
        'codListaSelecao': course_code
    }
    
    print(form_data)
    response = get_data(url,form_data)

    if response:
        tables = pd.read_html(StringIO(response.text))
        if tables:
            df = tables[0]

            df.drop(['Nr Inscrição', 'Candidato'], axis=1, inplace=True)

            return {
                'year': year,
                'type': type,
                'data_table': df.to_dict(orient="records")
            }
    
    return {}


def load_courses_data():
    data = get_courses_data()
    with open("data/courses.json", "w") as out:
            json.dump(data, out)

file_path = "data/courses.json"

# Load JSON data from the file
with open(file_path, 'r') as file:
    json_file_data = json.load(file)

JSON_FILE_PATH = "data/candidates.json"

def get_candidates_file():
    # Load existing data or create an empty list if the file doesn't exist
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []  
            
    return []

all_candidates = get_candidates_file()

for course_data in json_file_data['data']:
    print(course_data['year'], course_data['course_name'])
    candidates_data = get_candidates_data(course_data['year'], types_dict[course_data['type']], course_data['course_code'])

    if candidates_data:
        all_candidates.append(candidates_data)
    # Save updated list back to the file
    with open(JSON_FILE_PATH, "w") as out:
        json.dump(all_candidates, out, indent=4)
    time.sleep(5)