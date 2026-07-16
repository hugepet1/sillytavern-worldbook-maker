# -*- coding: utf-8 -*-
"""傻瓜式 SillyTavern 世界书生成器 · 中英双语。"""
from __future__ import annotations

import sys
from pathlib import Path
from tkinter import filedialog, messagebox

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import customtkinter as ctk

import theme as T
import ui_kit as kit
from core.export_st import load_draft
from core.models import WorldBookProject
from i18n import get_lang, set_lang, t, toggle_lang
from ui.step_chars import CharsStep
from ui.step_export import ExportStep
from ui.step_triggers import TriggersStep
from ui.step_world import WorldStep


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=T.BG)
        self.geometry("1080x780")
        self.minsize(920, 660)

        self.project = WorldBookProject()
        self.step_index = 0
        self._step_pills: list[ctk.CTkButton] = []

        self._build_chrome()
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self.pages: list[ctk.CTkFrame] = self._make_pages()
        for p in self.pages:
            p.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self._build_nav()
        self._apply_texts()
        self.show_step(0)

    def _build_chrome(self) -> None:
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(16, 6))

        left = ctk.CTkFrame(top, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True)
        self.lbl_title = ctk.CTkLabel(
            left, text="", font=ctk.CTkFont(size=22, weight="bold"), text_color=T.TEXT
        )
        self.lbl_title.pack(anchor="w")
        self.lbl_sub = ctk.CTkLabel(left, text="", font=ctk.CTkFont(size=12), text_color=T.MUTED)
        self.lbl_sub.pack(anchor="w", pady=(2, 0))

        right = ctk.CTkFrame(top, fg_color="transparent")
        right.pack(side="right")
        self.btn_lang = kit.ghost_btn(right, "中 / EN", self._toggle_lang, width=88)
        self.btn_lang.pack(side="left", padx=4)
        self.btn_open = kit.ghost_btn(right, "", self.open_file, width=88)
        self.btn_open.pack(side="left", padx=4)
        self.btn_new = kit.primary_btn(right, "", self.new_project, width=72)
        self.btn_new.pack(side="left", padx=4)

        self.pill_bar = ctk.CTkFrame(self, fg_color=T.CARD, corner_radius=14, height=52)
        self.pill_bar.pack(fill="x", padx=16, pady=(4, 10))
        self.pill_bar.pack_propagate(False)
        inner = ctk.CTkFrame(self.pill_bar, fg_color="transparent")
        inner.pack(expand=True)
        keys = ["step_world", "step_chars", "step_triggers", "step_export"]
        for i, key in enumerate(keys):
            btn = ctk.CTkButton(
                inner,
                text=t(key),
                width=140,
                height=34,
                corner_radius=17,
                fg_color=T.CARD_ALT,
                hover_color=T.BORDER,
                text_color=T.TEXT,
                command=lambda idx=i: self._jump(idx),
            )
            btn.pack(side="left", padx=6, pady=8)
            self._step_pills.append(btn)

    def _build_nav(self) -> None:
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=18, pady=(0, 14))
        self.btn_prev = kit.ghost_btn(nav, "", self.prev_step, width=110)
        self.btn_prev.pack(side="left")
        self.btn_next = kit.primary_btn(nav, "", self.next_step, width=120)
        self.btn_next.pack(side="right")

    def _apply_texts(self) -> None:
        self.title(t("app_title"))
        self.lbl_title.configure(text=t("app_title"))
        self.lbl_sub.configure(text=t("app_sub"))
        self.btn_open.configure(text=t("open"))
        self.btn_new.configure(text=t("new"))
        self.btn_lang.configure(text="EN" if get_lang() == "zh" else "中文")
        keys = ["step_world", "step_chars", "step_triggers", "step_export"]
        for i, key in enumerate(keys):
            self._step_pills[i].configure(text=t(key))
        self.btn_prev.configure(text=t("prev"))
        last = len(self.pages) - 1
        self.btn_next.configure(
            text=t("refresh_preview") if self.step_index == last else t("next")
        )

    def _toggle_lang(self) -> None:
        self._collect_current()
        toggle_lang()
        self._rebind_pages()
        self._apply_texts()
        self.show_step(self.step_index)

    def _make_pages(self) -> list[ctk.CTkFrame]:
        return [
            WorldStep(self.container, self.project),
            CharsStep(self.container, self.project),
            TriggersStep(self.container, self.project),
            ExportStep(self.container, self.project),
        ]

    def _jump(self, index: int) -> None:
        self._collect_current()
        self.show_step(index)

    def show_step(self, index: int) -> None:
        self.step_index = index
        for i, page in enumerate(self.pages):
            if i == index:
                page.lift()
        for i, pill in enumerate(self._step_pills):
            active = i == index
            pill.configure(
                fg_color=T.ACCENT if active else T.CARD_ALT,
                text_color="#06241c" if active else T.TEXT,
            )
        last = len(self.pages) - 1
        self.btn_prev.configure(state="normal" if index > 0 else "disabled")
        self.btn_next.configure(
            text=t("refresh_preview") if index == last else t("next")
        )
        if index == last:
            self.pages[last].refresh()  # type: ignore[attr-defined]

    def _collect_current(self) -> None:
        page = self.pages[self.step_index]
        if hasattr(page, "collect"):
            page.collect()

    def next_step(self) -> None:
        self._collect_current()
        last = len(self.pages) - 1
        if self.step_index < last:
            self.show_step(self.step_index + 1)
        else:
            self.pages[last].refresh()  # type: ignore[attr-defined]

    def prev_step(self) -> None:
        self._collect_current()
        if self.step_index > 0:
            self.show_step(self.step_index - 1)

    def new_project(self) -> None:
        if not messagebox.askyesno(t("new"), t("confirm_new")):
            return
        self.project = WorldBookProject()
        self._rebind_pages()
        self.show_step(0)

    def open_file(self) -> None:
        path = filedialog.askopenfilename(
            title=t("open"),
            filetypes=[
                ("Worldbook / JSON", "*.wbb.json;*.json"),
                ("All", "*.*"),
            ],
        )
        if not path:
            return
        try:
            self._collect_current()
            self.project = load_draft(path)
            self.project.rules = []
            self.project.immersion_rules = ""
            self._rebind_pages()
            self.show_step(0)
            messagebox.showinfo(t("opened"), Path(path).name)
        except Exception as exc:
            messagebox.showerror(t("open_fail"), str(exc))

    def _rebind_pages(self) -> None:
        for p in self.pages:
            p.destroy()
        self.pages = self._make_pages()
        for p in self.pages:
            p.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)


def main() -> None:
    set_lang("zh")
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
