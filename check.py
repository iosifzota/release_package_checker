import yaml
import json
import os

def parseYaml(file_path):
    parsed_data = {}
    with open(file_path, 'r') as file:
         parsed_data = yaml.safe_load(file)
    return parsed_data

"""
{
    "parent": "CCP",
    "subfolders": [
        {
            "parent": "10_env",
            "files": [
                "env1.test",
                "env2.test"
            ]
        },
        {
            "parent": "20_docs",
            "subfolders": [
                {
                    "parent": "Test",
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
        if key == 'parent':
            folder_name = value
            file_handler.write(f'{prev_indentation}- {key}: {folder_name}\n')
            prev_indentation += tab_spaces
        elif key == 'files':
            file_handler.write(f'{prev_indentation}files:\n')
            for file_name in value:
                file_handler.write(f'{prev_indentation + tab_spaces}- {file_name}\n')
        elif key == 'subfolders':
            file_handler.write(f'{prev_indentation}subfolders:\n')
            for subfolder_higherarchy in value:
                writeYaml(subfolder_higherarchy, file_handler, prev_indentation + tab_spaces)

                
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
- parent: CCP
  subfolders:
    - parent: 10_env
      files:
        - env1.test
        - env2.test
    - parent: 20_docs
      subfolders:
        - parent: Test
          files:
            - 01.rep
            - 02.rep
      files:
        - release_note.txt
        - timestamp.log
"""

def test_should_parse_yaml_and_reprint_it():
    file_name = 'should_parse_yaml_and_reprint_it.yaml'
    # Write yaml to file
    with open(file_name, 'w') as file:
        file.write(file_contents.strip())
    # Parse yaml from written file
    folder_structure = parseYaml(file_name)[0]

    # Traverse dictionary and convert back to yaml format.
    regen_file_name = 'should_parse_yaml_and_reprint_it_regenerated.yaml'
    with open(regen_file_name, 'w') as file:
        writeYaml(folder_structure, file)

    # Check that converstion from dict to yaml format worked fine.
    assert os.path.exists(regen_file_name)
    regen_file_contents = ''
    with open(regen_file_name, 'r') as file:
        regen_file_contents = file.read()
    assert file_contents.strip() == regen_file_contents.strip()

if __name__ == "__main__":
    test_should_parse_yaml_and_reprint_it()
    print("Everything passed")

# pretty = json.dumps(prime_service, indent=4)
# print(prime_service)
