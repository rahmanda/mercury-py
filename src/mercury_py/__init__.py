#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import colorlog

from .mercury_py import mercury_py

__all__ = ['mercury_py']
__title__ = 'mercury-py'
__author__ = 'Rahmanda Wibowo'
__license__ = 'Unlicense'
__copyright__ = 'Copyright 2017 Rahmanda Wibowo'


handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(levelname)s-%(lineno)d] %(message)s'))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(level=logging.INFO)
