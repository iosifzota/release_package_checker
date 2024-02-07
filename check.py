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
    ("parent", "CCP"),
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

def writeYaml(data_in_dict_format, file_path):
    for key, value in data_in_dict_format.items():
        if key == 'parent':
            print(f'- {key}: {value}')
        elif key == 'subfolders':
            print('subfolders:')
            for subfolder in value:
                for inner_key, inner_value in subfolder.items():
                    if inner_key == 'parent':
                        print(f'- {inner_key}: {inner_value}')                   
                    elif inner_key == 'subfolders':
                        print('crash')
                    elif inner_key == 'files':
                        print('files:')
                        for file_name in inner_value:
                            print(f'- {file_name}')



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
        file.write(file_contents)
    # Parse yaml from written file
    folder_structure = parseYaml(file_name)[0]

    # Traverse dictionary and convert back to yaml format.
    regen_file_name = 'should_parse_yaml_and_reprint_it_regenerated.yaml'
    writeYaml(folder_structure, regen_file_name)

    # # Check that converstion from dict to yaml format worked fine.
    # regen_file_contents = ''
    # assert os.path.exists(regen_file_name)
    # with open(regen_file_name, 'r') as file:
    #     regen_file_contents = file.read()
    # assert file_contents == regen_file_contents


if __name__ == "__main__":
    test_should_parse_yaml_and_reprint_it()
    print("Everything passed")

# pretty = json.dumps(prime_service, indent=4)
# print(prime_service)
