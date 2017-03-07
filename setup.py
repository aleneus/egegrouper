from setuptools import setup

setup(
    name='EGEGrouper',
    version='1.0',
    description='Tool for grouping EGEG examinations',
    author='Aleksandr Popov',
    author_email='aleneus@gmail.com',
    packages=['egegmvc', 'egegmvc.models', 'egegmvc.views'],
    scripts=['tkgrouper.py', 'igrouper.py'],
    install_requires = [
        'numpy',
        'matplotlib',
        'tabulate',
    ],
    entry_points={
        'console_scripts': [
            'igrouper = igrouper:main'
        ],
        'gui_scripts': [
            'tkgrouper = tkgrouper:main'
        ]
    },
)
