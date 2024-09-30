import os

import dotenv

dotenv.load_dotenv()

if not os.environ["TEST"]:
    print("TEST env var not found")
