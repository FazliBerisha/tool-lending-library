# tests/test_review_service.py
import pytest
from unittest.mock import MagicMock
from app.services.review_service import ReportService

@pytest.fixture
def mock_db_session():
    """Fixture to mock the SQLAlchemy database session."""
    return MagicMock()

def test_most_borrowed_tools(mock_db_session):
    # Mock the query result
    mock_db_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [
        ("Drill", 10),
        ("Hammer", 8),
    ]

    # Call the service method
    result = ReportService.most_borrowed_tools(mock_db_session, limit=5)

    # Assert the result
    assert result == [
        {"tool_name": "Drill", "borrow_count": 10},
        {"tool_name": "Hammer", "borrow_count": 8},
    ]

    # Verify query calls
    mock_db_session.query.assert_called()
    mock_db_session.query.return_value.join.assert_called()

def test_least_borrowed_tools(mock_db_session):
    # Mock the query result
    mock_db_session.query.return_value.join.return_value.filter.return_value.group_by.return_value.order_by.return_value.limit.return_value.all.return_value = [
        ("Wrench", 1),
        ("Saw", 2),
    ]

    # Call the service method
    result = ReportService.least_borrowed_tools(mock_db_session, limit=5)

    # Assert the result
    assert result == [
        {"tool_name": "Wrench", "borrow_count": 1},
        {"tool_name": "Saw", "borrow_count": 2},
    ]

    # Verify query calls
    mock_db_session.query.assert_called()
    mock_db_session.query.return_value.join.assert_called()
