import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import NamedTuple, Optional

_local_dir: Path


class PathManager:
    data_entry_path: Path = _local_dir / ""
    email_notice_path: Path = _local_dir / ""
    archive_path: Path = _local_dir / ""
    json_org_list_path: Path = _local_dir / ""


def get_current_fiscal_year():
    current_date = datetime.now()
    current_year = current_date.year
    fiscal_year_start_month = 10

    if current_date.month >= fiscal_year_start_month:
        fiscal_year = current_year + 1
    else:
        fiscal_year = current_year

    return fiscal_year


class PlanManager:
    ses: str
    annual: str
    detail: str
    promotion: str
    terminated: str
    long_term_plans: list[str] = [ses, annual]
    temporary_plans: list[str] = [detail, promotion]


class FYManager:
    def __init__(self):
        self.curr_fy: int = self._calc_current_fy()
        self.curr_end_date = datetime(self.curr_fy, 9, 30)
        self.next_fy = self.curr_fy + 1

    def _calc_current_fy(self):
        current_date = datetime.now()
        current_year = current_date.year
        fiscal_year_start_month = 10

        if current_date.month >= fiscal_year_start_month:
            fiscal_year = current_year + 1
        else:
            fiscal_year = current_year

        return fiscal_year

    def __str__(self):
        return "\n".join(f"{k}: {v}" for k, v in self.__dict__.items())


class DateManager:
    @staticmethod
    def convert_to_str(date: datetime) -> Optional[str]:
        try:
            return date.strftime("%Y-%m-%d")
        except:
            print(f"Unable to convert '{date} to datetime'")

    @staticmethod
    def convert_to_datetime(date_str: str) -> datetime:
        if not date_str:
            return
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m-%d-%Y",
            "%m/%d/%Y",
            "%m/%d/%y",
            "%m-%d",
            "%m/%d",
        ]
        for fmt in formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)

                if "%y" not in fmt.lower():
                    parsed_date = parsed_date.replace(year=datetime.now().year)
                return parsed_date
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized for: {date_str}")

    @staticmethod
    def compare_dates(start_date: datetime, end_date: datetime) -> None:
        if start_date >= end_date:
            raise ValueError(
                f"Invalid date range. Start date must be before the end date.\n"
                f"start_date: {start_date}\n"
                f"end_date: {end_date}\n"
                f"timedelta: {(end_date-start_date).days} days"
            )

    @staticmethod
    def validate_duration(
        start_date: datetime, end_date: datetime, plan_type: str
    ) -> None:
        DateManager.compare_dates(start_date, end_date)
        if plan_type not in PlanManager.temporary_plans:
            return
        min_detail_days = timedelta(days=90)
        max_detail_days = timedelta(days=365)
        actual_duration = end_date - start_date
        if min_detail_days <= actual_duration <= max_detail_days:
            return
        else:
            error_message = f"Invalid Detail duration: {actual_duration.days} days.\nMinimum: 90\nMaximum: 365"
            raise ValueError(error_message)

    def thirty_day_deadline(start_date: datetime) -> datetime:
        deadline = start_date + timedelta(days=30)
        return deadline




class NOAConfig(NamedTuple):
    title: str
    plan: str


NOA_MAP: dict[int, NOAConfig] = MappingProxyType()


class HRC(StrEnum):
    name1: str
    name2: str
    etc: str


class HRL(StrEnum):
    liaison1: str
    liaison2: str
    etc: str


@dataclass
class OrgConfig:
    consultant: str
    liaisons: tuple[str, ...]
    code_prefixes: tuple[str, ...]


ORG_MAP: dict[str, OrgConfig] = MappingProxyType()

@dataclass
class OrgCodeInfo:
    code: Optional[str] = None
    symbol: Optional[str] = None
    title: Optional[str] = None
    main_org: Optional[str] = None


@dataclass
class OrgParser:
    lookup_value: str

    def __post_init__(self):
        if not isinstance(self.lookup_value,str):
            self.lookup_value = str(self.lookup_value)
        self.lookup_value = self.lookup_value.strip()
        self.org: OrgCodeInfo = OrgCodeInfo()
        if len(self.lookup_value) == 10 and self.lookup_value.count("0") >= 3:
            self.org.code = self.lookup_value

    def __str__(self):
        return "\n".join(
            f"{k}: {v}"
            for k, v in self.org.__dict__.items()
        )

    def load_json(self) -> list[dict[str, str]]:
        with open(PathManager.json_org_list_path, "r", encoding="utf-8") as jf:
            return json.load(jf)

    def parse(self):
        if self.org.code is not None:
            self.fetch_org_info()

    def fetch_org_info(self) -> tuple[str, str]:
        org_list: list[dict[str, str]] = self.load_json()
        for div_data in org_list:
            if div_data["code"] == self.org.code:
                self.org.symbol = div_data["symbol"]
                self.org.title = div_data["title"]
                self.org.main_org = self.match_code_prefix(self.org.code)
    
    def match_code_prefix(self, text: str) -> None:
        for org, config in ORG_MAP.items():
            for prefix in config.code_prefixes:
                if text.upper().startswith(prefix):
                    return org
