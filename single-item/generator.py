import json 

def checkAllTypes(checkList):
    first_type = type(checkList[0])

    for item in checkList:
        if not isinstance(item, first_type):
            return False
    
    return True 

def CapitalCase(string):
    delimiters = [" ", "_", "-"]
    words = [string]

    for char in delimiters:
        new_words = []
        for word in words:
            new_words += word.split(char)
        words = new_words

    for ind, word in enumerate(words):
        words[ind] = word.capitalize()

    return ''.join(words)

def json_to_schema(data, schemaType="mainType"):
    keys = list(data.keys())

    generated_data = {}
    output_schema = ""

    for key in keys:
        value = data[key]
        if isinstance(value, str):
            generated_data[key] = "String"
        elif isinstance(value, bool):
            generated_data[key] = "Boolean"
        elif isinstance(value, int):
            generated_data[key] = "Int"
        elif isinstance(value, dict):
            if len(value) > 0:
                generated_data[key] = CapitalCase(key)
                output_schema += json_to_schema(data[key], schemaType=generated_data[key])
            else:
                print("Empty dictionary. Skipping due to Unexpected Behaviour")
        elif isinstance(value, list):
            if len(value) > 0:
                if not checkAllTypes(value):
                    print("Types in the list should be of the same type")
                    exit(0)

                firstval = value[0]
                if isinstance(firstval, str):
                    generated_data[key] = "[String]"
                elif isinstance(firstval, bool):
                    generated_data[key] = "[Boolean]"
                elif isinstance(firstval, int):
                    generated_data[key] = "[Int]"
                elif isinstance(firstval, dict):
                    new_dict = {}
                    for item in value:
                        for _key in item.keys():
                            if _key not in new_dict:
                                new_dict[_key] = item[_key]
                            else:
                                if not isinstance(new_dict[_key], type(item[_key])):
                                    print("Bad input, conflicting types. Unexpected Behaviour")
                                    exit(0)

                    generated_data[key] = f"[{CapitalCase(key)}]"
                    output_schema += json_to_schema(new_dict, schemaType=CapitalCase(key))
                else:
                    print("Unexpected argument parsed in the list")
                    exit(0)

            else:
                print("Empty list. Skipping due to Unexpected Behaviour")
        elif value is None:
            print("Found a none field. Unexpected behaviour. Skipping this")
        else:
            print(f"Unexpected argument parsed: {type(value)}")
            exit(0)

    new_output_schema = f"type {schemaType} " + json.dumps(generated_data)

    replace_rules = [
        (",", "\n"),
        ("\"", ""),
        ("}", "\n}\n"),
        ("{", "{\n ")
    ]

    for first, second in replace_rules:
        new_output_schema = new_output_schema.replace(first, second)

    output_schema += new_output_schema
    return output_schema



