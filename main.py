import requests
import json
from bs4 import BeautifulSoup

BASE_URL = 'https://www1.ufrgs.br/PortalEnsino/graduacaoprocessoseletivo/DivulgacaoDadosChamamento'
SISU = 'S'
VESTIBULAR = 1

# URL of the endpoint
url = f"{BASE_URL}/carregaCursos"


def getData(url, form_data): 
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
        


years = list(range(2016, 2025))
all_data = {}

for year in years:
    print(year)
    form_data = {
        "anoSelecao": year,
        "sequenciaSelecao": 1,
    }

    data = getData(url, form_data)
    all_data[year] = data
    print(all_data)

with open("data/cursos.json", "w") as out:
        json.dump(all_data, out)

