import json
import requests


class Portal:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.auth = None
        self.session = requests.Session()

    def login(self):
        """Realiza a autenticação e armazena o resultado em self.auth."""
        url = f"{self.base_url}/sessao"
        payload = {
            "login": self.username,
            "senha": self.password,
        }
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            self.auth = response.json()
        except requests.exceptions.HTTPError as error:
            raise (f"Portal Empresas: Falha na requisição: {error}")
        except requests.exceptions.RequestException as error:
            raise (f"Portal Empresas: Falha na conexão: {error}")

    def search_data(self, start_date, end_date):
        """Realiza a busca de atendimentos a partir de uma determinada data."""
        if self.auth is None:
            self.login()
        data = []
        url = f"{self.base_url}/v2/acionamentos/exportacao"
        headers = {
            "Authorization": f"Bearer {self.auth['token']}",
        }
        payload = {
            "minDate": start_date,
            "maxDate": end_date
        }
        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data.extend(response.json())
        except requests.exceptions.HTTPError as error:
            raise (f"Portal Empresas: Falha na requisição: {error}")
        except requests.exceptions.RequestException as error:
            raise (f"Portal Empresas: Falha na conexão: {error}")
        self.auth = None
        return data