from contextlib import contextmanager

# Context Manager handles a lifecycle using a setup - try - yield - finally block (functional rather than OOP)
# The session to be the entry-point into the database engine.

@contextmanager
def run_session(workspace_path: str = "."):

    # Setup sequence
    print("Setting up...")
    # Session state passed to the caller

    session_state = {
        "value":0,
        "status":"active",
        "path":workspace_path
        }

    # Hand control over to the caller/loop
    try:
        yield session_state

    # Teardown sequence

    finally:
        print("Exiting...")