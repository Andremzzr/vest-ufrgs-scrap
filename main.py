import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'https://www1.ufrgs.br/PortalEnsino/graduacaoprocessoseletivo/DivulgacaoDadosChamamento'
SISU = 'S'
VESTIBULAR = 1


def get_data(url, form_data): 
    options_dict = {}
    response = requests.post(url, data=form_data)

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
    years = list(range(2016, 2025))
    data = {}

    for year in years:
        form_vest = {
            "anoSelecao": year,
            "sequenciaSelecao": VESTIBULAR,
        }

        form_sisu = {
            "anoSelecao": year,
            "sequenciaSelecao": SISU,
        }

        vest_data = get_data(url, form_vest)
        sisu_data = get_data(url, form_sisu)

        data.setdefault(year, {})['vest'] = vest_data
        data[year]['sisu'] = sisu_data
        print(year)
    
    return data


def load_courses_data():
    data = get_courses_data()
    with open("data/courses.json", "w") as out:
            json.dump(data, out)

load_courses_data()