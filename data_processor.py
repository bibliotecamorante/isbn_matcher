# -*- coding: utf-8 -*-
"""
Classe per la logica di elaborazione dati (Business Logic)
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
from config import AppConfig
from utils import (
    normalizza_isbn, 
    valida_isbn, 
    trova_colonna_isbn, 
    trim_df, 
    normalizza_serie_isbn, 
    valida_serie_isbn
)
from excel_formatter import formatta_excel_isbn

# Livelli di Log
LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR = "ERROR"
LOG_SUCCESS = "SUCCESS"


class DataProcessor:
    """Classe per la logica di elaborazione dati"""
    
    def __init__(self, config: AppConfig):
        self.config = config
    
    def process_confronto_isbn(
        self, 
        files: List[Path], 
        log_callback: Callable[[str, str], None],
        progress_callback: Optional[Callable[[int, int], None]] = None,
        modalita: str = None  # "MATCH" o "NON_MATCH"
    ) -> Dict[str, Any]:
        """
        Confronta ISBN tra file Excel.
        Il primo file è la worklist di riferimento.
        
        Args:
            files: Lista di file da elaborare
            log_callback: Funzione per logging (message, level)
            progress_callback: Funzione per progress bar (current, total)
            modalita: "MATCH" per trovare corrispondenze, "NON_MATCH" per non corrispondenze
        
        Returns:
            Dict con statistiche: output, isbn_wl, match_trovati, duplicati_rimossi
        """
        if modalita is None:
            modalita = self.config.MODE_MATCH
        
        if modalita == self.config.MODE_MATCH:
            log_callback("🔍 Modalità: TROVA CORRISPONDENZE", LOG_INFO)
        else:
            log_callback("🔍 Modalità: TROVA NON CORRISPONDENZE", LOG_INFO)
        
        log_callback("Inizio confronto ISBN", LOG_INFO)
        
        if len(files) < 2:
            raise Exception("Servono almeno 2 file per il confronto ISBN")
        
        file_wl = files[0]
        file_non_wl = files[1:]
        
        log_callback(f"File Worklist: {file_wl.name}", LOG_INFO)
        
        if progress_callback:
            progress_callback(0, 100)
        
        # ====================================================================
        # STEP 1: Carica worklist (concatena tutti i fogli)
        # ====================================================================
        df_wl = pd.DataFrame()
        for nome, df in pd.read_excel(file_wl, sheet_name=None, dtype=str).items():
            if nome.lower() != self.config.SHEET_PARAMETRI:
                col_isbn = trova_colonna_isbn(df, self.config)
                if col_isbn:
                    df_wl = pd.concat([df_wl, df], ignore_index=True)
        
        if df_wl.empty:
            raise Exception("Nessuna colonna ISBN trovata nel file worklist")
        
        col_isbn_wl = trova_colonna_isbn(df_wl, self.config)
        if not col_isbn_wl:
            raise Exception("Colonna ISBN non trovata nella worklist")
        
        # Normalizza ISBN (VETTORIZZATO - molto più veloce!)
        df_wl[self.config.COL_ISBN_NORM] = normalizza_serie_isbn(
            df_wl[col_isbn_wl], 
            self.config
        )

        # Filtra ISBN validi (VETTORIZZATO)
        df_wl = df_wl[valida_serie_isbn(
            df_wl[self.config.COL_ISBN_NORM], 
            self.config
        )]
        
        # Diagnostica duplicati
        isbn_totali_prima = len(df_wl)
        isbn_unici_prima = df_wl[self.config.COL_ISBN_NORM].nunique()
        duplicati = isbn_totali_prima - isbn_unici_prima
        
        if duplicati > 0:
            log_callback(
                f"⚠️ Worklist: {isbn_totali_prima} righe totali, "
                f"{isbn_unici_prima} ISBN unici",
                LOG_WARNING
            )
            log_callback(f"   Rilevati {duplicati} duplicati (verranno rimossi)", LOG_WARNING)
        
        # Deduplicazione - mantiene prima occorrenza
        df_wl = df_wl.drop_duplicates(
            subset=[self.config.COL_ISBN_NORM], 
            keep='first'
        )

        log_callback(
            f"✅ ISBN unici nella worklist: {df_wl[self.config.COL_ISBN_NORM].nunique()}", 
            LOG_SUCCESS
        )
        
        if progress_callback:
            progress_callback(30, 100)
        
        # ====================================================================
        # STEP 2: Ricerca match negli altri file
        # ====================================================================
        # OTTIMIZZAZIONE: Converte ISBN worklist in set per lookup O(1)
        set_isbn_riferimento = set(df_wl[self.config.COL_ISBN_NORM])
        log_callback(f"📦 Set di riferimento creato ({len(set_isbn_riferimento)} ISBN)", LOG_INFO)
        
        isbn_trovati = set()
        total_files = len(file_non_wl)
        
        for idx, file in enumerate(file_non_wl):
            log_callback(f"Ricerca in: {file.name}", LOG_INFO)
            file_matches = 0
            
            if progress_callback:
                progress_callback(30 + int(40 * (idx / total_files)), 100)
            
            # OTTIMIZZAZIONE: Prima identifichiamo la colonna ISBN senza caricare dati
            for nome in pd.ExcelFile(file).sheet_names:
                if nome.lower() == self.config.SHEET_PARAMETRI:
                    continue
                
                # Carica solo le intestazioni (0 righe) per trovare la colonna ISBN
                df_headers = pd.read_excel(file, sheet_name=nome, nrows=0, dtype=str)
                col_isbn = trova_colonna_isbn(df_headers, self.config)
                
                if not col_isbn:
                    continue
                
                # Carica SOLO la colonna ISBN (risparmio enorme di memoria!)
                df_isbn_only = pd.read_excel(
                    file, 
                    sheet_name=nome, 
                    usecols=[col_isbn], 
                    dtype=str
                )
                
                # Normalizza ISBN (usa vettorizzazione quando possibile)
                df_isbn_only[self.config.COL_ISBN_NORM] = normalizza_serie_isbn(
                    df_isbn_only[col_isbn],
                    self.config
                )
                
                # Filtra validi (vettorizzato)
                mask_validi = valida_serie_isbn(
                    df_isbn_only[self.config.COL_ISBN_NORM],
                    self.config
                )
                isbn_validi = df_isbn_only.loc[mask_validi, self.config.COL_ISBN_NORM]
                
                # Trova match (usa set per performance O(1))
                matches = isbn_validi.isin(set_isbn_riferimento)
                
                if matches.any():
                    isbn_trovati.update(isbn_validi[matches].values)
                    file_matches += matches.sum()
            
            if file_matches > 0:
                log_callback(f"  Match in {file.name}: {file_matches}", LOG_SUCCESS)
        
        if progress_callback:
            progress_callback(70, 100)
        
        # ====================================================================
        # STEP 3: Filtra risultati in base alla modalità
        # ====================================================================
        # Crea maschera booleana (più efficiente e leggibile)
        is_present = df_wl[self.config.COL_ISBN_NORM].isin(isbn_trovati)

        if modalita == self.config.MODE_MATCH:
            # Modalità: trova ISBN che HANNO match
            if not isbn_trovati:
                raise Exception("Nessun match trovato tra la worklist e gli altri file")
            
            df_finale = df_wl[is_present].copy()
            output_prefix = "confronto_isbn"
            log_msg = "Match trovati"
        else:
            # Modalità: trova ISBN che NON HANNO match
            df_finale = df_wl[~is_present].copy()
            
            if df_finale.empty:
                raise Exception("Tutti gli ISBN della worklist hanno match negli altri file")
            
            output_prefix = "non_match_isbn"
            log_msg = "Non corrispondenze trovate"
        
        # Rimuovi colonna temporanea
        df_finale = df_finale.drop([self.config.COL_ISBN_NORM], axis=1)
        df_finale = trim_df(df_finale)
        
        # Verifica consistenza
        risultati_count = len(df_finale)
        
        output = file_non_wl[0].parent / f"{output_prefix}{self.config.SUFFIX_OUTPUT}"
        
        df_finale.to_excel(output, index=False, engine='openpyxl')
        
        if progress_callback:
            progress_callback(80, 100)
        
        # Applica formattazione Excel
        log_callback("Applicazione formattazione Excel...", LOG_INFO)
        formatta_excel_isbn(output, self.config, log_callback, progress_callback)
        
        if progress_callback:
            progress_callback(100, 100)
        
        log_callback(f"Riepilogo:", LOG_INFO)
        log_callback(f"  • ISBN worklist (unici): {isbn_unici_prima}", LOG_INFO)
        if duplicati > 0:
            log_callback(f"  • Duplicati rimossi: {duplicati}", LOG_WARNING)
        log_callback(f"  • {log_msg}: {risultati_count}", LOG_SUCCESS)
        
        return {
            'output': output,
            'isbn_wl': isbn_unici_prima,
            'match_trovati': risultati_count,
            'files_elaborati': len(files),
            'duplicati_rimossi': duplicati,
            'modalita': modalita
        }