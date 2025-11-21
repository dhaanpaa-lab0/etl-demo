import importlib
import inspect
import pkgutil

from .base import BaseEtlStep


def load_etl_steps():
    """Discover and instantiate all Plugin subclasses in this package."""
    etl_step_instances = {}

    # iterate over all modules in this package
    for finder, name, ispkg in pkgutil.iter_modules(__path__):
        if name == "base":
            continue  # skip base module

        module_name = f"{__name__}.{name}"
        module = importlib.import_module(module_name)

        # find classes that subclass Plugin
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseEtlStep) and obj is not BaseEtlStep:
                instance = obj()
                etl_step_instances[instance.name] = instance

    return etl_step_instances
