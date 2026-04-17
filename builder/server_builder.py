class ServerBuilder:
    def __init__(self):
        self.listen_port = "80"
        self.locations = []

    def set_listen(self, port):
        self.listen_port = port
        return self

    def add_location(self, location):
        self.locations.append(location)
        return self

    def build(self):
        content = "server {\n"
        content += f"listen {self.listen_port};\n"
        content += """error_page 404 = @custom_404;
error_page 502 = @custom_502;
location @custom_404 {
    content_by_lua_block {
        ngx.status = 404
        ngx.header["Content-Type"] = "application/json"
        ngx.say('{"status":"FAILURE","response_code":404,"response_message":"Resource Not Found"}')
        return ngx.exit(404)
    }
}
location @custom_502 {
    content_by_lua_block {
        ngx.status = 502
        ngx.header["Content-Type"] = "application/json"
        ngx.say('{"status":"FAILURE","response_code":502,"response_message":"Service Unavailable"}')
        return ngx.exit(502)
    }
}"""
        for location in self.locations:
            content += location.build()
        content += "}"
        return content
