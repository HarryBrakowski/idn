from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy import Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.apis.alchemy_base import Base
from src.model.frontend_types import aggrid_types


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
        info={"type": "text", "field": "name", "label": "Material Name", "maxLength": 25}
    )
    description: Mapped[str | None] = mapped_column(
        String(100), 
        info={"type": "largeText", "field": "description", "label": "Description", "maxLength": 100}
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





