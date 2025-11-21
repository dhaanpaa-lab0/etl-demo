from abc import ABC, abstractmethod

from etl.core import EtlEnvironment


class BaseEtlStep(ABC):
    """Base class that all etl steps must inherit from."""

    # unique name for lookup
    name: str = "unnamed"

    @abstractmethod
    def run(self, env: EtlEnvironment):
        """Do the plugin's work."""
        raise NotImplementedError
