from string import Template


def replace(template, target):
    return Template(template).substitute(**target)
