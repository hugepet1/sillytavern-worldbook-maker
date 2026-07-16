# -*- coding: utf-8 -*-
from __future__ import annotations

import customtkinter as ctk

import theme as T
from i18n import t


def section_header(parent, title_key: str, hint_key: str) -> None:
    ctk.CTkLabel(
        parent,
        text=t(title_key),
        font=ctk.CTkFont(size=20, weight="bold"),
        text_color=T.TEXT,
    ).pack(anchor="w", padx=20, pady=(18, 4))
    ctk.CTkLabel(
        parent,
        text=t(hint_key),
        font=ctk.CTkFont(size=12),
        text_color=T.MUTED,
        wraplength=860,
        justify="left",
    ).pack(anchor="w", padx=20, pady=(0, 12))


def labeled_entry(parent, label: str, value: str = "", placeholder: str = "") -> ctk.CTkEntry:
    ctk.CTkLabel(parent, text=label, text_color=T.MUTED, font=ctk.CTkFont(size=12)).pack(
        anchor="w", pady=(10, 3)
    )
    e = ctk.CTkEntry(
        parent,
        height=36,
        corner_radius=8,
        border_color=T.BORDER,
        fg_color=T.CARD_ALT,
        text_color=T.TEXT,
        placeholder_text=placeholder,
    )
    e.pack(fill="x")
    if value:
        e.insert(0, value)
    return e


def primary_btn(parent, text: str, command, **kw) -> ctk.CTkButton:
    opts = {**T.BTN, **kw}
    return ctk.CTkButton(parent, text=text, command=command, **opts)


def ghost_btn(parent, text: str, command, **kw) -> ctk.CTkButton:
    opts = {**T.BTN_GHOST, **kw}
    return ctk.CTkButton(parent, text=text, command=command, **opts)


def danger_btn(parent, text: str, command, **kw) -> ctk.CTkButton:
    opts = {**T.BTN_DANGER, **kw}
    return ctk.CTkButton(parent, text=text, command=command, **opts)
