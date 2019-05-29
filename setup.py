from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='big-fiubrother-detection',
    version='0.1.3',
    description='Big Fiubrother Face Detection application',
    license="GPLv3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=[],
    author='Eduardo Neira, Gabriel Gayoso',
    author_email='gabriel.gayoso@fi.uba.ar',
    packages=find_packages(),
    url= 'https://github.com/BigFiuBrother/big-fiubrother-detection',
    install_requires=['opencv-python', 'numpy', 'pyyaml'],
    include_package_data=True
)