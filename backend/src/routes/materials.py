from uuid import uuid4
from flask import request, jsonify
from src.apis.sqlite_api import SqliteApi
import src.model as model
from src.shared import path2db

def register_routes(app):

    @app.route("/api/v1/register-materials", methods=["POST"])
    def register_materials():
        data = request.json
        print("Received frontend data for api-call '/api/v1/register-materials'")

        # add uuid to each row of rowData
        column_spec = data['schema'] + [{'type': 'text', 'field': 'id'}]
        row_data = data['rowData']
        for row in row_data:
            row['id'] = str(uuid4())

        # write data to sqlite database
        with SqliteApi(path2db) as slapi:
            slapi.write_table(
                column_spec=column_spec,
                row_data=row_data, 
                table='materials',
                append=True
            )

            df = slapi.get_table(table='materials')
            print(df)
        return jsonify('recieved frontend data for api-call "/api/v1/register-materials"')



    @app.route("/api/v1/get-materials-and-data", methods=["POST"])
    def get_materials_and_data():
        data = request.json
        print("Received frontend data for api-call '/api/v1/get-materials-and-data'", data)

        # construct the json output
        output = {'materials': '', 'data': ''}

        # get the data of interest
        with SqliteApi(path2db) as slapi:
            # initialize the data table 'gui_data' - if not exists
            slapi.initialize_empty_table(
                table='gui_data',
                column_spec=model.gui_data_spec
            )

            # get the selected / matching materials first # TODO match with selected attributes
            df_materials = slapi.get_table(table='materials')

            if df_materials is not None:
                print('fetched materials dataframe', df_materials)
                output['materials'] = df_materials.to_dict(orient='records')


            # get the ids of interest
            material_ids = df_materials['id'].tolist() if df_materials is not None else []
            parameter_ids = [row['id'] for row in data['selectedParameters']['parameters']]

            # convert them to valid strings
            parameter_ids_sql = ", ".join(f"'{pid}'" for pid in parameter_ids)
            material_ids_sql = ", ".join(f"'{mid}'" for mid in material_ids)

            # then fetch all data matching these material_ids and the selected parameters
            columns = [
                "materials.*", 
                "gui_data.material_id", 
                "gui_data.parameter_id", 
                "gui_data.value", 
                "latest.max_ts"
            ]
            sql_filter = f"""
                LEFT JOIN
                    gui_data ON gui_data.material_id = materials.id
                INNER JOIN (
                    SELECT 
                        material_id, 
                        parameter_id, 
                        MAX(timestamp) AS max_ts
                    FROM gui_data
                        GROUP BY material_id, parameter_id
                ) latest
                    ON gui_data.material_id = latest.material_id
                    AND gui_data.parameter_id = latest.parameter_id
                    AND gui_data.timestamp = latest.max_ts
                WHERE
                    gui_data.parameter_id IN ({parameter_ids_sql}) AND
                    materials.id IN ({material_ids_sql})
            """
            df_data = slapi.get_table(table='materials', sql_filter=sql_filter, columns=columns)

            if df_data is not None:
                print('parameter data: ', df_data)
                output['data'] = df_data.to_dict(orient='records')

            cols = ['material_id', 'parameter_id', 'MAX(timestamp) AS max_ts']
            sql_filter = f"""WHERE timestamp IS NOT NULL GROUP BY material_id, parameter_id"""
            df_test = slapi.get_table(table='gui_data', sql_filter=sql_filter, columns=cols)
            print(df_test)

        return jsonify(output)