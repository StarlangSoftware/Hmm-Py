from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='NlpToolkit-Hmm',
    version='1.0.6',
    packages=['Hmm'],
    url='https://github.com/StarlangSoftware/Hmm-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Hidden Markov Model Library',
    install_requires=['NlpToolkit-Math', 'NlpToolkit-DataStructure'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
