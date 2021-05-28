# Python Standard Library Imports
from typing import Optional
from glob import glob
from os import path
from datetime import datetime
import pathlib

# Module Imports
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader, Template
from slug import slug

# rootbeer Imports
from .utils import *
from .errors import *


class RootbeerSSG:
    def __init__(self,
                 site_title: Optional[str] = 'RootbeerSSG!',
                 pretty_permalinks_on_blog_posts: bool = False,
                 pretty_permalinks_on_pages: bool = True,
                 sort_posts_by: Optional[str] = 'date',
                 sort_pages_by: Optional[str] = 'title',
                 sort_posts_reverse: bool = True,
                 sort_pages_reverse: bool = False,
                 date_format_for_content='%m/%d/%y at %H:%M',
                 content_directory: Optional[str] = 'rb_content',
                 output_directory: Optional[str] = 'public',
                 blog_directory: Optional[str] = 'blog',
                 theme_name: Optional[str] = 'RBDefault',
                 markdown_file_extention: Optional[str] = 'md',
                 list_of_required_metadata_fields: Optional[list] = None,
                 markdown_extentions: Optional[dict] = None,
                 log_rootbeer_steps: bool = True,
                 ) -> None:
        """
        The class that genrates all the site's data and renders everything. The core or the module.

        :param site_title: The title for your site. Default is "RootbeerSSG!"

        :param pretty_permalinks_on_blog_posts: Do not add the date the post was written to the post's url.
            Default is "False"

        :param pretty_permalinks_on_pages: Do not add the date the page was written to the page's url.
            Default is "True"

        :param sort_posts_by: How to sort the posts. The options are determined by the content's metadata.
            Default is "date"

        :param sort_pages_by: How to sort the pages. The options are determined by the content's metadata.
            Default is "title"

        :param sort_posts_reverse: Sort the posts reverse or not. Default is "True". Works best if you sort by date.

        :param sort_pages_reverse: Sort the pages reverse or not. Default is "False".

        :param date_format_for_content: The way to format the date of the content. Uses the % time formatting notation.
            Default is "%m/%d/%y at %H:%M", meaning "mm/dd/yy at H:M."
            example: "5/20/21 at 13:57" will be parsed as "5/20/21 at 1:37 PM"

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
        """

        # ! Make a plugin that allow un-pretty permalinks so the date_format and pretty_permalinks params can be
        # ! Optional and make it so they are stated in a config file for the plugin to un-clutter the main class.
        # ===== MUTABLE PARAMS =====
        if list_of_required_metadata_fields is None:
            # This just makes it so that the "title" metadata feild is required by default
            list_of_required_metadata_fields = ['title', 'date']
        if markdown_extentions is None:
            # This makes sure that the yaml markdown extentions is installed at all times.
            markdown_extentions = {'markdown-full-yaml-metadata': 'full_yaml_metadata'}

        # ===== GLOBAL VARIABLES =====
        self.site_title: str = site_title
        self.pretty_p: bool = pretty_permalinks_on_blog_posts
        self.pretty_p_pages: bool = pretty_permalinks_on_pages
        self.cont_dir: str = content_directory
        self.out_dir: str = output_directory
        self.blog_dir: str = blog_directory
        self.theme: str = theme_name
        self.themes_dir: str = 'themes'
        self.date_format: str = date_format_for_content

        self.sort_pages: str = sort_pages_by
        self.sort_pages_reversed: bool = sort_pages_reverse
        self.sort_posts: str = sort_posts_by
        self.sort_posts_reversed: bool = sort_posts_reverse

        self.required_metadata_fields: list = list_of_required_metadata_fields
        self.md_extentions: dict = markdown_extentions

        self.content: list = list()
        self.list_of_files_generated: list = list()
        self.content_types: list = ['post', 'page']

        self.log_steps = log_rootbeer_steps

        # ===== VARIABLES =====
        list_of_extentions_for_markdown: list = list()
        search_path: str = f'{self.themes_dir}/{self.theme}'

        # ===== PREPROCESSORS =====
        for ext in self.md_extentions:
            # Appends the import word into the list
            list_of_extentions_for_markdown.append(self.md_extentions[ext])

        if self.log_steps:
            f'{Fore.MAGENTA}Installing markdown extentions. . .{Fore.RESET}'
        rb_install_markdown_extras_modules(markdown_extentions.keys())
        if self.log_steps:
            print(f'{Fore.GREEN}Markdown extentions installed!{Fore.RESET}')

        # ===== INSTANCES =====
        # ? Creates a new object with the full_yaml_metadata extention already activated.
        self.md: Markdown = Markdown(extensions=list_of_extentions_for_markdown)
        self.env: Environment = Environment(loader=FileSystemLoader(searchpath=search_path))

        # ===== OPTIONAL VARIABLES =====
        self.md_ext: str = markdown_file_extention

        # ===== FUNCTION CALLS =====
        rb_create_and_or_clean_path(self.out_dir)
        self._rb_load_site_content()
        self._rb_render_all_content_types()

        # ===== SITE GEN FINISHED =====
        print(Fore.GREEN + f'Site generation {Fore.CYAN}complete!{Fore.GREEN} Your static files can be found in '
                           f'"{Fore.YELLOW}{self.out_dir}/{Fore.GREEN}".' + Fore.RESET)

    def _rb_load_site_content(self) -> None:
        # Creates the directory that contains the markdown if it does not exist already.
        rb_create_path_if_does_not_exist(self.cont_dir)
        if self.log_steps:
            print(f'{Fore.LIGHTYELLOW_EX}Generating Site. . .')

        # Cycles through all the files in any folders in the contetn directory.
        for file in glob(f'{self.cont_dir}/**/*.{self.md_ext}', recursive=True):
            with open(file) as content_file:
                if self.log_steps:
                    print(f'{Fore.LIGHTCYAN_EX}Reading "{path.basename(content_file.name)}". . .' + Fore.RESET)
                # Parses the content and saves it to a variable.
                parsed_content: str = self.md.convert(content_file.read())
                if self.log_steps:
                    print(f'{Fore.GREEN}"{path.basename(content_file.name)}" has been read!' + Fore.RESET)

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

            item['date'] = self.md.Meta['date']
            date: datetime = datetime.strptime(item['date'], self.date_format)
            item['date'] = date
            item['readable_date'] = date.strftime(self.date_format.replace('%H:%M', '%I:%M %p'))

            # Gets the content's slug
            item_path: str = path.splitext(path.relpath(content_file.name))[0]
            paths_to_remove: list = [f'{self.cont_dir}']
            for ct in self.content_types:
                # Addes the content types plural to the list of paths.
                # EX: content/pages
                paths_to_remove.append(f'{ct}s')
            final_path_list: list = [word for word in item_path.split('\\') if word not in paths_to_remove]
            item['slug'] = slug('/'.join(final_path_list))

            blog_out_dir = self.out_dir + '/' + self.blog_dir

            # Creates the content's url
            if item['metadata']['type'] == 'post':
                if self.pretty_p:
                    item['url'] = f'{blog_out_dir}/{item["slug"]}'
                else:
                    item['url'] = f'{blog_out_dir}/{item["date"].year}/{item["date"].month:0>2}/{item["date"].day:0>2}' \
                                  f'/{item["slug"]}'

            if item['metadata']['type'] == 'page':
                if self.pretty_p_pages:
                    item['url'] = f'{self.out_dir}/{item["slug"]}'
                else:
                    item['url'] = f'{self.out_dir}/{item["date"].year}/{item["date"].month:0>2}/' \
                                  f'{item["date"].day:0>2}/{item["slug"]}'

            # ? Finally, add the parsed content to the item.
            item['content'] = parsed_content
            # Append it to the list of content.
            self.content.append(item)

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
        for item in self.content:
            template: Template = self.env.get_template(f'{item["metadata"]["type"]}.html')
            content_path = item['url']

            if self.log_steps:
                print(f'{Fore.YELLOW}Rendering "{item["slug"]}". . .')

            pathlib.Path(content_path).mkdir(parents=True, exist_ok=True)
            with open(f'{content_path}/index.html', 'w') as file:
                file.write(
                    template.render(
                        this=item,
                        site_title=self.site_title
                    )
                )

            if self.log_steps:
                print(f'{Fore.GREEN}Rendered "{item["slug"]}"!')

        rb_copy_static_files_to_public_directory(self.cont_dir, self.out_dir, self.log_steps)
