# -*- coding: utf-8 -*-
"""
Funzioni di utilità per ISBN Matcher
"""
import pandas as pd
from typing import Any, Optional
from config import AppConfig


def normalizza_isbn(val: Any, config: AppConfig) -> str:
    """
    Normalizza un codice ISBN rimuovendo caratteri non validi.
    Mantiene solo numeri e X (per ISBN-10 con checksum X).
    
    Args:
        val: Valore da normalizzare
        config: Configurazione applicazione
    
    Returns:
        ISBN normalizzato (solo numeri e X)
    
    Esempi:
        >>> normalizza_isbn("978-88-123-4567-8")
        "9788812345678"
        >>> normalizza_isbn("88-123-4567-X")
        "881234567X"
    """
    if pd.isna(val):
        return ""
    val_str = str(val).strip().upper()
    # Usa regex da config per rimuovere caratteri non validi
    val_str = config.ISBN_CLEAN_RE.sub('', val_str)
    return val_str


def valida_isbn(isbn: str, config: AppConfig) -> bool:
    """
    Verifica se un ISBN è valido (lunghezza 10 o 13 caratteri).
    
    Args:
        isbn: ISBN normalizzato da validare
        config: Configurazione applicazione
    
    Returns:
        True se valido, False altrimenti
    """
    if not isbn:
        return False
    lunghezza = len(isbn)
    return config.MIN_ISBN_LENGTH <= lunghezza <= config.MAX_ISBN_LENGTH
    
    
def normalizza_serie_isbn(serie: pd.Series, config: AppConfig) -> pd.Series:
    """
    Normalizza un'intera colonna ISBN in un colpo solo (vettorizzato).
    Molto più veloce di .apply() su dataset con migliaia di righe.
    
    Args:
        serie: Serie pandas da normalizzare
        config: Configurazione applicazione
    
    Returns:
        Serie normalizzata
    
    Esempi:
        >>> s = pd.Series(["978-88-123", "88-456-X", None])
        >>> normalizza_serie_isbn(s, config)
        0    9788812345
        1    88456X
        2    
    """
    return (serie
            .fillna('')  # Gestisce NaN
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(config.ISBN_CLEAN_RE, '', regex=True))


def valida_serie_isbn(serie: pd.Series, config: AppConfig) -> pd.Series:
    """
    Valida un'intera colonna ISBN in un colpo solo (vettorizzato).
    
    Args:
        serie: Serie pandas di ISBN normalizzati
        config: Configurazione applicazione
    
    Returns:
        Serie booleana (True = valido)
    """
    lunghezze = serie.str.len()
    return (lunghezze >= config.MIN_ISBN_LENGTH) & (lunghezze <= config.MAX_ISBN_LENGTH)


def is_isbn_column_name(column_name: str, config: AppConfig) -> bool:
    """
    Verifica se il nome di una colonna è riconducibile a un ISBN.
    
    Args:
        column_name: Nome della colonna da verificare
        config: Configurazione applicazione
    
    Returns:
        True se la colonna è un ISBN, False altrimenti
    
    Esempi:
        >>> is_isbn_column_name("ISBN", config)
        True
        >>> is_isbn_column_name("Cod. ISBN", config)
        True
        >>> is_isbn_column_name("Titolo", config)
        False
    """
    if not column_name:
        return False
    col_norm = str(column_name).lower().strip().replace('.', '').replace(' ', '')
    varianti_norm = [v.lower().replace('.', '').replace(' ', '') for v in config.VARIANTI_ISBN]
    return col_norm in varianti_norm


def trova_colonna_isbn(df: pd.DataFrame, config: AppConfig) -> Optional[str]:
    """
    Trova la colonna ISBN in un DataFrame usando le varianti da config.
    
    Args:
        df: DataFrame da analizzare
        config: Configurazione con varianti colonne
    
    Returns:
        Nome della colonna ISBN trovata, o None se non trovata
    """
    for col in df.columns:
        if is_isbn_column_name(col, config):
            return col
    return None


def pulisci_serie(serie: pd.Series) -> pd.Series:
    """Pulisce una serie pandas rimuovendo NA e spazi."""
    return serie.dropna().astype(str).str.strip()


def trim_df(df: pd.DataFrame) -> pd.DataFrame:
    """Rimuove spazi dalle colonne stringa di un DataFrame."""
    string_columns = df.select_dtypes(include=['object']).columns
    df[string_columns] = df[string_columns].apply(lambda x: x.str.strip())
    return df