from abc import ABC, abstractmethod

from builder.method_builder import MethodBuilder


class Filter(ABC):
    def __init__(self, **kwargs):
        self.args = kwargs

    @abstractmethod
    def apply_filter(self, method: MethodBuilder):
        pass
