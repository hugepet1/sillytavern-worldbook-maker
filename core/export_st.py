# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Character, RuleEntry, WorldBookProject, _split_keys
from .triggers import (
    build_affection_system_content,
    build_trigger_content,
    build_trigger_keys,
)


def _base_entry(
    uid: int,
    *,
    comment: str,
    keys: list[str],
    content: str,
    constant: bool = False,
    order: int = 100,
    depth: int = 4,
) -> dict[str, Any]:
    return {
        "uid": uid,
        "key": keys,
        "keysecondary": [],
        "comment": comment,
        "content": content.strip(),
        "constant": constant,
        "vectorized": False,
        "selective": True,
        "selectiveLogic": 0,
        "addMemo": True,
        "order": order,
        "position": 0,
        "disable": False,
        "excludeRecursion": False,
        "preventRecursion": False,
        "matchPersonaDescription": False,
        "matchCharacterDescription": False,
        "matchCharacterPersonality": False,
        "matchCharacterDepthPrompt": False,
        "matchScenario": False,
        "matchCreatorNotes": False,
        "delayUntilRecursion": False,
        "probability": 100,
        "useProbability": True,
        "depth": depth,
        "group": "",
        "groupOverride": False,
        "groupWeight": 100,
        "scanDepth": None,
        "caseSensitive": None,
        "matchWholeWords": None,
        "useGroupScoring": None,
        "automationId": "",
        "role": None,
        "sticky": 0,
        "cooldown": 0,
        "delay": 0,
        "displayIndex": uid,
        "triggers": [],
        "characterFilter": {"isExclude": False, "names": [], "tags": []},
    }


def build_world_content(project: WorldBookProject) -> str:
    parts: list[str] = []
    title = project.book_name.strip() or "未命名世界书"
    parts.append(f"【世界观｜{title}】")
    if project.world_content.strip():
        parts.append(project.world_content.strip())
    return "\n".join(parts).strip()


def _char_fields_empty(char: Character) -> bool:
    return not any(
        getattr(char, f).strip()
        for f in (
            "age",
            "height",
            "body",
            "appearance",
            "hair_eyes",
            "clothing",
            "personality",
            "background",
            "skills_notes",
            "aliases",
        )
    )


def build_character_content(char: Character) -> str:
    # Preserve raw imported ST entry body when form fields were not filled.
    extra = char.extra_content.strip()
    if extra and _char_fields_empty(char):
        return extra

    name = char.name.strip() or "未命名角色"
    lines = [f"【角色｜{name}】"]

    def add(label: str, value: str) -> None:
        v = value.strip()
        if v:
            lines.append(f"{label}：{v}")

    add("别名", char.aliases)
    add("年龄", char.age)
    add("身高", char.height)
    add("身材", char.body)
    add("外貌", char.appearance)
    add("发型瞳色", char.hair_eyes)
    add("服装", char.clothing)
    add("性格", char.personality)
    add("背景", char.background)
    add("技能/台词备注", char.skills_notes)
    if extra:
        lines.append("")
        lines.append(extra)
    return "\n".join(lines).strip()


def build_entries(project: WorldBookProject) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    uid = 0

    world_keys = _split_keys(project.world_keys)
    if project.book_name.strip() and project.book_name.strip() not in world_keys:
        world_keys = [project.book_name.strip()] + world_keys
    if not world_keys:
        world_keys = ["世界观"]

    entries[str(uid)] = _base_entry(
        uid,
        comment=f"{project.book_name.strip() or '世界观'}·世界观",
        keys=world_keys,
        content=build_world_content(project),
        constant=project.world_constant,
        order=1,
        depth=4,
    )
    uid += 1

    for i, rule in enumerate(project.rules):
        title = rule.title.strip() or f"规则{i + 1}"
        comment = rule.comment.strip() or title
        entries[str(uid)] = _base_entry(
            uid,
            comment=comment,
            keys=rule.keyword_list(),
            content=rule.content.strip() or f"【{title}】",
            constant=rule.constant,
            order=10 + i,
            depth=4,
        )
        uid += 1

    aff_sys = build_affection_system_content(project)
    if aff_sys:
        entries[str(uid)] = _base_entry(
            uid,
            comment="好感度系统总则",
            keys=["好感度", "好感", "亲密度", "favor"],
            content=aff_sys,
            constant=True,
            order=40,
            depth=4,
        )
        uid += 1

    for i, tr in enumerate(project.triggers):
        content = build_trigger_content(tr)
        comment = tr.comment.strip() or tr.title.strip() or f"触发{i + 1}"
        entries[str(uid)] = _base_entry(
            uid,
            comment=comment,
            keys=build_trigger_keys(tr),
            content=content,
            constant=tr.constant,
            order=50 + i,
            depth=6,
        )
        uid += 1

    for i, char in enumerate(project.characters):
        comment = char.comment.strip() or (char.name.strip() or f"角色{i + 1}")
        entries[str(uid)] = _base_entry(
            uid,
            comment=comment,
            keys=char.keyword_list() or [char.name.strip() or f"角色{i + 1}"],
            content=build_character_content(char),
            constant=char.constant,
            order=100 + i,
            depth=8,
        )
        uid += 1

    return entries

