from os import path
from os import remove
from os import makedirs

def create_directory(directory_name):
  """ Create directory """
  if not path.exists(directory_name):
    makedirs(directory_name)
    print('The directory %s created.' % directory_name)
  else:
    print('The directory %s exists. Doing nothing.' % directory_name)

def create_file_with_content(directory_name, file_name, content):
  """ Create file with content and necessary directories """
  file_path = directory_name + '/' + file_name
  if not path.exists(file_path):
    create_directory(directory_name)
    file_name = open(file_path, 'w')
    file_name.write(content)
    file_name.close()
    print('The file %s created.' % file_path)
  else:
    print('The file %s exists. Doing nothing.' % file_path)

def delete_file(file_name):
  """ Delete file """
  if path.exists(file_name):
    os.remove(file_name)
    print('The file %s deleted.' % file_name)
  else:
    print('The file %s does not exists. Doing nothing.' % file_name)

""" Testing:
create_file_with_content('/tmp/test', 'test.txt', 'hello i am here\n')
delete_file('/tmp/test/test.txt')
"""
