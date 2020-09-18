# -*- coding: utf-8 -*-
#
# clowder documentation build configuration file, created by
# sphinx-quickstart on Thu Oct 26 14:08:07 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.

import os
import sys
from pathlib import Path

from recommonmark.transform import AutoStructify  # noqa

import clowder  # noqa


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
CLOWDER_DIR = str(Path('../clowder').resolve())
sys.path.insert(0, CLOWDER_DIR)

# -- Fix header links in markdown files -----------------------------------


# def format_markdown_headers(headers: List[str], file: str) -> str:
#     temp_file = file
#     for header in headers:
#         temp_file = temp_file.replace(f"#{header.replace('-', '')}", f"#{header}")
#     return temp_file
#
#
# toc_headers = [
#     "defaults-protocol"
# ]
#
# syntax_reference = Path('clowder-yml-syntax-reference.md').resolve()
# syntax_reference_contents = syntax_reference.read_text()
# syntax_reference_contents = format_markdown_headers(toc_headers, syntax_reference_contents)
# with syntax_reference.open("w", encoding="utf-8") as f:
#     f.write(syntax_reference_contents)


def escape_rst_file(contents: str) -> str:
    lines = contents.splitlines()
    formatted_lines = []
    for line in lines:
        if not line. startswith("---"):
            formatted_lines.append(line)
            continue
        previous_line = formatted_lines.pop()
        formatted_line = previous_line.replace(".", r"\.")
        formatted_lines.append(formatted_line)
        formatted_lines.append("-" * len(formatted_line))
    return "\n".join(formatted_lines)


def process_rst_files():
    rst_dir = Path("rst").resolve()
    rst_files = os.listdir(rst_dir)
    for rst_file in rst_files:
        path = rst_dir / rst_file
        content = path.read_text()
        output = escape_rst_file(content)
        with path.open("w", encoding="utf-8") as f:
            f.write(output)


# Escape spaces and underscores in generated rst
process_rst_files()

# -- General configuration ------------------------------------------------

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'recommonmark']

templates_path = ['_templates']

source_suffix = ['.rst', '.md']

master_doc = 'index'

project = u'clowder'
copyright = u'2017, Joe DeCapo'  # noqa
author = u'Joe DeCapo'

# The short X.Y version.
version = clowder.__version__
# The full version, including alpha/beta/rc tags.
release = clowder.__version__

language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'clowderdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'clowder.tex', u'clowder Documentation',
     u'Joe DeCapo', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'clowder', u'clowder Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'clowder', u'clowder Documentation',
     author, 'clowder', 'One line description of project.',
     'Miscellaneous'),
]


# app setup hook
def setup(app):
    app.add_config_value('recommonmark_config', {
        # 'url_resolver': lambda url: github_doc_root + url,
        # 'auto_toc_tree_section': 'Contents',
        'enable_math': False,
        'enable_inline_math': False,
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)
