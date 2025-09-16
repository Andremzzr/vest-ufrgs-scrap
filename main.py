import json
import sys

import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

from services.database_service import DatabaseService
from services.api_wrapper import get_data

BASE_URL = 'https://www1.ufrgs.br/PortalEnsino/graduacaoprocessoseletivo/DivulgacaoDadosChamamento'
DATA_JSON_FILE = 'output.json'
SISU = 'S'
VESTIBULAR = 1

types_dict = {
    'vest': VESTIBULAR,
    'sisu': SISU
}

KEY_MAP = {
    'Classificação': 'classification',
    'Média': 'score',
    'Vaga(s) de Concorrência': 'concurrence_type',
    'Período Vaga': 'period',
    'Vaga de Ingresso': 'enter_type',
    'Situação': 'status',
    'Data Situação': 'date',
    'Candidato': "name"
}

db_service = DatabaseService()



def get_courses_from_html(url, form_data): 
    options_dict = {}
    response = get_data(url, form_data)

    if response:
        soup = BeautifulSoup(response.text, "html.parser")
        select_element = soup.find(id="selectCurso")

        if not select_element: 
            return {}
        
        for option in select_element.find_all("option"):
            value = option.get("value")
            text = option.text.strip()
            if value:
                options_dict[value] = text

    return options_dict
        

def save_courses_data():
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
    
    with open(DATA_JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    return data

def get_courses_data():
    try:
        with open(DATA_JSON_FILE) as json_data:
            d = json.load(json_data)
            return d
    except Exception:
        return save_courses_data()


def get_candidates_data(year, type , course_code):
    url = f"{BASE_URL}/carregaDadosDivulgacao"
    form_data = {
        'anoSelecao': year,
        'sequenciaSelecao': type,
        'codListaSelecao': course_code
    }
    
    print(f"Form Data: {form_data}")
    response = get_data(url,form_data)

    if response:
       
        tables = pd.read_html(StringIO(response))
        

        if tables:
            df = tables[0]

            df.drop(['Nr Inscrição'], axis=1, inplace=True)
            
            # date formating
            df.loc[:, 'Data Situação'] = (
                pd.to_datetime(df['Data Situação'], dayfirst=True, errors='coerce')
                .dt.strftime('%Y-%m-%d')
                .where(lambda x: x.notna(), None)

            )   


            return {
                'year': year,
                'type': type,
                'data_table': df.to_dict(orient="records")
            }
    
    return {}

if __name__ == "__main__":
    command = int(sys.argv[1])
    course_filter = sys.argv[2]

    courses_data = [
        x for x in get_courses_data()["data"]
        if (not command or x["year"] == command)
        and (not course_filter or course_filter.lower() in x["course_name"].lower())
    ]

    total_reqs = len(courses_data)
    req_count = 1

    for course_data in courses_data :
        type = types_dict[course_data['type']]
        year = course_data["year"]
        course_name = course_data["course_name"]

        
        candidate_data = get_candidates_data(year, type, course_data['course_code'])
        candidates_data_translated = translated = [
            {**{KEY_MAP.get(k, k): v for k, v in item.items()},
            "year": year,
            "course_name": course_name,
            "exam_type": course_data["type"] }
            for item in candidate_data["data_table"]
        ]

        db_service.insert_batch(candidates_data_translated)
        print(f"Total requests {req_count}/{total_reqs}")
        req_count+=1
        
