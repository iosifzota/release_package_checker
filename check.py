import yaml
import os

def parseYaml(file_path):
    parsed_data = {}
    with open(file_path, 'r') as file:
        parsed_data = yaml.safe_load(file)
    return parsed_data
tab_spaces = ' ' * 2

def writeYaml(folder_info, file_handler, prev_indentation = ''):
    for info_label, info  in folder_info.items():
        if 'name_of_folder' == info_label:
            folder_name = info
            if '' == prev_indentation:
                file_handler.write(f'{info_label}: {folder_name}\n')
            else:
                file_handler.write(f'{prev_indentation}- {info_label}: {folder_name}\n')
                prev_indentation += tab_spaces

        elif 'files' == info_label:
            list_of_file_names = info
            file_handler.write(f'{prev_indentation}files:\n')
            for file_name in list_of_file_names:
                file_handler.write(f'{prev_indentation + tab_spaces}- {file_name}\n')
        elif 'subfolders' == info_label:
            list_of_subfolers = info
            file_handler.write(f'{prev_indentation}subfolders:\n')
            for subfolder_higherarchy in list_of_subfolers:
                writeYaml(subfolder_higherarchy, file_handler, prev_indentation + tab_spaces)
            
def check_folder_contents_recursive(parent_folder_path, folder_info):
    for info_label, info in folder_info.items():
        if 'name_of_folder' == info_label:
            folder_name = info
            parent_folder_path = f'{parent_folder_path}/{folder_name}'
            if not os.path.exists(parent_folder_path):
                return False
        elif 'files' == info_label:
            list_of_file_names = info
            for file_name in list_of_file_names:
                file_path = f'{parent_folder_path}/{file_name}'
                if not os.path.exists(file_path):
                    return False
        elif 'subfolders' == info_label:
            list_of_subfolders = info
            for subfolder_info in list_of_subfolders:
                pass
                # check_folder_contents_recursive(parent_folder_path, subfolder_info)
    return True   

def check_folder_contents(folder_path, yaml_desc_file_path):
    folder_info = parseYaml(yaml_desc_file_path)
    return check_folder_contents_recursive(os.path.dirname(folder_path), folder_info)
    
def create_empty_files(folder_path, filelist):
    for filen in filelist:
        with open(f'{folder_path}/{filen}', 'w') as file:
            file.write('...')

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

# Old version of code. See how clutter it is...
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
# pretty = json.dumps(prime_service, indent=4)
# print(prime_service)
