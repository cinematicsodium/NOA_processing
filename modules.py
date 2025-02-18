from dataclasses import dataclass


@dataclass
class Action:
    noa_code_int: int
    org: str
    employee: str
    supervisor: str
    start_date: str
    end_date: str
    direct_reports: str = ""
    liaison: str = ""
    noa_description: str = ""
    consultant: str = ""
    plan_type: str = ""
    deadline: str = ""
