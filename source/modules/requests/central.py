import json
import requests


class Central:
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.auth = None
        self.session = requests.Session()

    def login(self):
        """Realiza a autenticação e armazena o resultado em self.auth."""
        url = f"{self.base_url}/servico/login/session"
        payload = {
            "username": self.username,
            "password": self.password,
        }
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            self.auth = response.json()
        except requests.exceptions.HTTPError as error:
            raise (f"Central de Requisições: Falha na requisição: {error}")
        except requests.exceptions.RequestException as error:
            raise (f"Central de Requisições: Falha na conexão: {error}")

    def search_data(self, endpoint, start_date, end_date, page=1, callback=None):
        """Realiza a busca de dados a partir de uma determinada data e página."""
        if self.auth is None:
            self.login()

        data = []

        while True:
            url = f"{endpoint}{start_date}/{end_date}/{page}"
            headers = {
                "x-access-token": self.auth["accessToken"],
                "_id": self.auth["user"]["_id"],
            }
            try:
                response = self.session.get(url, headers=headers)
                response.raise_for_status()
                response_data = response.json()
                data.extend(response_data["docs"])
                if callback:
                    callback(page, response_data["pages"])
                if "pages" not in response_data or page >= response_data["pages"]:
                    break
                page += 1
            except requests.exceptions.HTTPError as error:
                raise (f"Central de Requisições: Falha na requisição: {error}")
                break
            except requests.exceptions.RequestException as error:
                raise (f"Central de Requisições: Falha na conexão: {error}")
                break
        self.auth = None
        return data

    def search_attendance_records(self, start_date, end_date, callback=None):
        """Realiza a busca de atividades a partir de uma determinada data."""
        endpoint = f"{self.base_url}/servico/historico/downloadjson/"
        return self.search_data(endpoint, start_date, end_date, callback=callback)

    def search_activity_records(self, start_date, end_date, callback=None):
        """Realiza a busca de histórico de atividades a partir de uma determinada data."""
        endpoint = f"{self.base_url}/servico/adm/atividades/json/"
        return self.search_data(endpoint, start_date, end_date, callback=callback)
