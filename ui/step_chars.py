# -*- coding: utf-8 -*-
from __future__ import annotations

import customtkinter as ctk

import theme as T
import ui_kit as kit
from core.export_st import build_character_content
from core.models import Character, WorldBookProject
from i18n import t

FIELDS = [
    ("name", "f_name", "entry"),
    ("aliases", "f_aliases", "entry"),
    ("age", "f_age", "entry"),
    ("height", "f_height", "entry"),
    ("body", "f_body", "entry"),
    ("appearance", "f_appearance", "text"),
    ("hair_eyes", "f_hair_eyes", "entry"),
    ("clothing", "f_clothing", "text"),
    ("personality", "f_personality", "text"),
    ("background", "f_background", "text"),
    ("skills_notes", "f_skills", "text"),
    ("custom_keys", "f_custom_keys", "entry"),
    ("comment", "f_comment", "entry"),
    ("extra_content", "f_extra", "text"),
]


class CharsStep(ctk.CTkFrame):
    def __init__(self, master, project: WorldBookProject, **kwargs):
        super().__init__(master, fg_color=T.CARD, corner_radius=16, **kwargs)
        self.project = project
        self._index: int | None = None
        self._widgets: dict = {}
        self._list_buttons: list = []
        self._build()
        if self.project.characters:
            self._select(0)
        else:
            self._set_enabled(False)

    def _build(self) -> None:
        kit.section_header(self, "chars_title", "chars_hint")
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(body, width=220, fg_color=T.CARD_ALT, corner_radius=12)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        left.grid_propagate(False)
        ctk.CTkLabel(left, text=t("char_list"), text_color=T.MUTED).pack(anchor="w", padx=12, pady=(12, 4))
        self.listbox = ctk.CTkScrollableFrame(left, fg_color="transparent", width=196)
        self.listbox.pack(fill="both", expand=True, padx=8, pady=4)
        row = ctk.CTkFrame(left, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=10)
        kit.primary_btn(row, t("add"), self._add, width=70).pack(side="left", padx=2)
        kit.danger_btn(row, t("delete"), self._delete, width=70).pack(side="left", padx=2)

        right = ctk.CTkScrollableFrame(body, fg_color=T.CARD_ALT, corner_radius=12)
        right.grid(row=0, column=1, sticky="nsew")
        self.form = right

        self.constant_var = ctk.CTkCheckBox(
            right, text=t("char_constant"), text_color=T.TEXT, fg_color=T.ACCENT
        )
        self.constant_var.pack(anchor="w", padx=12, pady=(12, 6))

        for field, key, kind in FIELDS:
            ctk.CTkLabel(right, text=t(key), text_color=T.MUTED, font=ctk.CTkFont(size=12)).pack(
                anchor="w", padx=12, pady=(8, 2)
            )
            if kind == "entry":
                w = ctk.CTkEntry(
                    right, height=34, corner_radius=8, fg_color=T.CARD, border_color=T.BORDER
                )
                w.pack(fill="x", padx=12)
            else:
                h = 110 if field in ("background", "extra_content", "skills_notes") else 72
                w = ctk.CTkTextbox(
                    right, height=h, corner_radius=8, fg_color=T.CARD, border_color=T.BORDER, border_width=1
                )
                w.pack(fill="x", padx=12)
            self._widgets[field] = w

        prev = ctk.CTkFrame(right, fg_color="transparent")
        prev.pack(fill="x", padx=12, pady=(14, 4))
        ctk.CTkLabel(prev, text=t("char_preview"), text_color=T.MUTED).pack(side="left")
        kit.ghost_btn(prev, t("refresh_preview"), self._refresh_preview, width=100).pack(side="right")
        self.preview = ctk.CTkTextbox(
            right, height=140, corner_radius=8, fg_color=T.CARD, border_width=1, border_color=T.BORDER
        )
        self.preview.pack(fill="x", padx=12, pady=(0, 14))
        self._rebuild_list()

    def _rebuild_list(self) -> None:
        for b in self._list_buttons:
            b.destroy()
        self._list_buttons.clear()
        for i, ch in enumerate(self.project.characters):
            label = ch.name.strip() or f"{t('new_char')}{i + 1}"
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

    def _set_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for w in list(self._widgets.values()) + [self.constant_var]:
            try:
                w.configure(state=state)
            except Exception:
                pass

    def _select(self, index: int) -> None:
        if self._index is not None and 0 <= self._index < len(self.project.characters):
            self._save()
        self._index = index
        self._load()
        self._rebuild_list()
        self._set_enabled(True)
        self._refresh_preview()

    def _get(self, field: str) -> str:
        w = self._widgets[field]
        return w.get("1.0", "end-1c") if isinstance(w, ctk.CTkTextbox) else w.get()

    def _set(self, field: str, value: str) -> None:
        w = self._widgets[field]
        if isinstance(w, ctk.CTkTextbox):
            w.delete("1.0", "end")
            w.insert("1.0", value or "")
        else:
            w.delete(0, "end")
            w.insert(0, value or "")

    def _save(self) -> None:
        if self._index is None or not (0 <= self._index < len(self.project.characters)):
            return
        ch = self.project.characters[self._index]
        for field, _, _ in FIELDS:
            setattr(ch, field, self._get(field))
        ch.constant = bool(self.constant_var.get())

    def _load(self) -> None:
        if self._index is None:
            return
        ch = self.project.characters[self._index]
        for field, _, _ in FIELDS:
            self._set(field, getattr(ch, field, "") or "")
        if ch.constant:
            self.constant_var.select()
        else:
            self.constant_var.deselect()

    def _add(self) -> None:
        if self._index is not None:
            self._save()
        self.project.characters.append(
            Character(name=f"{t('new_char')}{len(self.project.characters) + 1}")
        )
        self._select(len(self.project.characters) - 1)

    def _delete(self) -> None:
        if self._index is None or not self.project.characters:
            return
        del self.project.characters[self._index]
        if not self.project.characters:
            self._index = None
            for f, _, _ in FIELDS:
                self._set(f, "")
            self.constant_var.deselect()
            self.preview.delete("1.0", "end")
            self._set_enabled(False)
            self._rebuild_list()
            return
        self._index = min(self._index, len(self.project.characters) - 1)
        self._load()
        self._rebuild_list()
        self._refresh_preview()

    def _refresh_preview(self) -> None:
        if self._index is None or not (0 <= self._index < len(self.project.characters)):
            return
        self._save()
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", build_character_content(self.project.characters[self._index]))

    def collect(self) -> None:
        if self._index is not None:
            self._save()
