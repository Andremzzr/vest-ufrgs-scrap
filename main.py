import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import time

BASE_URL = 'https://www1.ufrgs.br/PortalEnsino/graduacaoprocessoseletivo/DivulgacaoDadosChamamento'
SISU = 'S'
VESTIBULAR = 1

types_dict = {
    'vest': VESTIBULAR,
    'sisu': SISU
}


def get_data(url, form_data):
    return requests.post(url, data=form_data)

def get_courses_from_html(url, form_data): 
    options_dict = {}
    response = get_data(url, form_data)

    if response.status_code == 200:
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
                key: vest_data[key] 
            })
        
        for key in sisu_data.keys():
            data['data'].append({
                'year': year,
                'type': 'sisu',
                key: sisu_data[key] 
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

    response = get_data(url,form_data)

    if response.status_code == 200:
        print(form_data)
        tables = pd.read_html(StringIO(response.text))
                
        if tables:
            df = tables[0]
            return {
                'year': year,
                'type': type,
                'data': df.to_dict(orient="records")
            }
    
    return {}


def load_courses_data():
    data = get_courses_data()
    with open("data/courses.json", "w") as out:
            json.dump(data, out)


load_courses_data()
# file_path = "data/courses.json"

# # Load JSON data from the file
# with open(file_path, 'r') as file:
#     data = json.load(file)

# for year in data.keys():
#     year_json = {}
#     for type in data[year].keys():
#         for course_code in data[year][type].keys():
#             candidates = get_candidates_data(year, types_dict[type], course_code)
#             year_json.setdefault(year, {})[course_code] = candidates
#             time.sleep(5)

# with open("data/candidates.json", "w") as out:
#     json.dump(year_json, out)