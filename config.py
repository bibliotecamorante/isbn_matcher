# -*- coding: utf-8 -*-
"""
Configurazioni dell'applicazione ISBN Matcher
"""
from dataclasses import dataclass, field
from typing import List, Dict
import re

@dataclass
class AppConfig:
    """Configurazioni centralizzate dell'applicazione"""
    
    # ========================================================================
    # COSTANTI DI STATO
    # ========================================================================
    
    MODE_MATCH: str = "MATCH"
    MODE_NON_MATCH: str = "NON_MATCH"
    
    
    # ========================================================================
    # RICONOSCIMENTO COLONNE - Varianti accettate
    # ========================================================================
    
    VARIANTI_ISBN: List[str] = field(default_factory=lambda: [
        'isbn', 'codice isbn', 'cod isbn', 'cod. isbn',
        'ean', 'codice', 'barcode', 'codiceean', 'codice ean'
    ])
    """Varianti accettate per la colonna ISBN"""
    
    # ========================================================================
    # OUTPUT E FILE GENERATI
    # ========================================================================
    
    SUFFIX_OUTPUT: str = "_confronto_isbn.xlsx"
    """Suffisso per file di output"""
    
    SHEET_PARAMETRI: str = "parametri"
    """Nome del foglio da ignorare in tutti i file Excel"""
    
    # ========================================================================
    # FORMATTAZIONE EXCEL
    # ========================================================================
    
    ABBREV: Dict[str, str] = field(default_factory=lambda: {
        "sezione": "Sez", 
        "specificazione": "Spec", 
        "sequenza": "Seq",
        "legami con titoli superiori o supplementi": "Legami", 
        "tipo provenienza": "Provenienza"
    })
    """Abbreviazioni per intestazioni colonne"""
    
    LARGHEZZE: Dict[str, int] = field(default_factory=lambda: {
        "descrizione isbd": 67,
        "isbd": 67,
        "titolo": 67,
        "collocazione": 14, 
        "disponibilità": 12,
        "data inv.": 13, 
        "inventario": 10, 
        "sequenza": 6, 
        "sezione": 6,
        "id. sbn": 14, 
        "legami con titoli superiori o supplementi": 22,
        "autore": 25,
        "autore estratto": 25,
        "anno pubblicazione": 12,
        "sebinayou (morante)": 20,
        "sebinayou (tutte)": 20,
        "link sbn": 15
    })
    """Larghezze colonne Excel (in caratteri)"""
    
    LARGHEZZE_DEFAULT: int = field(default=15)
    """Larghezza predefinita colonne Excel"""
    
    # ========================================================================
    # STILI EXCEL (Sebina Plus Theme)
    # ========================================================================

    # Colori (formato openpyxl - senza #)
    EXCEL_COLOR_HEADER: str = field(default='8DBEE3')
    """Colore header tabelle Excel (azzurro Sebina)"""

    EXCEL_COLOR_HEADER_FONT: str = field(default='000000')
    """Colore testo header (nero)"""

    # Dimensioni
    EXCEL_ROW_HEIGHT_HEADER: int = field(default=19)
    """Altezza riga intestazione Excel"""

    EXCEL_ROW_HEIGHT_DATA: int = field(default=30)
    """Altezza righe dati Excel"""

    EXCEL_COLUMN_WIDTH_ISBN: int = field(default=18)
    """Larghezza colonne ISBN"""

    EXCEL_ZOOM: int = field(default=110)
    """Livello zoom foglio Excel (%)"""
    
        
    # ========================================================================
    # PULIZIA DATI
    # ========================================================================
    
    COLS_RIMUOVI: List[str] = field(default_factory=lambda: [
        'Tipo documento', 
        'Tipo materiale dell\'inventario', 
        'Valore inventariale',
        'Prezzo acquisto', 
        'Oggetti digitali inventario', 
        'Oggetti digitali titolo'
    ])
    """Colonne da rimuovere automaticamente durante l'elaborazione"""
    
    PROVENIENZA_MAP: Dict[str, str] = field(default_factory=lambda: {
        'ACQUISTO': 'ACQ', 
        'ACQUISTO CENTRALIZZATO': 'ACQ', 
        'ACQUISTO RAGAZZI': 'ACQ',
        'ACQUISTO CENTRALIZZATO RAGAZZI': 'ACQ', 
        'SOSTITUZIONE': 'SOS', 
        'TRASFERIMENTO': 'TRA',
        'DONO': 'DON', 
        'DONO RAGAZZI': 'DON', 
        'SCAMBIO': 'SCA'
    })
    """Mappatura valori provenienza -> abbreviazioni"""
    
    # ========================================================================
    # REGEX E COSTANTI PER RICERCA ISBN
    # ========================================================================
    
    # Regex pre-compilata per pulizia ISBN (migliora performance in batch)
    ISBN_CLEAN_RE: re.Pattern = field(default_factory=lambda: re.compile(r'[^0-9X]'))
    """Pattern per pulire ISBN (mantiene solo numeri e X)"""
    
    # Split input multipli (supporta vari separatori)
    ISBN_SPLIT_RE: re.Pattern = field(default_factory=lambda: re.compile(r'[\n\r•,; \t]+'))
    """Pattern per separare ISBN multipli"""
    
    # Configurazione ricerca
    MIN_ISBN_LENGTH: int = field(default=10)
    """Lunghezza minima ISBN valido"""
    
    MAX_ISBN_LENGTH: int = field(default=13)
    """Lunghezza massima ISBN valido"""
    
    # Nomi colonne temporanee (evita stringhe hardcoded nel codice)
    COL_ISBN_NORM: str = field(default='_isbn_norm')
    """Nome colonna temporanea per ISBN normalizzati"""

    COL_ISBN_VALIDO: str = field(default='_isbn_valido')
    """Nome colonna temporanea per flag validità ISBN"""
    
    
    BATCH_SIZE_EXCEL: int = field(default=20)
    """Numero massimo celle per batch Excel (evita overflow)"""