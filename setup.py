from setuptools import setup, find_packages

version = '0.1'

setup(name='onapie',
      version=version,
      description="Ona API Python Library",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Ona Python API',
      author='Larry Weya',
      author_email='lweya@ona.io',
      url='https://github.com/onaio/onapie',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='onapie',
      install_requires=[
          'requests'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
