import json
from requests.models import Response
import os
import pandas as pd

def requestToJson(result):
    result:Response
    
    csvInfo = result.text.split('\n')
    headers = csvInfo[0].split(';')

        # Processando os dados e convertendo para JSON
    data = []
    for line in csvInfo[1:]:
        if line:  # Ignorar linhas vazias
            values = line.split(';')
            entry = {headers[i]: values[i].encode('ISO-8859-1').decode('utf-8', 'ignore') for i in range(len(headers))}
            data.append(entry)
        
    return data


def csvToJson(csvFile):
    
    json_data = None
    
    csvFile = os.path.join(os.path.abspath("."),"csvFiles", csvFile)
    
    if os.path.exists(csvFile):
        df = pd.read_csv(csvFile, sep=";")
        json_data = df.to_json(orient='records', lines=True, force_ascii=False)
        
    return json_data