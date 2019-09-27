from typing import List
from fonz.client import LookerClient
from fonz.validators import SqlValidator


class Runner:
    """Runs validations and returns JSON-style dictionaries with validation results.

    Args:
        base_url: Base URL for the Looker instance, e.g. https://mycompany.looker.com.
        project: Name of the Looker project to use.
        branch: Name of the Git branch to check out.
        client_id: Looker API client ID.
        client_secret: Looker API client secret.
        port: Desired API port to use for requests.
        api_version: Desired API version to use for requests.

    Attributes:
        client: Looker API client used for making requests.

    """

    def __init__(
        self,
        base_url: str,
        project: str,
        branch: str,
        client_id: str,
        client_secret: str,
        port: int = 19999,
        api_version: float = 3.1,
    ):
        self.project = project
        self.client = LookerClient(
            base_url, client_id, client_secret, port, api_version
        )
        self.client.update_session(project, branch)

    def validate_sql(self, selectors: List[str], batch: bool = False) -> List[dict]:
        sql_validator = SqlValidator(self.client, self.project)
        sql_validator.build_project(selectors)
        errors = sql_validator.validate(batch)
        return [vars(error) for error in errors]