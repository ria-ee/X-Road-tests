import os, json
import argparse
import ConfigParser


class ConfReader:
    '''
    Reads different configuration files, stores the data into a key-value list and allows getting the values from there.
    Supported configuration files:
    - ini files, keys are constructed from section name and option name, using . as a separator.
      Note: section [MAIN] means that options names are full keys (prefixes not added during parsing).
      Example INI:
        [MAIN]
        name=John
        [config]
        data=test

      Results in {'name': 'John', 'config.data': 'test'}

    - JSON files. These are directly converted to an internal dictionary, nothing else is parsed. You can use more
      complicated structures (eg. nested dictionaries) with JSON as they are parsed using internal JSON functions.

    - Files with key=value pairs on each line (empty lines are ignored)
      Example:
        name=John
        config.data=test

    - Command-line arguments
      These are directly converted to key-value pairs.
      Example: --name=John --config.data=test
    '''

    # Internal configuration dictionary
    config = {}

    class ArgumentsActionDict(argparse.Action):
        '''
        When called, returns a dictionary for ArgumentParser actions. If same keys are specified multiple times, later one
        will be used (first one is overwritten).
        '''

        @staticmethod
        def parse_config_value(val):
            '''
            Parses string values read from different sources to None, bool, int, float or string.

            Types of arguments without quotes (arg=14) or with DOUBLE quotes (arg="14") are automatically detected in this
            order: bool (True, False), int, float, str.
            To force string type, use SINGLE quotes (') around the argument.

            Examples:
            # arg becomes {'arg': True}
            # arg=None becomes {'arg': None}
            # arg="None" becomes {'arg': None}
            # arg=14 becomes {'arg': 14}
            # arg="14" becomes {'arg': 14}
            # arg='14' becomes {'arg': '14'}
            # arg=2.4 becomes {'arg': 2.4}
            # arg="2.4" becomes {'arg': 2.4}
            # arg='2.4' becomes {'arg': '2.4'}
            # arg=hello becomes {'arg': 'hello'}
            # arg="hello" becomes {'arg': 'hello'}
            # arg="hello" becomes {'arg': 'hello'}
            # arg=True becomes {'arg': True}
            # arg="True" becomes {'arg': True}
            # arg='True' becomes {'arg': 'True'}

            To use a single-quoted string as a value, surround it with another single quote on both sides. Example:
            # arg=hello becomes {'arg': 'hello'}
            # arg='hello' becomes {'arg': 'hello'}
            # arg="hello" becomes {'arg': 'hello'}
            # arg="'hello'" becomes {'arg': 'hello'}
            # arg=''hello'' becomes {'arg': '\'hello\''}

            :param val: str - value to parse
            :return: str - parsed value
            '''

            # Read True/False values
            if val is None:
                return None

            # Parse strings
            elif val == 'True':
                val = True
            elif val == 'False':
                val = False
            elif val == 'None':
                val = None
            elif val == '':
                val = None
            # Parse quoted strings
            elif val[0] == "'" and val[-1] == "'":
                val = val[1:-1]
            # For ini and key-val files where double quotes may be used
            elif val[0] == '"' and val[-1] == '"':
                val = val[1:-1]
            else:
                # Try to parse integers and floats.
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
            # Return value
            return val

        def __call__(self, parser, namespace, values, option_string=None):
            target = getattr(namespace, self.dest)
            for val in values:
                # Split key-value string to 1 or 2 element list
                sp = val.split('=', 1)
                if len(sp) == 1:
                    # Remove left dashes from key
                    key = sp[0].lstrip('-')  # Remove left dashes
                    # If one value, set the argument to be true
                    target[key] = True
                else:
                    key, val = sp
                    # Remove left dashes from key
                    key = key.lstrip('-')
                    # Set dict to value
                    target[key] = self.parse_config_value(val)

            setattr(namespace, self.dest, target)

    def clear_config(self):
        '''
        Clears the internal dictionary
        :return: None
        '''
        self.config = {}

    def set_config(self, conf):
        '''
        Appends/overwrites the internal configuration. Will not delete values that do not exist in dict conf
        :param conf: dict - dictionary with keys and values
        :return: None
        '''
        for key, value in conf.iteritems():
            self.set(key, value)

    def set(self, key, value):
        '''
        Sets a single key and value
        :param key: str - key
        :param value: arbitrary value, usually None, bool, int, float or str
        :return: None
        '''
        self.config[key] = value

    def read_command_line_arguments(self):
        '''
        Reads command-line arguments and updates configuration.
        :return: None
        '''
        parser = argparse.ArgumentParser(prefix_chars=' ')
        # Allow all arguments and parse them with ArgumentsActionDict, initialize with an empty dictionary
        parser.add_argument("options", nargs="*", action=self.ArgumentsActionDict, default={})
        # Parse the arguments
        args = parser.parse_args()
        # Save them internally
        self.set_config(args.options)

    def read_ini(self, ini_file):
        '''
        Reads an ini file.
        :param ini_file: str - path of the file to be parsed
        :return: None
        '''

        # Check if file exists. If not, the parser would fail silently.
        if not os.path.isfile(ini_file):
            raise RuntimeWarning('Configuration file not found: {0}'.format(ini_file))

        # Initialize the parser
        ini = ConfigParser.ConfigParser()

        # Read data
        ini.read(ini_file)

        # Get all sections
        sections = ini.sections()

        for section in sections:
            # Section called MAIN means no prefix so you can write full values there
            if section == 'MAIN':
                prefix = ''
            # Otherwise prefix will be "section."
            else:
                prefix = '{0}.'.format(section)

            # Get options in this section and loop over them
            options = ini.options(section)
            for option in options:
                # Generate key using our prefix (or nothing in case of MAIN)
                key = '{0}{1}'.format(prefix, option)
                # Set internal value
                self.set(key, self.ArgumentsActionDict.parse_config_value(ini.get(section, option)))

    def read_key_value_pairs(self, file):
        '''
        Read file with key=value pairs
        :param file: path of configuration file
        :return: None
        '''

        # Loop over the files
        for line in open(file, 'r'):
            # Strip extra characters and line endings
            line = line.lstrip('\t ').rstrip('\n\r\t ')

            # Split the line at first equals sign
            split_line = line.split('=', 1)
            if len(split_line) == 1:
                # Ignore key without value
                continue
            else:
                key, val = split_line
                # Remove extra whitespace from keys and values
                key = key.strip(' \t')
                val = val.strip(' \t')
                # Add the data with parsed value
                self.set(key, self.ArgumentsActionDict.parse_config_value(val))

    def read_json(self, file):
        '''
        Reads JSON file.
        :param file: path to JSON file
        :return: None
        '''
        # Open file
        with open(file) as json_file:
            # Load and parse JSON data
            data = json.load(json_file)
        # Set the configuration
        self.set_config(data)

    def get(self, key, default=None):
        '''
        Get a value using a key, or default if not found.
        :param key: str - key to look for
        :param default: default value if key is not found. None by default.
        :return: value or default value
        '''
        if key in self.config:
            return self.config[key]
        return default

    def get_string(self, key, default=''):
        '''
        Gets a string by key, or default is value is not a string.
        :param key: str - key
        :param default: str - default value
        :return: str or default value
        '''
        val = self.get(key, default)
        if isinstance(val, basestring):
            return val
        return default

    def get_int(self, key, default=0):
        '''
        Gets an integer by key, or default is value is not an integer.
        :param key: str - key
        :param default: int - default value
        :return: int or default value
        '''
        val = self.get(key, default)
        try:
            return int(val)
        except ValueError:
            return default

    def get_float(self, key, default=0.0):
        '''
        Gets a float by key, or default is value is not a float.
        :param key: str - key
        :param default: float - default value
        :return: float or default value
        '''
        val = self.get(key, default)
        try:
            return float(val)
        except ValueError:
            return default

    def get_bool(self, key, default=False):
        '''
        Gets a boolean by key, or default is value is not a boolean.
        :param key: str - key
        :param default: bool - default value
        :return: bool or default value
        '''
        val = self.get(key, default)
        if isinstance(val, bool):
            return val
        return default

    def __init__(self, default=None, init_command_line=True, ini_path=None, config_path=None, json_path=None):
        '''
        Initialize the class.
        :param default: dict | None - default configuration to load automatically
        :param init_command_line: bool - initialize with command-line arguments automatically
        :param ini_path: str | None - path to configuration INI file to be loaded automatically or None if not used
        :param config_path: str | None - path to configuration key=value pairs file to be loaded automatically or None if not used
        :param json_path: str | None - path to configuration JSON to be loaded automatically or None if not used
        '''

        # Default configuration
        if default is not None:
            self.set_config(default)

        # Init with command line arguments
        if init_command_line:
            self.read_command_line_arguments()

        # Check if ini file is set and parse the ini
        ini_file = self.get('ini', default=ini_path)
        if ini_file is not None:
            self.read_ini(ini_file)
            self.set('ini', ini_file)

        # Check if config file (key=value pairs) is set and parse it
        config_file = self.get('config', default=config_path)
        if config_file is not None:
            self.read_key_value_pairs(config_file)

        # Check if JSON config path is set and parse it
        json_file = self.get('json', default=json_path)
        if json_file is not None:
            self.read_json(json_file)

        # Init command line arguments again to override other configurations if they exist.
        # This allows the user to specify a full configuration file and override just some of the set parameters on
        # the command line.
        if init_command_line and (ini_file is not None or config_file is not None or json_file is not None):
            self.read_command_line_arguments()
