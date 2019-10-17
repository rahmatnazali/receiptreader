import yaml
import datetime


def generate_yaml_filename(filename_stem):
    return "{}_{}.yaml".format(str(datetime.datetime.now()).replace(":", "."), filename_stem)


def write_yaml(object, filePointer=None):
    if filePointer is None:
        return yaml.dump(object)
    yaml.dump(object, filePointer)
