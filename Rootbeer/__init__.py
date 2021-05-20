# Python Standard Library Imports
from typing import Union, Optional
from yaml import safe_load
from glob import glob

# Module Imports
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader
from colorama import Fore

# Rootbeer Imports
from .utils import *
from .errors import *


class RootbeerSSG:
    def __init__(self,
                 site_config: Union[str, dict, None] = '.rbconfig',
                 content_directory: Optional[str] = 'rb_content',
                 output_directory: Optional[str] = 'public',
                 blog_directory: Optional[str] = 'blog',
                 markdown_file_extention: Optional[str] = 'md',
                 list_of_required_metadata_fields: Optional[list] = None,
                 markdown_extentions: Optional[dict] = None,
                 rootbeer_plugins: Optional[dict] = None
                 ) -> None:
        """
        The class that genrates all the site's data and renders everything. The core or the module.

        :param site_config: The site's config can be either a python dictionary, or YAML syntax file. Both are falid.
            TOML syntax coming soon. Default is ".rbconfig"

        :param content_directory: The directory that contains the markdown files to parse. Default is "rb_content"

        :param output_directory: The directory to export all rendered files. Default is "public"

        :param blog_directory: The directory to put all the blog folders. Can be an emptry string if you want your blog
            files to be in the root. Default is "blog"

        :param markdown_file_extention: The file extention to use for your content. Default is "md"

        :param list_of_required_metadata_fields: A list of all the required fields for content metadata. If empty or
            None, then metadata is not required. Default is "title"

        :param markdown_extentions: The extentions to use for the markdown parser. You can find all the extentions
            avaliable here: [INSERT GITHUB WIKI PAGE HERE.] The extentions will be installed automaticlly. The key is
            the install name, the value is the import name.
            Default: KEY: "markdown-full-yaml-metadata" VALUE: "full_yaml_metadata"

        :param rootbeer_plugins: A dictionary of plugins to use for changing the way RootbeerSSG functions.
            The extentions will be isntalled automaticallly. Just like the markdown plugins, the key is the insall name,
            and the value is the import name. Default: {}
        """

        # ===== MUTABLE PARAMS =====
        if list_of_required_metadata_fields is None:
            # This just makes it so that the "title" metadata feild is required by default
            list_of_required_metadata_fields = ['title']
        if markdown_extentions is None:
            # This makes sure that the yaml markdown extentions is installed at all times.
            markdown_extentions = {'markdown-full-yaml-metadata': 'full_yaml_metadata'}
        if rootbeer_plugins is None:
            # TODO!! Work on making plugins soon.
            rootbeer_plugins = {}

        # ===== GLOBAL VARIABLES =====
        self.config_file = site_config
        self.cont_dir = content_directory
        self.out_dir = output_directory
        self.blog_dir = blog_directory

        self.required_metadata_fields = list_of_required_metadata_fields
        self.md_extentions = markdown_extentions

        self.content = list()
        self.list_of_files_generated = list()

        # ===== VARIABLES =====
        list_of_extentions_for_markdown = list()

        # ===== PREPROCESSORS =====
        for ext in self.md_extentions:
            # Appends the import word into the list
            list_of_extentions_for_markdown.append(self.md_extentions[ext])

        # ===== INSTANCES =====
        # ? Creates a new object with the full_yaml_metadata extention already activated.
        self.md = Markdown(extensions=list_of_extentions_for_markdown)
        self.env = Environment(loader=FileSystemLoader(searchpath='templates/'))

        # ===== OPTIONAL VARIABLES =====
        self.md_ext = markdown_file_extention

        # ===== FUNCTION CALLS =====
        self._rb_load_config()
        self._rb_load_site_content()
        self._rb_create_and_render_index()

        # ===== SITE GEN FINISHED =====
        print(Fore.GREEN + f'Site generation {Fore.CYAN}complete!{Fore.GREEN} Your static files can be found in '
                           f'"{Fore.YELLOW}{self.out_dir}/{Fore.GREEN}"' + Fore.RESET)

    def _rb_load_config(self) -> None:
        """
        Loads the site's config. The config file can have any extention, as long as it follows YAML's syntax.
        The default file is ".rbconfig"
        """
        with open(self.config_file, 'r') as conf_file:
            # ? Creates the config variable for the whole class.
            self.config = safe_load(conf_file)

    def _rb_load_site_content(self) -> None:
        # Creates the directory that contains the markdown if it does not exist already.
        rb_create_path_if_does_not_exist(self.cont_dir)

        # Cycles through all the files in any folders in the contetn directory.
        for file in glob(f'{self.cont_dir}/**/*.{self.md_ext}', recursive=True):
            with open(file) as content_file:
                # Parses the content and saves it to a variable.
                parsed_content = self.md.convert(content_file.read())

            item = dict()
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
        template = self.env.get_template('index.html')
        rb_create_and_or_clean_path(f'{self.out_dir}')
        with open(f'{self.out_dir}/index.html', 'w') as file:
            file.write(
                template.render(
                    title=self.config['site_name'],
                    content=self.content[0]['content']
                )
            )
