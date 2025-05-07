import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Entry point for BrainXio CLI."""
    logger.info("Starting BrainXio CLI")
    print("BrainXio CLI v0.1.0")

if __name__ == "__main__":  # pragma: no cover
    main()
