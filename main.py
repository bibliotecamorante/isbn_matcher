# -*- coding: utf-8 -*-
"""
ISBN Matcher - File di avvio dell'applicazione
"""
import sys
import tkinter as tk
from tkinter import messagebox
from gui import ISBNMatcherApp

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
            root.after(1000, lambda: messagebox.showwarning(
                "Funzionalità Limitata",
                "⚠️ La libreria 'tkinterdnd2' non è installata.\n\n"
                "Il drag & drop dei file non sarà disponibile.\n"
                "Usa il pulsante '➕ Aggiungi File' per caricare i file.\n\n"
                "Per abilitare il drag & drop, installa:\n"
                "pip install tkinterdnd2"
            ))
        
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Errore Critico", 
                           f"Impossibile avviare l'applicazione:\n\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
