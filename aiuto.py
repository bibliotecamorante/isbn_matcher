# -*- coding: utf-8 -*-
"""
Finestra di aiuto per ISBN Matcher con supporto multilingua
"""
import tkinter as tk
from tkinter import scrolledtext
from localization import Translations


def mostra_aiuto(parent, t: Translations):
    """
    Mostra la finestra di aiuto con la guida utente.
    
    Args:
        parent: Finestra principale dell'applicazione
        t: Oggetto Translations con le traduzioni
    """
    help_window = tk.Toplevel(parent)
    help_window.title(t.help_title)
    help_window.geometry("600x500")
    help_window.transient(parent)
    help_window.grab_set()
    
    # Header
    header = tk.Frame(help_window, bg="#2563eb", height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text=t.help_title, 
            font=("Arial", 18, "bold"),
            bg="#2563eb", fg="white").pack(pady=15)
    
    # Contenuto
    content = tk.Frame(help_window, bg="white", padx=20, pady=20)
    content.pack(fill=tk.BOTH, expand=True)
    
    text = scrolledtext.ScrolledText(content, 
                                    font=("Arial", 10),
                                    bg="white", 
                                    fg="#1e293b",
                                    relief=tk.FLAT, 
                                    wrap=tk.WORD)
    text.pack(fill=tk.BOTH, expand=True)
    
    help_text = f"""{t.help_what_does}

{t.help_what_does_content}


{t.help_how_to_use}

{t.help_how_to_use_content}


{t.help_output_format}

{t.help_output_format_content}


{t.help_tips}

{t.help_tips_content}


{t.help_isbn_columns}

{t.help_isbn_columns_content}


{t.help_troubleshooting}

{t.help_troubleshooting_content}
"""
    
    text.insert(1.0, help_text)
    text.config(state=tk.DISABLED)
    
    # Pulsante chiudi
    btn_frame = tk.Frame(help_window, bg="white", pady=10)
    btn_frame.pack(fill=tk.X)
    
    close_btn = tk.Button(btn_frame, text=t.btn_close,
                         command=help_window.destroy,
                         bg="#2563eb", fg="white",
                         font=("Arial", 10, "bold"),
                         padx=30, pady=8,
                         cursor="hand2", relief=tk.FLAT)
    close_btn.pack()
