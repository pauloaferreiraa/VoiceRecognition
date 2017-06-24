import ConfigParser

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read('config.txt')

def ConfigSectionMap(section):
    dic = {}
    options = config.options(section)
    for option in options:
        dic[option] = config.get(section,option)
    return dic