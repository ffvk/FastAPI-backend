from app.db.base import Base
from app.db.session import engine

def init_db():
    # Import all models to register them with SQLAlchemy
    from app.models import user
    Base.metadata.create_all(bind=engine)
