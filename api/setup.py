from setuptools import setup, find_packages
setup(
    name = 'hn_job_filter',
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)