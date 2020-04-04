import cherrypy
import mysql.connector
from mysql.connector import errorcode
import os
from mako.template import Template
from mako.lookup import TemplateLookup


path = os.path.abspath(os.path.dirname(__file__))

lookup = TemplateLookup(directories=[os.path.join(path, 'html')])


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="luk610",
  database="siteril"
)



class MainPage(object):

    @cherrypy.expose
    def index(self):
        template = lookup.get_template('index.html')
        return template.render()

    index.exposed = True

    @cherrypy.expose
    def displaybycategory(self, category):
        template = lookup.get_template('carcategory.html')

        mycursor = mydb.cursor()

        payload = 'SELECT * FROM cars WHERE category=' + '"' + category + '"'

        mycursor.execute(payload)

        result = mycursor.fetchall()

        return template.render(mydata=result, categ=category)

    displaybycategory.exposed = True

    @cherrypy.expose
    def displaybymake(self, make):
        template = lookup.get_template('carmake.html')

        mycursor = mydb.cursor()

        payload = 'SELECT * FROM cars WHERE make=' + '"' + make + '"'

        mycursor.execute(payload)

        result = mycursor.fetchall()

        return template.render(mydata=result)

    displaybycategory.exposed = True

    @cherrypy.expose
    def about(self):
        template = lookup.get_template('about.html')
        return template.render()

    about.exposed = True

    @cherrypy.expose
    def contact(self):
        template = lookup.get_template('contact.html')
        return template.render()

    contact.exposed = True

    @cherrypy.expose
    def carinfo(self, info):
        mycursor = mydb.cursor()

        payload = 'SELECT * FROM cars WHERE id=' + '"' + info + '"'

        mycursor.execute(payload)

        result = mycursor.fetchone()

        print(result)

        template = lookup.get_template('carinfo.html')

        return  template.render(info=result)

    carinfo.exposed = True

if __name__ == '__main__':

    conf_path_root = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(conf_path_root, "config.conf")
    cherrypy.config.update(conf_path)

    cherrypy.tree.mount(MainPage(), '/', config=conf_path)
    cherrypy.engine.start()
    cherrypy.engine.block()