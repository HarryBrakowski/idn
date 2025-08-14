from uuid import uuid4
from flask import request, jsonify
from src.apis.sqlite_api import SqliteApi
import src.model as model
from src.shared import path2db


def register_routes(app):
    @app.route("/api/v1/get-table", methods=["POST"])
    def get_table():
        data = request.json
        print("Received frontend data for api-call '/api/v1/get-table'")

        # get the data of interest
        with SqliteApi(path2db) as slapi:
            df = slapi.get_table(table='parameters')
            if df is not None:
                df = df.to_dict(orient='records')
            print(df)

        return jsonify(df)





    @app.route("/api/v1/save-manual-data", methods=["POST"])
    def save_manual_data():
        data = request.json
        print("Received frontend data for api-call '/api/v1/save-manual-data'", data)

        # bring rowData (ag grid rowData) in the form [{'material_id': 'id', 'parameter_id':'id', 'value':'id'}]
        row_data_reshaped = []
        for row in data['rowData']:
            for key,val in row.items():
                new_row = (
                    {'material_id': row['id'], 'parameter_id': key, 'value': str(val)} 
                        if key in data['parameters'] and (val is not None) and (val != "") # only valid parameter_ids AND actual values!
                        else None
                )

                if new_row:
                    row_data_reshaped.append(new_row)

        # get the data of interest
        with SqliteApi(path2db) as slapi:
            slapi.write_table(
                column_spec=model.gui_data_spec,
                row_data=row_data_reshaped, 
                table='gui_data',
                append=True
            )

            df = slapi.get_table(table='gui_data')
            print(df)

        return jsonify('recieved frontend data for api-call "/api/v1/save-manual-data"')
