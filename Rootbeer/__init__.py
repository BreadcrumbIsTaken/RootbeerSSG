# Python Standard Library Imports
from typing import Optional
from glob import glob
from os import path

# Module Imports
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader, Template
from colorama import Fore

# Rootbeer Imports
from .utils import *
from .errors import *


class RootbeerSSG:
    def __init__(self,
                 site_title: Optional[str] = 'RootbeerSSG!',
                 pretty_permalinks_on_blog_posts: bool = True,
                 sort_posts_by: Optional[str] = 'date',
                 sort_pages_by: Optional[str] = 'title',
                 sort_posts_reverse: bool = True,
                 sort_pages_reverse: bool = False,
                 date_format_for_content='%D at %I:%M %r',
                 content_directory: Optional[str] = 'rb_content',
                 output_directory: Optional[str] = 'public',
                 blog_directory: Optional[str] = 'blog',
                 templates_directory: Optional[str] = 'templates',
                 theme_name: Optional[str] = 'RBDefault',
                 markdown_file_extention: Optional[str] = 'md',
                 list_of_required_metadata_fields: Optional[list] = None,
                 markdown_extentions: Optional[dict] = None,
                 rootbeer_plugins: Optional[dict] = None,
                 log_rootbeer_steps: bool = True,
                 ) -> None:
        """
        The class that genrates all the site's data and renders everything. The core or the module.

        :param site_title: The title for your site. Default is "RootbeerSSG!"

        :param pretty_permalinks_on_blog_posts: Do not add the date the post was written to the post's url.
            Default is "True"

        :param sort_posts_by: How to sort the posts. The options are determined by the content's metadata.
            Default is "date"

        :param sort_pages_by: How to sort the pages. The options are determined by the content's metadata.
            Default is "title"

        :param sort_posts_reverse: Sort the posts reverse or not. Default is "True". Works best if you sort by date.

        :param sort_pages_reverse: Sort the pages reverse or not. Default is "False".

        :param date_format_for_content: The way to format the date of the content. Uses the % time formatting notation.
            Default is "%D at %I:%M %r", meaning "mm/dd/yy at H:M a.m./p.m."
            example: "5/20/21 at 11:57 a.m."

        :param content_directory: The directory that contains the markdown files to parse. Default is "rb_content"

        :param output_directory: The directory to export all rendered files. Default is "public"

        :param blog_directory: The directory to put all the blog folders. Can be an emptry string if you want your blog
            files to be in the root. Default is "blog"

        :param markdown_file_extention: The file extention to use for your content. Default is "md"

        :param list_of_required_metadata_fields: A list of all the required fields for content metadata. If empty or
            None, then metadata is not required. Default is ["title", "date"]

        :param markdown_extentions: The extentions to use for the markdown parser. You can find all the extentions
            avaliable here: [INSERT GITHUB WIKI PAGE HERE.] The extentions will be installed automaticlly. The key is
            the install name, the value is the import name.
            Default: KEY: "markdown-full-yaml-metadata" VALUE: "full_yaml_metadata"

        :param rootbeer_plugins: A dictionary of plugins to use for changing the way Rootbeer-SSG functions.
            The extentions will be isntalled automaticallly. Just like the markdown plugins, the key is the insall name,
            and the value is the import name. Default: {}
        """

        #! Make a plugin that allow un-pretty permalinks so the date_format and pretty_permalinks params can be
        #! Optional and make it so they are stated in a config file for the plugin to un-clutter the main class.
        # ===== MUTABLE PARAMS =====
        if list_of_required_metadata_fields is None:
            # This just makes it so that the "title" metadata feild is required by default
            list_of_required_metadata_fields = ['title', 'date']
        if markdown_extentions is None:
            # This makes sure that the yaml markdown extentions is installed at all times.
            markdown_extentions = {'markdown-full-yaml-metadata': 'full_yaml_metadata'}
        if rootbeer_plugins is None:
            # TODO!! Work on making plugins soon.
            rootbeer_plugins = {}

        # ===== GLOBAL VARIABLES =====
        self.site_title: str = site_title
        self.pretty_permalinks: bool = pretty_permalinks_on_blog_posts
        self.cont_dir: str = content_directory
        self.out_dir: str = output_directory
        self.blog_dir: str = blog_directory
        self.theme: str = theme_name
        self.template_dir: str = templates_directory

        self.required_metadata_fields: list = list_of_required_metadata_fields
        self.md_extentions: dict = markdown_extentions

        self.content: list = list()
        self.list_of_files_generated: list = list()
        self.content_types: list = ['post', 'page']

        # ===== VARIABLES =====
        list_of_extentions_for_markdown: list = list()
        search_path: str = f'{self.template_dir}/{self.theme}'

        # ===== PREPROCESSORS =====
        for ext in self.md_extentions:
            # Appends the import word into the list
            list_of_extentions_for_markdown.append(self.md_extentions[ext])

        # ===== INSTANCES =====
        # ? Creates a new object with the full_yaml_metadata extention already activated.
        self.md: Markdown = Markdown(extensions=list_of_extentions_for_markdown)
        self.env: Environment = Environment(loader=FileSystemLoader(searchpath=search_path))

        # ===== OPTIONAL VARIABLES =====
        self.md_ext: str = markdown_file_extention

        # ===== FUNCTION CALLS =====
        self._rb_load_site_content()
        self._rb_create_and_render_index()

        # ===== SITE GEN FINISHED =====
        print(Fore.GREEN + f'Site generation {Fore.CYAN}complete!{Fore.GREEN} Your static files can be found in '
                           f'"{Fore.YELLOW}{self.out_dir}/{Fore.GREEN}"' + Fore.RESET)

    def _rb_load_site_content(self) -> None:
        # Creates the directory that contains the markdown if it does not exist already.
        rb_create_path_if_does_not_exist(self.cont_dir)
        print(f'{Fore.LIGHTYELLOW_EX}Generating Site. . .')

        # Cycles through all the files in any folders in the contetn directory.
        for file in glob(f'{self.cont_dir}/**/*.{self.md_ext}', recursive=True):
            with open(file) as content_file:
                print(f'{Fore.LIGHTCYAN_EX}Reading "{path.basename(content_file.name)}". . .')
                # Parses the content and saves it to a variable.
                parsed_content: str = self.md.convert(content_file.read())
                print(f'{Fore.WHITE}"{path.basename(content_file.name)}" has been read!')

            item: dict = dict()
            # ? Assigns the file name to the item
            item['file_name'] = content_file.name

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
                            item['metadata'] = self.md.Meta
                else:
                    # If there is no metadata when it is required, throw and error.
                    raise RBContentMissingMetadata(f'The file, "{content_file.name}", does not contain any metadata.')

            # ? Finally, add the parsed content to the item.
            item['content'] = parsed_content
            # Append it to the list of content.
            self.content.append(item)

    def _rb_create_and_render_index(self) -> None:
        template: Template = self.env.get_template('index.html')
        rb_create_and_or_clean_path(f'{self.out_dir}')
        print(self.content[0])
        with open(f'{self.out_dir}/index.html', 'w') as file:
            file.write(
                template.render(
                    title=self.site_title,
                    content=self.content[0]['content'],
                    meta=self.content[0]['metadata']
                )
            )
