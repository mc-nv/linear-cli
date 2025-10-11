import os
from typing import Any, Dict, Optional

import requests

from src.logger import get_logger


class LinearClient:
    BASE_URL = "https://api.linear.app/graphql"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("LINEAR_CLI_TOKEN")
        self.logger = get_logger()
        if not self.token:
            raise ValueError(
                "Linear API token required. Use --token or set LINEAR_CLI_TOKEN env var"
            )
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}
        self.logger.debug("LinearClient initialized")

    def execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        self.logger.debug(f"Executing GraphQL query: {query[:100]}...")
        self.logger.debug(f"Variables: {variables}")

        response = requests.post(
            self.BASE_URL, json=payload, headers=self.headers, timeout=30
        )
        response.raise_for_status()

        self.logger.debug(f"Response status: {response.status_code}")

        data = response.json()
        if "errors" in data:
            errors = [error.get("message", str(error)) for error in data["errors"]]
            self.logger.error(f"GraphQL errors: {errors}")
            raise Exception(f"GraphQL errors: {', '.join(errors)}")

        self.logger.info("Query executed successfully")
        return data

    def ping(self) -> bool:
        query = "{ viewer { id name email } }"
        try:
            result = self.execute_query(query)
            return "data" in result and "viewer" in result["data"]
        except Exception as e:
            raise Exception(f"Failed to connect to Linear API: {str(e)}")
