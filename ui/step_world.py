# -*- coding: utf-8 -*-
from __future__ import annotations

import customtkinter as ctk

import theme as T
import ui_kit as kit
from core.models import WorldBookProject
from i18n import t


class WorldStep(ctk.CTkFrame):
    def __init__(self, master, project: WorldBookProject, **kwargs):
        super().__init__(master, fg_color=T.CARD, corner_radius=16, **kwargs)
        self.project = project
        self._build()

    def _build(self) -> None:
        kit.section_header(self, "world_title", "world_hint")
        form = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=(0, 16))

        self.book_name = kit.labeled_entry(form, t("book_name"), self.project.book_name)
        self.world_keys = kit.labeled_entry(
            form, t("world_keys"), self.project.world_keys or t("world_title")
        )
        self.world_constant = ctk.CTkCheckBox(
            form,
            text=t("world_constant"),
            text_color=T.TEXT,
            fg_color=T.ACCENT,
            hover_color=T.ACCENT_HOVER,
        )
        if self.project.world_constant:
            self.world_constant.select()
        self.world_constant.pack(anchor="w", pady=(12, 4))

        ctk.CTkLabel(form, text=t("world_body"), text_color=T.MUTED, font=ctk.CTkFont(size=12)).pack(
            anchor="w", pady=(12, 3)
        )
        self.world_content = ctk.CTkTextbox(
            form,
            height=360,
            corner_radius=10,
            fg_color=T.CARD_ALT,
            border_color=T.BORDER,
            border_width=1,
            text_color=T.TEXT,
        )
        self.world_content.pack(fill="both", expand=True)
        self.world_content.insert("1.0", self.project.world_content)

    def collect(self) -> None:
        self.project.book_name = self.book_name.get().strip() or t("unnamed_book")
        self.project.world_keys = self.world_keys.get().strip() or t("world_title")
        self.project.world_constant = bool(self.world_constant.get())
        self.project.world_content = self.world_content.get("1.0", "end-1c")
        self.project.immersion_rules = ""
