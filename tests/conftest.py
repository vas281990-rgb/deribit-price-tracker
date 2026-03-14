import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
 
@pytest.fixture
def mock_session():
    """
    Provides a mock DB session for unit testing.
    Isolates tests from the actual PostgreSQL instance to ensure they can run anywhere.
    """
    session = MagicMock(spec=AsyncSession)
    # spec=AsyncSession: Ensures the mock only allows valid AsyncSession methods.
    # If a non-existent method is called, the test will fail immediately.
    
    session.execute = AsyncMock()
    session.add = MagicMock()
    session.flush = AsyncMock()
    session.commit = AsyncMock()
    return session