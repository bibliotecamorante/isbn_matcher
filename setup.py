"""
Setup script per ISBN Matcher
Copyright © 2024 Biblioteca Morante
Licenza: MIT License
"""

from setuptools import setup, find_packages
import os

# Leggi il contenuto del README per la descrizione lunga
def read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

setup(
    # CAMBIA QUESTI
    name='isbn-matcher',
    version='1.0.0',
    author='Biblioteca Morante',
    author_email='bibliotecamorante@gmail.com',
    description='Applicazione per confronto ISBN tra file Excel',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/bibliotecamorante/isbn_matcher', 
    license='MIT',
    
    # Classificatori PyPI
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',  # CAMBIATO
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Natural Language :: Italian',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
    ],
    
    # Keywords per la ricerca
    keywords='isbn excel library biblioteca books catalog management',
    
    # Specifica i pacchetti del tuo progetto
    packages=find_packages(),  # Trova automaticamente i package
    
    # Oppure specifica manualmente:
    # py_modules=['main', 'config', 'data_processor', 'excel_formatter', 'gui', 'utils', 'aiuto'],
    
    # Dipendenze OBBLIGATORIE
    install_requires=[
        'openpyxl>=3.1.0',
        'pandas>=1.5.0',
    ],
    
    # Dipendenze opzionali
    extras_require={
        'full': [
            'tkinterdnd2>=0.3.0',
            'ttkbootstrap>=2.0.0',
        ],
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
        ],
    },
    
    # Requisiti Python
    python_requires='>=3.8',
    
    # Entry point per eseguire l'app da command line
    entry_points={
        'console_scripts': [
            'isbn-matcher=main:__main__',  # O 'isbn-matcher=main:main' se hai funzione main()
        ],
    },
    
    # File da includere nel package
    include_package_data=True,
    
    # Specifica file extra (opzionale)
    package_data={
        # Se hai file di configurazione, esempi, ecc.
        # 'isbn_matcher': ['data/*.csv', 'config/*.json'],
    },
    
    # Informazioni di contatto
    project_urls={
        'Homepage': 'https://github.com/bibliotecamorante/isbn_matcher',
        'Bug Reports': 'https://github.com/bibliotecamorante/isbn_matcher/issues',
        'Source': 'https://github.com/bibliotecamorante/isbn_matcher',
    },
)
