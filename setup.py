from setuptools import setup, find_packages
from io import open

console_scripts = []

console_scripts.append('{0}={1}.app:main'.format(find_packages('src')[0].replace('_', '-'),
                                                  find_packages('src')[0]))

setup(entry_points={'console_scripts': console_scripts},
      packages=find_packages(where='src'),
      package_dir={'': 'src'}) 