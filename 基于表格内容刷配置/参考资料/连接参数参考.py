ip: str = "",
host: str = "",
username: str = "",
password: Optional[str] = None,
secret: str = "",
port: Optional[int] = None,
device_type: str = "",
verbose: bool = False,
global_delay_factor: float = 1.0,
global_cmd_verify: Optional[bool] = None,
use_keys: bool = False,
key_file: Optional[str] = None,
pkey: Optional[paramiko.PKey] = None,
passphrase: Optional[str] = None,
disabled_algorithms: Optional[Dict[str, Any]] = None,
disable_sha2_fix: bool = False,
allow_agent: bool = False,
ssh_strict: bool = False,
system_host_keys: bool = False,
alt_host_keys: bool = False,
alt_key_file: str = "",
ssh_config_file: Optional[str] = None,
#
# Connect timeouts
# ssh-connect --> TCP conn (conn_timeout) --> SSH-banner (banner_timeout)
#       --> Auth response (auth_timeout)
conn_timeout: int = 10,
# Timeout to wait for authentication response
auth_timeout: Optional[int] = None,
banner_timeout: int = 15,  # Timeout to wait for the banner to be presented
# Other timeouts
blocking_timeout: int = 20,  # Read blocking timeout
timeout: int = 100,  # TCP connect timeout | overloaded to read-loop timeout
session_timeout: int = 60,  # Used for locking/sharing the connection
read_timeout_override: Optional[float] = None,
keepalive: int = 0,
default_enter: Optional[str] = None,
response_return: Optional[str] = None,
serial_settings: Optional[Dict[str, Any]] = None,
fast_cli: bool = True,
_legacy_mode: bool = False,
session_log: Optional[SessionLog] = None,
session_log_record_writes: bool = False,
session_log_file_mode: str = "write",
allow_auto_change: bool = False,
encoding: str = "utf-8",
sock: Optional[socket.socket] = None,
auto_connect: bool = True,
delay_factor_compat: bool = False,
disable_lf_normalization: bool = False,