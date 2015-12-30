from setuptools import setup

setup(
    name='yodel',
    version='1.0',
    description='Downloads the entire soundtrack of a Movie',
    url='https://github.com/TheChesireCat/yodel'
    author='Ankit Ramakrishnan',
    author_email='aliceoxenbury@gmail.com',
    license='MIT',
    packages=['yodel'],
    scripts=['bin/yodel'],
    install_requires=[
        'youtube-dl',
        'BeautifulSoup4',
        'eyed3',
        'requests'
    ]
)
