import json
import re
from datetime import datetime, timezone
from pathlib import Path

from app.schemas.template import TaskTemplateCreate, TaskTemplateRead, TaskTemplateUpdate


DEFAULT_TEMPLATES = [
    {
        "id": "news_article",
        "label": "News Article",
        "name": "News Monitor",
        "start_url": "https://example.com/news",
        "cron_expr": "0 */6 * * *",
        "parser_rules": None,
        "enabled": True,
        "description": "General article pages with readability fallback.",
        "tags": ["readability", "article", "general"],
        "usage_count": 0,
        "last_used_at": None,
    },
    {
        "id": "tender_notice",
        "label": "Tender Notice",
        "name": "Tender Notice Monitor",
        "start_url": "https://example.com/tenders",
        "cron_expr": "0 */2 * * *",
        "parser_rules": '{"title_selector":"h1","content_selector":".article-content"}',
        "enabled": True,
        "description": "Stable detail pages for bidding and procurement notices.",
        "tags": ["tender", "bidding", "detail-page"],
        "usage_count": 0,
        "last_used_at": None,
    },
    {
        "id": "portal_announcement",
        "label": "Portal Announcement",
        "name": "Portal Announcement Monitor",
        "start_url": "https://example.com/announcements",
        "cron_expr": "0 8,12,16 * * *",
        "parser_rules": '{"title_selector":".detail-title","content_selector":".detail-body"}',
        "enabled": True,
        "description": "A good baseline for enterprise or government notice portals.",
        "tags": ["portal", "announcement", "structured"],
        "usage_count": 0,
        "last_used_at": None,
    },
]


class TemplateService:
    def __init__(self) -> None:
        server_dir = Path(__file__).resolve().parents[2]
        self.template_dir = server_dir / "storage" / "templates"
        self.template_file = self.template_dir / "task_templates.json"

    async def list_task_templates(self) -> list[TaskTemplateRead]:
        templates = self._load_templates()
        return [TaskTemplateRead.model_validate(item) for item in templates]

    async def create_task_template(self, payload: TaskTemplateCreate) -> TaskTemplateRead:
        templates = self._load_templates()
        template_id = payload.id or self._slugify(payload.label)
        if any(item["id"] == template_id for item in templates):
            raise ValueError(f"Template {template_id} already exists")

        template = TaskTemplateRead(id=template_id, **payload.model_dump(exclude={"id"}))
        templates.append(template.model_dump())
        self._save_templates(templates)
        return template

    async def update_task_template(
        self,
        template_id: str,
        payload: TaskTemplateUpdate,
    ) -> TaskTemplateRead:
        templates = self._load_templates()
        for index, item in enumerate(templates):
            if item["id"] != template_id:
                continue
            updated = TaskTemplateRead(id=template_id, **payload.model_dump())
            templates[index] = updated.model_dump()
            self._save_templates(templates)
            return updated
        raise LookupError(f"Template {template_id} not found")

    async def delete_task_template(self, template_id: str) -> None:
        templates = self._load_templates()
        filtered = [item for item in templates if item["id"] != template_id]
        if len(filtered) == len(templates):
            raise LookupError(f"Template {template_id} not found")
        self._save_templates(filtered)

    async def track_task_template_use(self, template_id: str) -> TaskTemplateRead:
        templates = self._load_templates()
        for index, item in enumerate(templates):
            if item["id"] != template_id:
                continue
            item["usage_count"] = int(item.get("usage_count", 0)) + 1
            item["last_used_at"] = datetime.now(timezone.utc).isoformat()
            templates[index] = item
            self._save_templates(templates)
            return TaskTemplateRead.model_validate(item)
        raise LookupError(f"Template {template_id} not found")

    def _load_templates(self) -> list[dict]:
        self.template_dir.mkdir(parents=True, exist_ok=True)
        if not self.template_file.exists():
            self._save_templates(DEFAULT_TEMPLATES)
        loaded = json.loads(self.template_file.read_text(encoding="utf-8"))
        if not isinstance(loaded, list):
            raise ValueError("Template storage must contain a list")
        for item in loaded:
            item.setdefault("usage_count", 0)
            item.setdefault("last_used_at", None)
        return loaded

    def _save_templates(self, templates: list[dict]) -> None:
        self.template_dir.mkdir(parents=True, exist_ok=True)
        self.template_file.write_text(
            json.dumps(templates, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
        return slug or "template"
