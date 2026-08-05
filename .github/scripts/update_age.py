#!/usr/bin/env python3

import os
import re
from datetime import date, datetime
from pathlib import Path


BIRTHDAY_FORMAT = "%d.%m.%Y"
AGE_PATTERN = re.compile(r"(?<=<!-- age:start -->)\d+(?=<!-- age:end -->)")
README = Path(__file__).resolve().parents[2] / "README.md"


def calculate_age(birthday: date, today: date) -> int:
    return today.year - birthday.year - (
        (today.month, today.day) < (birthday.month, birthday.day)
    )


def main() -> None:
    birthday_value = os.environ.get("BIRTHDAY", "")

    if not re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", birthday_value):
        raise SystemExit("The birthday secret must use the format DD.MM.YYYY.")

    try:
        birthday = datetime.strptime(birthday_value, BIRTHDAY_FORMAT).date()
    except ValueError as error:
        raise SystemExit("The birthday secret does not contain a valid date.") from error

    today = date.today()
    if birthday > today:
        raise SystemExit("The birthday secret cannot be a date in the future.")

    readme = README.read_text(encoding="utf-8")
    updated_readme, replacements = AGE_PATTERN.subn(str(calculate_age(birthday, today)), readme)

    if replacements != 1:
        raise SystemExit("Expected exactly one age marker in README.md.")

    if updated_readme != readme:
        README.write_text(updated_readme, encoding="utf-8")


if __name__ == "__main__":
    main()
