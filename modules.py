from dataclasses import dataclass

@dataclass
class Action:
    code: int
    start_date: str
    employee: str
    end_date: str
    supervisor: str
    org: str
    deadline: str = ''
    consultant: str = ''
    liaison: str = ''
    noa: str = ''
    plan_type: str = ''
