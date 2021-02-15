from jeweb import Jeweb

web = Jeweb()

class Index:
    def GET(self, header, addr):
        return "Hello! from %s:%s\n" % addr + \
            "You are visiting %s page\n" % header.url

    def POST(self, header, addr):
        return "What???\n"

@web.errorHandler(404)
def page_not_found(header, addr, e):
    return "404 Not Found!!!! \n at %s:%s\n" % addr

web.addHandler('/', Index)

web.run()
