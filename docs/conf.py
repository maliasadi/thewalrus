#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Strawberry Fields documentation build configuration file, created by
# sphinx-quickstart on Fri Sep  8 14:44:21 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os, re
import inspect
import numba
from unittest.mock import MagicMock

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('_ext'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('.')), 'docs'))

#-------------------------------------------------------------------------
# Mock out all modules that aren't required for compiling of documentation
class Mock(MagicMock):
    __name__ = 'foo'

    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

class TypeMock(type):
    pass

MOCK_MODULES = [
    'cython',
    'thewalrus.libwalrus',
    ]

mock = Mock()
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.5'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    # 'sphinx.ext.imgmath',
    'sphinx.ext.napoleon',
    # 'sphinx.ext.inheritance_diagram',
    'sphinx.ext.viewcode',
    'sphinxcontrib.bibtex',
    'edit_on_github',
    'nbsphinx',
    'breathe',
    'exhale',
    'sphinx_copybutton'
]

bibtex_bibfiles = ['references.bib']

autosummary_generate = True
autosummary_imported_members = False

exclude_patterns = ['_build', '**.ipynb_checkpoints']
nbsphinx_execute = 'never'
nbsphinx_epilog = """
.. note:: :download:`Click here <../{{env.docname}}.ipynb>` to download this gallery page as an interactive Jupyter notebook.
"""

# Setup the breathe extension
breathe_projects = {
    "libwalrus C++": "./doxyoutput/xml"
}

breathe_default_project = "libwalrus C++"
breathe_domain_by_extension = {"hpp" : "cpp"}

# Setup the exhale extension
exhale_args = {
    # These arguments are required
    "containmentFolder":     "./libwalrus_cpp_api",
    "rootFileName":          "library_root.rst",
    "rootFileTitle":         "C++ Library API",
    "doxygenStripFromPath":  "..",
    # Suggested optional arguments
    "createTreeView":        True,
    # TIP: if using the sphinx-bootstrap-theme, you need
    # "treeViewIsBootstrap": True,
    "exhaleExecutesDoxygen": True,
    "exhaleDoxygenStdin":    "INPUT = ../include/stdafx.h ../include/libwalrus.hpp ../include/version.hpp ../include/eigenvalue_hafnian.hpp ../include/recursive_hafnian.hpp ../include/repeated_hafnian.hpp ../include/permanent.hpp ../include/hermite_multidimensional.hpp ../include/powtrace.hpp",
    # "exhaleUseDoxyfile": True
}

mathjax_path = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-MML-AM_CHTML"
nbsphinx_requirejs_path = ""

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates', 'xanadu_theme']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'The Walrus'
copyright = '2019, Xanadu Quantum Technologies Inc'
author = 'Xanadu Inc.'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version, including alpha/beta/rc tags.
import thewalrus
release = thewalrus.version()

# The short X.Y version.
version = re.match(r'^(\d+\.\d+)', release).expand(r'\1')

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%Y-%m-%d'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'nature'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
#html_sidebars = {
#    '**': [
#        'about.html',
#        'navigation.html',
#        'relations.html',  # needs 'show_related': True theme option to display
#        'searchbox.html',
#        'donate.html',
#    ]
#}
html_sidebars = {
    '**' : [
        'logo-text.html',
        'searchbox.html',
        'globaltoc.html',
        # 'sourcelink.html'
    ]
}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'thewalrusdoc'

# # -- Xanadu theme ---------------------------------------------------------
html_theme = 'xanadu_theme'
html_theme_path = ['.']

# Register the theme as an extension to generate a sitemap.xml
# extensions.append("guzzle_sphinx_theme")

# xanadu theme options (see theme.conf for more information)
html_theme_options = {
    # Set the path to a special layout to include for the homepage
    # "homepage": "special_index.html",

    # Set the name of the project to appear in the left sidebar.
    "project_nav_name": "The Walrus",
    "touch_icon": "_static/logo_new.png",

    # Set GA account ID to enable tracking
    "google_analytics_account": "UA-116279123-2",

    # colors
    "navigation_button": "#3a8ab1",
    "navigation_button_hover": "#2b5071",
    "toc_caption": "#2C96CC",
    "toc_hover": "#2C96CC",
    "table_header_bg": "#ffdce5",
    "table_header_border": "#2C96CC",
    "download_button": "#2C96CC",
}

edit_on_github_project = 'XanaduAI/thewalrus'
edit_on_github_branch = 'master/docs'

from custom_directives import CustomGalleryItemDirective


def process_numba_signature(app, what, name, obj, options, signature, return_annotation):
    if isinstance(obj, numba.core.registry.CPUDispatcher):
        original = obj.py_func
        orig_sig = inspect.signature(original)

        if (orig_sig.return_annotation) is inspect._empty:
            ret_ann = None
        else:
            ret_ann = orig_sig.return_annotation.__name__

        return (str(orig_sig), ret_ann)

    return (signature, return_annotation)


def setup(app):
    app.connect('autodoc-process-signature', process_numba_signature)
    app.add_directive('customgalleryitem', CustomGalleryItemDirective)
    app.add_css_file('xanadu_gallery.css')
