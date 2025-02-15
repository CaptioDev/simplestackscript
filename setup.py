from setuptools import setup, find_packages

setup(
    name='simplestackscript',
    version='0.2.3',
    packages=find_packages(), # find all packages in the current directory
    entry_points={
        'console_scripts': [
            's3 = simplestackscript.s3:main', # call the main function in the script
        ],
    },
    install_requires=[],
)