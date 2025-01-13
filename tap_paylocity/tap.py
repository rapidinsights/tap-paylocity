"""Paylocity tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_paylocity import streams


class TapPaylocity(Tap):
    """Paylocity tap class."""

    name = "tap-paylocity"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=True,  # Mark as protected to hide sensitive information.
            title="Client ID",
            description="The client ID for OAuth2 authentication.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,  # Mark as protected to hide sensitive information.
            title="Client Secret",
            description="The client secret for OAuth2 authentication.",
        ),
        th.Property(
            "company_id",
            th.StringType,
            required=True,
            title="Company ID",
            description="The unique company ID",
        ),
        # th.Property(
        #     "project_ids",
        #     th.ArrayType(th.StringType),
        #     required=True,
        #     title="Project IDs",
        #     description="Project IDs to replicate",
        # ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            description="The latest record date to sync",
        ),
        th.Property(
            "user_agent",
            th.StringType,
            description=(
                "A custom User-Agent header to send with each request. Default is "
                "'<tap_name>/<tap_version>'"
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.PaylocityStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.EmployeesStream(self),
            streams.EmployeeDetailsStream(self),
            streams.PunchDetails(self),
        ]


if __name__ == "__main__":
    TapPaylocity.cli()
