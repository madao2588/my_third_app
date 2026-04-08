from datetime import datetime
from pathlib import Path

from app.core.config import get_settings


settings = get_settings()
server_dir = Path(__file__).resolve().parents[2]


def save_snapshot(*, data_id: int, html: str, timestamp: datetime | None = None) -> str:
    current_time = timestamp or datetime.now()
    relative_dir = Path(settings.snapshot_dir) / current_time.strftime("%Y/%m/%d")
    absolute_dir = server_dir / relative_dir
    absolute_dir.mkdir(parents=True, exist_ok=True)

    relative_path = relative_dir / f"{data_id}.html"
    absolute_path = server_dir / relative_path
    absolute_path.write_text(html, encoding="utf-8")
    return relative_path.as_posix()
