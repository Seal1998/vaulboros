![vauloborous](https://i.ibb.co/WVJv10K/f8faa1b0-c2c9-4dbf-8f62-8f81cad8f351-b9775f6a-0760-470a-83f0-74c76aded9f2.png)

## Basic usage example

```python
from vaulboros.vault import Vault

import datetime, asyncio

t1 = datetime.datetime.now()

v = Vault.from_token("http://127.0.0.1", "hvs.qwerty123") # url and token

l = v.get_kv_location("testsecrets", load_location=True, load_location_recursive=True)

t2 = datetime.datetime.now()

print(f"Sync loaded {l.number_of_secrets} secrets. Time - {t2-t1}")

t1 = datetime.datetime.now()

l = asyncio.run(v.a_get_kv_location("testsecrets", load_location=True, load_location_recursive=True))

t2 = datetime.datetime.now()

print(f"Async loaded {l.number_of_secrets} secrets. Time - {t2-t1}")
```

```
Sync loaded 337 secrets. Time - 0:00:57.609791
Async loaded 337 secrets. Time - 0:00:02.802920
```