from io import StringIO
import pytest
import sys
import time
from mehr.stream.LogWrapper import LogProgress

@pytest.fixture()
def stderr_from_progress_logger():
    def _inner(num_lines, message):
        sys.stderr = StringIO()
        SUPRESSED_MESSAGE = "Another line."
    
        with LogProgress():
            for _ in range(num_lines):
                print(SUPRESSED_MESSAGE)
                sys.stderr.flush()
                
        output = sys.stderr.getvalue()
        return output
    return _inner
        

@pytest.mark.parametrize("num_lines", [0, 1, 2, 5, 10, 25, 1000])
@pytest.mark.parametrize("message", ["Hello, World!", "Just another message", "A" * 1000, "Some. Very. Punctuated. Message."])
def test_suppress_output(num_lines, message, stderr_from_progress_logger):
    output = stderr_from_progress_logger(num_lines, message)
    
    assert message not in output
    

@pytest.mark.parametrize("num_lines", [0, 1, 2, 5, 10, 25, 1000])
def test_proper_counting(num_lines, stderr_from_progress_logger):
    output = stderr_from_progress_logger(num_lines, "a message.")
    
    lines = output.split("\r")
    first_line = lines[1] # zero index is the clearing of the first output line and usually just the empty string
    last_line = lines[-1]
    
    assert "0it" in first_line
    assert f"{num_lines}it" in last_line
    