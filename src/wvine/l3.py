# -*- coding: utf-8 -*-
# Module: widevine_keys
# Created on: 10.12.2021
# Authors: medvm
# Version: 2.1.0

import base64
import json
import requests
from base64 import b64encode
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

from .cdm import cdm, deviceconfig
from .cdm.formats import wv_proto2_pb2 as wv_proto2
from .wvdecryptcustom import WvDecrypt

REQUEST_INTERVAL_IN_SEC = 2
PRINT_RESPONSE = False

_source_dir = Path(__file__).resolve().parent


def _parse_key(keys):
    if not keys:
        return None
    return keys[0].split(':')[-1]


def getkey(pssh, license_url, headers, cert_b64=None):
    """main func, emulates license request and then decrypt obtained license
    fileds that changes every new request is signature, expirationTimestamp, watchSessionId, puid, and rawLicenseRequestBase64 """

    params = urlparse(license_url).query

    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)

    raw_request = wvdecrypt.get_challenge()
    # request = b64encode(raw_request)
    # signature = cdm.hash_object

    responses = []
    # basic, mostly sites works
    responses.append(requests.post(url=license_url, headers=headers, data=raw_request, params=params))

    # some another sites support
    # responses.append(requests.post(url=lic_url, headers=headers, params=params, json={ "rawLicenseRequestBase64": str(request, "utf-8" ), }))

    sleep(REQUEST_INTERVAL_IN_SEC)

    for i, response in enumerate(responses):
        try:
            str(response.content, "utf-8")
        except UnicodeDecodeError:
            widevine_license = response
            if PRINT_RESPONSE:
                print(f'{chr(10)}license response status: {widevine_license}{chr(10)}')
            break
        else:
            if len(str(response.content, "utf-8")) > 500:
                widevine_license = response
                if PRINT_RESPONSE:
                    print(f'{chr(10)}license response status: {widevine_license}{chr(10)}')
                break

        if i == len(responses) - 1:
            print(f'{chr(10)}license response status: {response}')
            print(f'server reports: {str(response.content, "utf-8")}')
            print(f'server did not issue license, make sure you have correctly pasted all the required headers in the headers.py. Also check json/raw params of POST request.{chr(10)}')
            exit()

    lic_field_names = ['license', 'payload', 'getWidevineLicenseResponse']
    lic_field_names2 = ['license']

    open(Path(_source_dir, 'license_content.bin'), 'wb').write(widevine_license.content)

    license_b64 = ''
    try:
        if str(widevine_license.content, 'utf-8').find(':'):
            for key in lic_field_names:
                try:
                    license_b64 = json.loads(widevine_license.content.decode())[key]
                except:
                    pass
                else:
                    for key2 in lic_field_names2:
                        try:
                            license_b64 = json.loads(widevine_license.content.decode())[key][key2]
                        except:
                            pass
        else:
            license_b64 = widevine_license.content
    except:
        license_b64 = b64encode(widevine_license.content)

    wvdecrypt.update_license(license_b64)
    Correct, keys = wvdecrypt.start_process()
    if Correct:
        return _parse_key(keys)
    return None
