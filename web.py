import cherrypy
import redis
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
conn = redis.Redis("localhost")
class HelloWorld(object):
    @cherrypy.expose
    def index(self):
	tmpl = env.get_template('index.html')
	elements = conn.lrange( "top10namekeys", 0, -1 )
        return tmpl.render(elements = elements, conn = conn)
    @cherrypy.expose
    def greetUser(self, name=None):
        if name:
	    tmpl = env.get_template('index2.html')
            return tmpl.render(name = name, conn = conn)
        else:
            if name is None:
                # No name was specified
                return 'Please enter the right name <a href="./">here</a>.'

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
    
