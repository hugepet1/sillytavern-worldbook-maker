# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

import theme as T
import ui_kit as kit
from core.export_st import export_worldbook_json, preview_json_text, save_draft
from core.models import WorldBookProject
from i18n import t


class ExportStep(ctk.CTkFrame):
    def __init__(self, master, project: WorldBookProject, **kwargs):
        super().__init__(master, fg_color=T.CARD, corner_radius=16, **kwargs)
        self.project = project
        self._build()

    def _build(self) -> None:
        kit.section_header(self, "export_title", "export_hint")
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=20, pady=4)
        kit.ghost_btn(bar, t("refresh_preview"), self.refresh, width=110).pack(side="left", padx=4)
        kit.primary_btn(bar, t("export_json"), self.export_json, width=160).pack(side="left", padx=4)
        kit.ghost_btn(bar, t("save_draft"), self.save_project, width=140).pack(side="left", padx=4)

        self.summary = ctk.CTkLabel(self, text="", text_color=T.MUTED, anchor="w")
        self.summary.pack(fill="x", padx=20, pady=6)
        self.preview = ctk.CTkTextbox(
            self,
            corner_radius=12,
            fg_color=T.CARD_ALT,
            border_color=T.BORDER,
            border_width=1,
            text_color=T.TEXT,
            font=ctk.CTkFont(family="Consolas", size=12),
        )
        self.preview.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    def collect(self) -> None:
        pass

    def refresh(self) -> None:
        n_char = len(self.project.characters)
        n_trig = len(self.project.triggers)
        aff = sum(1 for x in self.project.triggers if x.kind == "affection")
        total = 1 + n_trig + n_char + (1 if aff else 0)
        self.summary.configure(
            text=t(
                "summary",
                book=self.project.book_name,
                trig=str(n_trig),
                char=str(n_char),
                n=str(total),
            )
        )
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", preview_json_text(self.project))

    def export_json(self) -> None:
        path = filedialog.asksaveasfilename(
            title=t("export_json"),
            defaultextension=".json",
            initialfile=f"{self.project.book_name or 'worldbook'}.json",
            filetypes=[("JSON", "*.json"), ("All", "*.*")],
        )
        if not path:
            return
        try:
            export_worldbook_json(self.project, path)
            messagebox.showinfo(t("export_ok"), f"{path}\n\n{t('export_tip')}")
        except Exception as exc:
            messagebox.showerror(t("export_fail"), str(exc))

    def save_project(self) -> None:
        path = filedialog.asksaveasfilename(
            title=t("save_draft"),
            defaultextension=".wbb.json",
            initialfile=f"{self.project.book_name or 'project'}.wbb.json",
            filetypes=[("Draft", "*.wbb.json"), ("JSON", "*.json")],
        )
        if not path:
            return
        try:
            if not str(path).endswith(".wbb.json"):
                path = str(Path(path).with_suffix("")) + ".wbb.json"
            save_draft(self.project, path)
            messagebox.showinfo(t("save_ok"), path)
        except Exception as exc:
            messagebox.showerror(t("save_fail"), str(exc))
