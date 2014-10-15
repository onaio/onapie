from setuptools import setup, find_packages

version = '0.1'

setup(name='onapie',
      version=version,
      description="Ona API Python Library",
      long_description="Python bindings to the Onadata REST API",
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7'],
      keywords='Ona Python API',
      author='Ona Kenya',
      author_email='tech@ona.io',
      url='https://github.com/onaio/onapie',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      test_suite='onapie',
      install_requires=['requests'],)
