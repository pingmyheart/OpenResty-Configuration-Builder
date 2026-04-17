from builder.method_builder import MethodBuilder
from filters.filter import Filter


class ProxyPassFilter(Filter):
    def apply_filter(self, method: MethodBuilder):
        method.set_proxy_pass(self.args.get("uri"))
