# -*- coding: utf-8 -*-
from __future__ import annotations

import customtkinter as ctk

import theme as T
import ui_kit as kit
from core.models import AffectionTier, TriggerRule, WorldBookProject
from core.triggers import build_trigger_content
from i18n import get_lang, t


class TriggersStep(ctk.CTkFrame):
    def __init__(self, master, project: WorldBookProject, **kwargs):
        super().__init__(master, fg_color=T.CARD, corner_radius=16, **kwargs)
        self.project = project
        self._index: int | None = None
        self._tier_rows: list = []
        self._list_buttons: list = []
        self._build()
        if self.project.triggers:
            self._select(0)
        else:
            self._show_kind("affection")
            self._set_enabled(False)

    def _kind_values(self) -> list[str]:
        return [t("kind_aff"), t("kind_item"), t("kind_custom")]

    def _kind_to_code(self, label: str) -> str:
        m = {t("kind_aff"): "affection", t("kind_item"): "item", t("kind_custom"): "custom"}
        # also match both langs
        if label in ("好感度", "Affection"):
            return "affection"
        if label in ("拾取物品", "Item pickup"):
            return "item"
        if label in ("自定义条件", "Custom"):
            return "custom"
        return m.get(label, "affection")

    def _code_to_kind(self, code: str) -> str:
        return {"affection": t("kind_aff"), "item": t("kind_item"), "custom": t("kind_custom")}.get(
            code, t("kind_aff")
        )

    def _build(self) -> None:
        kit.section_header(self, "trig_title", "trig_hint")
        tools = ctk.CTkFrame(self, fg_color="transparent")
        tools.pack(fill="x", padx=20, pady=(0, 8))
        kit.primary_btn(tools, t("add_aff"), lambda: self._add("affection"), width=110).pack(
            side="left", padx=3
        )
        kit.ghost_btn(tools, t("add_item"), lambda: self._add("item"), width=110).pack(side="left", padx=3)
        kit.ghost_btn(tools, t("add_custom"), lambda: self._add("custom"), width=100).pack(
            side="left", padx=3
        )

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(body, width=220, fg_color=T.CARD_ALT, corner_radius=12)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        left.grid_propagate(False)
        ctk.CTkLabel(left, text=t("trig_list"), text_color=T.MUTED).pack(anchor="w", padx=12, pady=(12, 4))
        self.listbox = ctk.CTkScrollableFrame(left, fg_color="transparent", width=196)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=4)
        kit.danger_btn(left, t("delete"), self._delete, width=100).pack(pady=10)

        right = ctk.CTkScrollableFrame(body, fg_color=T.CARD_ALT, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew")
        self.form = right

        ctk.CTkLabel(right, text=t("kind"), text_color=T.MUTED).pack(anchor="w", padx=12, pady=(12, 2))
        self.kind_menu = ctk.CTkOptionMenu(
            right,
            values=self._kind_values(),
            command=lambda _v: self._show_kind(self._kind_to_code(self.kind_menu.get())),
            width=180,
            fg_color=T.CARD,
            button_color=T.ACCENT,
            button_hover_color=T.ACCENT_HOVER,
        )
        self.kind_menu.pack(anchor="w", padx=12, pady=(0, 8))

        self.title_entry = kit.labeled_entry(right, t("entry_title"), placeholder=t("title_ph"))
        self.title_entry.pack_configure(padx=12)

        self.aff_frame = ctk.CTkFrame(right, fg_color="transparent")
        self.char_entry = kit.labeled_entry(self.aff_frame, t("apply_char"))
        row = ctk.CTkFrame(self.aff_frame, fg_color="transparent")
        row.pack(fill="x", pady=6)
        ctk.CTkLabel(row, text=t("aff_min"), text_color=T.MUTED).pack(side="left")
        self.amin = ctk.CTkEntry(row, width=70, fg_color=T.CARD)
        self.amin.insert(0, "0")
        self.amin.pack(side="left", padx=6)
        ctk.CTkLabel(row, text=t("aff_max"), text_color=T.MUTED).pack(side="left")
        self.amax = ctk.CTkEntry(row, width=70, fg_color=T.CARD)
        self.amax.insert(0, "100")
        self.amax.pack(side="left", padx=6)
        th = ctk.CTkFrame(self.aff_frame, fg_color="transparent")
        th.pack(fill="x", pady=(8, 2))
        ctk.CTkLabel(th, text=t("tiers"), text_color=T.MUTED).pack(side="left")
        kit.ghost_btn(th, t("add_tier"), lambda: self._add_tier(), width=80).pack(side="right")
        self.tiers_box = ctk.CTkFrame(self.aff_frame, fg_color="transparent")
        self.tiers_box.pack(fill="x")

        self.item_frame = ctk.CTkFrame(right, fg_color="transparent")
        self.item_entry = kit.labeled_entry(self.item_frame, t("item_name"))
        ctk.CTkLabel(self.item_frame, text=t("picker"), text_color=T.MUTED).pack(anchor="w", pady=(8, 2))
        self.picker_menu = ctk.CTkOptionMenu(
            self.item_frame,
            values=[t("anyone"), t("user"), t("role"), t("named")],
            width=180,
            fg_color=T.CARD,
            button_color=T.ACCENT,
        )
        self.picker_menu.pack(anchor="w")
        self.picker_extra = ctk.CTkEntry(
            self.item_frame, placeholder_text=t("named_ph"), fg_color=T.CARD, height=34
        )
        self.picker_extra.pack(fill="x", pady=6)

        self.custom_frame = ctk.CTkFrame(right, fg_color="transparent")
        ctk.CTkLabel(self.custom_frame, text=t("condition"), text_color=T.MUTED).pack(anchor="w")
        self.cond_box = ctk.CTkTextbox(
            self.custom_frame, height=80, fg_color=T.CARD, corner_radius=8, border_width=1, border_color=T.BORDER
        )
        self.cond_box.pack(fill="x", pady=4)

        ctk.CTkLabel(right, text=t("effect"), text_color=T.MUTED).pack(anchor="w", padx=12, pady=(10, 2))
        self.effect_box = ctk.CTkTextbox(
            right, height=90, fg_color=T.CARD, corner_radius=8, border_width=1, border_color=T.BORDER
        )
        self.effect_box.pack(fill="x", padx=12)
        self.keys_entry = kit.labeled_entry(right, t("extra_keys"))
        self.keys_entry.pack_configure(padx=12)
        self.constant_box = ctk.CTkCheckBox(
            right, text=t("trig_constant"), text_color=T.TEXT, fg_color=T.ACCENT
        )
        self.constant_box.pack(anchor="w", padx=12, pady=10)

        prev = ctk.CTkFrame(right, fg_color="transparent")
        prev.pack(fill="x", padx=12)
        ctk.CTkLabel(prev, text=t("trig_preview"), text_color=T.MUTED).pack(side="left")
        kit.ghost_btn(prev, t("refresh_preview"), self._refresh_preview, width=100).pack(side="right")
        self.preview = ctk.CTkTextbox(
            right, height=130, fg_color=T.CARD, corner_radius=8, border_width=1, border_color=T.BORDER
        )
        self.preview.pack(fill="x", padx=12, pady=(4, 14))

    def _show_kind(self, kind: str) -> None:
        self.aff_frame.pack_forget()
        self.item_frame.pack_forget()
        self.custom_frame.pack_forget()
        if kind == "affection":
            self.aff_frame.pack(fill="x", padx=12, after=self.title_entry)
        elif kind == "item":
            self.item_frame.pack(fill="x", padx=12, after=self.title_entry)
        else:
            self.custom_frame.pack(fill="x", padx=12, after=self.title_entry)

    def _clear_tiers(self) -> None:
        for a, b in self._tier_rows:
            a.master.destroy()
        self._tier_rows.clear()

    def _add_tier(self, threshold: str = "", effect: str = "") -> None:
        row = ctk.CTkFrame(self.tiers_box, fg_color="transparent")
        row.pack(fill="x", pady=2)
        e1 = ctk.CTkEntry(row, width=64, fg_color=T.CARD, placeholder_text="N")
        e1.pack(side="left")
        if threshold:
            e1.insert(0, threshold)
        ctk.CTkLabel(row, text="→", text_color=T.MUTED).pack(side="left", padx=4)
        e2 = ctk.CTkEntry(row, fg_color=T.CARD)
        e2.pack(side="left", fill="x", expand=True)
        if effect:
            e2.insert(0, effect)
        pair = (e1, e2)

        def _rm() -> None:
            if pair in self._tier_rows:
                self._tier_rows.remove(pair)
            row.destroy()

        kit.danger_btn(row, "×", _rm, width=28, height=28).pack(side="left", padx=4)
        self._tier_rows.append(pair)

    def _set_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for w in (
            self.kind_menu,
            self.title_entry,
            self.char_entry,
            self.amin,
            self.amax,
            self.item_entry,
            self.picker_menu,
            self.picker_extra,
            self.cond_box,
            self.effect_box,
            self.keys_entry,
            self.constant_box,
        ):
            try:
                w.configure(state=state)
            except Exception:
                pass

    def _rebuild_list(self) -> None:
        for b in self._list_buttons:
            b.destroy()
        self._list_buttons.clear()
        for i, tr in enumerate(self.project.triggers):
            if tr.kind == "affection":
                label = f"♥ {tr.character or tr.title or t('kind_aff')}"
            elif tr.kind == "item":
                label = f"◆ {tr.item_name or t('kind_item')}"
            else:
                label = f"◇ {tr.title or t('kind_custom')}"
            active = i == self._index
            btn = ctk.CTkButton(
                self.listbox,
                text=label,
                anchor="w",
                height=32,
                corner_radius=8,
                fg_color=T.ACCENT_DIM if active else "transparent",
                hover_color=T.BORDER,
                text_color=T.TEXT,
                command=lambda idx=i: self._select(idx),
            )
            btn.pack(fill="x", pady=2)
            self._list_buttons.append(btn)

    def _select(self, index: int) -> None:
        if self._index is not None and 0 <= self._index < len(self.project.triggers):
            self._save()
        self._index = index
        self._load()
        self._rebuild_list()
        self._set_enabled(True)
        self._refresh_preview()

    def _picker_value(self) -> str:
        p = self.picker_menu.get()
        extra = self.picker_extra.get().strip()
        if p in (t("named"), "指定角色", "Named character") and extra:
            return extra
        # store bilingual-neutral codes in data
        if p in (t("anyone"), "任何人", "Anyone"):
            return "任何人" if get_lang() == "zh" else "Anyone"
        if p in (t("user"), "用户", "User"):
            return "用户" if get_lang() == "zh" else "User"
        if p in (t("role"), "角色", "Character"):
            return "角色" if get_lang() == "zh" else "Character"
        return extra or p

    def _set_picker(self, picker: str) -> None:
        mapping = {
            "任何人": t("anyone"),
            "Anyone": t("anyone"),
            "用户": t("user"),
            "User": t("user"),
            "角色": t("role"),
            "Character": t("role"),
        }
        if picker in mapping:
            self.picker_menu.set(mapping[picker])
            self.picker_extra.delete(0, "end")
        else:
            self.picker_menu.set(t("named"))
            self.picker_extra.delete(0, "end")
            self.picker_extra.insert(0, picker)

    def _save(self) -> None:
        if self._index is None or not (0 <= self._index < len(self.project.triggers)):
            return
        tr = self.project.triggers[self._index]
        tr.kind = self._kind_to_code(self.kind_menu.get())
        tr.title = self.title_entry.get().strip()
        tr.character = self.char_entry.get().strip()
        tr.affection_min = self.amin.get().strip() or "0"
        tr.affection_max = self.amax.get().strip() or "100"
        tr.tiers = [
            AffectionTier(a.get().strip(), b.get().strip())
            for a, b in self._tier_rows
            if a.get().strip() or b.get().strip()
        ]
        tr.item_name = self.item_entry.get().strip()
        tr.picker = self._picker_value()
        tr.condition = self.cond_box.get("1.0", "end-1c")
        tr.effect = self.effect_box.get("1.0", "end-1c")
        tr.extra_keys = self.keys_entry.get().strip()
        tr.constant = bool(self.constant_box.get())
        tr.comment = tr.title or tr.character or tr.item_name or "trigger"

    def _load(self) -> None:
        if self._index is None:
            return
        tr = self.project.triggers[self._index]
        self.kind_menu.configure(values=self._kind_values())
        self.kind_menu.set(self._code_to_kind(tr.kind))
        self._show_kind(tr.kind)
        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, tr.title)
        self.char_entry.delete(0, "end")
        self.char_entry.insert(0, tr.character)
        self.amin.delete(0, "end")
        self.amin.insert(0, tr.affection_min or "0")
        self.amax.delete(0, "end")
        self.amax.insert(0, tr.affection_max or "100")
        self._clear_tiers()
        if tr.tiers:
            for x in tr.tiers:
                self._add_tier(x.threshold, x.effect)
        else:
            self._add_tier("20", "")
            self._add_tier("50", "")
            self._add_tier("80", "")
        self.item_entry.delete(0, "end")
        self.item_entry.insert(0, tr.item_name)
        self.picker_menu.configure(values=[t("anyone"), t("user"), t("role"), t("named")])
        self._set_picker(tr.picker or "任何人")
        self.cond_box.delete("1.0", "end")
        self.cond_box.insert("1.0", tr.condition)
        self.effect_box.delete("1.0", "end")
        self.effect_box.insert("1.0", tr.effect)
        self.keys_entry.delete(0, "end")
        self.keys_entry.insert(0, tr.extra_keys)
        if tr.constant:
            self.constant_box.select()
        else:
            self.constant_box.deselect()

    def _add(self, kind: str) -> None:
        if self._index is not None:
            self._save()
        tr = TriggerRule(kind=kind)
        if kind == "affection":
            names = [c.name.strip() for c in self.project.characters if c.name.strip()]
            tr.character = names[0] if names else ""
            tr.tiers = [
                AffectionTier("20", "Warm-up / 开始愿意多说话"),
                AffectionTier("50", "Trust / 愿意分享情报"),
                AffectionTier("80", "Unlock / 解锁特殊互动"),
            ]
            tr.title = f"{tr.character or 'Char'} affection"
        elif kind == "item":
            tr.effect = "Trigger effect / 触发效果……"
            tr.title = "Item pickup"
        else:
            tr.condition = "When… / 当……"
            tr.effect = "Then… / 则……"
            tr.title = "Custom"
        self.project.triggers.append(tr)
        self._select(len(self.project.triggers) - 1)

    def _delete(self) -> None:
        if self._index is None or not self.project.triggers:
            return
        del self.project.triggers[self._index]
        if not self.project.triggers:
            self._index = None
            self._clear_tiers()
            self._set_enabled(False)
            self.preview.delete("1.0", "end")
            self._rebuild_list()
            return
        self._index = min(self._index, len(self.project.triggers) - 1)
        self._load()
        self._rebuild_list()
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        if self._index is None or not (0 <= self._index < len(self.project.triggers)):
            return
        self._save()
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", build_trigger_content(self.project.triggers[self._index]))

    def collect(self) -> None:
        if self._index is not None:
            self._save()
