from datetime import timedelta

import sqlalchemy.orm
from sqlalchemy import create_engine

from .enums.public_consultation_type import PublicConsultationType
from .models.model_base import ModelBase
from .models.public_consultation import PublicConsultation
from .services.public_consultation_fetcher import PublicConsultationFetcher
from .services.slack_notifier import SlackNotifier
from .utils import get_current_time

slack_notifier = SlackNotifier()
try:
    with PublicConsultationFetcher() as public_consultation_fetcher:
        sql_engine = create_engine("sqlite:///data/sqlite.db")
        ModelBase.metadata.create_all(sql_engine)
        with sqlalchemy.orm.Session(sql_engine) as sql_session:
            for public_consultation_type in [
                PublicConsultationType.ATTISTIBAS_PLANOSANAS_DOKUMENTI,
                PublicConsultationType.PUBLISKAS_APSPRIESANAS,
                PublicConsultationType.SAISTOSO_NOTEIKUMU_PROJEKTI,
            ]:
                public_consultations = (
                    public_consultation_fetcher.fetch_public_consultations(
                        public_consultation_type
                    )
                )
                for public_consultation in public_consultations:
                    is_posted_to_slack = public_consultation.retrieve(sql_session)
                    if not is_posted_to_slack:
                        slack_notifier.post_public_consultation(public_consultation)
                    public_consultation.name = public_consultation.name
                    sql_session.merge(public_consultation)
                    sql_session.commit()
            one_year_ago = get_current_time() - timedelta(days=365)
            sql_session.query(PublicConsultation).filter(
                PublicConsultation.last_fetched_at < one_year_ago
            ).delete()
            sql_session.commit()
except Exception as e:
    slack_notifier.post_message(f"Check for new public consultations failed:\n{e}")
    raise
