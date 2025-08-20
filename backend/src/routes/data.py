from flask import request, jsonify
from sqlalchemy import and_, func
from src.model.model import Material, InputValue
from src.apis.alchemy_base import SessionLocal


def register_routes(app):
    @app.route("/api/v1/input-data/get", methods=["POST"])
    def get_input_data():
        data = request.json
        if data:
            selected_materials = data.get('selectedMaterials', None)
            selected_parameters = data.get('selectedParameters', {}).get('parameters', None)
            print("Received frontend data for api-call '/api/v1/input-data/get'")

        # early drop out if not data       
        if selected_materials is None or selected_parameters is None:
            print('Error during api-call "/api/v1/input-data/get". selectedMaterials and/or selectedParameters is None.')
            return []

        if len(selected_parameters) == 0:
            print('Early stop of api-call "/api/v1/input-data/get". Make valid parameter selections!.')
            return []

        # dynamically construct the logic filter -- to filter sql column vs selected value/id -- rather complex -- see Base Model
        material_filter = Material.dynamic_AND_filter(selected_materials)
        if material_filter is None:
            print('Early stop of api-call "/api/v1/input-data/get". Make valid material selections!.')
            return []



        # now get the data
        with SessionLocal() as session:
            # find the matching materials
            materials = session.query(Material).filter(material_filter).all()
            materials_row_data = [m.to_dict() for m in materials]

            # get the ids
            parameter_ids = [p['id'] for p in selected_parameters]
            material_ids = [m['id'] for m in materials_row_data]

            # subquery -- find the latest input data matching material_ids and parameter_ids
            subquery = (
                session
                    .query(
                        InputValue.material_id,
                        InputValue.parameter_id,
                        func.max(InputValue.timestamp).label("lts")
                    )
                    .filter(
                        and_(
                            InputValue.parameter_id.in_(parameter_ids),
                            InputValue.material_id.in_(material_ids)
                        )
                    )
                    .group_by(InputValue.material_id, InputValue.parameter_id)
                    .subquery()
            )

            # now actual data query -- join the latest timepoints with the original InputValue to get just the latest data
            input_data = (
                session
                .query(InputValue)
                .join(
                    subquery,
                    and_(
                        InputValue.material_id == subquery.c.material_id,
                        InputValue.parameter_id == subquery.c.parameter_id,
                        InputValue.timestamp == subquery.c.lts
                    )
                )
            ).all()
            input_data_row_data = [d.to_dict() for d in input_data]



        # now map the fetched input_data (if any) to the materials_rows_data
        row_data = []

        mapper = {
            (row.get('material_id', None), row.get('parameter_id', None)): row.get('value', None)
                for row in input_data_row_data
                if row.get('material_id') and row.get('parameter_id')
        }
        
        # actual mapping step
        for row in materials_row_data:
            material_id = row['id']

            for parameter_id in parameter_ids:
                # NOTE: Important to set None if there is no match
                row[str(parameter_id)] = mapper.get((material_id, parameter_id), None)
            
            row_data.append(row)

        
        if not row_data:
            print("No matching data found.")

        return jsonify(row_data)
    

    @app.route("/api/v1/input-data/submit", methods=["POST"])
    def submit_input_data():
        data:dict[str, list[dict] | list[int]] = request.json
        print("Received frontend data for api-call '/api/v1/input-data/submit'")

        # get the parameter ids as strings (from int)
        parameter_ids = [str(i) for i in data['parameters']]


        row_objects = []
        for pid in parameter_ids:
            for orow, nrow in zip(data['databaseRowData'], data['rowData']):
                # compare the previous database data with the new data
                old_val = str(orow.get(pid, 'Error')).strip() if orow.get(pid, 'Error') is not None else None
                new_val = str(nrow.get(pid)).strip() if nrow.get(pid) is not None else None

                # any missing pid means: parameters were selected without updating -- TODO: Frontend should also handle this problem
                if old_val == 'Error':
                    return jsonify('Error with api-call "/api/v1/input-data/submit". When selecting a new parameter re-update your data by clicking "Get your Data"')
                
                if (new_val != old_val):
                    print(f"detected changed value: {new_val}. For Material ID '{nrow['id']}' and Parameter ID '{pid}'")
                    # build the database row object
                    obj = InputValue(
                        material_id=nrow['id'], 
                        parameter_id=pid, 
                        value=new_val
                    )
                    row_objects.append(obj)

        with SessionLocal() as session:
            session.add_all(row_objects)
            session.commit()

        # return rowData
        return jsonify(data['rowData'])
