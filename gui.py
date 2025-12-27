# -*- coding: utf-8 -*-
"""
Interfaccia grafica per ISBN Matcher
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
import threading
import platform
import subprocess

from config import AppConfig
from data_processor import DataProcessor
from aiuto import mostra_aiuto


class ISBNMatcherApp:
    """Classe principale per l'interfaccia grafica"""
    
    def __init__(self, root, drag_drop_enabled=True):
        self.root = root
        self.drag_drop_enabled = drag_drop_enabled
        self.root.title("ISBN Matcher")
        self.root.geometry("900x800")
        self.root.minsize(800, 700)
        
        self.config = AppConfig()
        self.processor = DataProcessor(self.config)
        
        self.files: List[Path] = []
        self.output_file: Optional[Path] = None
        self.processing_thread: Optional[threading.Thread] = None
        self.stop_processing = threading.Event()
        
        # NUOVO: Variabile per modalità
        self.modalita = tk.StringVar(value=self.config.MODE_MATCH)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#2563eb", height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg="#2563eb")
        header_content.pack(fill=tk.BOTH, expand=True, padx=20)
        
        title_frame = tk.Frame(header_content, bg="#2563eb")
        title_frame.pack(expand=True)
        
        tk.Label(title_frame, text="📚 ISBN Matcher", 
                font=("Arial", 28, "bold"),
                bg="#2563eb", fg="white").pack(pady=(8, 2))
        
        tk.Label(title_frame, text="Confronto intelligente di codici ISBN tra file Excel", 
                font=("Arial", 11),
                bg="#2563eb", fg="#93c5fd").pack()
        
        # Pulsante aiuto in alto a destra
        help_btn = tk.Button(header_content, text="❓", 
                            command=self.show_help,
                            bg="#3b82f6", fg="white",
                            font=("Arial", 16, "bold"),
                            width=3, height=1,
                            cursor="hand2", relief=tk.FLAT,
                            borderwidth=0)
        help_btn.place(relx=1.0, rely=0.5, anchor=tk.E, x=-10)
        
        # Main content
        main = tk.Frame(self.root, bg="#f8fafc", padx=20, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # NUOVO: Sezione modalità
        self._setup_mode_section(main)
        # File section
        self._setup_file_section(main)
        # Action buttons
        self._setup_action_buttons(main)
        # Log
        self._setup_log_section(main)
        
        self.log("Applicazione avviata", "INFO")
        self.log("💡 Il PRIMO file caricato sarà la worklist di riferimento", "INFO")
    
    def _setup_mode_section(self, parent):
        """NUOVO: Sezione per selezionare la modalità di confronto"""
        mode_frame = tk.LabelFrame(parent, text="⚙️ Modalità Confronto",
                                   font=("Arial", 12, "bold"),
                                   bg="#f8fafc", padx=15, pady=12)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Contenitore orizzontale per i radio buttons
        radio_container = tk.Frame(mode_frame, bg="#f8fafc")
        radio_container.pack(fill=tk.X)
        
        # Radio button MATCH (sinistra)
        match_frame = tk.Frame(radio_container, bg="#f8fafc")
        match_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Radiobutton(
            match_frame,
            text="✅ Trova CORRISPONDENZE",
            variable=self.modalita,
            value=self.config.MODE_MATCH,
            font=("Arial", 10, "bold"),
            bg="#f8fafc",
            fg="#1e293b",
            selectcolor="#f8fafc",
            activebackground="#f8fafc",
            activeforeground="#1e293b",
            cursor="hand2",
            command=self._on_mode_change
        ).pack(anchor=tk.W)
        
        tk.Label(
            match_frame,
            text="ISBN presenti negli altri file",
            font=("Arial", 9),
            bg="#f8fafc",
            fg="#64748b"
        ).pack(anchor=tk.W, padx=22)
        
        # Radio button NON_MATCH (destra)
        nonmatch_frame = tk.Frame(radio_container, bg="#f8fafc")
        nonmatch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Radiobutton(
            nonmatch_frame,
            text="❌ Trova NON CORRISPONDENZE",
            variable=self.modalita,
            value=self.config.MODE_NON_MATCH,
            font=("Arial", 10, "bold"),
            bg="#f8fafc",
            fg="#1e293b",
            selectcolor="#f8fafc",
            activebackground="#f8fafc",
            activeforeground="#1e293b",
            cursor="hand2",
            command=self._on_mode_change
        ).pack(anchor=tk.W)
        
        tk.Label(
            nonmatch_frame,
            text="ISBN non presenti negli altri file",
            font=("Arial", 9),
            bg="#f8fafc",
            fg="#64748b"
        ).pack(anchor=tk.W, padx=22)
    
    def _on_mode_change(self):
        """Callback quando cambia la modalità"""
        if self.modalita.get() == self.config.MODE_MATCH:
            self.log("🔍 Modalità: TROVA CORRISPONDENZE", "INFO")
        else:
            self.log("🔍 Modalità: TROVA NON CORRISPONDENZE", "WARNING")
    
    def _setup_file_section(self, parent):
        file_frame = tk.LabelFrame(parent, text="",
                                   font=("Arial", 12, "bold"),
                                   bg="#f8fafc", padx=15, pady=15)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Titolo personalizzato con stili diversi
        title_frame = tk.Frame(file_frame, bg="#f8fafc")
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame, text="📁 File Caricati ",
                font=("Arial", 11, "bold"), bg="#f8fafc", 
                fg="#1e293b").pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="(Trascina i file qui) ",
                font=("Arial", 10), bg="#f8fafc", 
                fg="#94a3b8").pack(side=tk.LEFT)
        
        tk.Label(title_frame, text="Il PRIMO file è la worklist",
                font=("Arial", 10, "bold"), bg="#f8fafc", 
                fg="#3b82f6").pack(side=tk.LEFT)
        
        # Pulsanti
        btn_frame = tk.Frame(file_frame, bg="#f8fafc")
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_btn = self.create_btn(btn_frame, "➕ Aggiungi File", 
                                        self.add_files, "#10b981")
        self.add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.remove_sel_btn = self.create_btn(btn_frame, "➖ Rimuovi Selezionato",
                                               self.remove_selected, "#f97316", tk.DISABLED)
        self.remove_sel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = self.create_btn(btn_frame, "🗑️ Rimuovi Tutti",
                                         self.clear_files, "#ef4444", tk.DISABLED)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.move_up_btn = self.create_btn(btn_frame, "⬆️ Su",
                                           self.move_file_up, "#8b5cf6", tk.DISABLED)
        self.move_up_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.move_down_btn = self.create_btn(btn_frame, "⬇️ Giù",
                                             self.move_file_down, "#8b5cf6", tk.DISABLED)
        self.move_down_btn.pack(side=tk.LEFT)
        
        # Lista file
        list_frame = tk.Frame(file_frame, bg="white", relief=tk.SUNKEN, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, font=("Consolas", 10),
                                       yscrollcommand=scrollbar.set, 
                                       selectmode=tk.SINGLE,
                                       bg="white", relief=tk.FLAT, 
                                       highlightthickness=0, height=7)
        self.file_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.bind('<<ListboxSelect>>', lambda e: self.update_buttons())
        self.file_listbox.bind('<Delete>', lambda e: self.remove_selected())
        self.file_listbox.bind('<BackSpace>', lambda e: self.remove_selected())
        
        # Abilita drag & drop se disponibile
        if self.drag_drop_enabled:
            try:
                from tkinterdnd2 import DND_FILES
                self.file_listbox.drop_target_register(DND_FILES)
                self.file_listbox.dnd_bind('<<Drop>>', self.drop_files)
            except ImportError:
                pass
    
    def _setup_action_buttons(self, parent):
        action_frame = tk.Frame(parent, bg="#f8fafc")
        action_frame.pack(pady=(0, 15), fill=tk.X)
        
        center = tk.Frame(action_frame, bg="#f8fafc")
        center.pack(expand=True)
        
        self.process_btn = self.create_btn(center, "⚡ ELABORA FILE",
                                           self.process_files, "#2563eb", 
                                           tk.DISABLED, ("Arial", 13, "bold"), 20, 8)
        self.process_btn.pack(side=tk.LEFT, padx=8)
        
        self.open_btn = self.create_btn(center, "📂 APRI OUTPUT",
                                        self.open_output_file, "#10b981",
                                        tk.DISABLED, ("Arial", 13, "bold"), 20, 8)
        self.open_btn.pack(side=tk.LEFT, padx=8)
        
        # Progress bar
        progress_frame = tk.Frame(action_frame, bg="#f8fafc")
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate',
                                            length=600, maximum=100)
        self.progress_bar.pack()
        
        self.progress_label = tk.Label(progress_frame, text="",
                                       font=("Arial", 9), bg="#f8fafc", fg="#64748b")
        self.progress_label.pack(pady=(5, 0))
    
    def _setup_log_section(self, parent):
        log_frame = tk.LabelFrame(parent, text="📋 Log Attività",
                                 font=("Arial", 12, "bold"),
                                 bg="#f8fafc", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=2,
                                                  font=("Consolas", 9),
                                                  bg="#ffffff", fg="#1e293b",
                                                  relief=tk.FLAT, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Controlli log
        log_controls = tk.Frame(log_frame, bg="#f8fafc")
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        clear_log_btn = tk.Button(log_controls, text="🗑️ Pulisci Log",
                                 command=self.clear_log, bg="#64748b",
                                 fg="white", font=("Arial", 9),
                                 padx=10, pady=3, cursor="hand2", relief=tk.FLAT)
        clear_log_btn.pack(side=tk.LEFT)
    
    def create_btn(self, parent, text, command, bg, state=tk.NORMAL,
                   font=("Arial", 10, "bold"), padx=20, pady=8):
        return tk.Button(parent, text=text, command=command, bg=bg,
                        fg="white", disabledforeground="white",
                        font=font, padx=padx, pady=pady,
                        cursor="hand2", relief=tk.FLAT, state=state)
    
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {"INFO": "#0ea5e9", "SUCCESS": "#10b981", 
                 "WARNING": "#f59e0b", "ERROR": "#ef4444"}
        symbols = {"INFO": "ℹ️", "SUCCESS": "✅", 
                  "WARNING": "⚠️", "ERROR": "❌"}
        
        log_entry = f"[{timestamp}] {symbols.get(level, 'ℹ️')} {message}\n"
        
        def _update():
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            last_line = self.log_text.index("end-1c linestart")
            self.log_text.tag_add(level, last_line, "end-1c")
            self.log_text.tag_config(level, foreground=colors.get(level, "#64748b"))
        
        self.root.after(0, _update)
        
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Log pulito", "INFO")
        
    def update_progress(self, current: int, total: int):
        def _update():
            if total > 0:
                percentage = int((current / total) * 100)
                self.progress_bar['value'] = percentage
                self.progress_label.config(text=f"Elaborazione: {percentage}%")
            if current >= total:
                self.root.after(2000, self.reset_progress)
        self.root.after(0, _update)
    
    def reset_progress(self):
        self.progress_bar['value'] = 0
        self.progress_label.config(text="")
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Seleziona File Excel",
            filetypes=[("File Excel", "*.xlsx *.xls"), ("Tutti i file", "*.*")]
        )
        
        added = 0
        for file in files:
            path = Path(file)
            if path not in self.files:
                self.files.append(path)
                added += 1
        
        if added > 0:
            self.refresh_file_list()
            self.update_buttons()
            self.log(f"{added} file aggiunti", "SUCCESS")
    
    def remove_selected(self):
        selections = self.file_listbox.curselection()
        if selections:
            idx = selections[0]
            removed_file = self.files[idx].name
            self.files.pop(idx)
            self.refresh_file_list()
            self.update_buttons()
            self.log(f"Rimosso: {removed_file}", "INFO")
    
    def clear_files(self):
        self.files.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_buttons()
        self.log("Lista file svuotata", "INFO")
    
    def move_file_up(self):
        selection = self.file_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        idx = selection[0]
        self.files[idx], self.files[idx-1] = self.files[idx-1], self.files[idx]
        self.refresh_file_list()
        self.file_listbox.selection_set(idx-1)
        self.log(f"File spostato in posizione {idx}", "INFO")
    
    def move_file_down(self):
        selection = self.file_listbox.curselection()
        if not selection or selection[0] >= len(self.files) - 1:
            return
        idx = selection[0]
        self.files[idx], self.files[idx+1] = self.files[idx+1], self.files[idx]
        self.refresh_file_list()
        self.file_listbox.selection_set(idx+1)
        self.log(f"File spostato in posizione {idx+2}", "INFO")
    
    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for idx, path in enumerate(self.files):
            if idx == 0:
                self.file_listbox.insert(tk.END, f"{path.name}  [WORKLIST]")
            else:
                self.file_listbox.insert(tk.END, path.name)
    
    def update_buttons(self):
        state = tk.NORMAL if self.files else tk.DISABLED
        self.clear_btn.config(state=state)
        self.remove_sel_btn.config(state=state)
        self.process_btn.config(state=tk.NORMAL if len(self.files) >= 2 else tk.DISABLED)
        
        selection = self.file_listbox.curselection()
        if selection and len(self.files) > 1:
            idx = selection[0]
            self.move_up_btn.config(state=tk.NORMAL if idx > 0 else tk.DISABLED)
            self.move_down_btn.config(
                state=tk.NORMAL if idx < len(self.files) - 1 else tk.DISABLED
            )
        else:
            self.move_up_btn.config(state=tk.DISABLED)
            self.move_down_btn.config(state=tk.DISABLED)
    
    def process_files(self):
        if len(self.files) < 2:
            messagebox.showerror("Errore", "Servono almeno 2 file per il confronto")
            return
        
        self.process_btn.config(state=tk.DISABLED)
        self.add_btn.config(state=tk.DISABLED)
        
        self.processing_thread = threading.Thread(
            target=self.execute_processing, daemon=True
        )
        self.processing_thread.start()
    
    def execute_processing(self):
        try:
            files = self.files.copy()
            modalita = self.modalita.get()
            
            result = self.processor.process_confronto_isbn(
                files, self.log, self.update_progress, modalita=modalita
            )
            self.root.after(0, lambda: self.show_success(result))
        except Exception as e:
            error_msg = str(e)  # ✅ Cattura il messaggio subito
            self.root.after(0, lambda: self.show_error(error_msg))
    
    def show_success(self, result: Dict[str, Any]):
        self.process_btn.config(state=tk.NORMAL)
        self.add_btn.config(state=tk.NORMAL)
        self.output_file = result['output']
        self.open_btn.config(state=tk.NORMAL)
        
        # NUOVO: Personalizza messaggio in base alla modalità
        if result['modalita'] == self.config.MODE_MATCH:
            titolo = "✅ Corrispondenze trovate"
            emoji_risultato = "✅"
        else:
            titolo = "❌ Non corrispondenze trovate"
            emoji_risultato = "❌"
        
        msg = f"📁 File salvato: {result['output'].name}\n\n"
        msg += f"📚 ISBN unici worklist: {result['isbn_wl']}\n"
        if result.get('duplicati_rimossi', 0) > 0:
            msg += f"🗑️ Duplicati rimossi: {result['duplicati_rimossi']}\n"
        msg += f"{emoji_risultato} Risultati: {result['match_trovati']}\n"
        msg += f"📊 File elaborati: {result['files_elaborati']}"
        
        self.log("✅ Elaborazione completata con successo!", "SUCCESS")
        messagebox.showinfo(titolo, msg)
    
    def show_error(self, error: str):
        self.process_btn.config(state=tk.NORMAL)
        self.add_btn.config(state=tk.NORMAL)
        self.log(f"Errore: {error}", "ERROR")
        messagebox.showerror("Errore", f"❌ Si è verificato un errore:\n\n{error}")
    
    def open_output_file(self):
        if self.output_file and self.output_file.exists():
            try:
                if platform.system() == 'Windows':
                    import os
                    os.startfile(self.output_file)
                elif platform.system() == 'Darwin':
                    subprocess.run(['open', str(self.output_file)])
                else:
                    subprocess.run(['xdg-open', str(self.output_file)])
                self.log(f"Aperto: {self.output_file.name}", "SUCCESS")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile aprire il file: {str(e)}")
                self.log(f"Errore apertura file: {str(e)}", "ERROR")
        else:
            messagebox.showwarning("Attenzione", "Nessun file di output disponibile")
    
    def drop_files(self, event):
        """Gestisce il drag & drop di file"""
        files = self.root.tk.splitlist(event.data)
        added = 0
        for file in files:
            path = Path(file.strip('{}'))
            if path.suffix.lower() in ['.xlsx', '.xls'] and path not in self.files:
                self.files.append(path)
                added += 1
        
        if added > 0:
            self.refresh_file_list()
            self.update_buttons()
            self.log(f"{added} file aggiunti", "SUCCESS")
    
    def show_help(self):
        """Mostra la finestra di aiuto"""
        mostra_aiuto(self.root)