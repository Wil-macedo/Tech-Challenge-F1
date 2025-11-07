"""
Request handling functions for fetching and processing data from external sources.
"""
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import request
from libs.validations import is_valid_year_param
from errors import InvalidParam, CustomConnectionError


def my_request(links: dict, columns: list):
    """
    Fetch and process data from multiple URLs.

    Args:
        links: Dictionary mapping names to URLs
        columns: List of column names to extract from tables

    Returns:
        dict: Processed JSON data from all links

    Raises:
        InvalidParam: If year parameter is invalid
        CustomConnectionError: If data loading fails
    """
    json_result = {}
    query_string = ""
    ano = request.args.get("ano", default=None)

    if ano is not None:
        if not is_valid_year_param(ano):
            raise InvalidParam("Ano ou Intervalo inválido")

        query_string = f"ano={ano}"

        copylinks = links.copy()   # Cópia somente para iteração.
        for key, value in copylinks.items():
            links[f"{key}_{ano}"] = value + query_string
            del links[key]

    for key, link in links.items():
        if key != "Sem_Classificacao":  # Remove dados não classificados
            try:
                response = requests.get(link, timeout=30)
                soup = BeautifulSoup(response.text, 'html.parser')

                table = soup.find_all('table')[4]

                dataframe = pd.read_html(str(table))[0]

                dataframe = dataframe[columns]

                for index, row in dataframe.iterrows():
                    value: str = row[columns[1]]  # Segunda coluna tem os dados
                    result = value.split(".")

                    if result[0].isdigit():
                        continue
                    dataframe.drop(index, inplace=True)

                # Use 'records' for a different format
                json_data = dataframe.to_json(orient='records', lines=False)

                json_data: dict = json.loads(json_data)

                json_result[key] = json_data

            except Exception as ex:
                raise CustomConnectionError("Erro ao carregar os dados") from ex

    return json_result
