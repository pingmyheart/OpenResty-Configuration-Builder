FROM python:3.10-alpine
RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot

#Build Args
ARG SERVICE_VERSION
ARG SERVICE_NAME

# Service env variable
ENV ARTIFACT_NAME=$SERVICE_NAME
ENV ARTIFACT_VERSION=$SERVICE_VERSION

RUN mkdir -p /opt/$ARTIFACT_NAME

WORKDIR /opt/$ARTIFACT_NAME

COPY . .
RUN pip install -r requirements.txt

USER nonroot

ENTRYPOINT ["python3", "app.py"]