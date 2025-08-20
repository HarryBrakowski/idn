from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from sqlalchemy import create_engine, and_
from src.shared import db_path


# Connection
engine = create_engine(f"sqlite+pysqlite:///{db_path}", echo=True)

# Session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

# Base Model
class Base(DeclarativeBase):
    def to_dict(self) -> dict:
        """
        Convert the ORM object to a dictionary with following structure:
            row = {
                "col1": value,
                "col2": value,
                ...
            }
        """
        return {col.name:getattr(self, col.name) for col in self.__table__.columns}
    
    @classmethod
    def from_dict(cls, row: dict[str, any]):
        """
        Construct ORM object from a dictionary representing the datatable's row.

        Arguments:
            :cls: the ORM object / class
            :row: the current table row in this form:
                row = {
                    "col1": value,
                    "col2": value,
                    ...
                }
        """
        # get the table columns of the specified ORM object
        valid_keys = {c.name for c in cls.__table__.columns}

        # extract only the matching columns from row
        cleaned = {k: v for k, v in row.items() if k in valid_keys}

        return cls(**cleaned)


    @classmethod
    def dynamic_AND_filter(cls, criteria: dict[str, any]):
        """
        Build a dynamic filter to be used are simple argument within .filter().
        
        Arguments:
            :criteria: matches column-names with the respective values
        """
        # filter for valid selections && filter out keys that are no valid columns in 'materials'
        column_names = {c.name for c in cls.__table__.columns}
        valid_criteria = {k:v for k,v in criteria.items() if v and (k in column_names)}

        if len(valid_criteria) == 0:
            return None

        # logic orm filter content
        orm_filter = [getattr(cls, k)==v for k,v in valid_criteria.items()]
        return and_(*orm_filter)
