import os
import re
import shutil
from zipfile import ZipFile
from ruamel.std.zipfile import delete_from_zip_file
from utilities.config_reader import WORK_DIR, MEDO_DIR
from utilities.generate import generate_pdf


def file_direction(catalog_name: str, to_direct='', to_copy=''):
    if to_direct != '':
        os.mkdir(f'{WORK_DIR}/{to_direct}/{catalog_name}/')
    if to_copy != '':
        os.mkdir(f'{WORK_DIR}/{to_copy}/{catalog_name}/')
    for _, __, files in os.walk(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}'):
        for filename in files:
            if to_copy != '':
                shutil.copyfile(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}/{filename}',
                                f'{WORK_DIR}/{to_copy}/{catalog_name}/{filename}')
            if to_direct != '':
                shutil.move(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}/{filename}',
                            f'{WORK_DIR}/{to_direct}/{catalog_name}/{filename}')
    if to_direct != '':
        os.rmdir(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}/')
    return f'{WORK_DIR}/{to_copy}/{catalog_name}'


def copying_files(catalog_name: str, to_direct: str):
    os.mkdir(f'{WORK_DIR}/{to_direct}/{catalog_name}/')
    for _, __, files in os.walk(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}'):
        for filename in files:
            shutil.copy(f'{WORK_DIR}/{MEDO_DIR}/{catalog_name}/{filename}',
                        f'{WORK_DIR}/{to_direct}/{catalog_name}/{filename}')


def remove_file_from_zip(catalog_name: str, catalog: dict):
    for _, __, files in os.walk(catalog_name):
        for filename in files:
            if '.zip' in filename:
                with ZipFile(f"{catalog_name}/{filename}", "a") as myzip:
                    for item in myzip.namelist():
                        pattern = re.compile('.*.p7s|.*.xml|.*.png')
                        result = pattern.findall(item)
                        if not result:
                            delete_from_zip_file(f'{catalog_name}/{filename}', file_names=item)

                        myzip.close()
                """
                with ZipFile(f"{catalog_name}/{filename}", "a") as zipper:
                    for item1 in zipper.namelist():
                        if '.xml' in item1:
                            zipper.extract(item1)
                            ET.register_namespace('c', "urn:IEDMS:CONTAINER")
                            ET.register_namespace('xdms', "urn:IEDMS:CONTAINER")
                            tree = ET.parse(item1)
                            root = tree.getroot()
                            for child in root:
                                if child.tag == '{urn:IEDMS:CONTAINER}attachments':
                                    root.remove(child)
                            tree.write('passport.xml', encoding='UTF-8', xml_declaration=True)
                """
                with ZipFile(f"{catalog_name}/{filename}", "a") as zipfile:
                    generate_pdf(catalog['filename_pdf'], catalog)
                    zipfile.write(catalog['filename_pdf'])
                    os.remove(catalog['filename_pdf'])
                    zipfile.close()
