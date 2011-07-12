from setuptools import setup, find_packages
import os

version = '0.4dev'

setup(name='sealjet.tool',
      version=version,
      description="sealjet PDM commandline tool",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
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
