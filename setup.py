from setuptools import setup


def readme():
    with open('README.md') as rm:
        readme_file = rm.read()
    return readme_file


setup(
    name='rootbeer',
    version='1.0.0',
    description='The easy to use and very epic Static Site Generator for blogs!',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/BreadcrumbIsTaken/RootbeerSSG',
    author='Breadcrumb',
    license='CC BY-SA 4.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9.0',
        'Programming Language :: Python :: 3.8.6',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Framework :: Rootbeer',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Static Site Generation',
        'Topic :: Static Site Generation :: Blogs',
        'Topic :: Static Site Generation :: Pages',
        'Topic :: Static Site Generation :: Blogs and Pages'
    ],
    packages=['rootbeer'],
    include_package_data=True,
    install_requires=[
        'colorama',
        'Jinaj2',
        'Markdown',
        'markdown-full-yaml-metadata',
        'MarkupSafe',
        'PyYAML',
        'slug'
    ]
)