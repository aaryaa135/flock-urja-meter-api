"""Tests for the transformer service layer (mocked portal client, no live access)."""

import pytest

from app.portal.client import PortalClientError
from app.portal.models import TransformerListResponse
from app.service.transformer_service import list_transformers


def test_list_transformers_success(mock_portal_client, sample_transformer_list_response):
    """list_transformers should parse a valid portal response."""
    mock_portal_client.get.return_value.json.return_value = (
        sample_transformer_list_response.model_dump()
    )
    mock_portal_client.get.return_value.status_code = 200

    result = list_transformers(mock_portal_client, page=1)

    assert isinstance(result, TransformerListResponse)
    assert len(result.data) == 1
    assert result.data[0].code == "DT-001"
    assert result.data[0].name == "Malviya Nagar DT 1"
    assert result.data[0].feederCode == "F-001"
    assert result.data[0].capacityKva == 100

    mock_portal_client.get.assert_called_once()
    call_args = mock_portal_client.get.call_args
    assert "/portal/dts" in call_args.args[0]


def test_list_transformers_http_error(mock_portal_client):
    """list_transformers should raise PortalClientError on HTTP error status."""
    mock_portal_client.get.return_value.status_code = 500

    with pytest.raises(PortalClientError):
        list_transformers(mock_portal_client, page=1)


def test_list_transformers_invalid_json(mock_portal_client):
    """list_transformers should raise PortalClientError on invalid JSON."""
    mock_portal_client.get.return_value.status_code = 200
    mock_portal_client.get.return_value.json.side_effect = ValueError("bad json")

    with pytest.raises(PortalClientError):
        list_transformers(mock_portal_client, page=1)


def test_list_transformers_invalid_page(mock_portal_client):
    """list_transformers should raise ValueError for invalid page."""
    with pytest.raises(ValueError):
        list_transformers(mock_portal_client, page=0)
