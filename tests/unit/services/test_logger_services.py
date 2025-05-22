import logging
from unittest.mock import patch, MagicMock
from services import logger_services

def test_init_loggers_creates_debug_and_error_logger():
    with patch("services.logger_services.Logger") as MockLogger:
        # Mock .create_logger to return dummy logger objects
        mock_debug_logger = MagicMock(spec=logging.Logger)
        mock_error_logger = MagicMock(spec=logging.Logger)
        MockLogger.return_value.create_logger.side_effect = [mock_debug_logger, mock_error_logger]

        debug_logger, error_logger = logger_services.init_loggers("my_module.py")

        # Check Logger was called with correct levels
        MockLogger.assert_any_call(name="my_module.py", level="DEBUG")
        MockLogger.assert_any_call(name="my_module.py", level="ERROR")

        # Ensure create_logger was called twice
        assert MockLogger.return_value.create_logger.call_count == 2

        # Validate return values
        assert debug_logger == mock_debug_logger
        assert error_logger == mock_error_logger