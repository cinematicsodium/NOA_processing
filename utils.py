import os
import unicodedata
from datetime import date, datetime, timedelta
from pprint import pprint

import yaml
from constants import *
from modules import Action
from notices import LATE_NOTICE, STANDARD_NOTICE


class NameFormatting:
    @staticmethod
    def _parse_name_parts(raw_name: str) -> list[str]:
        return raw_name.split(" ") if " " in raw_name else raw_name

    def _format_last_name(last: str) -> str:
        chars = [char for char in last]
        if "'" in last:
            hyphen_idx = chars.index("'")
            if 1 <= hyphen_idx <= 2:
                chars[hyphen_idx + 1] = chars[hyphen_idx + 1].upper()
        elif last.lower().startswith("mc"):
            chars[2] = chars[2].upper()

        return "".join(chars)

    @staticmethod
    def _format_name_parts(name_parts: list[str] | str) -> tuple[str, str]:
        last, first = "", ""
        if isinstance(name_parts, list):
            if name_parts[0].endswith(","):
                last, first = name_parts[0][:-1], name_parts[1]
            elif "," in name_parts[0]:
                last, first = name_parts[0].split(",")
            else:
                first, last = name_parts[0], name_parts[1]
        elif isinstance(name_parts, str):
            if "," in name_parts:
                last, first = name_parts.split(",")

        uppercase_count = sum(1 for char in (last + first) if char.isupper())
        if not (2 <= uppercase_count <= 5):
            last, first = (
                NameFormatting._format_last_name(last.capitalize()),
                first.capitalize(),
            )

        return last, first

    @staticmethod
    def format_name(raw_name: str) -> str:
        if not raw_name:
            raise ValueError("Name field is blank.")

        name_parts = NameFormatting._parse_name_parts(raw_name)
        last, first = NameFormatting._format_name_parts(name_parts)

        return ", ".join([last, first])


def convert_to_datetime(date_value: str | date) -> datetime:
    if not date_value:
        return None

    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%m-%d",
        "%m/%d",
    ]
    if isinstance(date_value, str):
        current_year = TODAY.year
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_value, fmt)
                if not any(y in fmt for y in ["%Y", "%y"]):
                    parsed_date = parsed_date.replace(year=current_year)
                return parsed_date.date()
            except ValueError:
                continue
    elif isinstance(date_value, date):
        return date_value
    raise ValueError(f"Date format not recognized: {date_value}")


def convert_to_date_str(dt_date: date) -> str:
    return dt_date.strftime("%Y-%m-%d")


def compare_dates(start_date: date, end_date: date) -> None:
    if start_date >= end_date:
        raise ValueError(
            f"Invalid date range. Start date must be before the end date.\n"
            f"start_date:  {start_date}\n"
            f"end_date:    {end_date}"
        )
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def validate_detail_duration(start_date: date | str, end_date: date | str) -> None:
    start_date, end_date = convert_to_datetime(start_date), convert_to_datetime(
        end_date
    )
    compare_dates(start_date, end_date)
    minimum_detail_days: int = 90
    required_duration = timedelta(days=minimum_detail_days)
    actual_duration = end_date - start_date
    if actual_duration >= required_duration:
        return
    else:
        error_message = f"Invalid Detail duration: {actual_duration.days} days. Minimum required: {required_duration.days} days"
        raise ValueError(error_message)


def determine_thirty_day_deadline(start_date: date) -> str:
    deadline = start_date + timedelta(days=30)
    return deadline


def find_org_by_code(org_code: str) -> str:
    for org_name, code_prefixes in ORG_CODE_MAPPING.items():
        for prefix in code_prefixes:
            if org_code.startswith(prefix):
                return org_name
    raise ValueError(f"No matches found for org code: {org_code}")


def match_na_format(org_symbol: str) -> str:
    na_org_match = [
        org_name
        for org_name in ORG_MAPPING.keys()
        if org_name.lower() == f"na-{org_symbol}"
    ]
    if na_org_match:
        return na_org_match[0]


def find_org_by_symbol(org_symbol: str) -> str:
    def normalized(x: str) -> str:
        return str(x).lower().replace("-", "")

    normalized_symbol = normalized(org_symbol)

    na_org = match_na_format(org_symbol)
    if na_org:
        return na_org

    org_matches = [
        org_name
        for org_name in ORG_MAPPING.keys()
        if normalized_symbol in normalized(org_name)
    ]
    if not org_matches:
        raise ValueError(f"No matches found for org symbol: {org_symbol}")
    if len(org_matches) > 1:
        raise ValueError(f"Multiple matches found for org symbol: {org_symbol}")
    return org_matches[0]


def match_org(org_input: str | int) -> str:
    if org_input in ORG_MAPPING.keys():
        return org_input

    elif len(str(org_input)) == 10 or str(org_input).count("0") > 3:
        try:
            return find_org_by_code(org_input)
        except Exception:
            pass
    else:
        try:
            return find_org_by_symbol(org_input)
        except Exception:
            pass
    raise ValueError(f"No matches found for org input: {org_input}")


