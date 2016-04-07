"""Reports package

"""
__version__ = "$Rev: 10 $"
import pkg_resources
try:
    version = pkg_resources.require("reports")[0].version
except:
    version = __version__


from .report import Report
from .htmltable import HTMLTable
