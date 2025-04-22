from dataclasses import dataclass
from typing import Optional

import yaml
from constants import PathManager


@dataclass
class ActionProcessor:
    noa_code: Optional[int] = None
    noa_title: Optional[str] = None
    org: Optional[str] = None
    employee_name: Optional[str] = None
    supervisor_name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    direct_reports: Optional[str] = None
    liaison: Optional[str] = None
    consultant: Optional[str] = None
    plan_category: Optional[str] = None
    deadline: Optional[str] = None

    def load_data(self) -> None:
        with open(PathManager.data_entry_path, "r", encoding="utf-8") as yf:
            data = yaml.safe_load(yf)

    def populate(self) -> None:
        ydata: dict[str, str | int] = self.load_data()

        self.noa_code = ydata.get("noa_code")
        self.start_date = ydata.get("noa_code")
        self.end_date = ydata.get("end_date")
        self.employee_name = ydata.get("employee_name")
        self.supervisor_name = ydata.get("supervisor_name")
        self.direct_reports = ydata.get("direct_reports")
        self.pay_pool = ydata.get("pay_pool")
