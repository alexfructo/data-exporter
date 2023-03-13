import argparse
from datetime import datetime, timedelta

DATE_FORMAT = '%d-%m-%Y'

def validate_date_format(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False

def validate_date_range(start_date: str, end_date: str) -> bool:
    start_date_obj = datetime.strptime(start_date, DATE_FORMAT)
    end_date_obj = datetime.strptime(end_date, DATE_FORMAT)
    return start_date_obj <= end_date_obj

def validate_date_period(start_date: str, end_date: str, max_period: int) -> bool:
    start_date_obj = datetime.strptime(start_date, DATE_FORMAT)
    end_date_obj = datetime.strptime(end_date, DATE_FORMAT)
    period = (end_date_obj - start_date_obj).days
    return period <= max_period

def validate_action(action: str) -> bool:
    allowed_actions = ['exportar', 'inserir']
    return action in allowed_actions

def parse_args(max_period=7):
    parser = argparse.ArgumentParser(description='Data Exporter')
    parser.add_argument('-start_date', '--start_date', type=str, required=True, help='Data inicial (DD-MM-YYYY)', default='09-03-2023')
    parser.add_argument('-end_date', '--end_date', type=str, required=True, help='Data final (DD-MM-YYYY)', default='09-03-2023')
    parser.add_argument('-report', '--report', type=str, required=True, choices=['central_historico', 'central_atividades', 'portal_atendimentos', 'vonage_sessoes'], help='Tipo de relatório', default='central_historico')
    parser.add_argument('-action', '--action', type=str, required=True, choices=['exportar', 'inserir'], help='Tipo de ação', default='exportar')
    
    try:
        args = parser.parse_args()

        if not validate_date_format(args.start_date):
            raise ValueError('Data inicial deve estar no formato DD-MM-YYYY')

        if not validate_date_format(args.end_date):
            raise ValueError('Data final deve estar no formato DD-MM-YYYY')

        if not validate_date_range(args.start_date, args.end_date):
            raise ValueError('Data inicial não pode ser maior que a final')

        if not validate_date_period(args.start_date, args.end_date, max_period):
            raise ValueError(f'Período máximo de pesquisa é de {max_period} dias')
    except ValueError as e:
        parser.print_help()

    return args