# Jeweb
**Author: Jeefy**  
**Email: jeefy163@163.com jeefyol@outlook.com**  
**Url: https://github.com/jeefies/jeweb**  

## A simple web frame work

*No dependences*  
*Wait for completing the docs, thanks...*

- - -
Usage:
```
from jeweb import Jeweb

web = Jeweb()

class Index:
	def GET(self, header, addr):
		return ("Hello %s:%s\n" % addr
			"This is Jeweb server.")

	def POST(self, header, addr):
		return "Ops, your method is %s" % header.method

web.addHandler('/', Index)

@web.handler('/url')
class Url:
	def GET(self, header, addr):
		return "Your are visiting %s" header.url

HOST = "0.0.0.0"
PORT = "8000"

@web.errorHandler(404)
def page_not_found(header, addr, e):
	assert e.status_code = 404
	return "Page Not Found"

def internal_server_error(header, addr):
	return "500 Internal Server Error"

web.addErrorHandler(500, internal_server_error)

web.run(HOST, PORT)
```
