class LocationBuilder:
    def __init__(self):
        self.location = ""
        self.directives = []
        self.methods = []

    def set_location(self, location):
        self.location = location
        return self

    def add_directive(self, key, value):
        self.directives.append((key, value))
        return self

    def add_method(self, method):
        self.methods.append(method)
        return self

    def build(self):
        content = f"location {self.location} " + "{\n"
        for directive, value in self.directives:
            content += f"{directive} {value};\n"
        for method in self.methods:
            content += method.build()
        content += "}\n"
        return content
