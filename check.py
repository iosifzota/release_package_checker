import yaml
import json
import os
import shutil
import unittest

def parseYaml(file_path):
    parsed_data = {}
    with open(file_path, 'r') as file:
        parsed_data = yaml.safe_load(file)
    return parsed_data

"""
{
    "name_of_folder": "CCP",
    "subfolders": [
        {
            "name_of_folder": "10_env",
            "files": [
                "env1.test",
                "env2.test"
            ]
        },
        {
            "name_of_folder": "20_docs",
            "subfolders": [
                {
                    "name_of_folder": "Test",
                    "files": [
                        "01.rep",
                        "02.rep"
                    ]
                }
            ],
            "files": [
                "release_note.txt",
                "timestamp.log"
            ]
        }
    ]
}
 """
tab_spaces = ' ' * 2

def writeYaml(data_in_dict_format, file_handler, prev_indentation = ''):
    for key, value in data_in_dict_format.items():
        if 'name_of_folder' == key:
            folder_name = value
            if '' == prev_indentation:
                file_handler.write(f'{key}: {folder_name}\n')
            else:
                file_handler.write(f'{prev_indentation}- {key}: {folder_name}\n')
                prev_indentation += tab_spaces

        elif 'files' == key:
            file_handler.write(f'{prev_indentation}files:\n')
            for file_name in value:
                file_handler.write(f'{prev_indentation + tab_spaces}- {file_name}\n')
        elif 'subfolders' == key:
            file_handler.write(f'{prev_indentation}subfolders:\n')
            for subfolder_higherarchy in value:
                writeYaml(subfolder_higherarchy, file_handler, prev_indentation + tab_spaces)
            
def check_folder_contents_recursive(parent_folder_path, data_in_dict_format):
    for data_label, data in data_in_dict_format.items():
        if 'name_of_folder' == data_label:
            folder_name = data
            parent_folder_path = f'{parent_folder_path}/{folder_name}'
            if not os.path.exists(parent_folder_path):
                return False
        elif 'files' == data_label:
            list_of_file_names = data
            for file_name in list_of_file_names:
                file_path = f'{parent_folder_path}/{file_name}'
                if not os.path.exists(file_path):
                    return False
        elif 'subfolders' == data_label:
            for subfolder in data:
                pass
                # check_folder_contents_recursive(folder_path, subfolder)
    return True   

def check_folder_contents(folder_path, yaml_desc_file_path):
    data_in_dict_format = parseYaml(yaml_desc_file_path)
    return check_folder_contents_recursive(os.path.dirname(folder_path), data_in_dict_format)
    
def create_empty_files(folder_path, filelist):
    for filen in filelist:
        with open(f'{folder_path}/{filen}', 'w') as file:
            file.write('...')

# def writeYaml(data_in_dict_format, file_path):
#     prev_indentation = ''
#     for key, value in data_in_dict_format.items():
        
#         elif key == 'subfolders':
#             print(f'{prev_indentation}subfolders:')
#             inner_prev_indentation = prev_indentation + tab_spaces
#             for subfolder in value:
#                 inner_inner_prev_indentation = inner_prev_indentation + tab_spaces
#                 for inner_key, inner_value in subfolder.items():
#                     if inner_key == 'parent':
#                         print(f'{inner_prev_indentation}- {inner_key}: {inner_value}')
#                     elif inner_key == 'subfolders':
#                         print('crash')
#                         exit(0)
#                     elif inner_key == 'files':
#                         print(f'{inner_inner_prev_indentation}files:')
#                         for file_name in inner_value:
#                             print(f'{inner_inner_prev_indentation + tab_spaces}- {file_name}')

file_contents = """
name_of_folder: CCP
subfolders:
  - name_of_folder: 10_env
    files:
      - env1.test
      - env2.test
  - name_of_folder: 20_docs
    subfolders:
      - name_of_folder: Test
        files:
          - 01.rep
          - 02.rep
    files:
      - release_note.txt
      - timestamp.log
"""

from pyfakefs.fake_filesystem_unittest import TestCase

class TestCaseBasic(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_create_file(self):
        file_path = "/test/file.txt"
        self.assertFalse(os.path.exists(file_path))
        self.fs.create_file(file_path)
        self.assertTrue(os.path.exists(file_path))

    def test_should_parse_yaml_and_reprint_it(self):
        file_name = 'should_parse_yaml_and_reprint_it.yaml'
        # Write yaml to file
        with open(file_name, 'w') as file:
            file.write(file_contents.strip())
        # Parse yaml from written file
        folder_structure = parseYaml(file_name)

        # Traverse dictionary and convert back to yaml format.
        regen_file_name = 'should_parse_yaml_and_reprint_it_regenerated.yaml'
        with open(regen_file_name, 'w') as file:
            writeYaml(folder_structure, file)

        # Check that converstion from dict to yaml format worked fine.
        assert os.path.exists(regen_file_name) 
        regen_file_contents = '' 
        with open(regen_file_name, 'r') as file: 
            regen_file_contents = file.read()
        self.assertEqual(file_contents.strip(), regen_file_contents.strip())

    def test_should_check_if_folder_contens_match_given_yaml_description(self):
        folder_contents_description = """
    name_of_folder: test01
    files:
      - test1.txt
      - test2.md
    """
        folder_path = 'res/test01'
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        create_empty_files(folder_path, ['test1.txt', 'test2.md'])
        with open(f'{folder_path}/ desc.yaml', 'w') as file:
            file.write(folder_contents_description)

        self.assertTrue(check_folder_contents(folder_path, f'{folder_path}/desc.yaml'))


if __name__ == '__main__':
    unittest.main()  # pragma: no cover

# pretty = json.dumps(prime_service, indent=4)
# print(prime_service)
