from src.apis.alchemy_base import Base, engine, SessionLocal
from src.model.model import Material, MaterialSelectOption, Parameter, ParameterSelectOption, InputValue

# NOTE: 
#   execute as main (from backend): python -m src.model.init_data

def init_data():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        par_opts = [
            ParameterSelectOption(parameters_column_name='group', label='Mass Balance'), # id 1
            ParameterSelectOption(parameters_column_name='group', label='Quality Control'), # id 2...
            ParameterSelectOption(parameters_column_name='group', label='External Identifier'), # id 3...
            ParameterSelectOption(parameters_column_name='group', label='Process Parameter'), # id 4...
            ParameterSelectOption(parameters_column_name='group', label='Equipment'), # id 5...
            ParameterSelectOption(parameters_column_name='unit', label=''), # id 6
            ParameterSelectOption(parameters_column_name='unit', label='%'), # id 7
            ParameterSelectOption(parameters_column_name='unit', label='g/L'), # id 8
            ParameterSelectOption(parameters_column_name='unit', label='g'), # id 9
            ParameterSelectOption(parameters_column_name='unit', label='kg'), # id 10
            ParameterSelectOption(parameters_column_name='unit', label='L'), # id 11
        ]
        session.add_all(par_opts)
        session.commit()


        pars = [
            Parameter(type='number', group_id=1, name='Product Concentration', unit_id=8), #1
            Parameter(type='number', group_id=1, name='Intermediate Mass', unit_id=10), #2
            Parameter(type='number', group_id=1, name='Product Mass', unit_id=9), #3
            Parameter(type='number', group_id=2, name='Product Purity', unit_id=7), #4
            Parameter(type='date', group_id=4, name='Start Date of Execution', unit_id=6), #5
            Parameter(type='text', group_id=3, name='LIMS - Material ID', unit_id=6), #6
        ]
        session.add_all(pars)
        session.commit()


        mat_opts = [
            MaterialSelectOption(materials_column_name='project', label='Project A'), #1
            MaterialSelectOption(materials_column_name='project', label='Project B'), #2
            MaterialSelectOption(materials_column_name='department', label='Department A'), #3
            MaterialSelectOption(materials_column_name='procedure', label='Lab Experiment'), #4
            MaterialSelectOption(materials_column_name='procedure', label='Batch Manufacture'), #5
            MaterialSelectOption(materials_column_name='unit_procedure', label='Column Chromatography'), #6
            MaterialSelectOption(materials_column_name='unit_procedure', label='Dead End Filtration'), #7
            MaterialSelectOption(materials_column_name='unit_procedure', label='Tangential Flow Filtration'), #8
            MaterialSelectOption(materials_column_name='unit_procedure', label='Formulation'), #9
            MaterialSelectOption(materials_column_name='unit_procedure', label='Product Conditioning'), #10
            MaterialSelectOption(materials_column_name='operation', label='pH Adjustment'), #11
            MaterialSelectOption(materials_column_name='operation', label='Conductivity Adjustment'), #12
            MaterialSelectOption(materials_column_name='operation', label='Concentration Adjustment'), #13
            MaterialSelectOption(materials_column_name='operation', label='Chromatography - Elution'), #14
            MaterialSelectOption(materials_column_name='operation', label='Chromatography - Wash'), #15
            MaterialSelectOption(materials_column_name='operation', label='Product Transfer'), #16
            MaterialSelectOption(materials_column_name='operation', label='Additive Addition'), #17
            MaterialSelectOption(materials_column_name='operation', label='Temperature Adjustment'), #18
            MaterialSelectOption(materials_column_name='unit_procedure', label='Seed Train'), #19
            MaterialSelectOption(materials_column_name='unit_procedure', label='Batch Fermentation'), #20
            MaterialSelectOption(materials_column_name='unit_procedure', label='Fed Batch Fermentation'), #21
            MaterialSelectOption(materials_column_name='operation', label='Incubation'), #22
            MaterialSelectOption(materials_column_name='operation', label='Stirring'), #23
            MaterialSelectOption(materials_column_name='operation', label='Chromatography - Flowthrough'), #24
        ]
        session.add_all(mat_opts)
        session.commit()


        mats = [
            Material(project=1, department=3, procedure=5, unit_procedure=19, operation=22, name="Seed Train", description=""), #1
            Material(project=1, department=3, procedure=5, unit_procedure=21, operation=22, name="Harvest", description=""), #2
            Material(project=1, department=3, procedure=5, unit_procedure=7, operation=16, name="Clarified Harvest", description=""), #3
            Material(project=1, department=3, procedure=5, unit_procedure=6, operation=14, name="CHR Eluate", description=""), #4
            Material(project=1, department=3, procedure=5, unit_procedure=10, operation=17, name="Virus Inactivated Intermediate", description=""), #5
            Material(project=1, department=3, procedure=5, unit_procedure=6, operation=24, name="CHR Flowthrough", description=""), #6
            Material(project=1, department=3, procedure=5, unit_procedure=8, operation=13, name="TFF Concentrate", description=""), #7
            Material(project=1, department=3, procedure=5, unit_procedure=9, operation=17, name="Formulated Product", description=""), #8
        ]
        session.add_all(mats)
        session.commit()


        data = [
            # =========================================
            # Parameter 1: Product Concentration (g/L)
            # =========================================
            InputValue(material_id=1, parameter_id=1, value="0.50"),   # Seed Train
            InputValue(material_id=2, parameter_id=1, value="10.00"),  # Harvest
            InputValue(material_id=3, parameter_id=1, value="10.00"),  # Clarified Harvest
            InputValue(material_id=4, parameter_id=1, value="21.85"),  # CHR Eluate
            InputValue(material_id=5, parameter_id=1, value="21.96"),  # Virus Inactivated Intermediate
            InputValue(material_id=6, parameter_id=1, value="23.25"),  # CHR Flowthrough (Produkt)
            InputValue(material_id=7, parameter_id=1, value="53.70"),  # TFF Concentrate
            InputValue(material_id=8, parameter_id=1, value="40.00"),  # Formulated Product

            # =========================================
            # Parameter 2: Intermediate Mass (kg)
            # =========================================
            InputValue(material_id=1, parameter_id=2, value="200"),    # Seed Train
            InputValue(material_id=2, parameter_id=2, value="2000"),   # Harvest
            InputValue(material_id=3, parameter_id=2, value="1900"),   # Clarified Harvest
            InputValue(material_id=4, parameter_id=2, value="800"),    # CHR Eluate
            InputValue(material_id=5, parameter_id=2, value="780"),    # Virus Inactivated Intermediate
            InputValue(material_id=6, parameter_id=2, value="700"),    # CHR Flowthrough
            InputValue(material_id=7, parameter_id=2, value="300"),    # TFF Concentrate
            InputValue(material_id=8, parameter_id=2, value="400"),    # Formulated Product

            # =========================================
            # Parameter 3: Product Mass (g)
            # (calc: Conc × Mass;)
            # =========================================
            InputValue(material_id=1, parameter_id=3, value="100"),
            InputValue(material_id=2, parameter_id=3, value="20000"),
            InputValue(material_id=3, parameter_id=3, value="19000"),
            InputValue(material_id=4, parameter_id=3, value="17480"),
            InputValue(material_id=5, parameter_id=3, value="17130"),
            InputValue(material_id=6, parameter_id=3, value="16274"),
            InputValue(material_id=7, parameter_id=3, value="16111"),
            InputValue(material_id=8, parameter_id=3, value="15950"),

            # =========================================
            # Parameter 4: Product Purity (%)
            # =========================================
            InputValue(material_id=1, parameter_id=4, value="60"),   # Seed Train
            InputValue(material_id=2, parameter_id=4, value="80"),   # Harvest
            InputValue(material_id=3, parameter_id=4, value="80"),   # Clarified Harvest
            InputValue(material_id=4, parameter_id=4, value="90"),   # CHR Eluate
            InputValue(material_id=5, parameter_id=4, value="90"),   # Virus Inactivated Intermediate
            InputValue(material_id=6, parameter_id=4, value="95"),   # CHR Flowthrough (immer noch Produkt)
            InputValue(material_id=7, parameter_id=4, value="94"),   # TFF Concentrate
            InputValue(material_id=8, parameter_id=4, value="93"),   # Formulated Product

            # =========================================
            # Parameter 5: Start Date of Execution (Date)
            # =========================================
            InputValue(material_id=1, parameter_id=5, value="2024-01-01"),
            InputValue(material_id=2, parameter_id=5, value="2024-01-05"),
            InputValue(material_id=3, parameter_id=5, value="2024-01-07"),
            InputValue(material_id=4, parameter_id=5, value="2024-01-10"),
            InputValue(material_id=5, parameter_id=5, value="2024-01-12"),
            InputValue(material_id=6, parameter_id=5, value="2024-01-10"),
            InputValue(material_id=7, parameter_id=5, value="2024-01-15"),
            InputValue(material_id=8, parameter_id=5, value="2024-01-20"),

            # =========================================
            # Parameter 6: LIMS - Material ID (Text)
            # =========================================
            InputValue(material_id=1, parameter_id=6, value="LIMS-001"),
            InputValue(material_id=2, parameter_id=6, value="LIMS-002"),
            InputValue(material_id=3, parameter_id=6, value="LIMS-003"),
            InputValue(material_id=4, parameter_id=6, value="LIMS-004"),
            InputValue(material_id=5, parameter_id=6, value="LIMS-005"),
            InputValue(material_id=6, parameter_id=6, value="LIMS-006"),
            InputValue(material_id=7, parameter_id=6, value="LIMS-007"),
            InputValue(material_id=8, parameter_id=6, value="LIMS-008"),
        ]
        session.add_all(data)
        session.commit()
        
if __name__ == "__main__":
    init_data()
