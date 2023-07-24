import pydata_sphinx_theme
import datetime
import os
import sys
import cake

sys.path.append(os.path.abspath('../extensions'))

project = 'Documentation'
copyright = '2023, Seniatical'
author = 'Seniatical'
release = cake.__version__

extensions = [
   'sphinx.ext.autodoc', 
   'sphinx.ext.coverage', 
   'sphinx.ext.napoleon',
   'sphinx.ext.extlinks',
   'sphinx.ext.intersphinx',
   'sphinx.ext.autosummary',
]

intersphinx_mapping = {
  'py': ('https://docs.python.org/3', None),
}

templates_path = ['_templates']
exclude_patterns = ['*.md', '*.template']

html_theme = 'pydata_sphinx_theme'
html_logo = "_static/icon.png"

html_theme_options = {
   "favicons": [
        {
            "rel": "icon",
            "sizes": "16x16",
            "href": "icon.png",
        },
        {
            "rel": "icon",
            "sizes": "32x32",
            "href": "icon.png",
        },
        {
            "rel": "apple-touch-icon",
            "sizes": "180x180",
            "href": "icon.png"
        },
    ],

   "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/Seniatical/Cake",
            "icon": "fab fa-github",
        },
        {
            "name": "Discord",
            "url": "https://discord.gg/BPC3STaTRd",
            "icon": "fab fa-discord"
        },
    ],

   "use_edit_page_button": True,
   "collapse_navigation": False,
   "show_prev_next": False,
   "navigation_depth": 3,
   "search_bar_text": "Search the docs ...",
   "footer_start": ["last-updated"],
   "footer_end": ["copyright"],

   "announcement": "Cake is currently in its early stages, errors may be expected! If you happen to encounter any please report <a href='https://github.com/Seniatical/Cake/Issues'>here</a>",
}

html_sidebars = {
    "**": ["sidebar-nav-bs", "search-field"]
}

html_context = {
    "github_url": "https://github.com",
    "github_user": "Seniatical",
    "github_repo": "Cake",
    "github_version": "main",
    "doc_path": "source",
    "last_updated": datetime.datetime.utcnow().strftime('%d/%m/%Y'),
}

html_static_path = ['_static']

html_title = "Cake"

suppress_warnings = [
   "image.not_readable"
]
