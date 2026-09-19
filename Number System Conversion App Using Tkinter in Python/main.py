"""
MASA Radix & Numeral Systems Matrix
Developer: MASA
"""

import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class MasaRadixEngine(ctk.CTk):
    BASES = [
        ("Decimal (Base 10)", "DEC", 10),
        ("Binary (Base 2)", "BIN", 2),
        ("Hexadecimal (Base 16)", "HEX", 16),
        ("Octal (Base 8)", "OCT", 8),
    ]

    def __init__(self):
        super().__init__()

        self.title("MASA Radix Engine")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(fg_color="#0D1117")

        self.source_mode = ctk.StringVar(value="Decimal (Base 10)")
        self.output_vars = {}

        self._build_ui()

    def _build_ui(self):
        header_card = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=14, border_width=1, border_color="#30363D")
        header_card.pack(fill="x", padx=20, pady=(20, 15))

        title = ctk.CTkLabel(
            header_card,
            text="MASA RADIX ENGINE",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#58A6FF",
        )
        title.pack(pady=(12, 2))

        subtitle = ctk.CTkLabel(
            header_card,
            text="Real-Time Multi-Base Computational Matrix",
            font=ctk.CTkFont(size=11),
            text_color="#8B949E",
        )
        subtitle.pack(pady=(0, 12))

        input_card = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=14, border_width=1, border_color="#30363D")
        input_card.pack(fill="x", padx=20, pady=5)

        selector_row = ctk.CTkFrame(input_card, fg_color="transparent")
        selector_row.pack(fill="x", padx=16, pady=(14, 8))

        lbl_select = ctk.CTkLabel(selector_row, text="INPUT BASE", font=ctk.CTkFont(size=11, weight="bold"), text_color="#8B949E")
        lbl_select.pack(side="left")

        menu = ctk.CTkOptionMenu(
            selector_row,
            values=[b[0] for b in self.BASES],
            variable=self.source_mode,
            command=lambda _: self._perform_conversion(),
            fg_color="#238636",
            button_color="#2EA043",
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        menu.pack(side="right")

        self.input_entry = ctk.CTkEntry(
            input_card,
            placeholder_text="Enter number to convert...",
            font=ctk.CTkFont(family="Consolas", size=16),
            height=44,
            corner_radius=10,
            border_color="#30363D",
        )
        self.input_entry.pack(fill="x", padx=16, pady=(0, 14))
        self.input_entry.bind("<KeyRelease>", lambda _: self._perform_conversion())

        results_card = ctk.CTkFrame(self, fg_color="#161B22", corner_radius=14, border_width=1, border_color="#30363D")
        results_card.pack(fill="both", expand=True, padx=20, pady=(12, 20))

        lbl_res_header = ctk.CTkLabel(
            results_card,
            text="MATRIX OUTPUT",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#8B949E",
        )
        lbl_res_header.pack(anchor="w", padx=16, pady=(12, 6))

        for name, code, _ in self.BASES:
            self._build_matrix_row(results_card, name, code)

        self.notification_lbl = ctk.CTkLabel(
            self,
            text="System Ready",
            font=ctk.CTkFont(size=11),
            text_color="#8B949E",
        )
        self.notification_lbl.pack(pady=(0, 10))

    def _build_matrix_row(self, parent, full_name, tag):
        card = ctk.CTkFrame(parent, fg_color="#0D1117", corner_radius=10)
        card.pack(fill="x", padx=14, pady=5)

        tag_badge = ctk.CTkLabel(
            card,
            text=tag,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color="#58A6FF",
            fg_color="#1F2937",
            corner_radius=6,
            width=50,
            height=28,
        )
        tag_badge.pack(side="left", padx=(10, 8), pady=8)

        val_var = ctk.StringVar(value="-")
        self.output_vars[tag] = val_var

        field = ctk.CTkEntry(
            card,
            textvariable=val_var,
            font=ctk.CTkFont(family="Consolas", size=14),
            state="readonly",
            fg_color="transparent",
            border_width=0,
        )
        field.pack(side="left", fill="x", expand=True, padx=5)

        copy_btn = ctk.CTkButton(
            card,
            text="Copy",
            width=55,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#21262D",
            hover_color="#30363D",
            corner_radius=6,
            command=lambda v=val_var, t=tag: self._copy_value(v.get(), t),
        )
        copy_btn.pack(side="right", padx=10, pady=8)

    def _perform_conversion(self):
        raw = self.input_entry.get().strip()
        if not raw:
            for tag in self.output_vars:
                self.output_vars[tag].set("-")
            self.notification_lbl.configure(text="Awaiting input", text_color="#8B949E")
            return

        current_base_label = self.source_mode.get()
        base_radix = 10
        for name, _, radix in self.BASES:
            if name == current_base_label:
                base_radix = radix
                break

        try:
            val_dec = int(raw, base_radix)
            self.output_vars["DEC"].set(str(val_dec))
            self.output_vars["BIN"].set(bin(val_dec)[2:])
            self.output_vars["HEX"].set(hex(val_dec)[2:].upper())
            self.output_vars["OCT"].set(oct(val_dec)[2:])
            self.notification_lbl.configure(text="Conversion Synchronized", text_color="#3FB950")
        except ValueError:
            for tag in self.output_vars:
                self.output_vars[tag].set("Syntax Error")
            self.notification_lbl.configure(text=f"Invalid literal for {current_base_label}", text_color="#F85149")

    def _copy_value(self, val: str, tag: str):
        if val and val not in ["-", "Syntax Error"]:
            self.clipboard_clear()
            self.clipboard_append(val)
            self.notification_lbl.configure(text=f"Copied {tag} value to clipboard!", text_color="#58A6FF")


if __name__ == "__main__":
    app = MasaRadixEngine()
    app.mainloop()
