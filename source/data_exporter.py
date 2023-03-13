import argparse
import logging
import sys
from modules.config.config import Config
from modules.utils.utils import validate_action, validate_date_format, validate_date_period, validate_date_range
from modules.requests.central import CentralRequest
from modules.data_processor.central import CentralDataProcessor

config = Config()

MAX_CONCURRENT_REQUESTS = config.config_data.get('application').get('max_concurrent_requests')
MAX_PERIOD = config.config_data.get('application').get('max_period')
URL_BASE_CENTRAL = config.config_data.get('endpoints').get('url_base_central')
URL_BASE_PORTAL = config.config_data.get('endpoints').get('url_base_portal')
URL_BASE_VONAGE = config.config_data.get('endpoints').get('url_base_vonage')
USERNAME_CENTRAL = config.config_data.get('authentication').get('central').get('username')
PASSWORD_CENTRAL = config.config_data.get('authentication').get('central').get('password')

def parse_args():
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

        if not validate_date_period(args.start_date, args.end_date, MAX_PERIOD):
            raise ValueError(f'Período máximo de pesquisa é de {MAX_PERIOD} dias')
    except ValueError as e:
        logging.error(str(e))
        parser.print_help()
        sys.exit(1)

    return args

if __name__ == '__main__':
    arguments = parse_args()