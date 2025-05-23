from dataclasses import dataclass
from constants import TODAY

LINK: str

HEADER: str

TEMP_POSITION_TEXT: str

NOTICE_BODY: str

PAST_DUE_TEXT: str

PERFORMANCE_PLAN: str

FOOTER: str

@dataclass
class Notice:
    LONG_TERM: str
    TEMPORARY: str


def create_notice(is_late: bool, is_temporary: bool) -> str:
    base_components = [HEADER]
    if is_temporary:
        base_components.append(TEMP_POSITION_TEXT)
    base_components.append(NOTICE_BODY)
    if is_late:
        base_components.append(PAST_DUE_TEXT)
    base_components.extend([PERFORMANCE_PLAN, FOOTER])
    return "".join(base_components)


STANDARD_NOTICE: Notice = Notice(
    LONG_TERM=create_notice(is_late=False, is_temporary=False),
    TEMPORARY=create_notice(is_late=False, is_temporary=True),
)
LATE_NOTICE: Notice = Notice(
    LONG_TERM=create_notice(is_late=True, is_temporary=False),
    TEMPORARY=create_notice(is_late=True, is_temporary=True),
)
