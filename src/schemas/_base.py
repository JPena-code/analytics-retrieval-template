from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

_CONFIG_MODEL: ConfigDict = {
    "extra": "forbid",
    "alias_generator": AliasGenerator(serialization_alias=to_camel),
}


class Base(BaseModel):
    """Base model with configuration class"""

    model_config = _CONFIG_MODEL
