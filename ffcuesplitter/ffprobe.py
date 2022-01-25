# -*- coding: UTF-8 -*-
"""
Name: ffprobe.py
Porpose: simple cross-platform wrap for ffprobe
Compatibility: Python3
Platform: all platforms
Author: Gianluca Pernigotto <jeanlucperni@gmail.com>
Copyright: (c) 2018/2021 Gianluca Pernigotto <jeanlucperni@gmail.com>
license: GPL3
Rev: Nov.25.2021
Code checker: flake8, pylint
########################################################

This file is part of Videomass.

   Videomass is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   Videomass is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with Videomass.  If not, see <http://www.gnu.org/licenses/>.
"""
import subprocess
import platform
import json
from ffcuesplitter.exceptions import FFProbeError
from ffcuesplitter.utils import Popen


def from_kwargs_to_args(kwargs):
    """
    Helper function to build command line
    arguments out of dict.
    """
    args = []
    for key in sorted(kwargs.keys()):
        val = kwargs[key]
        args.append(f'-{key}')
        if val is not None:
            args.append(f'{val}')
    return args


def ffprobe(filename, cmd='ffprobe', **kwargs):
    """
    Run ffprobe on the specified file and return a
    JSON representation of the output.

    Raises:
        :class:`ffcuesplitter.FFProbeError`: if ffprobe
        returns a non-zero exit code;
        `ffcuesplitter.FFProbeError` from `OSError`,
        `FileNotFoundError` if a generic error.

    Usage:
        ffprobe(filename,
                cmd='/usr/bin oi/ffprobe',
                loglevel='error',
                hide_banner=None,
                etc,
                )
    """
    args = [cmd, '-show_format', '-show_streams', '-of', 'json']
    args += from_kwargs_to_args(kwargs)
    args += [filename]
    args = ' '.join(args) if platform.system() == 'Windows' else args

    try:
        with Popen(args,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   universal_newlines=True,
                   ) as proc:
            output, error = proc.communicate()

            if proc.returncode != 0:
                raise FFProbeError(f'ffprobe: {error}')

    except (OSError, FileNotFoundError) as excepterr:
        raise FFProbeError(excepterr) from excepterr

    else:
        return json.loads(output)
