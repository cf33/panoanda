"""
Created on Sat Sep 16 19:01:15 2017

@author: dariocorral
"""
from setuptools import setup, find_packages
import sys, os

setup(name='panoanda',
      version= '0.1',
      description="PANDAS integration for the OANDA REST API",
      long_description="""\
""",
      classifiers=[
            'Programming Language :: Python',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Intended Audience :: Financial and Insurance Industry'
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='OANDA FOREX wrapper REST API',
      author='Darío Corral',
      author_email='dario.corralmorales@gmail.com',
      url='http://github.com/dariocorral/panoanda',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['pandas==0.20.3',
                        'oandapy==0.1',
                        'DateTime',
                        'pytz'
              ],
      dependency_links=[
        'git+https://github.com/oanda/oandapy.git@master#egg=oandapy-0.1',
    ],  
       entry_points="""
              # -*- Entry points: -*-
              """,
    )
