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
