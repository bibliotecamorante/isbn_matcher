# -*- coding: utf-8 -*-
"""
ISBN Matcher - File di avvio dell'applicazione
"""
import sys
import tkinter as tk
from tkinter import messagebox
from gui import ISBNMatcherApp
from localization import get_translations

# Tentativo di importare tkinterdnd2 con fallback
try:
    from tkinterdnd2 import TkinterDnD
    DRAG_DROP_AVAILABLE = True
except ImportError:
    DRAG_DROP_AVAILABLE = False
    print("⚠️ Attenzione: tkinterdnd2 non disponibile. Drag & Drop disabilitato.")

def main():
    """Entry point dell'applicazione"""
    # Crea la finestra principale con o senza drag & drop
    if DRAG_DROP_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    try:
        app = ISBNMatcherApp(root, drag_drop_enabled=DRAG_DROP_AVAILABLE)
        
        # Avvisa l'utente se manca il drag & drop
        if not DRAG_DROP_AVAILABLE:
            # Usa le traduzioni dalla lingua corrente dell'app
            t = get_translations(app.current_lang.get())
            root.after(1000, lambda: messagebox.showwarning(
                t.warning_drag_drop_unavailable,
                t.warning_drag_drop_message
            ))
        
        root.mainloop()
    except Exception as e:
        # Usa traduzioni italiane come fallback per errori critici
        t = get_translations('it')
        messagebox.showerror(t.error_critical, 
                           f"{t.error_cannot_start}{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
