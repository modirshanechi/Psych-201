from glob import glob 
import zipfile

zipped_files = glob('*/*.zip')
print(zipped_files)
print(len(zipped_files))

for path_to_zip_file in zipped_files:
    print(path_to_zip_file)
    directory_to_extract_to = path_to_zip_file.removesuffix('.zip')
    directory_to_extract_to = directory_to_extract_to.removesuffix('.jsonl')
    directory_to_extract_to = directory_to_extract_to.removesuffix('prompts')
    print(directory_to_extract_to)
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)