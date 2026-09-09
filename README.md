# student-ml-api

A minimal prediction API used to demonstrate a professional MLOps workflow:
feature branches, pull request validation, containerisation, and versioned
image publishing to a container registry.

## Endpoints

| Method | Path          | Purpose                                    |
| ------ | ------------- | ------------------------------------------ |
| GET    | `/`           | Welcome message and application version    |
| GET    | `/health`     | Health check with application and model versions |
| GET    | `/model-info` | Model name, version, and description       |
| GET    | `/version`    | Application and model versions             |
| POST   | `/predict`    | Returns the numeric input multiplied by 2  |

## Development workflow

Direct commits to `main` are not permitted. All changes reach `main` through a
pull request that must pass automated CI.

```
feature branch -> pull request -> CI -> review -> merge -> version tag -> release
```

## Versioning

The `VERSION` file is the single source of truth for the application version.
Pushing a semantic version tag (for example `v1.0.0`) triggers the release
workflow, which builds and publishes the Docker image to the registry.
