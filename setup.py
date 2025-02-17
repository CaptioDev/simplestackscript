from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='simplestackscript',
    version='1.0.0-dev3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            's# = s#_package.s#:main',
        ],
    },
    install_requires=[],
    long_description=long_description,  # Use README.md as long description
    long_description_content_type="text/markdown",  # Important: Specify Markdown format
)