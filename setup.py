from setuptools import setup

import offensivecontent
version = offensivecontent.__version__

try:
    f = open('README')
    long_desc = f.read()
    f.close()
except:
    long_desc = ""

setup(name='offensivecontent',
      version=version,
      description='An application to mark peices of content as offensive',
      long_description=long_desc,
      author='Jose Soares',
      author_email='jsoares@washingtontimes.com',
      url='http://opensource.washingtontimes.com/projects/offensivecontent/',
      packages=['offensivecontent'],
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'License :: OSI Approved :: Apache Software License',
          ],
      )
