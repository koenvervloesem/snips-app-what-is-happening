#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This module contains a utility class to work with the configuration file
for the Snips skill.
"""

import ConfigParser
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    """This is a utility class to read and write the configuration file."""

    def to_dict(self):
        """Return a dict of the configuration sections and items."""
        return {section: {option_name: option
                          for option_name, option in self.items(section)}
                for section in self.sections()}

    @staticmethod
    def read_configuration_file(filename):
        """
        Read the configuration file in the parameter filename and
        return the sections and items as a dict.
        """
        with io.open(filename, encoding=CONFIGURATION_ENCODING_FORMAT) as conf:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(conf)
            return conf_parser.to_dict()

    @staticmethod
    def write_configuration_file(filename, data):
        """
        Write the dict in the parameter data to the file with
        the parameter filename as its filename."""
        conf_parser = SnipsConfigParser()
        for key in data.keys():
            conf_parser.add_section(key)
            for inner_key in data[key].keys():
                conf_parser.set(key, inner_key, data[key][inner_key])
        with open(filename, 'w') as configuration_file:
            conf_parser.write(configuration_file)
