# -*- coding: utf-8 -*-
"""
Sistema di localizzazione per ISBN Matcher
Supporta italiano e inglese
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class Translations:
    """Traduzioni per l'interfaccia utente"""
    
    # Window titles
    app_title: str
    help_title: str
    
    # Header
    app_subtitle: str
    
    # Mode section
    mode_section_title: str
    mode_match: str
    mode_match_desc: str
    mode_non_match: str
    mode_non_match_desc: str
    
    # File section
    files_loaded: str
    drag_drop_hint: str
    first_file_worklist: str
    btn_add_files: str
    btn_remove_selected: str
    btn_remove_all: str
    btn_move_up: str
    btn_move_down: str
    worklist_label: str
    
    # Action buttons
    btn_process: str
    btn_open_output: str
    processing_label: str
    
    # Log section
    log_title: str
    btn_clear_log: str
    
    # Help button
    btn_help: str
    
    # Help window content
    help_what_does: str
    help_what_does_content: str
    help_how_to_use: str
    help_how_to_use_content: str
    help_output_format: str
    help_output_format_content: str
    help_tips: str
    help_tips_content: str
    help_isbn_columns: str
    help_isbn_columns_content: str
    help_troubleshooting: str
    help_troubleshooting_content: str
    btn_close: str
    
    # Log messages
    log_app_started: str
    log_first_file_info: str
    log_mode_match: str
    log_mode_non_match: str
    log_files_added: str
    log_file_removed: str
    log_files_cleared: str
    log_file_moved_to: str
    log_processing_complete: str
    log_file_opened: str
    log_log_cleared: str
    
    # Processing messages
    proc_mode_match: str
    proc_mode_non_match: str
    proc_start_comparison: str
    proc_worklist_file: str
    proc_worklist_rows: str
    proc_duplicates_detected: str
    proc_duplicates_removed: str
    proc_unique_isbn: str
    proc_reference_set: str
    proc_searching_in: str
    proc_matches_in: str
    proc_applying_format: str
    proc_summary: str
    proc_worklist_unique: str
    proc_duplicates_removed_label: str
    proc_results_found: str
    proc_saving_format: str
    proc_format_complete: str
    proc_formatting_sheet: str
    
    # Error messages
    error_title: str
    error_occurred: str
    error_min_files: str
    error_no_isbn_worklist: str
    error_no_isbn_column: str
    error_no_matches: str
    error_all_matched: str
    error_open_file: str
    error_file_open_excel: str
    error_formatting: str
    error_critical: str
    error_cannot_start: str
    
    # Success messages
    success_title_match: str
    success_title_non_match: str
    success_file_saved: str
    success_worklist_isbn: str
    success_duplicates_removed: str
    success_results: str
    success_files_processed: str
    
    # Warning messages
    warning_title: str
    warning_no_output: str
    warning_drag_drop_unavailable: str
    warning_drag_drop_message: str
    
    # Info messages
    info_title: str


