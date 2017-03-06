from distutils.core import setup

setup(
    name='EGEGrouper',
    version='1.0',
    description='Tool for grouping EGEG examinations',
    author='Aleksandr Popov',
    author_email='aleneus@gmail.com',
    packages=['egegmvc', 'egegmvc.models', 'egegmvc.views'],
    scripts=['igrouper', 'tkgrouper']
)
