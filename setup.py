from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='simplestackscript',
    version='0.2.10',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            's3 = s3_package.s3:main',
        ],
    },
    install_requires=[],
    long_description=long_description,  # Use README.md as long description
    long_description_content_type="text/markdown",  # Important: Specify Markdown format
)