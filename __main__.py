from utils import *
from constants import *

LOAD_YAML: str = r'_load_.yaml'
NOTICE_TXT: str = r'_notice_.txt'
ARCHIVE_YAML: str = r'_archive_.yaml'
def main() -> None:
    try:
        print('processing...')
        action = get_yaml_data(file_path=LOAD_YAML)
        action.end_date = CURRENT_FY_END_DATE if not action.end_date else action.end_date
        action.deadline = determine_thirty_day_deadline(action.start_date)
        action.employee = Formatting.name(action.employee)
        action.supervisor = Formatting.name(action.supervisor)
        action.org = match_org(action.org)
        action.consultant, action.liaison = match_HRC_HRL(action.org)
        action.noa, action.plan_type = match_noa_plan(action.code)
        notice_template = match_notice(action.plan_type, action.deadline)
        formatted_notice = process_notice_template(notice_template, action)
        save_notice_to_file(file_path=NOTICE_TXT, formatted_notice=formatted_notice)
        save_to_yaml(save_path=ARCHIVE_YAML, action=action)
        print('processing complete.')
        print(f"{'.'*100}\n")
    except Exception as e:
        print(e)
main()
