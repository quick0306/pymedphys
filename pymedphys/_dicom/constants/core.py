# Copyright (c) 2008-2018 Darcy Mason and pydicom contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# This is a copy from the _dicom_dict.py file within pydicom copied from
# https://github.com/pydicom/pydicom/blob/de87f4694ddac7bdb8e20effd82b22eee0d104c0/pydicom/_dicom_dict.py


# This is to have a baseline copy so that it is known whether or not pydicom
# itself has updated its dictionary. When it updates its dictionary it should
# be confirmed that the anonymisation function is still effective.

# pylint: disable=C0301

"""DICOM data dictionary auto-generated by ``pydicom.generate_dicom_dict.py``"""

import functools
import json
from os import path

from pymedphys._imports import pydicom

from pymedphys._data import download

# Many thanks to the Medical Connections for offering free
# valid UIDs (http://www.medicalconnections.co.uk/FreeUID.html)
# Their service was used to obtain the following root UID for PyMedPhys:
PYMEDPHYS_ROOT_UID = "1.2.826.0.1.3680043.10.188"


# Each dict entry is pydicom.tag.Tag : (VR, VM, Name, Retired, Keyword)
HERE = path.dirname(path.abspath(__file__))
BASELINE_DICOM_REPEATERS_DICT_FILEPATH = path.join(
    HERE, "baseline_repeaters_dictionary.json"
)


@functools.lru_cache(maxsize=1)
def get_baseline_dicom_dict():

    baseline_dicom_dict_filepath = download.zip_data_paths(
        "baseline_dicom_dictionary.zip"
    )[0]

    with open(baseline_dicom_dict_filepath) as in_file:
        BASELINE_DICOM_DICT = json.load(in_file)
        BASELINE_DICOM_DICT = {
            pydicom.tag.Tag(int(key)): BASELINE_DICOM_DICT[key]
            for key in BASELINE_DICOM_DICT
        }

    return BASELINE_DICOM_DICT


@functools.lru_cache(maxsize=1)
def get_baseline_dicom_repeaters_dict():
    with open(BASELINE_DICOM_REPEATERS_DICT_FILEPATH) as in_file:
        BASELINE_DICOM_REPEATERS_DICT = json.load(in_file)

    return BASELINE_DICOM_REPEATERS_DICT


@functools.lru_cache(maxsize=1)
def get_baseline_keyword_vr_dict():
    BASELINE_DICOM_DICT = get_baseline_dicom_dict()
    BASELINE_DICOM_REPEATERS_DICT = get_baseline_dicom_repeaters_dict()

    COMBINED_DICOM_DICT = {**BASELINE_DICOM_DICT, **BASELINE_DICOM_REPEATERS_DICT}

    BASELINE_KEYWORD_VR_DICT = {
        COMBINED_DICOM_DICT[tag][4]: COMBINED_DICOM_DICT[tag][0]
        for tag in COMBINED_DICOM_DICT
    }

    return BASELINE_KEYWORD_VR_DICT


DICOM_SOP_CLASS_NAMES_MODE_PREFIXES = {
    "CT Image Storage": "CT",
    "Enhanced CT Image Storage": "CTE",
    "MR Image Storage": "MR",
    "Enhanced MR Image Storage": "MRE",
    "Positron Emission Tomography Image Storage": "PT",
    "Enhanced PET Image Storage": "PTE",
    "RT Image Storage": "RI",
    "RT Dose Storage": "RD",
    "RT Plan Storage": "RP",
    "RT Ion Plan Storage": "RN",
    "RT Structure Set Storage": "RS",
    "Computed Radiography Image Storage": "CR",
    "Ultrasound Image Storage": "US",
    "Enhanced Ultrasound Image Storage": "USE",
    "X-Ray Angiographic Image Storage": "XA",
    "Enhanced XA Image Storage": "XAE",
    "Nuclear Medicine Image Storage": "NM",
    "Secondary Capture Image Storage": "SC",
}


class NotInBaselineError(KeyError):
    pass


def get_baseline_dict_entry(tag):
    """Vendored from ``pydicom.datadict``

    Return the tuple (VR, VM, name, is_retired, keyword) from the
    baseline DICOM dictionary.

    If the entry is not in the main dictionary, check the masked ones,
    e.g. repeating groups like 50xx, etc.
    """
    if not isinstance(tag, pydicom.tag.BaseTag):
        tag = pydicom.tag.Tag(tag)
    try:
        return get_baseline_dicom_dict()[tag]
    except KeyError:
        if not tag.is_private:
            mask_x = pydicom.datadict.mask_match(tag)
            if mask_x:
                return get_baseline_dicom_repeaters_dict()[mask_x]
        raise NotInBaselineError(
            "pydicom.tag.Tag {0} not found in DICOM dictionary".format(tag)
        )
