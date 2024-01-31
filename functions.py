import logging
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile
from utilities.utilities import file_direction, remove_file_from_zip
from utilities.config_reader import WORK_DIR, MEDO_DIR, DSP_ID, PCHO_ID, FAILED


def analize_medo():
    direc = f'{WORK_DIR}/{MEDO_DIR}'
    files_list = []
    for i in os.listdir(direc):
        obj = {
            'type': '',
            'name': i,
            'dest': False,
            'annotation': None,
            'date_number': None,
            'filename_pdf': None,
            'page_cnt': '1',
            'error_state': False,
        }
        for _, __, files in os.walk(f'{direc}/{i}'):
            for filename in files:
                try:
                    if '.xml' in filename:
                        ET.register_namespace('c', "urn:IEDMS:CONTAINER")
                        ET.register_namespace('xdms', "http://www.infpres.com/IEDMS")
                        tree_og = ET.parse(f'{direc}/{i}/{filename}')
                        root_og = tree_og.getroot()

                        if root_og.find('.//{http://www.infpres.com/IEDMS}kind') is not None \
                                and \
                                root_og.find('.//{http://www.infpres.com/IEDMS}kind').text == 'Обращение':
                            obj['type'] = root_og.find('.//{http://www.infpres.com/IEDMS}kind').text
                            continue

                        ET.register_namespace('xdms', "urn:IEDMS:MESSAGE")
                        if root_og.find('.//{urn:IEDMS:MESSAGE}deliveryIndex'
                                               '/{urn:IEDMS:MESSAGE}destination') is not None:
                            for id in root_og.findall('.//{urn:IEDMS:MESSAGE}deliveryIndex'
                                                   '/{urn:IEDMS:MESSAGE}destination'
                                                   '/{urn:IEDMS:MESSAGE}destination'):
                                if id.attrib.get('{urn:IEDMS:MESSAGE}uid') == PCHO_ID:
                                    obj['dest'] = True

                    if '.zip' in filename:
                        with ZipFile(f"{direc}/{i}/{filename}", "r") as myzip:
                            for item in myzip.namelist():
                                if '.xml' in item:
                                    with myzip.open(item, "r") as hello_file:
                                        ET.register_namespace('c', "urn:IEDMS:CONTAINER")
                                        ET.register_namespace('xdms', "urn:IEDMS:CONTAINER")
                                        tree = ET.parse(hello_file)
                                        root = tree.getroot()

                                        if root.find('.//{urn:IEDMS:CONTAINER}annotation') is not None:
                                            obj['annotation'] = root.find('.//{urn:IEDMS:CONTAINER}annotation').text

                                        if root.find('.//{urn:IEDMS:CONTAINER}number') is not None:
                                            obj['date_number'] = root.find('.//{urn:IEDMS:CONTAINER}number').text

                                        if root.find('.//{urn:IEDMS:CONTAINER}date') is not None:
                                            obj['date_number'] += ' от ' + root.find('.//{urn:IEDMS:CONTAINER}date').text

                                        if root.find('.//{urn:IEDMS:CONTAINER}pagesQuantity') is not None:
                                            obj['page_cnt'] = root.find('.//{urn:IEDMS:CONTAINER}pagesQuantity').text

                                        if root.find('./{urn:IEDMS:CONTAINER}document') is not None:
                                            obj['filename_pdf'] = root.find('./{urn:IEDMS:CONTAINER}document') \
                                                .attrib.get('{urn:IEDMS:CONTAINER}localName')

                                        # проверка на тип
                                        if root.find('.//{urn:IEDMS:CONTAINER}classification') is not None:
                                            obj['type'] += root.find('.//{urn:IEDMS:CONTAINER}classification').text

                                        if obj['type'] == DSP_ID:
                                            title = root.findall('.//{urn:IEDMS:CONTAINER}addressee'
                                                                 '/{urn:IEDMS:CONTAINER}organization'
                                                                 '/{urn:IEDMS:CONTAINER}title')
                                            if title is not None:
                                                for elem in title:
                                                    if elem.text == 'Правительство Челябинской области':
                                                        obj['dest'] = True  # ВЕРНУТЬ НА TRUE !!!!!!!!
                                                for id in root.findall('.//{urn:IEDMS:CONTAINER}addressee'
                                                                       '/{urn:IEDMS:CONTAINER}organization'):
                                                    if id.attrib.get('{urn:IEDMS:CONTAINER}id') == PCHO_ID:
                                                        obj['dest'] = True  # ВЕРНУТЬ НА TRUE !!!!!!!!
                                    hello_file.close()


                except Exception:
                    shutil.move(f'{direc}/{i}', f'{WORK_DIR}/{FAILED}/{i}')
                    e = sys.exc_info()[1]
                    logging.error(f'ERROR {e.args}')
                    obj['error_state'] = True
                    break
        if not obj['error_state']:
            files_list.append(obj)

    return files_list


def file_manager(catalogs_list: list):
    for catalog in catalogs_list:
        try:
            if catalog['type'] == 'Обращение':
                file_direction(catalog_name=catalog['name'], to_direct='dsp_tezis')

            elif catalog['type'] == 'Информация ограниченного распространения':
                if catalog['dest']:
                    file_direction(catalog_name=catalog['name'], to_direct='dsp_pcho')
                else:
                    file_direction(catalog_name=catalog['name'], to_copy='dsp_tezis')
                    remove_file_from_zip(f'{WORK_DIR}/{MEDO_DIR}/{catalog["name"]}', catalog)
                    file_direction(catalog_name=catalog['name'], to_direct='sed_in')

            else:
                file_direction(catalog_name=catalog['name'], to_direct='sed_in')
        except Exception:
            shutil.move(f'{WORK_DIR}/{MEDO_DIR}/{catalog["name"]}/', f'{WORK_DIR}/{FAILED}/{catalog["name"]}/')
            e = sys.exc_info()[1]
            logging.error(f'{e.args[0]}')
            continue
    return len(catalogs_list)
