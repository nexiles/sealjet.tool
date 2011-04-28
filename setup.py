from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='sealjet.tool',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Stefan Eletzhofer',
      author_email='se@nexiles.de',
      url='http://projects.nexiles.com/sealjet',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sealjet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'argparse',
          'httplib2',
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts': [
              'sealjetpdm = sealjet.tool:main',
              ]
          }
      )
