"""Tests for type definitions and response objects."""

from pyturnstile._types import TurnstileResponse, TurnstileValidationError


class TestTurnstileResponse:
    """Test TurnstileResponse class."""

    def test_init_with_full_data(self, mock_success_response):
        """Test initialization with complete response data."""
        response = TurnstileResponse(mock_success_response)

        assert response.success is True
        assert response.challenge_ts == "2024-01-01T00:00:00.000Z"
        assert response.hostname == "example.com"
        assert response.action == "login"
        assert response.cdata == "session123"
        assert response.error_codes == []
        assert response.metadata == {"ephemeral_id": "device-123"}

    def test_init_with_minimal_data(self):
        """Test initialization with minimal response data."""
        response = TurnstileResponse({"success": True})  # ty:ignore[missing-typed-dict-key]

        assert response.success is True
        assert response.challenge_ts == ""
        assert response.hostname == ""
        assert response.action == ""
        assert response.cdata == ""
        assert response.error_codes == []
        assert response.metadata == {}

    def test_init_with_failure(self, mock_failure_response):
        """Test initialization with failed validation."""
        response = TurnstileResponse(mock_failure_response)

        assert response.success is False
        assert response.error_codes == ["invalid-input-response"]

    def test_to_dict(self, mock_success_response):
        """Test conversion to dictionary."""
        response = TurnstileResponse(mock_success_response)
        response_dict = response.to_dict()

        assert isinstance(response_dict, dict)
        assert response_dict["success"] is True
        assert response_dict["hostname"] == "example.com"
        assert response_dict["action"] == "login"

    def test_model_dump(self, mock_success_response):
        """Test model_dump alias."""
        response = TurnstileResponse(mock_success_response)
        dumped = response.model_dump()

        assert dumped == response.to_dict()

    def test_bool_operator_success(self, mock_success_response):
        """Test boolean evaluation for successful response."""
        response = TurnstileResponse(mock_success_response)
        assert bool(response) is True

    def test_bool_operator_failure(self, mock_failure_response):
        """Test boolean evaluation for failed response."""
        response = TurnstileResponse(mock_failure_response)
        assert bool(response) is False

    def test_str_representation(self, mock_success_response):
        """Test string representation."""
        response = TurnstileResponse(mock_success_response)
        str_repr = str(response)

        assert "TurnstileResponse" in str_repr
        assert "success=True" in str_repr
        assert "hostname=example.com" in str_repr

    def test_repr(self, mock_success_response):
        """Test repr representation."""
        response = TurnstileResponse(mock_success_response)
        assert repr(response) == str(response)


class TestTurnstileValidationError:
    """Test TurnstileValidationError exception."""

    def test_exception_creation(self):
        """Test creating TurnstileValidationError."""
        error = TurnstileValidationError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)
