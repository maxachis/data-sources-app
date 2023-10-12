import datetime
import re
import json
import ast

def convert_dates_to_strings(data_dict):
    for key, value in data_dict.items():
        if isinstance(value, datetime.date):
            data_dict[key] = value.strftime('%Y-%m-%d')
    return data_dict

def format_arrays(data_dict):
    for key, value in data_dict.items():
        if value is not None and type(value) is str:
            if re.search(r"\"?\[ ?\".*\"\ ?]\"?", value, re.DOTALL):
                data_dict[key] = json.loads(value.strip('\"'))
    return data_dict

def transform_string_array_to_array(string):
    try:
        parsed_list = ast.literal_eval(string)
        if isinstance(parsed_list, list):
            return parsed_list
        else:
            return []
    except (SyntaxError, ValueError):
        print("Invalid input. Please provide a valid string representation of a list.")
        return []