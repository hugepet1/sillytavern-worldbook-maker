# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Character:
    name: str = ""
    aliases: str = ""
    age: str = ""
    height: str = ""
    body: str = ""
    appearance: str = ""
    hair_eyes: str = ""
    clothing: str = ""
    personality: str = ""
    background: str = ""
    skills_notes: str = ""
    custom_keys: str = ""
    comment: str = ""
    constant: bool = False
    extra_content: str = ""

    def alias_list(self) -> list[str]:
        return _split_keys(self.aliases)

    def custom_key_list(self) -> list[str]:
        return _split_keys(self.custom_keys)

    def keyword_list(self) -> list[str]:
        keys: list[str] = []
        if self.name.strip():
            keys.append(self.name.strip())
        keys.extend(self.alias_list())
        keys.extend(self.custom_key_list())
        seen: set[str] = set()
        out: list[str] = []
        for k in keys:
            if k and k not in seen:
                seen.add(k)
                out.append(k)
        return out

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Character":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class RuleEntry:
    """系统机制/纪律条目（沉浸锁、起装、经济等）。"""

    title: str = "未命名规则"
    keys: str = ""
    content: str = ""
    constant: bool = False
    comment: str = ""

    def keyword_list(self) -> list[str]:
        keys = _split_keys(self.keys)
        title = self.title.strip()
        if title and title not in keys:
            keys = [title] + keys
        return keys or ([title] if title else ["规则"])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RuleEntry":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class AffectionTier:
    """好感度档位：达到 threshold 时触发 effect。"""

    threshold: str = "50"
    effect: str = ""


@dataclass
class TriggerRule:
    """条件触发：好感度档位 / 捡到物品 / 自定义条件。"""

    kind: str = "affection"  # affection | item | custom
    title: str = ""
    # affection
    character: str = ""  # 绑定角色名，空=全员/用户指定
    affection_min: str = "0"
    affection_max: str = "100"
    tiers: list[AffectionTier] = field(default_factory=list)
    # item
    item_name: str = ""
    picker: str = "任何人"  # 用户 / 角色 / 任何人 / 指定角色名
    # custom
    condition: str = ""
    # shared
    effect: str = ""  # item/custom 主效果；affection 可作总说明
    extra_keys: str = ""
    constant: bool = False
    comment: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TriggerRule":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        raw = {k: v for k, v in data.items() if k in known}
        tiers = raw.get("tiers") or []
        raw["tiers"] = [
            AffectionTier(**t) if isinstance(t, dict) else t for t in tiers
        ]
        return cls(**raw)


@dataclass
class WorldBookProject:
    book_name: str = "未命名世界书"
    world_content: str = ""
    immersion_rules: str = ""
    world_constant: bool = True
    world_keys: str = "世界观"
    rules: list[RuleEntry] = field(default_factory=list)
    characters: list[Character] = field(default_factory=list)
    triggers: list[TriggerRule] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": 3,
            "book_name": self.book_name,
            "world_content": self.world_content,
            "immersion_rules": self.immersion_rules,
            "world_constant": self.world_constant,
            "world_keys": self.world_keys,
            "rules": [r.to_dict() for r in self.rules],
            "characters": [c.to_dict() for c in self.characters],
            "triggers": [t.to_dict() for t in self.triggers],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorldBookProject":
        chars = [Character.from_dict(c) for c in data.get("characters", [])]
        rules = [RuleEntry.from_dict(r) for r in data.get("rules", [])]
        triggers = [TriggerRule.from_dict(t) for t in data.get("triggers", [])]
        return cls(
            book_name=data.get("book_name", "未命名世界书"),
            world_content=data.get("world_content", ""),
            immersion_rules=data.get("immersion_rules", ""),
            world_constant=bool(data.get("world_constant", True)),
            world_keys=data.get("world_keys", "世界观"),
            rules=rules,
            characters=chars,
            triggers=triggers,
        )


def _split_keys(raw: str) -> list[str]:
    if not raw:
        return []
    for sep in ("，", ";", "；", "|", "\n", "\t"):
        raw = raw.replace(sep, ",")
    return [p.strip() for p in raw.split(",") if p.strip()]
