"""Tests for the meter service layer (mocked portal client, no live access)."""

import pytest

from app.portal.client import PortalClientError
from app.portal.models import MeterSearchResponse
from app.service.meter_service import list_meters, search_meters


def test_search_meters_success(mock_portal_client, sample_meter_search_response):
    """search_meters should parse a valid portal response."""
    mock_portal_client.get.return_value.json.return_value = (
        sample_meter_search_response.model_dump()
    )
    mock_portal_client.get.return_value.status_code = 200

    result = search_meters(mock_portal_client, query="J100000", page=1, page_size=20)

    assert isinstance(result, MeterSearchResponse)
    assert result.page == 1
    assert result.pageSize == 20
    assert result.total == 403
    assert len(result.data) == 1
    assert result.data[0].meterId == "J100000"

    mock_portal_client.get.assert_called_once()
    call_args = mock_portal_client.get.call_args
    assert "/portal/meters/search" in call_args.args[0]


def test_search_meters_empty_results(mock_portal_client):
    """search_meters should handle zero results."""
    mock_portal_client.get.return_value.json.return_value = {
        "data": [],
        "page": 1,
        "pageSize": 20,
        "total": 0,
    }
    mock_portal_client.get.return_value.status_code = 200

    result = search_meters(mock_portal_client, query="NO_MATCH", page=1, page_size=20)

    assert result.total == 0
    assert result.data == []


def test_search_meters_http_error(mock_portal_client):
    """search_meters should raise PortalClientError on HTTP error status."""
    mock_portal_client.get.return_value.status_code = 500

    with pytest.raises(PortalClientError):
        search_meters(mock_portal_client, query="J100000", page=1, page_size=20)


def test_search_meters_invalid_json(mock_portal_client):
    """search_meters should raise PortalClientError on invalid JSON."""
    mock_portal_client.get.return_value.status_code = 200
    mock_portal_client.get.return_value.json.side_effect = ValueError("bad json")

    with pytest.raises(PortalClientError):
        search_meters(mock_portal_client, query="J100000", page=1, page_size=20)


def test_search_meters_invalid_page(mock_portal_client):
    """search_meters should raise ValueError for invalid page."""
    with pytest.raises(ValueError):
        search_meters(mock_portal_client, query="J100000", page=0, page_size=20)


def test_search_meters_invalid_page_size(mock_portal_client):
    """search_meters should raise ValueError for invalid page_size."""
    with pytest.raises(ValueError):
        search_meters(mock_portal_client, query="J100000", page=1, page_size=0)


def test_list_meters_delegates_to_search(mock_portal_client, sample_meter_search_response):
    """list_meters should call search_meters with empty query."""
    mock_portal_client.get.return_value.json.return_value = (
        sample_meter_search_response.model_dump()
    )
    mock_portal_client.get.return_value.status_code = 200

    result = list_meters(mock_portal_client, page=1, page_size=20)

    assert result.total == 403
    call_args = mock_portal_client.get.call_args
    params = call_args.kwargs.get("params", {})
    assert params.get("q") == ""
