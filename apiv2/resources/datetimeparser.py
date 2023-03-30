from datetime import datetime
from flask_restx import abort


def parse_datetime(in_str: str | None) -> datetime | None:
    if in_str is None:
        return None
    try:
        return datetime.fromisoformat(in_str)
    except ValueError as error:
        abort(400, message=f"Error parsing 'date' field:{error}")
