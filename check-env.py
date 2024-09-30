import os
import sys

import config  # noqa

if not os.environ["TEST"]:
    print("TEST env var not found")
    sys.exit(1)

print("TEST", os.environ["TEST"])
