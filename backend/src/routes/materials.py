from flask import request, jsonify
from src.model.model import Material, MaterialSelectOption
from src.apis.alchemy_base import SessionLocal



def register_routes(app):

    @app.route("/api/v1/materials/schema", methods=["GET"])
    def get_materials_schema():
        '''
        Get the aggrid schema defined via ORM - info argument
        '''
        schema = []

        with SessionLocal() as session:

            # get all selectable options for material definition
            opts_all = session.query(MaterialSelectOption).all()

            # dynamically construct the schema based on info argument in ORM object 'Material'
            for col in Material.__table__.columns:
                if col.info:
                    info = col.info.copy()

                    # handle select option population
                    if col.info.get('type') == 'select':

                        # filter for matching column_names
                        opts = {opt.id: opt.label for opt in opts_all if opt.materials_column_name==info['field']}

                        # construct the array of field-label dicts
                        info['options'] = [{'field': k, 'label': v} for k,v in opts.items()]
                    
                    schema.append(info)
        return jsonify(schema)



    @app.route("/api/v1/materials/submit-options", methods=["POST"])
    def submit_material_options():
        data = request.json
        print("Received frontend data for api-call '/api/v1/materials/submit-options': ", data)

        if data.get("rowData") is None:
            return jsonify('Error during api-call "/api/v1/materials/submit-options". rowData is "None".')

        new_options = []
        for row in data.get("rowData"):
            new_option = MaterialSelectOption(materials_column_name=row.get('material_feature'), label=row.get('option'))
            new_options.append(new_option)

        with SessionLocal() as session:
            session.add_all(new_options)
            session.commit()

        return jsonify('response from api-call "/api/v1/materials/submit-options"')



    @app.route("/api/v2/materials/register", methods=["POST"])
    def register_new_materials():
        data = request.json
        print("Received frontend data for api-call '/api/v2/materials/register': ", data)

        if data.get('rowData', None) is None:
            return jsonify('Error during api-call "/api/v2/materials/register". rowData is "None".')

        new_materials = []
        for row in data.get('rowData'):
            m = Material(
                project=row.get('project'),
                department=row.get('department'),
                procedure=row.get('procedure'),
                unit_procedure=row.get('unit_procedure'),
                operation=row.get('operation'),
                name=row.get('name'),
                description=row.get('description'),
                date=row.get('date')
            )
            new_materials.append(m)

        with SessionLocal() as session:
            session.add_all(new_materials)
            session.commit()

        return jsonify('response from api-call "/api/v2/materials/register"')
