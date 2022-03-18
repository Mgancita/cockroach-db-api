"""Project configurations."""

import logging
import sys
from typing import Union

from environ import Env
from fastapi.security import OAuth2PasswordBearer
from google.cloud import secretmanager_v1beta1 as secretmanager  # type: ignore
from google.cloud.logging import Client, Logger, Resource

from v1.schemas import PropertyBaseModel


class SecretsConfig(PropertyBaseModel):
    """Base class for secrets."""

    SECRET_KEY: str = "thesecretsauce"
    DATABASE_URL: str = "'cockroachdb://root@localhost:26257/defaultdb?sslmode=disable'"
    TEST_DATABASE_NAME: str = "testdb"

    @property
    def TEST_URL(self) -> str:
        """Return the test database URL."""
        return self.DATABASE_URL.replace("api", self.TEST_DATABASE_NAME)


class Config:
    """Base class for various configurations."""

    def get_logger(self, project_id: str) -> Union[logging.Logger, Logger]:
        """Get application logger."""
        if project_id:
            logging_client = Client()
            return logging_client.logger("run.googleapis.com%2Fpython")

        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        return logging.getLogger(__name__)

    def get_resource(self, project_id: str, service_name: str) -> Resource:
        """Get GCP resource."""
        return Resource(
            type="cloud_run_revision",
            labels={"project_id": project_id, "service_name": service_name},
        )

    def build_secrets_config(self, project_id: str = "") -> SecretsConfig:
        """Build a SecretsConfig instance.

        Args:
            project_id (str, optional): The project ID on GCP. Defaults to "".

        Returns:
            SecretsConfig: An instance of SecretsConfig populated with values.

        """
        result = SecretsConfig()
        if not project_id:
            return result

        secrets_client = secretmanager.SecretManagerServiceClient()
        for secret_id in ["SECRET_KEY", "DATABASE_URL", "TEST_DATABASE_NAME"]:
            version_path = secrets_client.secret_version_path(project_id, secret_id, "latest")
            secret_version = secrets_client.access_secret_version(version_path)
            secret_data = secret_version.payload.data.decode("UTF-8")
            setattr(result, secret_id, secret_data)
        return result


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")

env = Env()
project_id = env("PROJECT_ID", default="")
service_name = env("SERVICE_NAME", default="cockroach-db-api")

testing = "pytest" in "".join(sys.argv)

c = Config()
logger = c.get_logger(project_id)
resource = c.get_resource(project_id, service_name)

# if running in a project, cloud run or cloud build
apisecrets = c.build_secrets_config(project_id)
