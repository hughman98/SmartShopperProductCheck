from setuptools import setup, find_packages
  
setup(
    name='SmartShopper',
    version='1.0',
    description='SE project: group 22',
    author="CSC510 - Group 22, Chandrahas Reddy Mandapati, Harini Bharata, Sri Pallavi Damuluri, Niraj Lavani, sandesh A S": ,
    author_email="sgaladha@ncsu.edu",
    packages=find_packages(),
    tests_require=['pytest'],
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python",
          "Development Status :: 2- Pre-Alpha",
          "Intended Audience :: Developers",
          "Topic :: SE Fall 21 Project",
      ],


    license='MIT',
    install_requires=['python', 'pytest'],
)