def get_action_details(code_int: int) -> tuple:
    code_match = action_dict().get(code_int)
    if code_match:
        title, plan = code_match
        return (f"{code_int} - {title}", plan)
    raise ValueError(f"Unable to match plan type to org: {code_int}")


def match_HRC_HRL(org_str: str) -> tuple:
    plan_match = ORG_MAPPING.get(org_str)
    if plan_match:
        return plan_match
    raise ValueError(f"Unable to match plan type to org: {org_str}")


def generate_direct_report_section(direct_reports: list | str) -> str:
    if not direct_reports:
        return ""

    tab = " " * 8
    if isinstance(direct_reports, list):
        formatted_emp_list = [f"{tab}- {employee}" for employee in direct_reports]
        formatted_emp_str = "\n".join(formatted_emp_list)
    else:
        formatted_emp_str = f"{tab}- {direct_reports}"
    final_format = f"  - direct reports:\n{formatted_emp_str}"
    return final_format


def generate_notice_template(plan_type: str, deadline: date) -> str:
    if TODAY < deadline:
        if plan_type in LONG_TERM_PLANS:
            return STANDARD_NOTICE.LONG_TERM
        else:
            return STANDARD_NOTICE.TEMPORARY
    elif TODAY >= deadline:
        if plan_type in LONG_TERM_PLANS:
            return LATE_NOTICE.LONG_TERM
        else:
            return LATE_NOTICE.TEMPORARY


def process_notice_template(notice: str, action: Action) -> str:
    replacements = {
        "$FISCAL_YEAR": CURRENT_FY,
        "$ACTION": action.noa_title,
        "$ORG": action.org,
        "$EMPLOYEE": action.employee,
        "$FMT_EMPLOYEE": "".join(action.employee.split(" ", 1)),
        "$EMP_LAST": action.employee.split()[0][:-1],
        "$SUPERVISOR": action.supervisor,
        "$SUPV_LAST": action.supervisor.split()[0][:-1],
        "$CONSULTANT": action.consultant[:-1],
        "$LIAISON": action.liaison,
        "$EFFECTIVE_DATE": action.start_date,
        "$DEADLINE": action.deadline,
        "$END_DATE": action.end_date,
        "$PLAN_TYPE": action.plan_type,
        "$DIRECT_REPORTS": generate_direct_report_section(action.direct_reports),
    }
    for placeholder, text in replacements.items():

        notice = notice.replace(placeholder, str(text))
    return notice


def format_direct_reports(direct_reports: list | str) -> list[str]:
    if isinstance(direct_reports, list):
        formatted_names = [
            NameFormatting.format_name(employee) for employee in direct_reports
        ]
        formatted_names.sort()
    else:
        formatted_names = NameFormatting.format_name(direct_reports)
    return formatted_names


def validate_action_items(action: Action) -> Action:
    required_fields: dict[str, str] = {
        "code": action.noa_code_int,
        "start": action.start_date,
        "employee": action.employee,
        "supervisor": action.supervisor,
        "org": action.org,
    }
    missing_required: list[str] = [k for k, v in required_fields.items() if not v]
    if missing_required:
        raise ValueError(
            f'The following fields are blank: {", ".join(missing_required)}'
        )

    action.end_date = CURRENT_FY_END_DATE if not action.end_date else action.end_date
    action.start_date = convert_to_datetime(action.start_date)
    action.end_date = convert_to_datetime(action.end_date)
    compare_dates(action.start_date, action.end_date)
    action.employee = NameFormatting.format_name(action.employee)
    action.supervisor = NameFormatting.format_name(action.supervisor)
    action.direct_reports = (
        ""
        if not action.direct_reports
        else format_direct_reports(action.direct_reports)
    )
    action.org = match_org(action.org)
    return action


def prep_yaml_data(file_path: str) -> None:
    def normalized_lines(text: str) -> list[str]:
        return (
            unicodedata.normalize("NFKD", text)
            .replace("\t", " ")
            .replace("\n\n", "\n")
            .replace("Name: ", "")
        ).split("\n")

    with open(file_path, "r") as f:
        data = f.read()
        if not data:
            raise ValueError(f"No content found in file {file_path}")

    raw_lines = normalized_lines(data)
    cleaned_lines = [line.strip() for line in raw_lines]

    with open(file_path, "w") as f:
        for cleaned in cleaned_lines:
            f.write(f"{cleaned}\n")


def get_yaml_data(file_path: str) -> Action | list[Action]:
    prep_yaml_data(file_path)
    with open(file_path) as file:
        yaml_data: dict[str, str | int] = yaml.safe_load(file)
        if not yaml_data:
            raise ValueError("No data has been entered for processing.")
        for k, v in yaml_data.items():
            if isinstance(v, str):
                yaml_data[k] = v.strip()
    action = Action(
        noa_code_int=yaml_data.get("code"),
        start_date=yaml_data.get("start"),
        end_date=yaml_data.get("end"),
        employee=yaml_data.get("employee"),
        supervisor=yaml_data.get("supervisor"),
        direct_reports=yaml_data.get("direct_reports"),
        org=yaml_data.get("org"),
    )
    action = validate_action_items(action)
    if isinstance(action.noa_code_int, str):
        if len(action.noa_code_int) == 3:
            action.noa_code_int = int(action.noa_code_int)
        elif action.noa_code_int[0:3].isdigit():
            action.noa_code_int = int(action.noa_code_int.split()[0])
    return action


