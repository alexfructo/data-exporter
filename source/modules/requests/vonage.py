import json
import requests


class Vonage:
    def __init__(self, token, base_url):
        self.token = token
        self.base_url = base_url
        self.session = requests.Session()

    def find_session_by_id(self, session_id):
        """Realiza a busca de dados de uma sessão a partir de um id de sessão"""

        url = f"{self.base_url}/vonage/getSession"
        headers = {
            "Authorization": f"Bearer {self.token}",
        }
        payload = {"sessionId":session_id}
        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.HTTPError as error:
            raise(f"Vonage: Falha na requisição: {error}")
        except requests.exceptions.RequestException as error:
            raise(f"Vonage: Falha na conexão: {error}")
        
        return response_data
    
    def search_vonage_events(self, attendance_records, callback=None):
        """Realiza a busca de eventos em uma sessão a partir de uma lista de registros de atendimentos"""

        attendance_session_events = []
        total_items = len(attendance_records)
        for index, attendance in enumerate(attendance_records):
            if callback:
                callback(index + 1, total_items)
            session = self.find_session_by_id(attendance.get('idAttendanceVonage'))
            if session is not None:
                for event in session.get('session').get('events'):
                    event_item = {
                        'idAttendanceVonage': attendance.get('idAttendanceVonage', ''),
                        'centralId': attendance.get('centralId', ''),
                        'status': session.get('status', ''),
                        'session':{
                            'patientName': session.get('session').get('patientName'),
                            'birthDate': session.get('session').get('birthDate'),
                            'document': session.get('session').get('document'),
                            'email': session.get('session').get('email'),
                            'phone': session.get('session').get('phone'),
                            'expertise': session.get('session').get('expertise'),
                            'healthInsurance': session.get('session').get('healthInsurance'),
                            'clientName': session.get('session').get('clientName')
                        },
                        'events':{
                            'oldQueue': event.get('oldQueue', ''),
                            'newQueue': event.get('newQueue', ''),
                            'eventType': event.get('eventType', ''),
                            'origin': event.get('origin', ''),
                            'created_at': event.get('created_at', ''),
                            'name': event.get('name', ''),
                            'role': event.get('role', ''),
                            'userData':{
                                'name': event.get('userData', {}).get('name', ''),
                                'userType': event.get('userData', {}).get('userType', '')
                            }
                        },
                        'waitingTimes':{
                            'wait_reception': session.get('waitingTimes', {}).get('wait_reception', ''),
                            'reception': session.get('waitingTimes', {}).get('reception', ''),
                            'wait_doctor': session.get('waitingTimes', {}).get('wait_doctor', ''),
                            'doctor': session.get('waitingTimes', {}).get('doctor', ''),
                            'wait_support': session.get('waitingTimes', {}).get('wait_support', ''),
                            'support': session.get('waitingTimes', {}).get('support', ''),
                        }
                    }
                    attendance_session_events.append(event_item)
        
        return attendance_session_events