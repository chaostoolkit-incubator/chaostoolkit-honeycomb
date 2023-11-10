import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version

elif sys.version_info < (3, 8):
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version("chaostoolkit-honeycomb")
except PackageNotFoundError:
    __version__ = "unknown"
