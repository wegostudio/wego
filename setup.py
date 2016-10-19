from setuptools import setup, find_packages

setup(
    name = 'wego',
    version = '0.9.3',
    keywords = ('wechat sdk'),
    description = 'dead simple wechat sdk',
    url = 'https://github.com/wegostudio/wego',
    author = 'Quseit',
    author_email = 'sciooga@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    license = 'Apache License',
    install_requires = ['requests'],
)
