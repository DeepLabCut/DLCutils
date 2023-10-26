import yaml


def read_config(config_path: str) -> dict:
    """
    Reads structured config file defining a project.

    :param config_path: path to config file
    """

    try:
        with open(config_path, "r") as ymlfile:
            config_file = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        raise (
            "Could not find the config file at "
            + config_path
            + " \n Please make sure the path is correct and the file exists"
        )

    return config_file
