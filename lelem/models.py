
from .common import * # noqa: F403, F401

class ModelProperties(TypedDict):
    by: str
    default: Optional[bool]

class Model:
    def __init__(self, name: str, properties: ModelProperties):
        self.__dict__ = cast(Dict[str, Any], properties)
        try:
            self.full_name = self.name or name
        except:
            self.full_name = name
        self.name = name
        self.default = properties.get("default", False)

    def __repr__(self):
        return f"Model(name={self.name}, by={self.by}, default={self.default})"

class Models:
    def __init__(self, yaml_file: str = ROOT + "/models.yml"):
        self._yaml: Dict[str, ModelProperties] = {}
        self._models: Dict[str, Model] = {}
        self._yaml_file = yaml_file
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

    def print_table(self):
        from tabulate import tabulate

        table = [{"model": key, **value} for key, value in self._yaml.items()]
        print(tabulate(table, headers="keys", tablefmt="grid"))

def find_model(model_name):
    models = Models()
    model = models.match(model_name)
    if model == []:
        print(f"Error: no model matches {model_name}")
        exit(1)
    elif isinstance(model, list):
        matched_models = model
        for m in matched_models:
            if m.name == model_name:
                return m
        print(f"Error: more than one model match: {[model.name for model in model]}")
        exit(1)
    return model
