# -*- coding: utf-8 -*-
#
# clowder documentation build configuration file, created by
# sphinx-quickstart on Thu Oct 26 14:08:07 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
from pathlib import Path

CLOWDER_DIR = str(Path('../clowder').resolve())
sys.path.insert(0, CLOWDER_DIR)

import clowder

# -- Fix header links in markdown files -----------------------------------

clowder_yaml_syntax_reference_file = Path('clowder-yml-syntax-reference.md').resolve()
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_file.read_text()
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsprotocol", "#defaults-protocol")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultssource", "#defaults-source")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsremote", "#defaults-remote")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsbranch", "#defaults-branch")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultstag", "#defaults-tag")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultscommit", "#defaults-commit")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsgitlfs", "#defaults-git-lfs")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsgitrecursive", "#defaults-git-recursive")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsgitdepth", "#defaults-git-depth")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#defaultsgitconfig", "#defaults-git-config")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#sourcesname", "#sources-name")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#sourcesurl", "#sources-url")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#sourcesprotocol", "#sources-protocol")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsname", "#projects-name")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectssource", "#projects-source")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsbranch", "#projects-branch")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectstag", "#projects-tag")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectscommit", "#projects-commit")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectspath", "#projects-path")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsremote", "#projects-remote")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsgroups", "#projects-groups")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforkname", "#projects-fork-name")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforksource", "#projects-fork-source")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforkremote", "#projects-fork-remote")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforkbranch", "#projects-fork-branch")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforktag", "#projects-fork-tag")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsforkcommit", "#projects-fork-commit")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsgitlfs", "#projects-git-lfs")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsgitrecursive", "#projects-git-recursive")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsgitdepth", "#projects-git-depth")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsgitconfig", "#projects-git-config")
clowder_yaml_syntax_reference_contents = clowder_yaml_syntax_reference_contents.replace("#projectsfork", "#projects-fork")
with clowder_yaml_syntax_reference_file.open("w", encoding="utf-8") as f:
    f.write(clowder_yaml_syntax_reference_contents)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add Markdown support
source_parsers = {
   '.md': 'recommonmark.parser.CommonMarkParser',
}

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'clowder'
copyright = u'2017, Joe DeCapo'
author = u'Joe DeCapo'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'4.0b6'
# The full version, including alpha/beta/rc tags.
release = u'4.0b6'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
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
