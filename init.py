# not sure it will work or not whatever
import os
if __name__ == '__main__':
  # crawl '.' folder and run all py files
  for file in os.listdir('.'):
    if file.endswith('.py'):
      exec(open(file).read())