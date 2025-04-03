import logging
from datetime import datetime, timedelta

import sqlalchemy
import sqlalchemy.orm

from .models.model_base import ModelBase
from .models.public_consultation import PublicConsultation
from .parameters import (
    DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS,
    ENABLED_PUBLIC_CONSULTATION_TYPES,
)
from .services.public_consultation_fetcher import PublicConsultationFetcher
from .services.slack_notifier import SlackNotifier
from .utils import create_sql_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logging.info("Check for new public consultations started")
slack_notifier = SlackNotifier()
try:
    with PublicConsultationFetcher() as public_consultation_fetcher:
        sql_engine = create_sql_engine()
        ModelBase.metadata.create_all(sql_engine)
        with sqlalchemy.orm.Session(sql_engine) as sql_session:
            for public_consultation_type in ENABLED_PUBLIC_CONSULTATION_TYPES:
                public_consultations = (
                    public_consultation_fetcher.fetch_public_consultations(
                        public_consultation_type
                    )
                )
                for public_consultation in public_consultations:
                    if public_consultation.is_closed:
                        continue
                    is_posted_to_slack = public_consultation.retrieve(sql_session)
                    if not is_posted_to_slack:
                        slack_notifier.post_public_consultation(public_consultation)
                    public_consultation.name = public_consultation.name
                    sql_session.merge(public_consultation)
                    sql_session.commit()
            if DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS:
                delete_inactive_public_consultations_older_than = (
                    datetime.now()
                    - timedelta(days=DAYS_TO_STORE_INACTIVE_PUBLIC_CONSULTATIONS)
                )
                sql_session.query(PublicConsultation).filter(
                    PublicConsultation.last_fetched_at
                    < delete_inactive_public_consultations_older_than
                ).delete()
                sql_session.commit()
except Exception as e:
    slack_notifier.post_message(f"Check for new public consultations failed:\n{e}")
    logging.error(f"Check for new public consultations failed:\n{e}")
    raise
logging.info("Check for new public consultations completed successfully")