def save_notice_to_file(file_path: str, formatted_notice: str) -> None:
    with open(file_path, "w") as f:
        f.write(formatted_notice)


def save_to_yaml_archive(archive_path: str, action: Action) -> None:
    action.start_date = convert_to_datetime(action.start_date)
    action.end_date = convert_to_datetime(action.end_date)

    with open(archive_path, "r") as yaml_archive:
        data: dict = yaml.safe_load(yaml_archive) or {}

    data.setdefault(TODAY, {})
    if not isinstance(data[TODAY], dict):
        data[TODAY] = {}
    data["most_recent"] = [TODAY, action.employee]

    if isinstance(action.liaison, str) and ";" in action.liaison:
        action.liaison = [hrl.strip() for hrl in action.liaison.split(";")]

    action_dict = vars(action).copy()
    action_dict.pop("employee", None)
    action_dict.pop("code_str", None)
    action_dict["code"] = action_dict.pop("code_int", None)
    if action.direct_reports == "":
        action_dict.pop("direct_reports", None)

    data[TODAY][action.employee] = action_dict

    with open(archive_path, "w") as yaml_archive:
        yaml.safe_dump(data, yaml_archive, indent=4)
        pprint({action.employee: action_dict})


def reset_yaml_file() -> None:
    keys: list[str] = [
        "code",
        "start",
        "end",
        "employee",
        "supervisor",
        "direct_reports",
        "org",
    ]

    with open(DATA_ENTRY_YAML, "w") as file:
        for key in keys:
            file.write(f"{key}: \n")

        file.write("\n")

        file.write("\n".join(f"# {k}: {v[0]}" for k, v in action_dict().items()))


def reset_notice_file() -> None:
    with open(NOTICE_TXT, "w") as file:
        pass


def reset_action_files() -> None:
    reset_yaml_file()
    reset_notice_file()
    print(
        f"\nsuccessfully reset to default:\n"
        f"•  {os.path.basename(DATA_ENTRY_YAML)}\n"
        f"•  {os.path.basename(NOTICE_TXT)}"
    )


def undo_most_recent() -> None:
    with open(ARCHIVE_YAML, "r") as yfile:
        file_data: dict = yaml.safe_load(yfile)
    most_recent = file_data.get("most_recent")
    if not most_recent:
        raise ValueError("Most recent action not found.")

    action_date, employee = most_recent
    date_string = datetime.strftime(action_date, "%Y-%m-%d")

    employee_data = (
        file_data[action_date].get(employee)
        if isinstance(file_data[action_date], dict)
        else None
    )
    if not employee_data:
        raise ValueError(
            "No data found for the following:\n"
            f"\t- Name: {employee}\n"
            f"\t- Date: {date_string}\n"
        )

    file_data[action_date].pop(employee)
    file_data["most_recent"] = None
    with open(ARCHIVE_YAML, "w") as yfile:
        yaml.safe_dump(file_data, yfile, indent=4)
        print(
            f"\nSuccessly reversed the most recent action:\n"
            f"\tName: {employee}\n"
            f"\tDate: {date_string}\n"
        )


def _get_user_input(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        user_input = input(f"\n{prompt}: ").strip()
        if user_input:  # Allow spaces in input
            return user_input
        elif not user_input and prompt in ["End Date", "Direct Reports"]:
            return ""
        print(
            "\nError: Invalid entry. Please try again ({} retries remaining).".format(
                max_retries - attempt - 1
            )
        )
    raise ValueError("Maximum retries exceeded. Unable to proceed.")


def _update_yaml_file(data: dict) -> None:
    with open(DATA_ENTRY_YAML, "r+") as yfile:
        yaml_data = yaml.safe_load(yfile) or {}  # Handle empty or non-existent file
        yaml_data.update(data)
        yfile.seek(0)
        yaml.safe_dump(yaml_data, yfile, indent=4)
        yfile.truncate()


def manual_entry() -> None:
    fields = {
        "Code": "code",
        "Start Date": "start",
        "End Date": "end",
        "Employee Name": "employee",
        "Supervisor Name": "supervisor",
        "Direct Reports": "direct_reports",
        "Organization": "org",
    }

    input_data = {v: _get_user_input(k) for k, v in fields.items()}

    if any(
        not val
        for key, val in input_data.items()
        if key not in ["end", "direct_reports"]
    ):
        print("Unable to proceed. Insufficient data provided.")
        return

    _update_yaml_file(input_data)


if __name__ == "__main__":
    manual_entry()


def code_to_org(code_str: str = None):
    if code_str is None:
        org_code = input("org code: ").strip()
    else:
        org_code = code_str

    print(f"\n{match_org(org_code)}\n")
