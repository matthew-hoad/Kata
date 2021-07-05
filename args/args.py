import sys, string

ARG_SCHEMA = {
    "name": {
        "type": str
    },
    "type": {
        "type": [
            str,
            int,
            bool,
            float
        ]
    },
    "description": {
        "type": str
    },
    "default":{
        "type": [
            str,
            int,
            bool,
            float,
            type(None)
        ]
    }
}

args_schema = [
    {
        "name": "l",
        "type": bool,
        "description": "Boolean: flag to denote that logging should be enabled",
        "default": False
    },
    {
        "name": "p",
        "type": int,
        "description": "Integer: port number to use",
        "default": 80
    },
    {
        "name": "d",
        "type": str,
        "description": "String: path to save logs to",
        "default": None
    }
]

class ArgParser:
    """
    Utility class for parsing arguments against a given schema.
    The schema in question must match that of ARG_SCHEMA

    Attributes
    ----------
    schema : list of dicts
        The schema of the arguments to be parsed
    
    Usage
    -----
    ```python
    >>>myparser = ArgParser(myschema)
    >>>myparser.parse_args(sys.argv[1:])
    >>>print(myparser.get_arg_value("my_arg_name"))
    'myargvalue'
    >>>
    ```

    """
    def __init__(self, args_schema):
        """
        Parameters
        ----------
        args_schema : list of dicts
        """
        self.schema = args_schema
        self._used_names = []
        for sub_schema in self.schema:
            self._validate_schema(sub_schema)
        self._values = {}

    def help(self, arg_name):
        """
        Get info on the arg with name `arg_name` as provided in `arg_schema`

        Parameters
        ----------
        arg_name : str
            The name of the arg to get info about
        """
        if arg_name in [i['name'] for i in self.schema]:
            argument = [i for i in self.schema if arg_name==i['name']][0]
            return argument['description']
        else:
            raise KeyError(f"Arg with name {arg_name} does not exist.")

    def _validate_schema(self, sub_schema):
        # if the sub_schema has a name property
        # and that arg hasn't already been defined
        # then add that to _used_names
        if 'name' in sub_schema.keys():
            if sub_schema['name'] not in self._used_names:
                self._used_names.append(sub_schema['name'])
            else:
                raise KeyError(f"An arg schema with the name {sub_schema['name']} already exists!")
        else:
            raise Exception(f"Schema does not have a name property")
        # iterate over each key in ARG_SCHEMA
        for k, v in ARG_SCHEMA.items():
            if k not in sub_schema.keys():
                raise KeyError(f"Arg property {k} not in schema with name")
            if type(v['type']) == list:
                if k == "default":
                    if not any([isinstance(sub_schema[k], vtype) for vtype in v['type']]):
                        raise TypeError(f"Arg property {k} in schema with name {sub_schema['name']} is an invalid type. Expected one of {str(v['type'])} but got {sub_schema[k]}")
                elif k == "type":
                    if sub_schema[k] not in v['type']:
                        raise TypeError(f"Arg property {k} in schema with name {sub_schema['name']} is an invalid type. Expected one of {str(v['type'])} but got {sub_schema[k]}")
            else:
                if not isinstance(sub_schema[k], v['type']):
                    raise TypeError(f"Arg property {k} in schema with name {sub_schema['name']} is an invalid type. Expected {v['type']} but got {type(sub_schema[k])}")

    def _check_argument_is_arg(self, argument):
        """
        Used for checking if the next `argument` is an arg or a value.

        Parameters
        ----------
        argument : str
            The value to check
        
        Outputs
        -------
        result : bool
            True if the next argument is a valid format for an arg
            Otherwise, False
        """
        # check if argument begins with a "-" and is 2 characters long
        if argument[0] == "-" and len(argument) == 2:
            arg_name = argument[1]
            #check that the second character is a letter
            if arg_name in string.ascii_lowercase + string.ascii_uppercase:
                return True
        return False

    def parse_args(self, arguments):
        """
        Parse the `arguments` list given the defined `args_schema`

        Parameters
        ----------
        arguments : list of str
            The arguments, most likely from `sys.argv[1:]`, to be parsed
        
        Outputs
        -------
        None - sets properties of `_values` which can be read using `get_value(arg_name)`
        """
        while len(arguments) > 0:
            if self._check_argument_is_arg(arguments[0]):
                arg_name = arguments[0][1]
                # check that the letter matches one of the named arguments in the schema
                arg_schema = [i for i in self.schema if arg_name==i['name']]
                if len(arg_schema) == 1:
                    # if there was a match, then check against the schema for type
                    # as that will determine how we get the value
                    arg_schema = arg_schema[0]
                    # if the type is bool
                    if arg_schema['type'] == bool:
                        self._values[arg_name] = True
                        arguments.pop(0)
                    # if the type is int or float
                    elif arg_schema['type'] in [int, float]:
                        # check if there is another element in the arg list before naively trying to use it
                        if len(arguments) == 1:
                            raise Exception(f"Expected a value to follow arg {arg_name}")
                        # check that the next value in arguments is not another arg, but a value
                        if not self._check_argument_is_arg(arguments[1]):
                            try:
                                # set the value using the next argument
                                arg_value = arg_schema['type'](arguments[1])
                                self._values[arg_name] = arg_value
                                # remove the argument and the value from the so
                                # that they're not processed again
                                arguments.pop(0)
                                arguments.pop(0)
                            except TypeError as te:
                                raise TypeError(f"Invalid type for argument '{arg_name}''. Could not convert str value to {str(arg_schema['type'])}.")
                        else:
                            raise Exception(f"Tried to parse {str(arg_schema['type'])} value for arg '{arg_name}' but got another arg instead.")
                    # if the type is str
                    elif arg_schema['type'] == str:
                        # check if there is another element in the arg list before naively trying to use it
                        if len(arguments) == 1:
                            raise Exception(f"Expected a value to follow arg {arg_name}")
                        # set the value using the next argument
                        self._values[arg_name] = arguments[1]
                        # remove the argument and the value from the so
                        # that they're not processed again
                        arguments.pop(0)
                        arguments.pop(0)

                elif len(arg_schema) == 0:
                    raise Exception(f"Unknown argument {arg_name}.")
                elif len(arg_schema) > 1:
                    raise Exception(
                        f"Please review arg_schema as there are multiple args defined for the same name. "+
                        "This should not happen but it seems to have happened anyway."
                    )
            else:
                raise Exception(f"Format incorrect for named argument. Name must be a single letter")
        for sub_schema in self.schema:
            if sub_schema['name'] not in self._values.keys():
                if sub_schema['default'] is None:
                    raise Exception(f"A value must be provided for argument {sub_schema['name']} as no default is specified.")
                self._values[sub_schema['name']] = sub_schema['default']

    def get_arg_value(self, arg_name):
        """
        Return the value of the arg with name `arg_name`

        Parameters
        ----------
        arg_name : str
            The name of the arg to retrieve the value of
        
        Outputs
        -------
        result : Any of [int, str, bool, float]
        """
        if arg_name in self._values.keys():
            return self._values[arg_name]
        else:
            raise KeyError(f"Arg with name {arg_name} does not exist")

if __name__ == "__main__":
    print(str(sys.argv))
    arg_parser = ArgParser(args_schema)
    arguments = sys.argv[1:]
    arg_parser.parse_args(arguments)
    for k in arg_parser._values.keys():
        print(f"arg: {k} value: {arg_parser.get_arg_value(k)}\nDescription: {arg_parser.help(k)}\n")
