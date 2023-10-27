import requests
from bs4 import BeautifulSoup
import json
import datetime

date = datetime.date.today()        

medici = [
    {'id': 'xxx', 'nome': 'MARIO ROSSI'}
]

def getDisponibilita(id):
    response = requests.post('https://salute.regione.veneto.it/servizi/cerca-medici-e-pediatri?p_p_id=MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&p_p_col_id=column-3&p_p_col_count=1&_MEDICI_WAR_portalgeoreferenziazione_INSTANCE_F5Pm_action=result', {
        'idLuogo': id
    })
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')
    assistitiIllimitati = 0

    if (len(table)):
        table = table[0]
        tr = table.find('tbody').find_all('tr')
        assistitiIllimitati = int(tr[0].find_all('td')[1].text)

    return assistitiIllimitati

def sendMessage(message):
    url = "https://xxx.execute-api.eu-west-1.amazonaws.com/prod/messages"
    payload = json.dumps({
        "Records": [
            {
                "EventSource": "ws",
                "Message": message
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    requests.request("POST", url, headers=headers, data=payload)


def dailyCheck(event=None, context=None):
    hasMedici = []

    for medico in medici:
        disponibilita = getDisponibilita(medico['id'])
        if disponibilita > 0 or date.weekday() == 0:
            hasMedici.append(medico['nome'] +": " + str(disponibilita))

    if len(hasMedici) > 0:
            message = "\n".join(hasMedici)
            sendMessage("👨‍⚕️*DISPONIBILITÀ MEDICI*:\n" + message)

def lambda_handler(event, context):
    dailyCheck()
