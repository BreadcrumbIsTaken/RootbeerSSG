# Python Standard Library Imports
from yaml import safe_load
from glob import glob

# Module Imports
from markdown import Markdown

# Rootbeer Imports
from .utils import *
from .errors import RBContentMetadataMissingRequiredField, RBContentMissingMetadata


class RootbeerSSG:
    def __init__(self, config_file='.rbconfig',
                 content_directory='rb_content',
                 markdown_file_extention='md',
                 list_of_required_metadata_fields=['title']) -> None:
        # ===== VARIABLES =====
        self.config_file = config_file
        self.cont_dir = content_directory

        self.required_metadata_fields = list_of_required_metadata_fields

        self.content = list()

        # ===== INSTANCES =====
        # Creates a new object with the full_yaml_metadata extention already activated.
        self.md = Markdown(extensions=['full_yaml_metadata'])

        # ===== OPTIONAL VARIABLES =====
        self.md_ext = markdown_file_extention

        # ===== FUNCTION CALLS =====
        self._rb_load_config()
        self._rb_load_site_content()

    def _rb_load_config(self) -> None:
        """
        Loads the site's config. The config file can have any extention, as long as it follows YAML's syntax.
        The default file is ".rbconfig"
        """
        with open(self.config_file, 'r') as conf_file:
            # Creates the config variable for the whole class..
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
            # Assigns the file name to the item
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
                            # If all checks pass then assign the metadata to the item.
                            item['metadata'] = self.md.Meta
                else:
                    # If there is no metadata when it is required, throw and error.
                    raise RBContentMissingMetadata(f'The file, "{content_file.name}", does not contain any metadata.')

            # Finally, add the parsed content to the item.
            item['content'] = parsed_content
            # Append it to the list of content.
            self.content.append(item)
