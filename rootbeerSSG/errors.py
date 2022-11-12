class RBContentMetadataMissingRequiredField(Exception):
    """
    Gets thrown if the content is missing the metadata specified in the list of required metadata fields when
    initiating a new rootbeer object.
    """
    pass


class RBContentMissingMetadata(Exception):
    """
    Gets thrown if the content is missing metadata. Will only be thrown if the file does not have any metadata and if
    there are any items in the list of required metadata fields when initilizing a new rootbeer object.
    """
    pass