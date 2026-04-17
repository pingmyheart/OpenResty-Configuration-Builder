class MethodBuilder:
    def __init__(self):
        self.method = "GET"
        self.lua_block = None
        self.proxy_pass = None
        self.rewrite = None

    def set_method(self, method):
        self.method = method
        return self

    def set_lua_block(self, lua_block):
        self.lua_block = lua_block
        return self

    def set_proxy_pass(self, proxy_pass):
        self.proxy_pass = proxy_pass
        return self

    def set_rewrite(self, rewrite):
        self.rewrite = rewrite
        return self

    def build(self):
        content = f"if ($request_method = {self.method}) " + "{\n"
        content += self.lua_block.build() if self.lua_block else ""
        content += f"rewrite {self.rewrite[0]} {self.rewrite[1]} break;\n" if self.rewrite else ""
        content += f"proxy_pass {self.proxy_pass};\n" if self.proxy_pass else ""
        content += "}\n"
        return content
