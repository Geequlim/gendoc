# -*- coding: utf-8 -*-
# import os
import sphinx_rtd_theme
from recommonmark.parser import CommonMarkParser

needs_sphinx = '1.4'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    # 'sphinx.ext.mathjax',
    'breathe'
]

breathe_projects = {"${project}": "${build_dir}/doxygen/xml/"}
breathe_default_project = "${project}"
breathe_domain_by_extension = {
    "h": "cpp",
    "hpp": "cpp",
}
breathe_default_members = ('members', 'undoc-members', 'protected-members')
breathe_implementation_filename_extensions = ['.c', '.cc', '.cpp', 'cxx']

templates_path = ['_templates']

source_parsers = {
    '.md': CommonMarkParser,
}
source_suffix = ['.rst', '.md']
source_encoding = 'utf-8-sig'
master_doc = 'index'

# General information about the project.
project = u'${project}'
copyright = u'2016, ${author}'
author = u'${author}'

# The short X.Y version.
version = u'${version}'
# The full version, including alpha/beta/rc tags.
release = u'${version}'

language = None
exclude_patterns = ['${build_dir}', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output --
html_theme = "sphinx_rtd_theme"
html_theme_path = ["_themes", sphinx_rtd_theme.get_html_theme_path()]
html_context = {
    'css_files': ['_static/style.css'],
}
html_title = u'${project} v${version}'
# html_short_title = None
# html_logo = None
# html_favicon = None
#
# The empty string is equivalent to '%b %d, %Y'.
# html_last_updated_fmt = None
# A file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# Output file base name for HTML help builder.
htmlhelp_basename = '${project}doc'
# html_extra_path = []

# -- Options for LaTeX output --
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

# Grouping the document tree into LaTeX files.
latex_documents = [
    (master_doc, '${project}.tex', u'${project} Documentation',
     u'${author}', 'manual'),
]

# The name of an image file (relative to this directory)
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#
# latex_use_parts = False

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# If false, no module index is generated.
#
# latex_domain_indices = True

# -- Options for manual page output --
# One entry per manual page. List of tuples
man_pages = [
    (master_doc, '${project}', u'${project} Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False

# -- Options for Texinfo output --
# Grouping the document tree into Texinfo files.
texinfo_documents = [
    (master_doc, '${project}', u'${project} Documentation',
     author, '${project}', 'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# -- Options for Epub output --
# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# The basename for the epub file. It defaults to the project name.
# epub_basename = project

# The HTML theme for the epub output.
# epub_theme = 'epub'

# The language of the text.
# epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
# epub_scheme = ''

# The unique identifier of the text. This can be a ISBN or homepage.
# epub_identifier = ''

# A unique identification for the text.
# epub_uid = ''

# A tuple containing the cover image and cover page html template filenames.
# epub_cover = ()

# A sequence of (type, uri, title) tuples for the guide element of content.opf.
# epub_guide = ()

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_pre_files = []

# HTML files that should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
# epub_post_files = []

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# The depth of the table of contents in toc.ncx.
# epub_tocdepth = 3

# Allow duplicate toc entries.
# epub_tocdup = True

# Choose between 'default' and 'includehidden'.
# epub_tocscope = 'default'

# Fix unsupported image types using the Pillow.
# epub_fix_images = False

# Scale large images.
# epub_max_image_width = 0

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# epub_show_urls = 'inline'

# If false, no index is generated.
# epub_use_index = True

def setup(app):
    app.add_stylesheet('_static/style.css')
