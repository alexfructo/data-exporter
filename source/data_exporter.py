import argparse
import logging
import sys
from modules.config.config import Config
from modules.utils.utils import validate_action, validate_date_format, validate_date_period, validate_date_range

config = Config()
MAX_CONCURRENT_REQUESTS = config.config_data.get('application').get('max_concurrent_requests')
MAX_PERIOD = config.config_data.get('application').get('max_period')
URL_BASE_CENTRAL = config.config_data.get('endpoints').get('url_base_central')
URL_BASE_PORTAL = config.config_data.get('endpoints').get('url_base_portal')
URL_BASE_VONAGE = config.config_data.get('endpoints').get('url_base_vonage')

def parse_args():
    parser = argparse.ArgumentParser(description='Data Exporter')
    parser.add_argument('-start-date', '--start-date', type=str, required=True, help='Data inicial (DD-MM-YYYY)')
    parser.add_argument('-end-date', '--end-date', type=str, required=True, help='Data final (DD-MM-YYYY)')
    parser.add_argument('-report', '--report', type=str, required=True, choices=['central_historico', 'central_atividades', 'portal_atendimentos', 'vonage_sessoes'], help='Tipo de relatório')
    parser.add_argument('-action', '--action', type=str, required=True, choices=['exportar', 'inserir'], help='Tipo de ação')
    
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
