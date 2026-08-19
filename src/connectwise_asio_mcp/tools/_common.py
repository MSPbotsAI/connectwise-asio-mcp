from .._json import error_envelope

NO_TOKEN = error_envelope(
    "not_configured",
    "No ConnectWise Asio access token. Send the X-ConnectWise-Asio-Token header.",
    False,
)
