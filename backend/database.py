from sqlmodel import create_engine, SQLModel
from models import Patient


sqlite_file_name = "patient_records.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    """Initializes the database and creates tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session