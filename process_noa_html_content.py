from datetime import datetime, timedelta
from time import sleep

from bs4 import BeautifulSoup


def get_html_content() -> str:
    file: str
    with open(file, "r") as f:
        html_content: str = f.read()
        sections: list[str] = [
            section.strip() for section in html_content.split("<tr>") if section.strip()
        ]
        cleaned_content: str = "\n".join(
            line.strip()
            for section in sections
            for line in section.split("\n")
            if line.strip()
        )
    with open(file,'w') as f:
        pass
    return cleaned_content


def extract_text_from_html(html_content: str) -> list[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    return [line.strip() for line in soup.get_text().split("\n") if line.strip()]


def extract_award_items(cleaned_content: list[str]):
    award_items: list[tuple[str,...]] = []
    for i, line in enumerate(cleaned_content):
        if i + 5 >= len(cleaned_content):
            continue
        if any(line.startswith(code) for code in ["840", "841", "846", "847", "849"]):
            noa_code: int = int(cleaned_content[i][:3])
            award_date: datetime = datetime.strptime(cleaned_content[i + 1], "%m/%d/%Y")
            award_value: int = int(
                float(
                    "".join(
                        char
                        for char in cleaned_content[i + 5]
                        if char.isdigit() or char == "."
                    )
                )
            )
            award_items.append((noa_code, award_date, award_value))
    return award_items


def is_within_one_year(award_date: datetime) -> bool:
    today: datetime = datetime.now()
    one_year_ago: datetime = today - timedelta(days=365)
    return one_year_ago <= award_date <= today


def filter_by_date(extracted_info: list[tuple]) -> list[tuple]:
    date_filtered_items: list[tuple] = [
        extracted for extracted in extracted_info if is_within_one_year(extracted[1])
    ]
    return date_filtered_items


def format_content(date_filtered_items: list[tuple]) -> str:
    code_map: dict[int, str] = {
        840: {"category": "IND"},
        841: {"category": "GRP"},
        846: {"category": "IND"},
        847: {"category": "GRP"},
        849: {"category": "IND"},
    }
    header: str = f'"[Count: {len(date_filtered_items)}] ...\n'
    string: str = ""
    for item in date_filtered_items:
        noa_code, item_date, amount = item
        category: str = code_map[noa_code]['category']
        amount: str = f"${amount}" if noa_code in (840,841,849) else f"{amount} hrs."
        string += f">>> {item_date.date()}, NOA {noa_code}, {category}, {amount}\n"
    return (header + string).strip()+'"'


def save_to_file(string: str) -> None:
    with open("file.txt", "w") as file:
        file.write(string)
        print(string)
        print("...saved to file.\n")


def main():
    while True:
        html_content = get_html_content()
        if html_content:
            cleaned_content = extract_text_from_html(html_content)
            extracted_info = extract_award_items(cleaned_content)
            if not extracted_info:
                print("[count: 0]")
                continue
            date_filtered_items = filter_by_date(extracted_info)
            formatted_string = format_content(date_filtered_items)
            save_to_file(formatted_string)
        sleep(2)
    

main()
