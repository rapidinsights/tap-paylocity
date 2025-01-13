"""Stream type classes for tap-paylocity."""

from __future__ import annotations

import typing as t
import requests

from datetime import datetime
from datetime import timedelta
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.pagination import BasePageNumberPaginator

from tap_paylocity.client import PaylocityStream, PaylocityNextGenStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"


class EmployeesStream(PaylocityStream):
    """Stream for retrieving all employees from Paylocity."""

    name = "employees"
    path = "/v2/companies/{companyId}/employees"
    primary_keys: t.ClassVar[list[str]] = ["employeeId"]
    replication_key = None  # Set to the appropriate field if incremental sync is supported

    schema = th.PropertiesList(
        th.Property("employeeId", th.StringType, description="Unique identifier for the employee."),
        th.Property("statusCode", th.StringType, description="Code for an employees current status"),
        th.Property("statusTypeCode", th.StringType, description="")
        # Add additional properties as per the API response
    ).to_dict()

    def get_new_paginator(self):
        return BasePageNumberPaginator(start_value=0)

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.
        
        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)

        params["companyId"] = self.config.get("company_id")

        if next_page_token:
            params["pagenumber"] = next_page_token


        return params

    def get_child_context(
        self,
        record: dict,
        context: dict | None,
    ) -> dict | None:
        """Returns a context object for child streams.

        Args:
            record: A record from this stream.
            context: The stream sync context.

        Returns:
            A context object for child streams.
        """
        return {
            "employeeId": record["employeeId"],
            "statusCode": record["statusCode"],
        }


class EmployeeDetailsStream(PaylocityStream):
    """Stream for retrieving employee details from Paylocity."""

    name = "employee_details"
    path = "/v2/companies/{companyId}/employees/{employeeId}"
    primary_keys: t.ClassVar[list[str]] = ["employeeId"]
    replication_key = None
    ignore_parent_replication_keys = True

    parent_stream_type = EmployeesStream

    schema = th.PropertiesList(
        th.Property("employeeId", th.StringType, description="Unique identifier fror the employee."),
        th.Property("firstName", th.StringType, description="Employee's first name."),
        th.Property("lastName", th.StringType, description="Employee's last name."),
        th.Property("employeeStatus", th.StringType, description="Emoloyee status code."),
        th.Property("annualSalary", th.NumberType, description="Employee annual salary."),
        th.Property("baseRate", th.NumberType, description="Employee base compensation rate."),
        th.Property("payType", th.StringType, description="Employee type of pay."),
        th.Property("ratePer", th.StringType, description="Rate of pay for base rate."),
        th.Property("payFrequency", th.StringType, description="How often employee is paid."),
        th.Property("jobTitle", th.StringType, description="Employee's job title."),
        th.Property("positionCode", th.StringType, description="Employee's position code."),
        th.Property("supervisorEmployeeId", th.StringType, description="Employee ID of supervisor."),
        th.Property("hireDate", th.DateTimeType, description="Date employee was hired."),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters.
        
        Args:
            context: Stream sync context.
            next_page_token: Next offset.

        Returns:
            A dictionary of URL query parameters.
        """
        params = super().get_url_params(context, next_page_token)

        params["companyId"] = self.config.get("company_id")
        params["employeeId"] = context["employeeId"]

        return params

    def post_process(
        self,
        row: dict,
        context: dict | None = None
    ) -> dict | None:
        """Post-process a row.

        Args:
            row: A row.
            context: The stream sync context.

        Returns:
            The processed row.

        """
        new_row = super().post_process(row, context)
        if new_row:

            new_row["employeeStatus"] = new_row.get("status", {}).get("employeeStatus")
            new_row["payType"] = new_row.get("primaryPayRate", {}).get("payTyp")
            new_row["annualSalary"] = new_row.get("primaryPayRate", {}).get("annualSalary")
            new_row["baseRate"] = new_row.get("primaryPayRate", {}).get("baseRate")
            new_row["ratePer"] = new_row.get("primaryPayRate", {}).get("ratePer")
            new_row["payFrequency"] = new_row.get("primaryPayRate", {}).get("payFrequency", "")
            
            new_row["jobTitle"] = new_row.get("departmentPosition", {}).get("jobTitle", "")
            new_row["positionCode"] = new_row.get("departmentPosition", {}).get("positionCode", "")
            new_row["supervisorEmployeeId"] = new_row.get("departmentPosition", {}).get("supervisorEmployeeId", "")
            new_row["hireDate"] = new_row.get("status", {}).get("hireDate")

        return new_row


class PunchDetails(PaylocityNextGenStream):
    """Stream for getting an Employee's PunchDetails."""

    name = "punch_details"
    path = "/apiHub/time/v1/companies/149471/employees/{employeeId}/punchDetails"
    primary_keys: t.ClassVar[list[str]] = ["employeeId", "relativeStart", "punchID"]
    # replication_key = "relativeEnd"
    ignore_parent_replication_keys = True

    parent_stream_type = EmployeesStream

    schema = th.PropertiesList(
        th.Property("employeeId", th.StringType, description="Unique identifier for the employee."),
        th.Property("badgeNumber", th.IntegerType, description="Badge number of the employee."),
        th.Property("relativeStart", th.DateTimeType, description="Start time for the worked shift."),
        th.Property("relativeEnd", th.DateTimeType, description="End time for the worked shift."),
        th.Property("punchID", th.StringType, description="Unique identifier for the punch."),
        th.Property("origin", th.StringType, description="Origin of the punch."),
        th.Property("date", th.DateType, description="Date of the punch."),
        th.Property("punchType", th.StringType, description="Type of punch (e.g., work, lunch)."),
        th.Property("relativeOriginalStart", th.DateTimeType, description="Original start time for the punch."),
        th.Property("relativeOriginalEnd", th.DateTimeType, description="Original end time for the punch."),
        th.Property("durationSeconds", th.IntegerType, description="Duration of the punch in seconds."),
        th.Property("earnings", th.NumberType, description="Earnings for the punch."),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: str | None,
    ) -> dict[str, t.Any]:
        """Get URL query parameters."""
        params = super().get_url_params(context, next_page_token)

        # Add fixed parameters
        params["companyId"] = self.config.get("company_id")
        params["employeeId"] = context["employeeId"]

        # Handle date ranges dynamically
        relative_start = self.config.get("start_date")
        relative_end = self.config.get("end_date") or datetime.now().isoformat()

        # Convert to ISO format for the API
        params["relativeStart"] = relative_start
        params["relativeEnd"] = relative_end

        return params

    def parse_response(self, response) -> t.Iterable[dict]:
        """Parse API responses into individual segment records."""
        if not response:
            return

        records = response.json()
        for record in records:
            if "relativeEnd" not in record:
                # This field must exist for tracking state through the replication key (relativeEnd)
                record["relativeEnd"] = record["segments"][0]["date"]
            for segment in record.get("segments", []):
                # Merge top-level keys with segment keys
                yield {
                    **{k: v for k, v in record.items() if k != "segments"},  # Exclude "segments"
                    **segment,  # Include individual segment details
                }


