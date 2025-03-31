
from .common import * # noqa: F403, F401

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SPACES = os.path.abspath(os.path.join(ROOT, "../llm-actor-spaces/spaces"))

class ModelProperties(TypedDict):
    by: str
    default: Optional[bool]

class Model:
    def __init__(self, name: str, properties: ModelProperties):
        self.__dict__ = cast(Dict[str, Any], properties)
        self.name = name
        self.full_name = str(properties.get("name", name))
        self.default = properties.get("default", False)

    def __repr__(self):
        return f"Model(name={self.name}, by={self.by}, default={self.default})"

class Models:
    def __init__(self, yaml_file: str = ROOT + "/models.yml"):
        self._yaml: Dict[str, ModelProperties] = {}
        self._models: Dict[str, Model] = {}
        with open(yaml_file, "r") as file:
            self._yaml = yaml.safe_load(file)

    def find(self, name: str) -> Optional[Model]:
        if name not in self._models:
            if name not in self._yaml:
                return None
            model = Model(name, self._yaml[name])
            self._models[name] = model
            return model
        return self._models.get(name)

    def match(self, name: str) -> Model | List[Model]:
        models = [Model(model, props) for model, props in self._yaml.items() if re.search(name, model)]
        if len(models) == 1:
            return models[0]
        return models
