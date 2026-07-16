# -*- coding: utf-8 -*-
"""把好感度/拾取等触发规则拼成世界书 content。"""
from __future__ import annotations

from .models import TriggerRule, WorldBookProject, _split_keys


KIND_LABEL = {
    "affection": "好感度",
    "item": "拾取物品",
    "custom": "自定义条件",
}


def build_trigger_content(tr: TriggerRule) -> str:
    kind = tr.kind if tr.kind in KIND_LABEL else "custom"
    title = tr.title.strip() or _default_title(tr)

    if kind == "affection":
        who = tr.character.strip() or "（未指定角色，默认对当前提及角色生效）"
        lines = [
            f"【触发｜好感度｜{title}】",
            f"适用角色：{who}",
            f"好感度范围：{tr.affection_min.strip() or '0'} ～ {tr.affection_max.strip() or '100'}",
            "判定：对话出现好感/亲密度/favor 或本条关键词时，按数值档位执行（可多档并存，取已达到的最高相关档）。",
            "",
            "■ 档位表（达到该值即触发）",
        ]
        tiers = sorted(
            [t for t in tr.tiers if str(t.threshold).strip() or t.effect.strip()],
            key=lambda t: _num(t.threshold),
        )
        if not tiers:
            lines.append("（尚未填写档位）")
        else:
            for t in tiers:
                lines.append(f"· ≥ {t.threshold.strip() or '?'}：{t.effect.strip() or '（未写效果）'}")
        if tr.effect.strip():
            lines.append("")
            lines.append("■ 总说明")
            lines.append(tr.effect.strip())
        lines.append("")
        lines.append("■ 演出要求")
        lines.append("达到档位时必须在剧情/对白中体现对应变化；未达档位禁止提前触发高档内容。")
        return "\n".join(lines)

    if kind == "item":
        item = tr.item_name.strip() or "（未命名物品）"
        picker = tr.picker.strip() or "任何人"
        lines = [
            f"【触发｜拾取物品｜{title}】",
            f"物品：{item}",
            f"拾取者条件：{picker}",
            "",
            "■ 触发时机",
            f"当「{picker}」捡到 / 获得 / 放入背包或安全箱「{item}」时立刻触发。",
            "",
            "■ 触发效果",
            tr.effect.strip() or "（未填写效果）",
            "",
            "■ 演出要求",
            "描写发现与拾取过程；效果用对白/行动落地，勿只报系统提示。",
        ]
        return "\n".join(lines)

    # custom
    lines = [
        f"【触发｜自定义｜{title}】",
        "■ 条件",
        tr.condition.strip() or "（未填写条件）",
        "",
        "■ 效果",
        tr.effect.strip() or "（未填写效果）",
        "",
        "■ 演出要求",
        "条件满足时执行效果；未满足时禁止剧透该效果。",
    ]
    return "\n".join(lines)


def build_trigger_keys(tr: TriggerRule) -> list[str]:
    keys: list[str] = []
    keys.extend(_split_keys(tr.extra_keys))
    if tr.title.strip():
        keys.append(tr.title.strip())

    if tr.kind == "affection":
        keys.extend(["好感度", "好感", "亲密度", "favor"])
        if tr.character.strip():
            keys.append(tr.character.strip())
        for t in tr.tiers:
            if t.threshold.strip():
                keys.append(f"好感{t.threshold.strip()}")
    elif tr.kind == "item":
        keys.extend(["捡到", "拾取", "获得", "摸到"])
        if tr.item_name.strip():
            keys.append(tr.item_name.strip())
        if tr.picker.strip() and tr.picker.strip() not in ("任何人", "用户", "角色"):
            keys.append(tr.picker.strip())
    else:
        keys.append("触发")
        keys.extend(_split_keys(tr.condition)[:3])

    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k and k not in seen:
            seen.add(k)
            out.append(k)
    return out or ["触发"]


def build_affection_system_content(project: WorldBookProject) -> str | None:
    aff = [t for t in project.triggers if t.kind == "affection"]
    if not aff:
        return None
    lines = [
        "【好感度系统总则｜常驻】",
        "本世界存在好感度（亲密度）。默认用 0–100（各角色条目可另定范围）。",
        "增减由剧情行为决定：帮助、送礼、同生共死、背叛、冷暴力等。",
        "当对话提到好感/亲密度，或触达角色档位关键词时，查阅对应【触发｜好感度】条目并演出。",
        "禁止跳档：未达数值不得表现高档亲密/解锁内容。",
        "",
        "已配置好感条目：",
    ]
    for t in aff:
        who = t.character.strip() or "未指定角色"
        n = len([x for x in t.tiers if x.effect.strip() or x.threshold.strip()])
        lines.append(f"· {who} — {t.title.strip() or '好感档位'}（{n} 档）")
    return "\n".join(lines)


def _default_title(tr: TriggerRule) -> str:
    if tr.kind == "affection":
        return f"{tr.character.strip() or '角色'}好感档位"
    if tr.kind == "item":
        return f"捡到{tr.item_name.strip() or '物品'}"
    return "自定义触发"


def _num(s: str) -> float:
    try:
        return float(str(s).strip())
    except ValueError:
        return 0.0
