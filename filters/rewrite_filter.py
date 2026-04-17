from builder.method_builder import MethodBuilder
from filters.filter import Filter


class RewriteFilter(Filter):
    def apply_filter(self, method: MethodBuilder):
        method.set_rewrite((self.args["regex"], self.args["replacement"]))
