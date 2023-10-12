from flask import request
from flask_restful import Resource
from middleware.security import api_required
from utilities.convert_dates_to_strings import convert_dates_to_strings
from utilities.common import transform_string_array_to_array
import spacy
import json

class AdvancedSearch(Resource):
  def __init__(self, **kwargs):
    self.psycopg2_connection = kwargs['psycopg2_connection']
  
  @api_required
  def get(self):
    try:
        data_sources = {'count': 0, 'data': []}

        params = request.args.to_dict()

        conditions = ""
        search_string = ['name', 'description', 'supplying_entity', 'originating_entity', 'source_url']
        agency_search_keys = ['agency_name', 'state_iso', 'county_name', 'municipality', 'agency_type', 'jurisdiction_type']
        for key, value in params.items():
            if key in search_string:
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(value)
                lemmatized_tokens = [token.lemma_ for token in doc]
                new_value = " ".join(lemmatized_tokens)
                conditions += f"data_sources.{key} ILIKE '%{new_value}%'"
            elif key in agency_search_keys:
                if key == "agency_name":
                    conditions += f"agencies.name = '{value}'"
                elif key == "county_name":
                    conditions += f"agencies.county_name = '[\"{value}\"]'"
                else:
                    conditions += f"agencies.{key} = '{value}'"
            else:
                conditions += f"data_sources.{key} = '{value}'"
            conditions += " AND "

        if 'records_not_online' not in params:
            conditions += "data_sources.records_not_online IS NOT TRUE AND "
        
        conditions += "data_sources.approved IS TRUE"

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

        column_names = ['data_source_name', 'description', 'record_type', 'source_url', 'record_format', 'coverage_start', 'coverage_end', 'agency_supplied', 'agency_name', 'municipality', 'state_iso']

        data_source_matches = [dict(zip(column_names, result)) for result in results]

        for item in data_source_matches:
           convert_dates_to_strings(item)

        data_sources = {
            "count": len(data_source_matches),
            "data": data_source_matches
        }

        return data_sources
        
    except Exception as e:
        print(str(e))
        # webhook_url = os.getenv('WEBHOOK_URL')
        # message = {'content': 'Error during advanced search operation: ' + str(e) + "\n" + f"Query Params: {params}\n"}
        # requests.post(webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"})
        return data_sources

data_source_options = [
    "record_type",
    "access_type",
    "record_format",
    "agency_aggregation", # aggregation_type?
    "data_portal_type"
    # "access_restrictions" - doesn't exist in database
]

agency_options = [
    "name",
    "state_iso",
    "county_name",
    "municipality",
    "agency_type",
    "jurisdiction_type"
]

options_to_format = ['access_type', 'record_format', 'county_name']

class AdvancedSearchOptions(Resource): 
    def __init__(self, **kwargs):
        self.psycopg2_connection = kwargs['psycopg2_connection']
    
    @api_required
    def get(self):
        options = {}

        def format_result_options(results):
            consolidated_results = [result[0] for result in results if result[0] is not None]
            formatted_results = []
            for item in consolidated_results:
                formatted_results.append(transform_string_array_to_array(item))
            consolidated_formatted_results = [result[0] for result in formatted_results if result[0] is not None]
            unique_results = []
            for item in consolidated_formatted_results:
                if item not in unique_results:
                    unique_results.append(item)
            return unique_results
            
        def get_options_for_field(field, table):
            cursor = self.psycopg2_connection.cursor()
            cursor.execute('SELECT DISTINCT {} FROM {}'.format(field, table))
            results = cursor.fetchall()
            if field in options_to_format:
                unique_results = format_result_options(results)
                options[field] = unique_results
            else:
                consolidated_results = [result[0] for result in results if result[0] is not None]
                options[field] = consolidated_results

        try:
            for field in data_source_options:
                get_options_for_field(field, "data_sources")
            for field in agency_options:
                get_options_for_field(field, "agencies")

            return options
        except Exception as e:
            print(str(e))
            return options