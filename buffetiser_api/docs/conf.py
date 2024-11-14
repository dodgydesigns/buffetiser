# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django

sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buffetiser_api.settings')
sys.path.insert(0, os.path.abspath('../buffetiser_api/'))
# print("----------------------------------------------------------")
# print(sys.path)
# print(os.listdir(os.path.abspath('../buffetiser_api/')))
# print("----------------------------------------------------------")
django.setup()
sys.path.insert(0, os.path.abspath('..'))

# 
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Buffetiser'
copyright = '2024, Graeme Muller'
author = 'Graeme Muller'
release = '0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.coverage', 'sphinx.ext.napoleon', 'sphinx_rtd_theme',]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
