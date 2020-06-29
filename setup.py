from setuptools import setup
import os
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name='dashboard_lib',
    version='0.0.1',
    description='My private package from private github repo',
    url='git@github.com:guilherme-passos1793/dashboard_lib2.git',
    author='Guilherme Passos',
    author_email='guilherme.passos1793@gmail.com',
    license='unlicense',
    packages=['dashboard_lib'],
    zip_safe=False, install_requires =install_requires
)