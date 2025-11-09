import sys
import logging
import structlog

log = structlog.stdlib.get_logger()

def configure_logging():

    # Generic Python base logging system (No timestamp yet)
    logging.basicConfig(
        format="%(message)s", # To be formatted later
        stream=sys.stdout, # Standard output in terminal
        level=logging.INFO, # Log levels (INFO, WARNING, ERROR only)
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"), # ISO 8601 timestamp
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name, # Usually 'Schrodinger'
            structlog.processors.StackInfoRenderer(), # TBD
            structlog.processors.format_exc_info,
            structlog.processors.KeyValueRenderer(
                key_order=["event", "source", "destination", "status", "timestamp"]
            ),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


""""
To be tested later:

log.info("Copy started", source="./data/en", destination="./output/en")

OUTPUT:
event="Starting clone" source="./data/en" destination="./output/en" status="in_progress" timestamp="2025-11-02T19:40:00"
event="Clone complete" source="./data/en" destination="./output/en" status="success" timestamp="2025-11-02T19:40:05"
"""
