import unittest
import io
import sys
from engine.session import run_session

class TestSessionLifecycle(unittest.TestCase):

    def test_happy_path(self):

        # In-memory text buffer
        captured = io.StringIO()
        # Anything written to stdout is redirected to this buffer (not terminal)
        sys.stdout = captured

        try:
            with run_session("./mock_workspace") as session:

                # Clean state
                assert session["path"] == "./mock_workspace"
                assert session["value"] == 0
                assert session["status"] == "active"

                assert "Setting up..." in captured.getvalue()

        finally:
            # Return stdout to point to the terminal before any other tests
            sys.stdout = sys.__stdout__

        # Since sessions must always execute the finally block, even if there were a crash part-way we should still see the exiting logs.
        final_logs = captured.getvalue()
        assert "Exiting..." in final_logs

# If this test file is run directly, it represents __main__ and runs only these tests with the relevant return value if they pass. Else, you can discover it with the README command.

if __name__ == "__main__":
    unittest.main()