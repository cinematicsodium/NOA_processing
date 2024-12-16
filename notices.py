from dataclasses import dataclass
from modules import Action

LINK: str = ''
HEADER: str = ''
SEC_0: str = ''
SEC_1: str = ''
SEC_2: str = ''
SEC_3: str = ''
FOOTER: str = ''

@dataclass
class Notice:
    LONG_TERM: str
    TEMPORARY: str


def create_notice(is_late: bool, is_temporary: bool) -> str:
    base_components = [HEADER]
    if is_temporary:
        base_components.append(SEC_0)
    base_components.append(SEC_1)
    if is_late:
        base_components.append(SEC_2)
    base_components.extend([SEC_3, FOOTER])
    return ''.join(base_components)


STANDARD_NOTICE: Notice = Notice(
    LONG_TERM = create_notice(is_late=False, is_temporary=False),
    TEMPORARY = create_notice(is_late=False, is_temporary=True),
)
LATE_NOTICE: Notice = Notice(
    LONG_TERM = create_notice(is_late=True, is_temporary=False),
    TEMPORARY = create_notice(is_late=True, is_temporary=True)
)
