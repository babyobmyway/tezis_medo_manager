import os
from xml.dom.minidom import parse, parseString
from zipfile import ZipFile
from utilities.utilities import file_direction, remove_file_from_zip
from utilities.config_reader import WORK_DIR, MEDO_DIR, DSP_ID, PCHO_ID


def analize_medo():
    direc = f'{WORK_DIR}/{MEDO_DIR}'
    files_list = []
    for i in os.listdir(direc):
        obj = {
            'type': '',
            'name': i,
            'dest': False
        }
        for _, __, files in os.walk(f'{direc}/{i}'):
            for filename in files:

                if '.zip' in filename:
                    with ZipFile(f"{direc}/{i}/{filename}", "r") as myzip:
                        for item in myzip.namelist():
                            if '.xml' in item:
                                with myzip.open(item, "r") as hello_file:
                                    text_xml = hello_file.read()
                                    document = parseString(text_xml)
                                    if not document.getElementsByTagName("xdms:classification"):
                                        obj['type'] = document.getElementsByTagName('c:classification')[0] \
                                            .firstChild \
                                            .nodeValue
                                    else:
                                        obj['type'] = document.getElementsByTagName("xdms:classification")[0] \
                                            .firstChild \
                                            .nodeValue
                                        if obj['type'] == DSP_ID:
                                            for x in document.getElementsByTagName('xdms:addressee'):
                                                if PCHO_ID in \
                                                        x.getElementsByTagName('xdms:title')[0] \
                                                                .firstChild \
                                                                .nodeValue:
                                                    obj['dest'] = True
                                hello_file.close()

                if '.xml' in filename:
                    document = parse(f'{direc}/{i}/{filename}')
                    if document.getElementsByTagName("xdms:kind"):
                        obj['type'] = document.getElementsByTagName("xdms:kind")[0].firstChild.nodeValue
        files_list.append(obj)

    return files_list


def file_manager(catalogs_list: list):
    for catalog in catalogs_list:
        if catalog['type'] == 'Обращение':
            file_direction(catalog_name=catalog['name'], to_direct='dsp_tezis', to_copy='sed_in')

        elif catalog['type'] == 'Информация ограниченного распространения':
            if catalog['dest']:
                file_direction(catalog_name=catalog['name'], to_direct='dsp_pcho')
            else:
                directory_copy = file_direction(catalog_name=catalog['name'], to_direct='dsp_tezis', to_copy='sed_in')
                remove_file_from_zip(directory_copy)

        else:
            file_direction(catalog_name=catalog['name'], to_direct='sed_in')
