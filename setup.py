"""
Setup script per ISBN Matcher
Copyright © 2024 Biblioteca Morante
Licenza: MIT License
"""
from setuptools import setup, find_packages
import os

def read_file(filename):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='isbn-matcher',
    version='1.0.0',
    author='Biblioteca Morante',
    author_email='bibliotecamorante@gmail.com',
    description='Applicazione per confronto ISBN tra file Excel',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/bibliotecamorante/isbn_matcher',
    license='MIT',
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Operating System :: OS Independent',
        'Natural Language :: Italian',
    ],
    
    keywords='isbn excel library books catalog management',
    
    # ⚠️ IMPORTANTE: Non usare find_packages() se i file sono nella root
    # Usa py_modules invece
    py_modules=[
        'main',
        'config', 
        'data_processor', 
        'excel_formatter', 
        'gui', 
        'utils', 
        'aiuto'
    ],
    
    install_requires=[
        'openpyxl>=3.1.0',
        'pandas>=2.0.0',
    ],
    
    extras_require={
        'full': [
            'tkinterdnd2>=0.3.0',
        ],
    },
    
    python_requires='>=3.8',
    
    # ⚠️ IMPORTANTE: Entry point corretto
    entry_points={
        'console_scripts': [
            'isbn-matcher=main:main',
        ],
    },
    
    include_package_data=True,
    
    project_urls={
        'Homepage': 'https://github.com/bibliotecamorante/isbn_matcher',
        'Bug Reports': 'https://github.com/bibliotecamorante/isbn_matcher/issues',
        'Source': 'https://github.com/bibliotecamorante/isbn_matcher',
    },
)
