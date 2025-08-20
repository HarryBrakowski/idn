from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apis.alchemy_base import Base, engine, SessionLocal
from src.model.frontend_types import aggrid_types

# NOTE: 
#   execute as main (from backend): python -m src.model.model


class Material(Base):
    '''
    NOTE: 
      MODEL + Frontend ALLOWs DYNAMIC CHANGES OF THE CORE META DATA MARKED BELOW
          --> But align with src.routes.materials "/api/v2/materials/register"
    
      info argument in each mapped_column: 
          - contains column definition for aggrid creation ('schema' Prop in 'frontend/src/components/grid/grid.jsx')
          - info.type: allows all options defined in 'frontend/src/shared-data/type-defs.js'
          - info.type = select
              --> this will automatically enable interactive definition of 'select options' in the resp. frontend-page
              --> database column type must be integer then (column will store 'MaterialSelectOption.id')
    '''
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(default=lambda: str(uuid4()), unique=True, index=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    # ---------- # Core Meta Data Start here
    project: Mapped[int] = mapped_column(
        Integer, 
        info={"type": "select", "field": "project", "label": "Project"}
    )
    department: Mapped[int] = mapped_column(
        Integer, 
        info={"type": "select", "field": "department", "label": "Department"}
    )
    procedure: Mapped[int] = mapped_column(
        Integer, 
        info={"type": "select", "field": "procedure", "label": "Procedure"}
    )
    unit_procedure: Mapped[int] = mapped_column(
        Integer, 
        info={"type": "select", "field": "unit_procedure", "label": "Unit Procedure"}
    )
    operation: Mapped[int] = mapped_column(
        Integer, 
        info={"type": "select", "field": "operation", "label": "Operation"}
    )
    name: Mapped[str] = mapped_column(
        String(30),
        info={"type": "text", "field": "name", "label": "Name", "maxLength": 25}
    )
    description: Mapped[str | None] = mapped_column(
        String(100), 
        info={"type": "largeText", "field": "description", "label": "Description", "maxLength": 100}
    )
    date: Mapped[str] = mapped_column(
        String(100), 
        info={"type": "date", "field": "date", "label": "Date of Execution"}
    )


class Parameter(Base):
    __tablename__ = "parameters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(default=lambda: str(uuid4()), unique=True, index=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    type: Mapped[str] = mapped_column(
        String(30), 
        info={
            "field": "type", 
            "label": "Data Type", 
            "type": "select", 
            "options": [t for t in aggrid_types if t["field"]!="select"] # statically set based on available aggrid types
        }
    )
    group_id: Mapped[int] = mapped_column( # uses parameters_select_options.id
        Integer, 
        info={"type": 'select', "field": 'group', "label": 'Parameter Group'}
    )
    name: Mapped[str] = mapped_column(
        String(30),
        info={"type": 'text', "field": 'name', "label": 'Parameter Name'}
        )
    unit_id: Mapped[int | None] = mapped_column( # uses parameters_select_options.id
        Integer, 
        info={"type": 'select', "field": 'unit', "label": 'Unit'}
    )



class MaterialSelectOption(Base):
    __tablename__ = "materials_select_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    materials_column_name: Mapped[str] = mapped_column(String(30)) # frontend ensures alignment with column names in 'materials' table
    label:Mapped[str] = mapped_column(String(30))


class ParameterSelectOption(Base):
    __tablename__ = "parameters_select_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    parameters_column_name: Mapped[str] = mapped_column(String(30)) # frontend ensures alignment with column names in 'parameters' table -- allowed: "group", "unit"
    label:Mapped[str] = mapped_column(String(30))



class InputValue(Base):
    __tablename__ = "input_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    parameter_id: Mapped[int] = mapped_column(ForeignKey("parameters.id"))
    value: Mapped[str | None] = mapped_column(String(50))

    __table_args__ = (
        Index("idx_timestamp", "timestamp"),
        Index("idx_material_parameter", "material_id", "parameter_id")
    )





def init_db():
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        par_opts = [
            ParameterSelectOption(parameters_column_name='group', label='Mass Balance'), # id 1
            ParameterSelectOption(parameters_column_name='group', label='Quality Control'), # id 2...
            ParameterSelectOption(parameters_column_name='group', label='External Identifier'),
            ParameterSelectOption(parameters_column_name='group', label='Process Parameter'),
            ParameterSelectOption(parameters_column_name='group', label='Equipment'),
            ParameterSelectOption(parameters_column_name='unit', label=''),
            ParameterSelectOption(parameters_column_name='unit', label='%'),
            ParameterSelectOption(parameters_column_name='unit', label='g/L'),
            ParameterSelectOption(parameters_column_name='unit', label='g'),
            ParameterSelectOption(parameters_column_name='unit', label='L'),
        ]
        session.add_all(par_opts)
        session.commit()

        pars = [
            Parameter(type='number', group_id=1, name='Product Mass', unit_id=9),
            Parameter(type='number', group_id=2, name='Product Purity', unit_id=7),
            Parameter(type='text', group_id=3, name='LIMS - Material ID', unit_id=6),
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
            Material(project=1, department=3, procedure=5, unit_procedure=19, operation=22, name="Seed Train", description="", date="2025-08-20"),
            Material(project=1, department=3, procedure=5, unit_procedure=21, operation=22, name="Harvest", description="", date="2025-08-25"),
            Material(project=1, department=3, procedure=5, unit_procedure=7, operation=16, name="Clarified Harvest", description="", date="2025-08-25"),
            Material(project=1, department=3, procedure=5, unit_procedure=6, operation=14, name="CHR Eluate", description="", date="2025-08-26"),
            Material(project=1, department=3, procedure=5, unit_procedure=10, operation=17, name="Virus Inactivated Intermediate", description="", date="2025-08-26"),
            Material(project=1, department=3, procedure=5, unit_procedure=6, operation=24, name="CHR Flowthrough", description="", date="2025-08-27"),
            Material(project=1, department=3, procedure=5, unit_procedure=8, operation=13, name="TFF Concentrate", description="", date="2025-08-27"),
            Material(project=1, department=3, procedure=5, unit_procedure=9, operation=17, name="Formulated Product", description="", date="2025-08-28"),
        ]
        session.add_all(mats)
        session.commit()
        
if __name__ == "__main__":
    init_db()