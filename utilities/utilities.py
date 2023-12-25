import os
import re
import shutil
from zipfile import ZipFile
from ruamel.std.zipfile import delete_from_zip_file


def file_direction(catalog_name: str, to_direct: str, to_copy=''):
    os.mkdir(f'C:/tezis_directory/{to_direct}/{catalog_name}/')
    if to_copy != '':
        os.mkdir(f'C:/tezis_directory/{to_copy}/{catalog_name}/')
    for _, __, files in os.walk(f'C:/tezis_directory/medo_in/{catalog_name}'):
        for filename in files:
            if to_copy != '':
                shutil.copyfile(f'C:/tezis_directory/medo_in/{catalog_name}/{filename}',
                                f'C:/tezis_directory/{to_copy}/{catalog_name}/{filename}')
            shutil.move(f'C:/tezis_directory/medo_in/{catalog_name}/{filename}',
                        f'C:/tezis_directory/{to_direct}/{catalog_name}/{filename}')
    os.rmdir(f'C:/tezis_directory/medo_in/{catalog_name}/')
    if to_copy != '':
        return f'C:/tezis_directory/{to_copy}/{catalog_name}'


def copying_files(catalog_name: str, to_direct: str):
    os.mkdir(f'C:/tezis_directory/{to_direct}/{catalog_name}/')
    for _, __, files in os.walk(f'C:/tezis_directory/medo_in/{catalog_name}'):
        for filename in files:
            shutil.copy(f'C:/tezis_directory/medo_in/{catalog_name}/{filename}',
                        f'C:/tezis_directory/{to_direct}/{catalog_name}/{filename}')


def remove_file_from_zip(catalog_name: str):
    for _, __, files in os.walk(catalog_name):
        for filename in files:

            if '.zip' in filename:
                with ZipFile(f"{catalog_name}/{filename}", "r") as myzip:
                    for item in myzip.namelist():
                        pattern = re.compile('.*.p7s|.*.xml|.*.png')
                        result = pattern.findall(item)
                        if not result:
                            delete_from_zip_file(f'{catalog_name}/{filename}', file_names=item)