# wvine
Forked from https://github.com/medvm/widevine_keys

Must have your own device key files `device_private_key`, `device_client_id_blob` and put them on `src/wvine/cdm/devices/android_generic/`

### Installation
-----
```
pip install git+https://github.com/famgz/wvine.git
```

### Usage
-----
```
from wvine import getkey
pssh = YOUR_PSSH
license = YOUR_LICENSE
headers = YOUR_HEADERS
key = getkey(pssh, license, headers)
```
