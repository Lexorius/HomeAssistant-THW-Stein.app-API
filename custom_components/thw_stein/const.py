"""Global constants used by the THW‑Stein integration.

Only *key names* for configuration are stored here – **not** the user data itself.
Having them in a single place avoids hard‑coded strings and potential typos.
"""

DOMAIN = "thw_stein"

# Keys coming from Config‑Flow / Options‑Flow
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_BUNAME = "buname"            # Name der Business‑Unit / OV
CONF_SCAN_INTERVAL = "scan_interval"

# Default polling interval (seconds)
DEFAULT_SCAN_INTERVAL = 300
