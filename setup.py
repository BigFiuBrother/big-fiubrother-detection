from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='big-fiubrother-detection',
    version='0.1.6',
    description='Big Fiubrother Face Detection application',
    license="GPLv3",
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=['big_fiubrother_detection_demo_files.py', 'big_fiubrother_detection_demo_webcam.py', 'big_fiubrother_detection_output_compare.py'],
    author='Eduardo Neira, Gabriel Gayoso',
    author_email='gabriel.gayoso@fi.uba.ar',
    packages=['big_fiubrother_detection'],
    url='https://github.com/BigFiuBrother/big-fiubrother-detection',
    install_requires=['opencv-python', 'numpy', 'pyyaml'],
    include_package_data=True
)