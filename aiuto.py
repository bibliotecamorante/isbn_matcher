# -*- coding: utf-8 -*-
"""
Finestra di aiuto per ISBN Matcher
"""
import tkinter as tk
from tkinter import scrolledtext


def mostra_aiuto(parent):
    """
    Mostra la finestra di aiuto con la guida utente.
    
    Args:
        parent: Finestra principale dell'applicazione
    """
    help_window = tk.Toplevel(parent)
    help_window.title("Aiuto - ISBN Matcher")
    help_window.geometry("600x500")
    help_window.transient(parent)
    help_window.grab_set()
    
    # Header
    header = tk.Frame(help_window, bg="#2563eb", height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    
    tk.Label(header, text="❓ Guida Rapida", 
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
    
    help_text = """📚 COSA FA QUESTA APP

Confronta una lista di ISBN (worklist) con altri file Excel e trova:
• Corrispondenze: ISBN presenti in entrambi
• Non corrispondenze: ISBN della worklist mancanti negli altri file


🎯 COME USARE

1. SCEGLI LA MODALITÀ
   ✅ Corrispondenze: trova ISBN comuni
   ❌ Non corrispondenze: trova ISBN mancanti

2. CARICA I FILE
   • Il PRIMO file è la worklist (lista di riferimento)
   • Aggiungi altri file da confrontare
   • Puoi trascinare i file nella finestra (drag & drop)

3. ELABORA
   • Clicca "⚡ ELABORA FILE"
   • Attendi il completamento
   • Clicca "📂 APRI OUTPUT" per vedere il risultato


⚙️ FORMATTAZIONE OUTPUT

Il file Excel generato include:
• Header abbreviati (Sez, Spec, Seq...)
• Larghezze colonne ottimizzate
• Intestazione con sfondo azzurro
• Prima riga bloccata (freeze panes)
• Zoom al 110%


💡 SUGGERIMENTI

• La worklist può avere più fogli: verranno uniti automaticamente
• I duplicati nella worklist vengono rimossi automaticamente
• Il foglio "parametri" viene sempre ignorato
• Puoi riordinare i file con i pulsanti ⬆️ ⬇️


🔍 COLONNE ISBN RICONOSCIUTE

L'app riconosce automaticamente colonne con nomi come:
• ISBN, Codice ISBN, Cod. ISBN
• EAN, Codice EAN
• Codice, Barcode


❌ RISOLUZIONE PROBLEMI

• Se il file non si apre: chiudi Excel e riprova
• Se non trova ISBN: verifica che il nome colonna sia corretto
• Per problemi: controlla il log nella sezione "📋 Log Attività"
"""
    
    text.insert(1.0, help_text)
    text.config(state=tk.DISABLED)
    
    # Pulsante chiudi
    btn_frame = tk.Frame(help_window, bg="white", pady=10)
    btn_frame.pack(fill=tk.X)
    
    close_btn = tk.Button(btn_frame, text="Chiudi",
                         command=help_window.destroy,
                         bg="#2563eb", fg="white",
                         font=("Arial", 10, "bold"),
                         padx=30, pady=8,
                         cursor="hand2", relief=tk.FLAT)
    close_btn.pack()