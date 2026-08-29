from app.models.document_model import Document
from app.models.user_model import User


def test_models_can_be_imported_without_circular_import():
    assert Document.__tablename__ == "documents"
    assert User.__tablename__ == "users"
