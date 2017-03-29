from setuptools import setup

try:
    from pyqt_distutils.build_ui import build_ui
    cmdclass = {"build_ui": build_ui}
except ImportError:
    cmdclass = {}

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
