# -*- coding: utf-8 -*-

"""Top-level package for omigami."""

__author__ = """Data Revenue GmbH"""
__email__ = "giulio@datarevenue.com"
__version__ = "0.1.0"

import logging
import sys
from omigami.feature_selector import FeatureSelector
from ._version import get_versions


__version__ = get_versions()["version"]
del get_versions

logger = logging.getLogger("omigami")
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(name)-26s %(levelname)-7s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)
