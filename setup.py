from setuptools import setup
from setuptools.command.build_py import build_py
from pyqt_distutils.build_ui import build_ui
cmdclass = {"build_ui": build_ui}

class CustomBuildPy(build_py):
    def run(self):
        self.run_command('build_ui')
        build_py.run(self)

cmdclass['build_py'] = CustomBuildPy

setup(
    name="Plover: Fancy Tape",
    version="0.0.1",
    description="Paper tape, but with fancy fading",
    author="Ted Morin",
    author_email="morinted@gmail.com",
    license="GPLv2+",
    install_requires=[
        "plover>=4.0.0.dev0",
    ],
    py_modules=[
        'fancy_tape',
    ],
    include_package_data=True,
    entry_points="""
    [plover.gui.qt.tool]
    fancy_tape = fancy_tape:FancyTape
    """,
    cmdclass=cmdclass,
    setup_requires = [
        'setuptools-scm',
    ],
    zip_safe=True,
)
