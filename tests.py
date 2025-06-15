# from subdirectory.filename import function_name
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file

# print(get_file_content("calculator", "main.py"))
# print(get_file_content("calculator", "pkg/calculator.py"))
# print(get_file_content("calculator", "/bin/cat"))

# print(get_file_content("calculator", "lorem.txt"))

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))