def export_worldbook_json(project: WorldBookProject, path: str | Path) -> Path:
    path = Path(path)
    data = {"entries": build_entries(project)}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_draft(project: WorldBookProject, path: str | Path) -> Path:
    path = Path(path)
    path.write_text(json.dumps(project.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_draft(path: str | Path) -> WorldBookProject:
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if "entries" in data and "characters" not in data:
        return import_st_worldbook(data)
    return WorldBookProject.from_dict(data)


def _looks_like_character(content: str, comment: str) -> bool:
    if any(m in content[:60] for m in ("【角色｜", "【干员｜")):
        return True
    if "·外观" in comment or comment.endswith("外观技能语音"):
        return True
    return False


def import_st_worldbook(data: dict[str, Any]) -> WorldBookProject:
    """Best-effort import of SillyTavern worldbook JSON into editable project."""
    entries = data.get("entries") or {}

    def sort_key(item: tuple[str, Any]) -> int:
        k, e = item
        try:
            return int(e.get("uid", k))
        except (TypeError, ValueError):
            return 0

    sorted_items = sorted(entries.items(), key=sort_key)
    project = WorldBookProject()
    chars: list[Character] = []
    rules: list[RuleEntry] = []

    if not sorted_items:
        return project

    _first_uid, first = sorted_items[0]
    project.book_name = (
        str(first.get("comment") or "导入世界书").replace("·世界观", "").strip() or "导入世界书"
    )
    project.world_content = str(first.get("content") or "")
    project.world_constant = bool(first.get("constant", True))
    keys = first.get("key") or []
    if isinstance(keys, list):
        project.world_keys = ",".join(str(k) for k in keys)

    for _, e in sorted_items[1:]:
        content = str(e.get("content") or "")
        comment = str(e.get("comment") or "")
        keys = e.get("key") or []
        key_str = ",".join(str(k) for k in keys) if isinstance(keys, list) else ""

        if _looks_like_character(content, comment):
            name = ""
            for tag in ("【角色｜", "【干员｜"):
                if tag in content:
                    start = content.find(tag) + len(tag)
                    end = content.find("】", start)
                    if end > start:
                        name = content[start:end].split("·")[0].split()[0]
                        break
            if not name:
                name = comment.split("·")[0].strip() or (str(keys[0]) if keys else "未命名")
            aliases = ""
            if isinstance(keys, list) and keys:
                rest = [str(k) for k in keys if str(k) != name]
                aliases = ",".join(rest)
            chars.append(
                Character(
                    name=name,
                    aliases=aliases,
                    comment=comment,
                    constant=bool(e.get("constant", False)),
                    extra_content=content,
                )
            )
        else:
            title = comment or (str(keys[0]) if keys else "规则")
            rules.append(
                RuleEntry(
                    title=title,
                    keys=key_str,
                    content=content,
                    constant=bool(e.get("constant", False)),
                    comment=comment or title,
                )
            )

    project.rules = rules
    project.characters = chars
    return project

def preview_json_text(project: WorldBookProject) -> str:
    data = {"entries": build_entries(project)}
    return json.dumps(data, ensure_ascii=False, indent=2)
