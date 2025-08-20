from flask import request, jsonify
from src.model.model import Parameter, ParameterSelectOption
from src.apis.alchemy_base import SessionLocal

def register_routes(app):

    @app.route("/api/v1/parameters/schema", methods=["GET"])
    def get_parameters_schema():
        '''
        Get the aggrid schema defined via ORM - info argument
        '''
        schema = []

        with SessionLocal() as session:
            opts_all = session.query(ParameterSelectOption).all()

            for col in Parameter.__table__.columns:
                if col.info:
                    info = col.info.copy()

                    # handle select option population -- thereby ignore the 'type' column that is already defined in model.py
                    if col.info.get('type') == 'select' and col.info.get('field') != 'type':

                        # filter for matching column_names
                        opts = {opt.id: opt.label for opt in opts_all if opt.parameters_column_name==info['field']}

                        # construct the array of field-label dicts
                        info['options'] = [{'field': k, 'label': v} for k,v in opts.items()]
                    
                    schema.append(info)
        return jsonify(schema)


    @app.route("/api/v1/parameters/table", methods=["GET"])
    def get_parameters_table():
        rowData = []
        with SessionLocal() as session:
            parameters = session.query(Parameter).all()
            details = session.query(ParameterSelectOption).all()
            option_map = {d.id: d.label for d in details}

            for p in parameters:
                row = p.to_dict()

                # match the unit and group ids with the actual label from "parameters_select_options"
                # and construct the field + label for proper frontend processing
                row['unit'] = option_map.get(p.unit_id, "")
                row['group'] = option_map.get(p.group_id, "")
                row['field'] = p.id, 
                row['label'] = f"{p.name} [{row['unit']}]" if row['unit'] else f"{p.name}"

                rowData.append(row)
        return jsonify(rowData)


    @app.route("/api/v1/parameters/submit-options", methods=["POST"])
    def submit_parameter_options():
        data = request.json
        print("Received frontend data for api-call '/api/v1/parameters/submit-options': ", data)

        if data.get("rowData") is None:
            return jsonify('Error during api-call "/api/v1/parameters/submit-options". rowData is "None".')

        new_options = []
        for row in data.get("rowData"):
            new_option = ParameterSelectOption(parameters_column_name=row.get('parameter_feature'), label=row.get('option'))
            new_options.append(new_option)

        with SessionLocal() as session:
            session.add_all(new_options)
            session.commit()

        return jsonify('response from api-call "/api/v1/parameters/submit-options"')


    @app.route("/api/v2/parameters/register", methods=["POST"])
    def register_new_parameters():
        data = request.json
        print("Received frontend data for api-call '/api/v2/parameters/register': ", data)

        if data.get('rowData', None) is None:
            return jsonify('Error during api-call "/api/v2/parameters/register". rowData is "None".')

        new_parameters = []
        for row in data.get('rowData'):
            p = Parameter(type=row.get('type'), group_id=row.get('group'), name=row.get('name'), unit_id=row.get('unit'))
            new_parameters.append(p)

        with SessionLocal() as session:
            session.add_all(new_parameters)
            session.commit()

        return jsonify('response from api-call "/api/v2/parameters/register"')



