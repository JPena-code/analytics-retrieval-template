from sqlalchemy.engine import Engine

from ...models import BaseTable


def sync_hypertables(engine: Engine):
    pass


def create_hypertable(engine: Engine, model: type[BaseTable]):
    if model is None:
        raise ValueError("Model is required, cannot be None")
