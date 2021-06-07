from os import path

config_file_defualt_contents = '''
# ===== NOTE =====
# ALL URLS AND FOLDER DIRS SHOULD NOT HAVE A TRAILING SLASH.
# DO:
# https://example.com
# public
# DON'T:
# https://example.com/
# public/
# The urls and directories won't be generated correctly.

site_title: RootbeerSSG!

url: http://localhost:8000

pretty_permalinks_on_posts: true
pretty_permalinks_on_pages: false

sort_posts_by: date
sort_pages_by: title

sort_posts_reverse: false
sort_pages_reverse: true

date_format_for_content: "%m/%d/%y at %H:%M"

content_directory: content
output_directory: public
blog_directory: blog

themes_dir: themes
theme_name: RBDefault

# The file extentions for your markdown files. DO NOT HAVE A . AT THE FRONT
markdown_file_extention: md

list_of_required_metadata_fields:
  - title
  - date

markdown_extentions:
  # The first value is the extentions's install name.
  # The second value is the extention's import name.
  # If you are doing a built in markdown extention, then just do ~, null, or markdown
  # Example:
  # ~: fenced_code
  markdown-full-yaml-metadata: full_yaml_metadata
auto_install_markdown_extentions: false
'''


def rb_create_default_config_file(config_file) -> None:
    if not path.exists(config_file):
        with open(config_file, 'w') as file:
            file.write(config_file_defualt_contents)