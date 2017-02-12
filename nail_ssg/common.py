def dict_concat(dict1, dict2):
    for key in dict2:
        if type(dict2[key]) == dict:
            if key not in dict1 or type(dict1[key]) != dict:
                dict1[key] = {}
            dict_concat(dict1[key], dict2[key])
        elif type(dict2[key]) == list:
            if key not in dict1 or type(dict1[key]) != list:
                dict1[key] = []
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
