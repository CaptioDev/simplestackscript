from setuptools import setup, find_packages

setup(
    name='simplestackscript',
    version='0.2.0',
    packages=find_packages(), # find all packages in the current directory
    entry_points={
        'console_scripts': [
            's3 = s3_package.s3:main', # call the main function in your script
        ],
    },
    install_requires=[],
)