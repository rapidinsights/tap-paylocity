from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class PaylocityAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Paylocity WebLinkAPI."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Paylocity API.

        Returns:
            A dict with the request body
        """
        return {
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
            "grant_type": "client_credentials",
            "scope": "WebLinkAPI",  # Fixed scope as required by Paylocity.
        }

    @classmethod
    def create_for_stream(cls, stream) -> PaylocityAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint="https://api.paylocity.com/IdentityServer/connect/token",
            oauth_scopes="WebLinkAPI",  # Define the required scope here.
        )


class PaylocityNextGenAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for Paylocity NextGenAPI."""

    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the Paylocity API.

        Returns:
            A dict with the request body
        """
        return {
            "client_id": self.config["nextgen_client_id"],
            "client_secret": self.config["nextgen_client_secret"],
            "grant_type": "client_credentials",
            "scope": "",  # Fixed scope as required by Paylocity.
        }

    @classmethod
    def create_for_stream(cls, stream) -> PaylocityAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            auth_endpoint="https://dc1prodgwext.paylocity.com/public/security/v1/token",
            oauth_scopes="",  # Define the required scope here.
        )


