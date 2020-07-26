# Copyright (C) 2020 Simon Biggs
# Copyright 2001-2017 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Code vendored from:
# https://github.com/python/cpython/blob/a667e1c66a62d509c39d30abf11778213a1e1ca0/Lib/logging/__init__.py#L1896-L1999

import logging

from pymedphys import _config

_patch_applied = False
_basicConfig = logging.basicConfig


def apply_logging_patch():
    global _patch_applied  # pylint: disable = global-statement

    if not _config.is_cli:
        raise ValueError(
            "This patch globally adjusts the logging module. This patch is "
            "not to be used within pymedphys while it is in library mode "
            "as standard library monkey patches can be exceptionally confusing "
            "to a library user. "
            "This is only to be used when pymedphys is being called via "
            "CLI."
        )

    if _patch_applied:
        raise ValueError("This patch has already been applied.")

    def basicConfig(**kwargs):
        force = kwargs.pop("force", False)
        if force:
            for h in logging.root.handlers[:]:  # pylint: disable = no-member
                logging.root.removeHandler(h)  # pylint: disable = no-member
                h.close()

        _basicConfig(**kwargs)

    logging.basicConfig = basicConfig
    _patch_applied = True