# Traduzioni italiane
IT = Translations(
    # Window titles
    app_title="ISBN Matcher",
    help_title="Aiuto - ISBN Matcher",
    
    # Header
    app_subtitle="Confronto intelligente di codici ISBN tra file Excel",
    
    # Mode section
    mode_section_title="⚙️ Modalità Confronto",
    mode_match="✅ Trova CORRISPONDENZE",
    mode_match_desc="ISBN presenti negli altri file",
    mode_non_match="❌ Trova NON CORRISPONDENZE",
    mode_non_match_desc="ISBN non presenti negli altri file",
    
    # File section
    files_loaded="📁 File Caricati",
    drag_drop_hint="(Trascina i file qui)",
    first_file_worklist="Il PRIMO file è la worklist",
    btn_add_files="➕ Aggiungi File",
    btn_remove_selected="➖ Rimuovi Selezionato",
    btn_remove_all="🗑️ Rimuovi Tutti",
    btn_move_up="⬆️ Su",
    btn_move_down="⬇️ Giù",
    worklist_label="[WORKLIST]",
    
    # Action buttons
    btn_process="⚡ ELABORA FILE",
    btn_open_output="📂 APRI OUTPUT",
    processing_label="Elaborazione",
    
    # Log section
    log_title="📋 Log Attività",
    btn_clear_log="🗑️ Pulisci Log",
    
    # Help button
    btn_help="❓",
    
    # Help window content
    help_what_does="📚 COSA FA QUESTA APP",
    help_what_does_content="""Confronta una lista di ISBN (worklist) con altri file Excel e trova:
• Corrispondenze: ISBN presenti in entrambi
• Non corrispondenze: ISBN della worklist mancanti negli altri file""",
    
    help_how_to_use="🎯 COME USARE",
    help_how_to_use_content="""1. SCEGLI LA MODALITÀ
   ✅ Corrispondenze: trova ISBN comuni
   ❌ Non corrispondenze: trova ISBN mancanti

2. CARICA I FILE
   • Il PRIMO file è la worklist (lista di riferimento)
   • Aggiungi altri file da confrontare
   • Puoi trascinare i file nella finestra (drag & drop)

3. ELABORA
   • Clicca "⚡ ELABORA FILE"
   • Attendi il completamento
   • Clicca "📂 APRI OUTPUT" per vedere il risultato""",
    
    help_output_format="⚙️ FORMATTAZIONE OUTPUT",
    help_output_format_content="""Il file Excel generato include:
• Header abbreviati (Sez, Spec, Seq...)
• Larghezze colonne ottimizzate
• Intestazione con sfondo azzurro
• Prima riga bloccata (freeze panes)
• Zoom al 110%""",
    
    help_tips="💡 SUGGERIMENTI",
    help_tips_content="""• La worklist può avere più fogli: verranno uniti automaticamente
• I duplicati nella worklist vengono rimossi automaticamente
• Il foglio "parametri" viene sempre ignorato
• Puoi riordinare i file con i pulsanti ⬆️ ⬇️""",
    
    help_isbn_columns="🔍 COLONNE ISBN RICONOSCIUTE",
    help_isbn_columns_content="""L'app riconosce automaticamente colonne con nomi come:
• ISBN, Codice ISBN, Cod. ISBN
• EAN, Codice EAN
• Codice, Barcode""",
    
    help_troubleshooting="❌ RISOLUZIONE PROBLEMI",
    help_troubleshooting_content="""• Se il file non si apre: chiudi Excel e riprova
• Se non trova ISBN: verifica che il nome colonna sia corretto
• Per problemi: controlla il log nella sezione "📋 Log Attività" """,
    
    btn_close="Chiudi",
    
    # Log messages
    log_app_started="Applicazione avviata",
    log_first_file_info="💡 Il PRIMO file caricato sarà la worklist di riferimento",
    log_mode_match="🔍 Modalità: TROVA CORRISPONDENZE",
    log_mode_non_match="🔍 Modalità: TROVA NON CORRISPONDENZE",
    log_files_added="file aggiunti",
    log_file_removed="Rimosso",
    log_files_cleared="Lista file svuotata",
    log_file_moved_to="File spostato in posizione",
    log_processing_complete="✅ Elaborazione completata con successo!",
    log_file_opened="Aperto",
    log_log_cleared="Log pulito",
    
    # Processing messages
    proc_mode_match="🔍 Modalità: TROVA CORRISPONDENZE",
    proc_mode_non_match="🔍 Modalità: TROVA NON CORRISPONDENZE",
    proc_start_comparison="Inizio confronto ISBN",
    proc_worklist_file="File Worklist",
    proc_worklist_rows="righe totali",
    proc_duplicates_detected="⚠️ Worklist",
    proc_duplicates_removed="Rilevati {duplicati} duplicati (verranno rimossi)",
    proc_unique_isbn="✅ ISBN unici nella worklist",
    proc_reference_set="📦 Set di riferimento creato",
    proc_searching_in="Ricerca in",
    proc_matches_in="Match in",
    proc_applying_format="Applicazione formattazione Excel...",
    proc_summary="Riepilogo:",
    proc_worklist_unique="• ISBN worklist (unici)",
    proc_duplicates_removed_label="• Duplicati rimossi",
    proc_results_found="trovati",
    proc_saving_format="Salvataggio formattazione...",
    proc_format_complete="✅ Formattazione completata",
    proc_formatting_sheet="Formattazione foglio",
    
    # Error messages
    error_title="Errore",
    error_occurred="❌ Si è verificato un errore:\n\n",
    error_min_files="Servono almeno 2 file per il confronto",
    error_no_isbn_worklist="Nessuna colonna ISBN trovata nel file worklist",
    error_no_isbn_column="Colonna ISBN non trovata nella worklist",
    error_no_matches="Nessun match trovato tra la worklist e gli altri file",
    error_all_matched="Tutti gli ISBN della worklist hanno match negli altri file",
    error_open_file="Impossibile aprire il file",
    error_file_open_excel="Il file '{filename}' è aperto in Excel.\nChiudilo e riprova l'operazione.",
    error_formatting="❌ Errore formattazione",
    error_critical="Errore Critico",
    error_cannot_start="Impossibile avviare l'applicazione:\n\n",
    
    # Success messages
    success_title_match="✅ Corrispondenze trovate",
    success_title_non_match="❌ Non corrispondenze trovate",
    success_file_saved="📁 File salvato",
    success_worklist_isbn="📚 ISBN unici worklist",
    success_duplicates_removed="🗑️ Duplicati rimossi",
    success_results="Risultati",
    success_files_processed="📊 File elaborati",
    
    # Warning messages
    warning_title="Attenzione",
    warning_no_output="Nessun file di output disponibile",
    warning_drag_drop_unavailable="Funzionalità Limitata",
    warning_drag_drop_message="""⚠️ La libreria 'tkinterdnd2' non è installata.

Il drag & drop dei file non sarà disponibile.
Usa il pulsante '➕ Aggiungi File' per caricare i file.

Per abilitare il drag & drop, installa:
pip install tkinterdnd2""",
    
    # Info messages
    info_title="Informazione",
)


