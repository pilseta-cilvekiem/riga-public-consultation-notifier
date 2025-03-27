import json
from datetime import timedelta
from os import environ

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import create_engine

from .enums.public_consultation_type import PublicConsultationType
from .models.model_base import ModelBase
from .models.public_consultation import PublicConsultation
from .services.public_consultation_fetcher import PublicConsultationFetcher
from .services.slack_notifier import SlackNotifier
from .utils import (
    get_current_time,
    get_optional_secret_value,
    get_required_environment_variable,
)

slack_notifier = SlackNotifier()
try:
    with PublicConsultationFetcher() as public_consultation_fetcher:
        sql_query_json = environ.get("SQLALCHEMY_QUERY_JSON")
        sql_url = sqlalchemy.URL.create(
            get_required_environment_variable("SQLALCHEMY_DRIVER"),
            environ.get("SQLALCHEMY_USERNAME"),
            get_optional_secret_value("sqlalchemy_password"),
            environ.get("SQLALCHEMY_HOST"),
            environ.get("SQLALCHEMY_PORT"),
            environ.get("SQLALCHEMY_DATABASE"),
            json.loads(sql_query_json) if sql_query_json else None,
        )
        sql_engine = create_engine(sql_url)
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
                    if public_consultation.is_closed:
                        continue
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
