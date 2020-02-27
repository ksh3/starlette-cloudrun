# Starlette GCP CloudRun

## Local Setup

```
docker-compose up -d
pipenv install
pipenv shell
python main.py
```

## GCP Setup

- The following code must be borrowed from the community cloud builder and added to your container registry.
- Use kaniko.

`gcloud config set builds/use_kaniko True`

```
  # cloudbuild.yaml
  - id: "INJECT SERVICE"
    name: "docker/compose:1.19.0"
    args: ["up", "-d"]
  - id: "BUILD"
    name: gcr.io/kaniko-project/executor
    args:
      - "--destination=gcr.io/$PROJECT_ID/starlette-app:$TAG_NAME"
```