# Traduzioni inglesi
EN = Translations(
    # Window titles
    app_title="ISBN Matcher",
    help_title="Help - ISBN Matcher",
    
    # Header
    app_subtitle="Smart ISBN code comparison between Excel files",
    
    # Mode section
    mode_section_title="⚙️ Comparison Mode",
    mode_match="✅ Find MATCHES",
    mode_match_desc="ISBNs present in other files",
    mode_non_match="❌ Find NON-MATCHES",
    mode_non_match_desc="ISBNs not present in other files",
    
    # File section
    files_loaded="📁 Loaded Files",
    drag_drop_hint="(Drag files here)",
    first_file_worklist="The FIRST file is the worklist",
    btn_add_files="➕ Add Files",
    btn_remove_selected="➖ Remove Selected",
    btn_remove_all="🗑️ Remove All",
    btn_move_up="⬆️ Up",
    btn_move_down="⬇️ Down",
    worklist_label="[WORKLIST]",
    
    # Action buttons
    btn_process="⚡ PROCESS FILES",
    btn_open_output="📂 OPEN OUTPUT",
    processing_label="Processing",
    
    # Log section
    log_title="📋 Activity Log",
    btn_clear_log="🗑️ Clear Log",
    
    # Help button
    btn_help="❓",
    
    # Help window content
    help_what_does="📚 WHAT THIS APP DOES",
    help_what_does_content="""Compares a list of ISBNs (worklist) with other Excel files and finds:
• Matches: ISBNs present in both
• Non-matches: ISBNs from worklist missing in other files""",
    
    help_how_to_use="🎯 HOW TO USE",
    help_how_to_use_content="""1. CHOOSE MODE
   ✅ Matches: find common ISBNs
   ❌ Non-matches: find missing ISBNs

2. LOAD FILES
   • The FIRST file is the worklist (reference list)
   • Add other files to compare
   • You can drag files into the window (drag & drop)

3. PROCESS
   • Click "⚡ PROCESS FILES"
   • Wait for completion
   • Click "📂 OPEN OUTPUT" to see the result""",
    
    help_output_format="⚙️ OUTPUT FORMATTING",
    help_output_format_content="""The generated Excel file includes:
• Abbreviated headers (Sec, Spec, Seq...)
• Optimized column widths
• Header with blue background
• First row frozen (freeze panes)
• 110% zoom""",
    
    help_tips="💡 TIPS",
    help_tips_content="""• The worklist can have multiple sheets: they will be merged automatically
• Duplicates in the worklist are removed automatically
• The "parameters" sheet is always ignored
• You can reorder files with ⬆️ ⬇️ buttons""",
    
    help_isbn_columns="🔍 RECOGNIZED ISBN COLUMNS",
    help_isbn_columns_content="""The app automatically recognizes columns with names like:
• ISBN, ISBN Code, ISBN Cod.
• EAN, EAN Code
• Code, Barcode""",
    
    help_troubleshooting="❌ TROUBLESHOOTING",
    help_troubleshooting_content="""• If the file won't open: close Excel and try again
• If ISBN not found: check that the column name is correct
• For issues: check the log in "📋 Activity Log" section""",
    
    btn_close="Close",
    
    # Log messages
    log_app_started="Application started",
    log_first_file_info="💡 The FIRST file loaded will be the reference worklist",
    log_mode_match="🔍 Mode: FIND MATCHES",
    log_mode_non_match="🔍 Mode: FIND NON-MATCHES",
    log_files_added="files added",
    log_file_removed="Removed",
    log_files_cleared="File list cleared",
    log_file_moved_to="File moved to position",
    log_processing_complete="✅ Processing completed successfully!",
    log_file_opened="Opened",
    log_log_cleared="Log cleared",
    
    # Processing messages
    proc_mode_match="🔍 Mode: FIND MATCHES",
    proc_mode_non_match="🔍 Mode: FIND NON-MATCHES",
    proc_start_comparison="Starting ISBN comparison",
    proc_worklist_file="Worklist File",
    proc_worklist_rows="total rows",
    proc_duplicates_detected="⚠️ Worklist",
    proc_duplicates_removed="Detected {duplicates} duplicates (will be removed)",
    proc_unique_isbn="✅ Unique ISBNs in worklist",
    proc_reference_set="📦 Reference set created",
    proc_searching_in="Searching in",
    proc_matches_in="Matches in",
    proc_applying_format="Applying Excel formatting...",
    proc_summary="Summary:",
    proc_worklist_unique="• Worklist ISBN (unique)",
    proc_duplicates_removed_label="• Duplicates removed",
    proc_results_found="found",
    proc_saving_format="Saving formatting...",
    proc_format_complete="✅ Formatting completed",
    proc_formatting_sheet="Formatting sheet",
    
    # Error messages
    error_title="Error",
    error_occurred="❌ An error occurred:\n\n",
    error_min_files="At least 2 files are required for comparison",
    error_no_isbn_worklist="No ISBN column found in worklist file",
    error_no_isbn_column="ISBN column not found in worklist",
    error_no_matches="No matches found between worklist and other files",
    error_all_matched="All worklist ISBNs have matches in other files",
    error_open_file="Cannot open file",
    error_file_open_excel="The file '{filename}' is open in Excel.\nClose it and try again.",
    error_formatting="❌ Formatting error",
    error_critical="Critical Error",
    error_cannot_start="Cannot start application:\n\n",
    
    # Success messages
    success_title_match="✅ Matches found",
    success_title_non_match="❌ Non-matches found",
    success_file_saved="📁 File saved",
    success_worklist_isbn="📚 Unique worklist ISBNs",
    success_duplicates_removed="🗑️ Duplicates removed",
    success_results="Results",
    success_files_processed="📊 Files processed",
    
    # Warning messages
    warning_title="Warning",
    warning_no_output="No output file available",
    warning_drag_drop_unavailable="Limited Functionality",
    warning_drag_drop_message="""⚠️ The 'tkinterdnd2' library is not installed.

File drag & drop will not be available.
Use the '➕ Add Files' button to load files.

To enable drag & drop, install:
pip install tkinterdnd2""",
    
    # Info messages
    info_title="Information",
)


# Dizionario per accesso rapido
LANGUAGES: Dict[str, Translations] = {
    'it': IT,
    'en': EN
}


def get_translations(lang_code: str = 'it') -> Translations:
    """
    Ottiene le traduzioni per la lingua specificata.
    
    Args:
        lang_code: Codice lingua ('it' o 'en')
    
    Returns:
        Oggetto Translations con le traduzioni
    """
    return LANGUAGES.get(lang_code, IT)