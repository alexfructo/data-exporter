import json
import os
from typing import Dict


class Config:
    def __init__(self, config_file_path: str = 'config/config.json'):
        self.config_file_path = config_file_path
        self.config_data = {}
        self.load_config()

    def load_config(self) -> None:
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as f:
                self.config_data = json.load(f)
        else:
            self.create_config_file()

    def create_config_file(self) -> None:
        config_template = {
            "application": {
                "max_concurrent_requests": 10,
                "max_period": 7
            },
            "endpoints": {
                "url_base_central": "",
                "url_base_portal": "",
                "url_base_vonage": ""
            },
            "authentication": {
                "vonage": {
                    "token": ""
                },
                "central": {
                    "username": "",
                    "password": ""
                },
                "portal": {
                    "username": "",
                    "password": ""
                }
            },
            "database": {
                "host": "",
                "port": "",
                "username": "",
                "password": "",
                "stage": {
                    "database": "",
                    "vonage_table": "",
                    "central_table": "",
                    "portal_table": ""
                },
                "production": {
                    "database": "",
                    "vonage_table": "",
                    "central_table": "",
                    "portal_table": ""
                },
                "data":{
                    "central": {
                        "attendance":{
                            "columns":{
            
                            },
                            "rename_cloumns":{
            
                            }
                        },
                        "activity":{
                            "columns":{
            
                            },
                            "rename_cloumns":{
            
                            }
                        }
                    },
                    "portal":{
                        "attendance":{
                            "columns":{
            
                            },
                            "rename_cloumns":{
            
                            }
                        }
                    }
                }
            }
        }
        os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
        with open(self.config_file_path, 'w') as f:
            json.dump(config_template, f, indent=4)
        self.config_data = config_template

    def get_config(self) -> Dict:
        return self.config_data
