try:
    from pip.req import parse_requirements
    from pip.download import PipSession
except Exception:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
from setuptools import setup
from setuptools import find_packages


version = '0.0.1dev'

# Figure out project requirements
install_reqs = parse_requirements('./requirements.txt', session=PipSession())
requires = [str(ir.req) for ir in install_reqs]

# Configure setup
setup(
    name="jira-scheduler",
    version=version,
    description='juwai jira scheduler',
    long_description=open('README.md').read(),
    author='Barry Bao',
    author_email='dev@juwai.com',
    url='http://dev.juwai.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    data_files=[('jw', ['src/jw/settings.cfg'])],
    namespace_packages=['jw'],
    zip_safe=False,
    entry_points={
        'console_scripts': ['scheduler-start=jw.scripts.scheduler:main'],
    },
    install_requires=requires
)
