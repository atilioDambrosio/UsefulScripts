import os
from datetime import datetime

import numpy as np
import json
from collections.abc import Iterable

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

def pretty_search(dict_or_list, key_to_search, search_for_first_only=False):
    """
    Give it a dict or a list of dicts and a dict key (to get values of),
    it will search through it and all containing dicts and arrays
    for all values of dict key you gave, and will return you set of them
    unless you wont specify search_for_first_only=True

    :param dict_or_list:
    :param key_to_search:
    :param search_for_first_only:
    :return:
    """
    search_result = []
    if isinstance(dict_or_list, dict):
        for key in dict_or_list:
            key_value = dict_or_list[key]
            if key == key_to_search:
                if search_for_first_only:
                    return [key, key_value]
                else:
                    search_result.append([key,key_value])
            if isinstance(key_value, dict) or isinstance(key_value, list) or isinstance(key_value, set):
                _search_result = pretty_search(key_value, key_to_search, search_for_first_only)
                if _search_result and search_for_first_only:
                    return list(flatten([key, _search_result]))
                elif _search_result:
                    for result in _search_result:
                        aaa = [key]
                        aaa.extend(result)
                        search_result.append(aaa)
    elif isinstance(dict_or_list, list) or isinstance(dict_or_list, set):
        for element in dict_or_list:
            if isinstance(element, list) or isinstance(element, set) or isinstance(element, dict):
                _search_result = pretty_search(element, key_to_search, search_result)
                if _search_result and search_for_first_only:
                    return _search_result
                elif _search_result:
                    for result in _search_result:
                        search_result.append(result)
    return search_result if search_result else None

def timestr_to_num(timestr):
    return mdates.date2num(datetime.strptime('0' + timestr if timestr[1] == ':' else timestr, '%Y/%m/%d %H:%M:%S'))

def size_array(self, array):
    return array.ndim and array.size

def diff_new_elements(_list, _list_actual):
    new_atte = []
    if size_array(_list):
        for plan in _list:
            pair = (np.setdiff1d(plan, _list_actual)).tolist()
            if len(pair) > 0:
                new_atte.append(plan.tolist())
    return new_atte

def diff_remove_elements(_list, _list_actual):
    del_atte = []
    list_remove_elements = np.array([])
    if size_array(_list_actual):
        if size_array(_list):
            for plan in _list_actual:
                pair = (np.setdiff1d(plan, _list)).tolist()
                if len(pair) > 0:
                    del_atte.append(plan.tolist())
            if len(del_atte) > 0:
                list_remove_elements = _list_actual
        else:
            list_remove_elements = _list_actual
    return list_remove_elements

def read_config(path_file):
    with open(outfile) as json_file:
        data = json.load(json_file)
    return data

def save_name_dir_and_files(path_file):
    listOfdir = {}
    _listOffiles = []
    list_of_files = {}
    for nombre_directorio, dirs, ficheros in os.walk(path_file):
        dir = nombre_directorio.split("/")
        dir = dir[-1]
        listOfdir[dir] = []
        for nombre_fichero in ficheros:
            nombre_fichero = os.path.splitext(nombre_fichero)[0]
            if not nombre_fichero in _listOffiles:
                _listOffiles.append(nombre_fichero)
            else:
                list_of_files[nombre_fichero] = dir
    filePathTemp = os.path.join("/mnt", "ramdisk", "satlist.json")
    with open(filePathTemp, 'w+', encoding='utf8') as outfile:
        json.dump(list_of_files, outfile, indent=4, ensure_ascii=False)

def get_name_dir_and_files(path_file):
    listOfdir = {}
    _listOffiles = []
    list_of_files = {}
    for nombre_directorio, dirs, ficheros in os.walk(path_file):
        dir = nombre_directorio.split("/")
        dir = dir[-1]
        listOfdir[dir] = []
        for nombre_fichero in ficheros:
            nombre_fichero = os.path.splitext(nombre_fichero)[0]
            if not nombre_fichero in _listOffiles:
                _listOffiles.append(nombre_fichero)
            else:
                list_of_files[nombre_fichero] = dir
    return list_of_files

def get_numpy_file(outfile):
    try:
        array = np.load(outfile, allow_pickle=True)
    except:
        array = np.array([[]])
    return array

