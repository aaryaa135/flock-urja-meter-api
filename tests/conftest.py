"""Pytest configuration and shared fixtures."""

from unittest.mock import MagicMock

import pytest

from app.portal.client import PortalClient
from app.portal.models import (
    MeterRecord,
    MeterSearchResponse,
    TransformerListResponse,
    TransformerRecord,
)


@pytest.fixture
def mock_portal_client():
    """Return a mocked PortalClient."""
    client = MagicMock(spec=PortalClient)
    return client


@pytest.fixture
def sample_meter_record():
    """Return a sample verified meter record."""
    return MeterRecord(
        meterId="J100000",
        serialNo="SE33962",
        make="HPL",
        phaseType="single",
        installStatus="Decommissioned",
        dtCode="DT-001",
    )


@pytest.fixture
def sample_meter_search_response(sample_meter_record):
    """Return a sample verified meter search response."""
    return MeterSearchResponse(
        data=[sample_meter_record],
        page=1,
        pageSize=20,
        total=403,
    )


@pytest.fixture
def sample_transformer_record():
    """Return a sample verified transformer record."""
    return TransformerRecord(
        code="DT-001",
        name="Malviya Nagar DT 1",
        feederCode="F-001",
        capacityKva=100,
    )


@pytest.fixture
def sample_transformer_list_response(sample_transformer_record):
    """Return a sample verified transformer list response."""
    return TransformerListResponse(data=[sample_transformer_record])
