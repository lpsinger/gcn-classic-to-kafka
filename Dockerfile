FROM python:3.10 AS build
ENV POETRY_VIRTUALENVS_CREATE false
RUN curl -sSL https://install.python-poetry.org | python -
COPY . /src
WORKDIR /src
RUN $HOME/.local/bin/poetry install --no-dev

FROM python:3.10-slim
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build /src/ /src/
COPY --from=build /usr/local/bin/gcn-classic-to-kafka /usr/local/bin/
ENTRYPOINT ["gcn-classic-to-kafka"]
USER nobody:nogroup
