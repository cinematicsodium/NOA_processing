from datetime import datetime


DATA_ENTRY_YAML_PATH: str
NOTICE_TXT_PATH: str
ARCHIVE_YAML_PATH: str


TODAY = datetime.now().date()
FISCAL_YEAR_START_MONTH = 10
def get_current_fiscal_year():
    current_year = datetime.now().year
    return current_year + 1 if datetime.now().month >= FISCAL_YEAR_START_MONTH else current_year
CURRENT_FISCAL_YEAR: str
CURRENT_FISCAL_YEAR_END_DATE: str
NEXT_FISCAL_YEAR: str


SES: str
ANNUAL: str
DETAIL: str
PROMO: str
TERM: str
LONG_TERM_PLANS: list[str] = [SES, ANNUAL]
TEMPORARY_PLANS: list[str] = [DETAIL, PROMO]


class Consultants: # Class used for dot notation simplication.
    NAME: str = "Name"
HRC: Consultants = Consultants()

class Liaisons:
    NAME: str = "name@email.gov"
HRL: Liaisons = Liaisons()

ORG_MAPPING: dict[str, list[str]] = {
    "org_name": [HRC.NAME,HRL.NAME]
}


ORG_CODE_MAPPING: dict[str,list[str]] = {}


ACTION_DETAILS: dict[int, list[str]] = {}

def action_dict() -> dict[int, list[str]]:
    for details in ACTION_DETAILS.values():
        if details[0][0].isdigit():
            raise ValueError(f"Action code details must not start with a digit: {details[0]}")
    return ACTION_DETAILS
