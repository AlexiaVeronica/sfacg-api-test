from setuptools import setup

setup(
    name='seach_book',
    version='1.0',
    packages=['search'],
    url='',
    license='',
    author='Elaina',
    author_email='75843578@qq.com',
    include_package_data=True,
    zip_safe=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'search = search.search_book:main'
        ]
    },
    description=''
)
