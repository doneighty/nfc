import sys

try:
    from config import SDM_MASTER_KEY
except:
    # this is ok
    pass
else:
    print("WARNING! Detected SDM_MASTER_KEY configuration variable. "
          "This refers to the obsolete key derivation algorithm. If you are relying on the"
          "old algorithm, please downgrade sdm-backend to older version.")
    sys.exit(1)
