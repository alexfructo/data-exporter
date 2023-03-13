
import logging
import sys
import os
from modules.config.config import Config
from modules.utils.utils import parse_args
from modules.requests.central import CentralRequest
from modules.data_processor.central import CentralDataProcessor

if __name__ == '__main__':
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json')

    config = Config(config_file_path)
    arguments = parse_args(max_period=config.application.max_period)