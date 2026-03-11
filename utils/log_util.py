"""Logging utilities for MCP-Bench.

Provides custom logging handlers and configuration for cross-platform compatibility,
particularly handling Unicode encoding issues on Windows.
"""
import logging
import sys


class ErrorIgnoringHandler(logging.StreamHandler):
    """Stream handler that silently ignores Unicode encoding errors on Windows."""
    
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            try:
                stream.write(msg + self.terminator)
            except UnicodeEncodeError:
                # Skip this message entirely if it can't be encoded
                return
            except Exception:
                # Skip any other encoding issues
                return
            self.flush()
        except Exception:
            # Don't call handleError as it might print to console
            pass


def configure_logging(level=logging.INFO, log_file='benchmark.log'):
    """Configure logging with Unicode-safe console output and UTF-8 file logging.
    
    Args:
        level: Logging level (default: logging.INFO)
        log_file: Path to log file (default: 'benchmark.log')
    """
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Configure logging with our custom handler
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            ErrorIgnoringHandler(),  # Console - ignore Unicode errors
            logging.FileHandler(log_file, encoding='utf-8')  # File - save everything
        ],
        force=True  # Force reconfiguration
    )