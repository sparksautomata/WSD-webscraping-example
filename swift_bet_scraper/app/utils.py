NON_FILE_PATH_CHARACTERS = ["\\", "/", ":", "*", "?", '"', "<", ">", "|", " "]


def clean_string_for_filepath(string: str) -> str:
    for char in NON_FILE_PATH_CHARACTERS:
        string = string.replace(char, "_")
    return string
