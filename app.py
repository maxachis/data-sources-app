from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.User import User
from resources.QuickSearch import QuickSearch
from resources.AdvancedSearch import AdvancedSearch, AdvancedSearchOptions
from resources.DataSources import DataSources
from resources.Agencies import Agencies
from resources.Archives import Archives
from middleware.initialize_psycopg2_connection import initialize_psycopg2_connection

psycopg2_connection = initialize_psycopg2_connection()

app = Flask(__name__)
api = Api(app)
CORS(app)

api.add_resource(User, '/user', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(QuickSearch, '/quick-search/<search>/<location>', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(Archives, '/archives', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(AdvancedSearch, '/advanced-search', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(AdvancedSearchOptions, '/advanced-search-options', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(DataSources, '/data-sources', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})
api.add_resource(Agencies, '/agencies/<page>', resource_class_kwargs={'psycopg2_connection': psycopg2_connection})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
