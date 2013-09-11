from setuptools import setup, find_packages

setup(
    name='Tarrasque',
    version='0.1',
    description='A Dota 2 replay view library.',
    long_description=open('README.md').read(),
    author='Laurie Clark-Michalek',
    author_email='lclarkmichalek@gmail.com',
    zip_safe=True,
    url='https://github.com/bluepeppers/Tarrasque',
    license='MIT',
    packages=find_packages(),
    keywords='dota replay',
    install_requires=[
      'skadi'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ])