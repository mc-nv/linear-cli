"""Linear API client."""

import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class LinearClient:
    """Client for interacting with the Linear API."""

    API_URL = "https://api.linear.app/graphql"

    def __init__(self, api_token: Optional[str] = None):
        """Initialize Linear client.

        Args:
            api_token: Linear API token. If not provided, reads from LINEAR_CLI_TOKEN env var.
        """
        self.api_token = api_token or os.getenv("LINEAR_CLI_TOKEN")
        if not self.api_token:
            raise ValueError(
                "Linear API token is required. "
                "Provide it via --token argument or LINEAR_CLI_TOKEN environment variable."
            )

        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
        }
        logger.debug("Linear client initialized")

    def _execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query.

        Args:
            query: GraphQL query string.
            variables: Query variables.

        Returns:
            Response data.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        logger.debug(f"Executing query: {query[:100]}...")

        response = requests.post(self.API_URL, json=payload, headers=self.headers)
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            error_messages = [
                error.get("message", "Unknown error") for error in data["errors"]
            ]
            raise Exception(f"GraphQL errors: {', '.join(error_messages)}")

        logger.debug("Query executed successfully")
        return data.get("data", {})

    def create_issue(
        self,
        title: str,
        description: Optional[str] = None,
        team_id: Optional[str] = None,
        priority: Optional[int] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create a new issue.

        Args:
            title: Issue title.
            description: Issue description.
            team_id: Team ID to create the issue in.
            priority: Issue priority (0-4).
            labels: List of label IDs.

        Returns:
            Created issue data.
        """
        query = """
        mutation IssueCreate($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    description
                    priority
                    url
                    state {
                        name
                    }
                }
            }
        }
        """

        input_data = {"title": title}

        if description:
            input_data["description"] = description
        if team_id:
            input_data["teamId"] = team_id
        if priority is not None:
            input_data["priority"] = priority
        if labels:
            input_data["labelIds"] = labels

        variables = {"input": input_data}

        logger.info(f"Creating issue: {title}")
        result = self._execute_query(query, variables)

        if result.get("issueCreate", {}).get("success"):
            logger.info("Issue created successfully")
            return result["issueCreate"]["issue"]
        else:
            raise Exception("Failed to create issue")

    def get_issue(self, issue_id: str) -> Dict[str, Any]:
        """Get an issue by ID.

        Args:
            issue_id: Issue ID or identifier.

        Returns:
            Issue data.
        """
        query = """
        query Issue($id: String!) {
            issue(id: $id) {
                id
                identifier
                title
                description
                priority
                url
                state {
                    name
                }
                assignee {
                    name
                    email
                }
                creator {
                    name
                    email
                }
                createdAt
                updatedAt
            }
        }
        """

        variables = {"id": issue_id}

        logger.info(f"Fetching issue: {issue_id}")
        result = self._execute_query(query, variables)

        return result.get("issue", {})

    def list_issues(
        self, team_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """List issues.

        Args:
            team_id: Filter by team ID.
            limit: Maximum number of issues to return.

        Returns:
            List of issues.
        """
        query = """
        query Issues($first: Int, $filter: IssueFilter) {
            issues(first: $first, filter: $filter) {
                nodes {
                    id
                    identifier
                    title
                    description
                    priority
                    url
                    state {
                        name
                    }
                    createdAt
                    updatedAt
                }
            }
        }
        """

        variables = {"first": limit}

        if team_id:
            variables["filter"] = {"team": {"id": {"eq": team_id}}}

        logger.info(f"Listing issues (limit: {limit})")
        result = self._execute_query(query, variables)

        return result.get("issues", {}).get("nodes", [])

    def search_issues(self, query_str: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search for issues.

        Args:
            query_str: Search query string.
            limit: Maximum number of results.

        Returns:
            List of matching issues.
        """
        query = """
        query SearchIssues($query: String!, $first: Int) {
            searchIssues(query: $query, first: $first) {
                nodes {
                    id
                    identifier
                    title
                    description
                    priority
                    url
                    state {
                        name
                    }
                    createdAt
                    updatedAt
                }
            }
        }
        """

        variables = {"query": query_str, "first": limit}

        logger.info(f"Searching issues: {query_str}")
        result = self._execute_query(query, variables)

        return result.get("searchIssues", {}).get("nodes", [])

    def get_my_issues(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get issues assigned to the current user.

        Args:
            limit: Maximum number of issues to return.

        Returns:
            List of issues assigned to the current user.
        """
        query = """
        query MyIssues($first: Int) {
            viewer {
                assignedIssues(first: $first) {
                    nodes {
                        id
                        identifier
                        title
                        description
                        priority
                        url
                        state {
                            name
                        }
                        dueDate
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """

        variables = {"first": limit}

        logger.info(f"Fetching your assigned issues (limit: {limit})")
        result = self._execute_query(query, variables)

        return result.get("viewer", {}).get("assignedIssues", {}).get("nodes", [])
