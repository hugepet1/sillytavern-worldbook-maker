# -*- coding: utf-8 -*-
"""中英双语文案。"""
from __future__ import annotations

_LANG = "zh"

TEXTS: dict[str, dict[str, str]] = {
    "app_title": {
        "zh": "傻瓜式 SillyTavern 世界书生成器",
        "en": "SillyTavern Worldbook Maker (Easy)",
    },
    "app_sub": {
        "zh": "世界观 → 角色 → 条件触发 → 导出 JSON",
        "en": "Lore → Characters → Triggers → Export JSON",
    },
    "lang": {"zh": "中文", "en": "EN"},
    "new": {"zh": "新建", "en": "New"},
    "open": {"zh": "打开", "en": "Open"},
    "prev": {"zh": "上一步", "en": "Back"},
    "next": {"zh": "下一步", "en": "Next"},
    "refresh_preview": {"zh": "刷新预览", "en": "Refresh"},
    "step_world": {"zh": "1 世界观", "en": "1 Lore"},
    "step_chars": {"zh": "2 角色", "en": "2 Cast"},
    "step_triggers": {"zh": "3 触发", "en": "3 Triggers"},
    "step_export": {"zh": "4 导出", "en": "4 Export"},
    "world_title": {"zh": "世界观", "en": "World Lore"},
    "world_hint": {
        "zh": "写书名和设定正文。勾选常驻后，SillyTavern 会始终注入这条。",
        "en": "Name your book and write the lore. Constant = always injected in SillyTavern.",
    },
    "book_name": {"zh": "世界书名称", "en": "Book name"},
    "world_keys": {"zh": "关键词（逗号分隔）", "en": "Keywords (comma-separated)"},
    "world_constant": {"zh": "常驻条目（constant）", "en": "Constant entry"},
    "world_body": {"zh": "世界观正文", "en": "Lore text"},
    "unnamed_book": {"zh": "未命名世界书", "en": "Untitled Worldbook"},
    "chars_title": {"zh": "角色", "en": "Characters"},
    "chars_hint": {
        "zh": "左侧增删角色，右侧填档案。别名会自动变成触发关键词。",
        "en": "Add characters on the left; fill fields on the right. Aliases become keywords.",
    },
    "char_list": {"zh": "角色列表", "en": "Cast list"},
    "add": {"zh": "新增", "en": "Add"},
    "delete": {"zh": "删除", "en": "Delete"},
    "char_constant": {"zh": "该角色常驻", "en": "Constant for this character"},
    "char_preview": {"zh": "正文预览", "en": "Entry preview"},
    "new_char": {"zh": "新角色", "en": "New character"},
    "f_name": {"zh": "名字 *", "en": "Name *"},
    "f_aliases": {"zh": "别名（逗号 → 关键词）", "en": "Aliases (comma → keywords)"},
    "f_age": {"zh": "年龄", "en": "Age"},
    "f_height": {"zh": "身高", "en": "Height"},
    "f_body": {"zh": "身材", "en": "Body"},
    "f_appearance": {"zh": "外貌", "en": "Appearance"},
    "f_hair_eyes": {"zh": "发型 / 瞳色", "en": "Hair / eyes"},
    "f_clothing": {"zh": "服装", "en": "Outfit"},
    "f_personality": {"zh": "性格", "en": "Personality"},
    "f_background": {"zh": "背景故事", "en": "Backstory"},
    "f_skills": {"zh": "技能 / 台词备注", "en": "Skills / voice notes"},
    "f_custom_keys": {"zh": "自定义关键词", "en": "Extra keywords"},
    "f_comment": {"zh": "条目备注", "en": "Entry comment"},
    "f_extra": {"zh": "附加正文", "en": "Extra text"},
    "trig_title": {"zh": "条件触发", "en": "Conditional Triggers"},
    "trig_hint": {
        "zh": "好感≥多少触发什么；或捡到某物品触发什么。",
        "en": "When affection ≥ N → do X. Or when an item is picked up → do Y.",
    },
    "trig_list": {"zh": "触发列表", "en": "Trigger list"},
    "add_aff": {"zh": "＋好感度", "en": "+ Affection"},
    "add_item": {"zh": "＋捡到物品", "en": "+ Item pickup"},
    "add_custom": {"zh": "＋自定义", "en": "+ Custom"},
    "kind": {"zh": "类型", "en": "Type"},
    "kind_aff": {"zh": "好感度", "en": "Affection"},
    "kind_item": {"zh": "拾取物品", "en": "Item pickup"},
    "kind_custom": {"zh": "自定义条件", "en": "Custom"},
    "entry_title": {"zh": "条目标题", "en": "Entry title"},
    "title_ph": {"zh": "可空，自动生成", "en": "Optional, auto title"},
    "apply_char": {"zh": "适用角色", "en": "Character"},
    "aff_min": {"zh": "最小", "en": "Min"},
    "aff_max": {"zh": "最大", "en": "Max"},
    "tiers": {"zh": "档位：达到数值 → 效果", "en": "Tiers: threshold → effect"},
    "add_tier": {"zh": "加一档", "en": "Add tier"},
    "item_name": {"zh": "物品名称", "en": "Item name"},
    "picker": {"zh": "谁捡到会触发", "en": "Who picks it up"},
    "anyone": {"zh": "任何人", "en": "Anyone"},
    "user": {"zh": "用户", "en": "User"},
    "role": {"zh": "角色", "en": "Character"},
    "named": {"zh": "指定角色", "en": "Named character"},
    "named_ph": {"zh": "指定角色名", "en": "Character name"},
    "condition": {"zh": "触发条件", "en": "Condition"},
    "effect": {"zh": "效果说明", "en": "Effect"},
    "extra_keys": {"zh": "额外关键词", "en": "Extra keywords"},
    "trig_constant": {"zh": "本条常驻", "en": "Constant"},
    "trig_preview": {"zh": "生成预览", "en": "Preview"},
    "export_title": {"zh": "预览与导出", "en": "Preview & Export"},
    "export_hint": {
        "zh": "导出可直接导入 SillyTavern 的世界书 JSON。",
        "en": "Export a SillyTavern World Info JSON ready to import.",
    },
    "export_json": {"zh": "导出世界书 JSON", "en": "Export Worldbook JSON"},
    "save_draft": {"zh": "保存工程草稿", "en": "Save project draft"},
    "confirm_new": {
        "zh": "清空当前内容并新建？",
        "en": "Clear everything and start a new project?",
    },
    "opened": {"zh": "已打开", "en": "Opened"},
    "open_fail": {"zh": "打开失败", "en": "Open failed"},
    "export_ok": {"zh": "导出成功", "en": "Exported"},
    "export_fail": {"zh": "导出失败", "en": "Export failed"},
    "save_ok": {"zh": "已保存", "en": "Saved"},
    "save_fail": {"zh": "保存失败", "en": "Save failed"},
    "export_tip": {
        "zh": "可在 SillyTavern → 世界书 中导入。",
        "en": "Import via SillyTavern → World Info.",
    },
    "summary": {
        "zh": "书名：{book}　｜　触发：{trig}　｜　角色：{char}　｜　条目约：{n}",
        "en": "Book: {book}  |  Triggers: {trig}  |  Characters: {char}  |  ~{n} entries",
    },
}


def get_lang() -> str:
    return _LANG


def set_lang(lang: str) -> None:
    global _LANG
    _LANG = "en" if lang == "en" else "zh"


def toggle_lang() -> str:
    set_lang("en" if _LANG == "zh" else "zh")
    return _LANG


def t(key: str, **kwargs: str) -> str:
    block = TEXTS.get(key, {})
    s = block.get(_LANG) or block.get("zh") or key
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s
