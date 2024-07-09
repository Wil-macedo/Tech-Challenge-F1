import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import request
from libs.validations import isValidYearParam
from errors import InvalidParam, ConnectionError


def myRequest(links:dict, columns:list):
    
    jsonResult = {}
    queryString = ""
    ano = request.args.get("ano", default=None)
    
    if ano is not None:

        if not isValidYearParam(ano):
            raise InvalidParam(f"Ano ou Intervalo inválido")

        queryString = f"ano={ano}"
        
        copylinks = links.copy()   # Cópia somente para iteração.
        for key, value in copylinks.items():
            links[key+"_"+str(ano)] = value + queryString
            del links[key]

    
    for key, link in links.items():
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table')[4]
        
            df = pd.read_html(str(table))[0]
            df = df[columns]    
            
            for index, row in df.iterrows():
                value:str = row[columns[1]]  # Segunda coluna tem os dados
                result = value.split(".")
                
                if result[0].isdigit():
                    continue
                else:
                    df.drop(index, inplace=True)
                    
            jsonData = df.to_json(orient='records', lines=False)  # Use 'records' for a different format
            jsonData:dict = json.loads(jsonData)
            
            jsonResult[key] = jsonData
 
        except Exception as ex:
            print(ex)
            raise ConnectionError(f"Erro ao carregar os dados")
        
    return jsonResult   