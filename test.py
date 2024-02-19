from check import *

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
        with open(f'{folder_path}/desc.yaml', 'w') as file:
            file.write(folder_contents_description)

        self.assertTrue(check_folder_contents(folder_path, f'{folder_path}/desc.yaml'))


if __name__ == '__main__':
    unittest.main()  # pragma: no cover