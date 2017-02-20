from setuptools import setup, find_packages

setup(
    name='ilswbot',
    author='Arne Beer',
    author_email='arne@twobeer.de',
    version='0.1.0',
    description='Is Lukas schon wach?',
    keywords='Lol',
    url='http://github.com/Nukesor/ilswlol-bot',
    license='MIT',
    install_requires=[
        'python-telegram-bot==5.3.0',
        'urllib3==1.20'
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Environment :: Console'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ilswbot=ilswbot:main'
        ]
    })
