from flask import request
from flask_restful import Resource
from middleware.security import api_required
from utilities.convert_dates_to_strings import convert_dates_to_strings
import spacy
import requests
import json
import os
import datetime

class AdvancedSearch(Resource):
  def __init__(self, **kwargs):
    self.psycopg2_connection = kwargs['psycopg2_connection']
  
  @api_required
  def get(self):
    try:
        data_sources = {'count': 0, 'data': []}

        params = request.args.to_dict()

        conditions = ""
        search_string = ['name', 'description', 'supplying_entity', 'originating_entity']
        agency_search_keys = ['agency_name', 'state', 'county', 'municipality', 'agency_type', 'jurisdiction_type']
        for key, value in params.items():
            if key in search_string:
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(value)
                lemmatized_tokens = [token.lemma_ for token in doc]
                new_value = " ".join(lemmatized_tokens)
                conditions += f"data_sources.{key} ILIKE %{new_value}%"
            elif key in agency_search_keys:
                if key == "agency_name":
                  conditions += f"agencies.name = {value}"
                else:
                  conditions += f"agencies.{key} = {value}"
            else:
                conditions += f"data_sources.{key} = {value}"
            conditions += " AND "

        if 'records_not_online' not in params:
            conditions += "data_sources.records_not_online IS NOT TRUE AND "
        
        conditions += "data_sources.approved IS TRUE"

        print(conditions)
        cursor = self.psycopg2_connection.cursor()

        sql_query = """
            SELECT
                data_sources.name AS data_source_name,
                data_sources.description,
                data_sources.record_type,
                data_sources.source_url,
                data_sources.record_format,
                data_sources.coverage_start,
                data_sources.coverage_end,
                data_sources.agency_supplied,
                agencies.name AS agency_name,
                agencies.municipality,
                agencies.state_iso
            FROM
                agency_source_link
            INNER JOIN
                data_sources ON agency_source_link.airtable_uid = data_sources.airtable_uid
            INNER JOIN
                agencies ON agency_source_link.agency_described_linked_uid = agencies.airtable_uid
            WHERE
                
        """

        sql_query_with_conditions = sql_query + conditions

        cursor.execute(sql_query_with_conditions)

        results = cursor.fetchall()
        print(results)

        # column_names = ['data_source_name', 'description', 'record_type', 'source_url', 'record_format', 'coverage_start', 'coverage_end', 'agency_supplied', 'agency_name', 'municipality', 'state_iso']

        # data_source_matches = [dict(zip(column_names, result)) for result in results]

        # for item in data_source_matches:
        #    convert_dates_to_strings(item)

        # data_sources = {
        #     "count": len(data_source_matches),
        #     "data": data_source_matches
        # }

        # current_datetime = datetime.datetime.now()
        # datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # query_results = json.dumps(data_sources['data'])

        # cursor_query_log = self.psycopg2_connection.cursor()
        # sql_query_log = "INSERT INTO quick_search_query_logs (search, location, results, result_count, datetime_of_request) VALUES (%s, %s, %s, %s, %s)"
        # cursor_query_log.execute(sql_query_log, (search, location, query_results, data_sources['count'], datetime_string))
        # self.psycopg2_connection.commit()

        return data_sources
        
    except Exception as e:
        print(str(e))
        # webhook_url = os.getenv('WEBHOOK_URL')
        # message = {'content': 'Error during quick search operation: ' + str(e) + "\n" + f"Search term: {search}\n" + f'Location: {location}'}
        # requests.post(webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"})
        return data_sources
