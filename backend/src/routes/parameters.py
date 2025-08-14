from uuid import uuid4
from flask import request, jsonify
from src.apis.sqlite_api import SqliteApi
import src.model as model
from src.shared import path2db

def register_routes(app):
    @app.route("/api/v1/register-parameters", methods=["POST"])
    def register_parameters():
        data = request.json
        print("Received frontend data for api-call '/api/v1/register-parameters'")

        # add uuid to each row of rowData -- type to be included to set the correct sql column type within SqliteApi
        column_spec = data['schema'] + [{'type': 'text', 'field': 'id'}]
        row_data = data['rowData']
        for row in row_data:
            row['id'] = str(uuid4())

        # write data to sqlite database
        with SqliteApi(path2db) as slapi:
            slapi.write_table(
                column_spec=column_spec,
                row_data=row_data, 
                table='parameters',
                append=True
            )

            df = slapi.get_table(table='parameters')
            print(df)
        return jsonify('recieved frontend data for api-call "/api/v1/register-parameters"')
