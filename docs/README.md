# cloudrun-fastapi Docs

- [Code Architecture](#code-architecture)
- [Local Development](#local-development)
- [Secrets Manager](#secrets-manager)
- [Run tests and CI checks locally](#run-tests-and-ci-checks-locally)
- [Working with Postgres](#working-with-postgres)
- [Docker and Google Container Registry](#docker-and-google-container-registry)
- [Cloud Build, Deployment, running a live Cloud Run service](#cloudbuild-deployment-running-a-live-cloud-run-service)
- [DNS Setup with Managed Domain Mappings](#dns-setup-with-managed-domain-mappings)
- [Google Cloud Scheduler Integration](google-cloud-scheduler-Integration)
- [Google Cloud Pub Sub Integration](google-cloud-pub-sub-integration)

Future Features:
- Login With Google & Other OAuth Proviers <!-- https://medium.com/data-rebels/fastapi-google-as-an-external-authentication-provider-3a527672cf33 -->

#### Code Architecture

```sh
.
├── alembic                 # alembic migrations and configs
│   └── versions            # alembic migrations
├── docs                    # all markdown documentation and sample scripting
├── tests                   # tests and related general test configs
│   └── v1                  # tests for v1 api
└── v1                      # v1 api
│   ├── daos                # data access objects for interfacing with datastores and 3rd party data sources
│   ├── routers             # actual http route definitions that pass http data requests to services
│   ├── schemas             # data definitions for routers, services, and daos
│   └── services            # middle layer that abstracts daos from routers
├── .coveragerc             # Coverage configuration
├── .dockerignore           # Files to ignore in docker images
├── .editorconfig           # Editor configuration to automatically format files
├── .flake8                 # flake8 configuration
├── Dockerfile              # Docker configuration used by cloudbuild.yaml
├── alembic.ini             # Configuration for Alembic migrations
├── cloudbuild.yaml         # Configuration for Google Build
├── cloudbuild-pytest.yaml  # Configuration for PR testing Google Build
├── config.py               # general api configurations
├── database.py             # database connection specs
├── gunicorn_config.py      # Configuration for production Gunicorn server
├── LICENSE                 # License
├── main.py                 # api entrypoint
├── models.py               # database orm models
├── mypy.ini                # mypy configuration
├── poetry.lock             # Depedency lock file
├── poetry.toml             # Poetry settings
├── pyproject.toml          # Project and CI/CD settings
├── README.md               # README


```


#### Local Development

```sh
# Install poetry, install requirements, and enter virtual environment
install poetry && poetry install && poetry shell
# running with uvicorn, recommended for development
uvicorn main:api --reload
# running with gunicorn, recommended for production
gunicorn main:api -c gunicorn_config.py
```

#### Secrets Manager

When working across multiple projects and accounts in GCP, it's suggested that you reauth with the following command `gcloud auth application-default login` when working with GCP Secrets Manager locally.

Remotely, you will have to configure the Cloud Run and Cloud Build service accounts to have Secret Manager Secret Accessor permissions. In this example we are using the default Compute (GCE) service account for Cloud Run services.

#### Run tests and CI checks locally

```sh
# Unit/coverage testing
poetry run pytest

# Styling
poetry run flake8 v1/ tests/ main.py models.py

# Formatting
poetry run black .

# Type hinting
poetry run mypy
```

#### Working with Postgres

We are using alembic to facilitate migrations with PostgreSQL. As this template stands, we are using the default user `postgres` and database `postgres`. We suggest you use your own user, password, and database for production.

To create your migrations locally:

```sh
# create the migration
PYTHONPATH=. alembic revision --autogenerate -m "initial setup"
# apply the migration
PYTHONPATH=. alembic upgrade head
# view history
PYTHONPATH=. alembic current -vvv
PYTHONPATH=. alembic history -vvv
```

To create your migrations on a cloudsql instance:

```sh
cloud_sql_proxy -instances=PROJECT_ID:REGION:INSTANCE_NAME -dir=/tmp/cloudsql
# then run the commands as listed above
```

If you want to directly connect to the remote database, while the proxy is running in one session, run the following command in another shell session:

```sh
psql "sslmode=disable host=/tmp/cloudsql/PROJECT_ID:REGION:INSTANCE_NAME user=postgres dbname=postgres"
```

#### Docker and Google Container Registry

This is handled by Cloud Build, but incase you'd like to do this without Cloud Build:

```sh
docker build -t us.gcr.io/$PROJECT_ID/cloud_run_fastapi .
docker run -p 8000:8000 -it us.gcr.io/$PROJECT_ID/cloud_run_fastapi:latest
docker push us.gcr.io/$PROJECT_ID/cloud_run_fastapi
```

#### CloudBuild, Deployment, running a live Cloud Run service

To deploy this API to Cloud Run, you will need to have the following

- [Create GitHub app triggers](https://cloud.google.com/cloud-build/docs/automating-builds/create-github-app-triggers) which will trigger the build process as noted in `cloudbuild.yaml`.
- Have a PostgreSQL instance created in GCP that you will use for the service. There is no demo instance created as there is no free tier for Cloud SQL PSQL 😔. This instance will have to be referenced in the Cloud Run deployment in the `--set-cloudsql-instances` argument which is specified with a sample value in the `cloudbuild.yaml` template.
- Additionally, replace the service account value with the appropriate service account address for the `--service-account` parameter in the cloud run deploy command in `cloudbuild.yaml`


#### DNS Setup with Managed Domain Mappings

In `cloudbuild.yaml` there is a step called `"create google cloud infrastructure"` which shows how to create a domain name mapping for a cloud run service.
You will have to place a substitution variable in the cloud build trigger for your api (`_MY_DOMAIN` as mentioned in `cloudbuild.yaml`).


#### Google Cloud Scheduler Integration

In `cloudbuild.yaml` there is a step called `"create google cloud infrastructure"` which deploys a google cloud scheduler job to make HTTP requests to an endpoint you provide. You will have to place a substitution variable in the cloud build trigger for your api (`_MY_DOMAIN` as mentioned in `cloudbuild.yaml`).

#### Google Cloud Pub Sub Integration

In `cloudbuild.yaml` there is a step called `"create google cloud infrastructure"` which deploys pubsub topic and subscription that are utilized by the `routers/pubsub.py` router. You will have to place a substitution variable in the cloud build trigger for your api (`_SERVICE_ACCOUNT_ADDRESS` as mentioned in `cloudbuild.yaml`). That service account should be able to create tokens and be authorized as a pubsub service account.
