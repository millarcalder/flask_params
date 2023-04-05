project = 'flask_parameters'
copyright = '2023, Millar Calder'
author = 'Millar Calder'
release = '0.0.2'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_theme_options = {
    'sidebar_width': '250px'
}
