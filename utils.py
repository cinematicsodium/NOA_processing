from notices import STANDARD_NOTICE, LATE_NOTICE
from datetime import datetime, timedelta
from string import ascii_uppercase
from modules import Action
from constants import *
import yaml

TODAY = datetime.now()

class Formatting:
    @staticmethod
    def name(raw_name: str) -> str:
        name_parts: list[str] = [name_part.strip() for name_part in raw_name.split()]
        last, first = '',''
        if name_parts[0].lower() == 'name:':
            last, first = name_parts[1][:-1], name_parts[2]
        elif name_parts[0].endswith(','):
            last, first = name_parts[0][:-1],name_parts[1]
        elif ',' in name_parts[0]:
            last, first = name_parts[0].split(',')
        else:
            first, last = name_parts[0],name_parts[1]
        upper_count = sum(1 for char in raw_name if char in ascii_uppercase)
        if upper_count > 5:
            last, first = last.capitalize(), first.capitalize()
        return ', '.join([last,first])


def convert_date(date_str: str) -> str:
    current_year = TODAY.year
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%m-%d-%Y',
        '%m/%d/%Y',
        '%m/%d/%y',
        '%m-%d',
        '%m/%d',
    ]
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            if not any(y in fmt for y in ['%Y','%y']):
                parsed_date = parsed_date.replace(year=current_year)
            return parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            continue
    raise ValueError(f'Date format not recognized: {date_str}')


def determine_thirty_day_deadline(start_date: str) -> str:
    dt_start = datetime.strptime(start_date, '%Y-%m-%d')
    deadline = dt_start + timedelta(days=30)
    return deadline.strftime('%Y-%m-%d')


def match_org(org_str: str) -> str:
    org_match = [org for org in ORG_MAPPING.keys() if org.lower().replace('-','').startswith(org_str.lower().replace('-',''))]
    if len(org_match) == 1:
        return org_match[0]
    raise ValueError(f'Unidenitifed org: {org_str}')


def match_noa_plan(code_int: int) -> tuple:
    code_match = ACTION_MAPPING.get(code_int)
    if code_match:
        title, plan = code_match
        return (f'{code_int} - {title}',plan[0])
    raise ValueError(f'Unidentified NOA code: {code_int}')


def match_HRC_HRL(org_str: str) -> tuple:
    plan_match = ORG_MAPPING.get(org_str)
    if plan_match:
        return plan_match
    raise ValueError(f'Unidenitifed org: {org_str}')


def match_notice(plan_type: str, deadline: str) -> str:
    deadline = datetime.strptime(deadline, '%Y-%m-%d')
    if TODAY <= deadline:
        if plan_type in LONG_TERM_PLANS:
            return STANDARD_NOTICE.LONG_TERM
        return STANDARD_NOTICE.TEMPORARY
    elif TODAY > deadline:
        if plan_type in LONG_TERM_PLANS:
            return LATE_NOTICE.LONG_TERM
        return LATE_NOTICE.TEMPORARY


def process_notice_template(notice: str, action: Action) -> str:
    replacements = {
        '$EMPLOYEE':        action.employee,
        '$ACTION':          action.noa,
        '$EFFECTIVE_DATE':  action.start_date,
        '$FISCAL_YEAR':     CURRENT_FY,
        '$DEADLINE':        action.deadline,
        '$PLAN_TYPE':       action.plan_type,
        '$EFFECTIVE_DATE':  action.start_date,
        '$END_DATE':        action.end_date,
        '$SUPERVISOR':      action.supervisor,
        '$ORG':             action.org,
        '$CONSULTANT':      action.consultant[:-1],
        '$LIAISON':         action.liaison,
        '$ORG':             action.org,
        '$EMP_LAST':        action.employee.split()[0][:-1],
        '$SUPV_LAST':       action.supervisor.split()[0][:-1],
    }
    for placeholder, text in replacements.items():
        notice = notice.replace(placeholder,str(text))
    return notice


def get_yaml_data(file_path: str) -> Action | list[Action]:
    with open(file_path) as file:
        yaml_data: dict = yaml.safe_load(file)
        if not yaml_data:
            raise ValueError('No data has been entered for processing.')
    action = Action(
        code        = yaml_data['code'],
        start_date  = convert_date(yaml_data['start']),
        end_date    = convert_date(yaml_data['end']),
        employee    = Formatting.name(yaml_data['employee']),
        supervisor  = Formatting.name(yaml_data['supervisor']),
        org         = match_org(yaml_data['org']),
    )
    action.end_date = CURRENT_FY_END_DATE if not action.end_date else convert_date(action.end_date)
    if not isinstance(action.code,int) and ' ' in action.code:
        action.code = int(action.code.split()[0])
    return action


def save_notice_to_file(file_path: str, formatted_notice: str) -> None:
    with open(file_path,'w') as f:
        f.write(formatted_notice)


def save_to_yaml(save_path: str, action: Action) -> None:
    today = TODAY.strftime('%Y-%m-%d')
    employee = action.employee

    with open(save_path,'r+') as save_file:
        data: dict = yaml.safe_load(save_file)
        if not data:
            data = {}
        if not data.get(today):
            data[today] = {}
        if ';' in action.liaison:
            action.liaison = [hrl.strip() for hrl in action.liaison.split(';')]
        data[today][employee] = action.__dict__
        del data[today][employee]['employee']
        save_file.seek(0)
        yaml.safe_dump(data, save_file)
