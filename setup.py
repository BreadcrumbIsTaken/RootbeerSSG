from setuptools import setup


def readme():
    with open('README.md', 'r', encoding='utf-8') as rm:
        readme_file = rm.read()
    return readme_file


setup(
    name='rootbeerSSG',
    version='1.0.1',
    description='The easy to use and very epic Static Site Generator for blogs!',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/BreadcrumbIsTaken/RootbeerSSG',
    author='Breadcrumb',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable'
    ],
    packages=['rootbeerSSG'],
    include_package_data=True,
    install_requires=[
        'blinker',
        'Jinja2',
        'Markdown',
        'markdown-full-yaml-metadata',
        'MarkupSafe',
        'PyYAML',
        'slug'
    ],
)
