import os
import shutil
import subprocess
import sys
import tempfile
import setuptools

# Ref : https://packaging.python.org/single_source_version/#single-sourcing-the-version
with open('colos/_version.py') as vf:
    exec(vf.read())

# Best Flow :
# Clean previous build & dist
# $ gitchangelog >CHANGELOG.rst
# change version in code and changelog
# $ python setup.py prepare_release
# WAIT FOR TRAVIS CHECKS
# $ python setup.py publish
# => TODO : try to do a simpler "release" command


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PrepareReleaseCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "prepare a release of pyros"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""

        # change version in code and changelog before running this
        subprocess.check_call("git commit CHANGELOG.rst pyros/_version.py CHANGELOG.rst -m 'v{0}'".format(__version__), shell=True)
        subprocess.check_call("git push", shell=True)

        print("You should verify travis checks, and you can publish this release with :")
        print("  python setup.py publish")
        sys.exit()


# Clean way to add a custom "python setup.py <command>"
# Ref setup.py command extension : https://blog.niteoweb.com/setuptools-run-custom-code-in-setup-py/
class PublishCommand(setuptools.Command):
    """Command to release this package to Pypi"""
    description = "releases pyros to Pypi"
    user_options = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):
        """runner"""
        # TODO : clean build/ and dist/ before building...
        subprocess.check_call("python setup.py sdist", shell=True)
        subprocess.check_call("python setup.py bdist_wheel", shell=True)
        # OLD way:
        # os.system("python setup.py sdist bdist_wheel upload")
        # NEW way:
        # Ref: https://packaging.python.org/distributing/
        subprocess.check_call("twine upload dist/*", shell=True)

        subprocess.check_call("git tag -a {0} -m 'version {0}'".format(__version__), shell=True)
        subprocess.check_call("git push --tags", shell=True)
        sys.exit()



setuptools.setup(name='colos',
    version=__version__,
    description='ColOS : A frmework to manage collaborative processes',
    url='http://github.com/asmodehn/colos',
    author='AlexV',
    author_email='asmodehn@gmail.com',
    license='BSD',
    packages=[
        'colos',
    ],
    entry_points={
        # 'console_scripts': [
        #     'colos = colos.__main__:main'
        # ]
    },
    # this is better than using package data ( since behavior is a bit different from distutils... )
    include_package_data=True,  # use MANIFEST.in during install.
    install_requires=[
        'lockfile',
        'python-daemon',
    ],
    extras_require={
    },
    dependency_links=[
    ],
    # Reference for optional dependencies : http://stackoverflow.com/questions/4796936/does-pip-handle-extras-requires-from-setuptools-distribute-based-sources

    test_suite="nose.collector",
    tests_require=["nose"],
    cmdclass={
        'prepare_release': PrepareReleaseCommand,
        'publish': PublishCommand,
    },
    zip_safe=False,  # TODO testing...
)
