import os
import configparser


class PropertiesOperations:

    @staticmethod
    def read_properties(self, section_property, name_property):
        config = configparser.RawConfigParser()
        property_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(property_dir)
        config.read(r'../Files/ConfigFile.properties')
        get_property = config.get(section_property, name_property)
        return get_property