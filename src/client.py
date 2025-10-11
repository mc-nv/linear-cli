import os
from typing import Any, Dict, Optional

import requests


class LinearClient:
    BASE_URL = "https://api.linear.app/graphql"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("LINEAR_CLI_TOKEN")
        if not self.token:
            raise ValueError(
                "Linear API token required. Use --token or set LINEAR_CLI_TOKEN env var"
            )
        self.headers = {"Authorization": self.token, "Content-Type": "application/json"}

    def execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        response = requests.post(
            self.BASE_URL, json=payload, headers=self.headers, timeout=30
        )
        response.raise_for_status()
        data = response.json()
        if "errors" in data:
            errors = [error.get("message", str(error)) for error in data["errors"]]
            raise Exception(f"GraphQL errors: {', '.join(errors)}")
        return data

    def ping(self) -> bool:
        query = "{ viewer { id name email } }"
        try:
            result = self.execute_query(query)
            return "data" in result and "viewer" in result["data"]
        except Exception as e:
            raise Exception(f"Failed to connect to Linear API: {str(e)}")
