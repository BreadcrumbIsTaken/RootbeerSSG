# Python Standard Library Imports
from glob import glob
from os import path
from datetime import datetime
from importlib import import_module
from urllib.parse import urljoin
import pathlib

# Module Imports
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader, Template, Markup
from slug import slug
from yaml import safe_load

# rootbeer Imports
from .utils import *
from .errors import *
from .signals import *
from .create_config_file import rb_create_default_config_file
from .create_default_theme import rb_create_default_theme


class RootbeerSSG:
    def __init__(self, config_file: str = '.rbconfig') -> None:
        """
        The class that genrates all the site's data and renders everything. The core or the module.

        :param config_file: The config file for your site. Uses YAML syntax. Does not have to be a .rbconfig file.
            Default: .rbconfig

        :return: None
        """

        rb_create_default_config_file(config_file)

        # ===== READ CONFIG =====
        with open(config_file, 'r') as config_f:
            self.config = safe_load(config_f.read())

        # ! Make a plugin that allow un-pretty permalinks so the date_format and pretty_permalinks params can be
        # ! Optional and make it so they are stated in a config file for the plugin to un-clutter the main class.
        # ===== MUTABLE PARAMS =====
        if 'list_of_required_metadata_fields' in self.config:
            # This just makes it so that the "title" metadata feild is required by default
            list_of_required_metadata_fields = ['title', 'date']
        if 'markdown_extentions' in self.config:
            # This makes sure that the yaml markdown extentions is installed at all times.
            markdown_extentions = {'markdown-full-yaml-metadata': 'full_yaml_metadata'}

        list_of_files_to_gen: list = [
            'plugins',
            self.config['content_directory'],
            'themes',
            f'{self.config["content_directory"]}/static',
            f'{self.config["content_directory"]}/pages',
            f'{self.config["content_directory"]}/posts',
        ]

        for file in list_of_files_to_gen:
            rb_create_path_if_does_not_exist(file)

        with open('plugins/__init__.py', 'w') as plugins_main:
            plugins_main.write('# :) hi')

        if not path.exists(f'{self.config["themes_dir"]}/RBDefault'):
            rb_create_default_theme(self.config['themes_dir'])

        # ===== GLOBAL VARIABLES =====
        self.site_title: str = self.config['site_title']
        self.pretty_p: bool = self.config['pretty_permalinks_on_posts']
        self.pretty_p_pages: bool = self.config['pretty_permalinks_on_pages']
        self.cont_dir: str = self.config['content_directory']
        self.out_dir: str = self.config['output_directory']
        self.blog_dir: str = self.config['blog_directory']
        self.theme: str = self.config['theme_name']
        self.themes_dir: str = self.config['themes_dir']
        self.date_format: str = self.config['date_format_for_content']
        self.site_url: str = self.config['url']

        self.sort_pages: str = self.config['sort_pages_by']
        self.sort_pages_reversed: bool = self.config['sort_pages_reverse']
        self.sort_posts: str = self.config['sort_posts_by']
        self.sort_posts_reversed: bool = self.config['sort_posts_reverse']

        self.required_metadata_fields: list = self.config['list_of_required_metadata_fields']
        self.md_extentions: dict = self.config['markdown_extentions']

        self.content: list = list()
        self.content_types: list = ['post', 'page']

        # ===== VARIABLES =====
        list_of_extentions_for_markdown: list = list()
        search_path: str = f'{self.themes_dir}/{self.theme}'

        if self.config['auto_install_markdown_extentions']:
            rb_install_markdown_extras_modules(self.config['markdown_extentions'].keys())

        # ===== PREPROCESSORS =====
        for ext in self.md_extentions:
            # Appends the import word into the list
            list_of_extentions_for_markdown.append(self.md_extentions[ext])

        # ===== INSTANCES =====
        # ? Creates a new object with the full_yaml_metadata extention already activated.
        self.md: Markdown = Markdown(extensions=list_of_extentions_for_markdown)
        self.env: Environment = Environment(loader=FileSystemLoader(searchpath=search_path))
        self.env.lstrip_blocks = True
        self.env.trim_blocks = True

        # ===== JINJA2 FILTERS =====
        self.env.filters['mdify'] = lambda text: Markup(self.md.convert(text))
        self.env.filters['abs_url'] = lambda url: self._rb_return_absolute_url(url)
        self.env.filters['slugify'] = lambda text: slug(text)

        # ===== PLUGIN LOADING =====
        if 'plugins' in self.config:
            list_of_plugins = [plugin for plugin in self.config['plugins']]

            for plugin in list_of_plugins:
                import_module(f'plugins.{plugin}')

        # ===== OPTIONAL VARIABLES =====
        self.md_ext: str = self.config['markdown_file_extention']

        # ===== FUNCTION CALLS =====
        rb_create_and_or_clean_path(self.out_dir)

        print(f'Generating Site. . .')

        after_content_load.send(self)

        self._rb_load_site_content()

        before_content_load.send(self)

        # ===== CONTENT SORTING =====
        self.pages: list = list()
        self.posts: list = list()
        for cont in self.content:
            if cont['metadata']['type'] == 'page':
                self.pages.append(cont)
            elif cont['metadata']['type'] == 'post':
                self.posts.append(cont)

        before_content_render.send(self)

        self._rb_render_all_content_types()

        after_content_render.send(self)

        before_render_index.send(self)

        self._rb_render_index_page()

        after_render_index.send(self)

        before_render_archive.send(self)

        self._rb_render_post_archive_page()

        after_render_archive.send(self)

        # ===== SITE GEN FINISHED =====
        print(f'Site generation complete! Your static files can be found in "{self.out_dir}/".')

    def _rb_load_site_content(self) -> None:
        """
        Loads the site's content

        :return: None
        """
        # Creates the directory that contains the markdown if it does not exist already.
        rb_create_path_if_does_not_exist(self.cont_dir)

        # Cycles through all the files in any folders in the contetn directory.
        for file in glob(f'{self.cont_dir}/**/*.{self.md_ext}', recursive=True):
            with open(file, 'r', encoding='utf-8') as content_file:
                # Parses the content and saves it to a variable.
                parsed_content: str = self.md.convert(content_file.read())

            self.item: dict = dict()
            # ? Assigns the file name to the item
            self.item['file_name'] = content_file.name

            # Checks to see if the metadata is required.
            if self.required_metadata_fields:
                # Checks to see if the content has metadata.
                if self.md.Meta:
                    # Cycles through each of the required fields.
                    for field in self.required_metadata_fields:
                        # Checks to see if the field is in the metadata or not.
                        if field not in self.md.Meta:
                            raise RBContentMetadataMissingRequiredField(
                                f'The file, "{content_file.name}", is missing the'
                                f' required metadata: {field}.')
                        else:
                            # ? If all checks pass then assign the metadata to the item.
                            self.item['metadata'] = self.md.Meta
                else:
                    # If there is no metadata when it is required, throw and error.
                    raise RBContentMissingMetadata(f'The file, "{content_file.name}", does not contain any metadata.')

            during_content_load.send(self)

            self.item['date'] = self.md.Meta['date']
            date: datetime = datetime.strptime(self.item['date'], self.date_format)
            self.item['date'] = date
            self.item['readable_date'] = date.strftime(self.date_format.replace('%H:%M', '%I:%M %p'))

            # Gets the content's slug
            item_path: str = path.splitext(path.relpath(content_file.name))[0]
            paths_to_remove: list = [f'{self.cont_dir}']
            for ct in self.content_types:
                # Addes the content types plural to the list of paths.
                # EX: content/pages
                paths_to_remove.append(f'{ct}s')
            final_path_list: list = [word for word in item_path.split('\\') if word not in paths_to_remove]
            self.item['slug'] = slug('/'.join(final_path_list))

            blog_out_dir = self.out_dir + '/' + self.blog_dir

            # Creates the content's url
            if self.item['metadata']['type'] == 'post':
                if self.pretty_p:
                    self.item['content_path_url'] = f'{blog_out_dir}/{self.item["slug"]}'
                    self.item['url'] = f'{self.blog_dir}/{self.item["slug"]}'
                else:
                    self.item[
                        'content_path_url'] = f'{blog_out_dir}/{self.item["date"].year}/' \
                                              f'{self.item["date"].month:0>2}/{self.item["date"].day:0>2}/' \
                                              f'{self.item["slug"]}'
                    self.item['url'] = f'{self.blog_dir}/{self.item["date"].year}/' \
                                       f'{self.item["date"].month:0>2}/{self.item["date"].day:0>2}/{self.item["slug"]}'

            if self.item['metadata']['type'] == 'page':
                if self.pretty_p_pages:
                    self.item['content_path_url'] = f'{self.out_dir}/{self.item["slug"]}'
                    self.item['url'] = f'{self.item["slug"]}'
                else:
                    self.item[
                        'content_path_url'] = f'{self.out_dir}/{self.item["date"].year}/' \
                                              f'{self.item["date"].month:0>2}/' \
                                              f'{self.item["date"].day:0>2}/{self.item["slug"]}'
                    self.item['url'] = f'{self.item["date"].year}/{self.item["date"].month:0>2}/' \
                                       f'{self.item["date"].day:0>2}/{self.item["slug"]}'
            # ? Finally, add the parsed content to the item.
            self.item['content'] = parsed_content

            # Append it to the list of content.
            self.content.append(self.item)

            sort_content_types: dict = dict()
            sort_content_types['page'] = dict()
            sort_content_types['post'] = dict()
            sort_content_types['page']['sort_by'] = self.sort_pages
            sort_content_types['page']['sort_reversed'] = self.sort_pages_reversed
            sort_content_types['post']['sort_by'] = self.sort_posts
            sort_content_types['post']['sort_reversed'] = self.sort_posts_reversed

            for content_type in self.content_types:
                self.content.sort(key=lambda x: sort_content_types[content_type]['sort_by'],
                                  reverse=sort_content_types[content_type]['sort_reversed'])

    def _rb_render_all_content_types(self) -> None:
        """
        Renders all the content types.

        :return: None
        """
        for item in self.content:
            template: Template = self.env.get_template(f'{item["metadata"]["type"]}.html')
            content_path = item['content_path_url']

            during_content_render.send(self)

            pathlib.Path(content_path).mkdir(parents=True, exist_ok=True)
            with open(f'{content_path}/index.html', 'w', encoding='utf-8') as file:
                file.write(
                    template.render(
                        rootbeer=self,
                        this=item,
                        config=self.config,
                    )
                )

        rb_copy_static_files_to_public_directory(self.cont_dir, self.out_dir)

    def _rb_render_index_page(self) -> None:
        """
        Renders the index page.

        :return: None
        """
        template: Template = self.env.get_template('index.html')
        with open(f'{self.out_dir}/index.html', 'w', encoding='utf-8') as index_file:
            during_render_index.send(self)

            index_file.write(
                template.render(
                    posts=self.posts,
                    pages=self.pages,
                    config=self.config,
                    rootbeer=self
                )
            )

        # pprint(self.pagination.link_map(self.config['pagination_format'],
        #                                 url=f'{self.config["url"]}/{self.blog_dir}/archive/page-$page'))

    def _rb_render_post_archive_page(self) -> None:
        template: Template = self.env.get_template('archive.html')
        # for page in range(self.pagination.page_count):
        #     page += 1
        rb_create_path_if_does_not_exist(f'{self.out_dir}/{self.blog_dir}/archive/')
        with open(f'{self.out_dir}/{self.blog_dir}/archive/index.html', 'w', encoding='utf-8') as archive:
            during_render_archive.send(self)

            archive.write(
                template.render(
                    posts=self.posts,
                    config=self.config,
                    rootbeer=self
                )
            )

    def _rb_return_absolute_url(self, rel_url: str) -> str:
        return urljoin(self.site_url, rel_url)
