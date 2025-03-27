from enum import Enum


class PublicConsultationType(Enum):
    ATTISTIBAS_PLANOSANAS_DOKUMENTI = "attistibas-planosanas-dokumenti"
    PUBLISKAS_APSPRIESANAS = "publiskas-apspriesanas"
    SAISTOSO_NOTEIKUMU_PROJEKTI = "saistoso-noteikumu-projekti"

    @property
    def display_name(self) -> str:
        return {
            PublicConsultationType.ATTISTIBAS_PLANOSANAS_DOKUMENTI: "Attīstības plānošanas dokuments",
            PublicConsultationType.PUBLISKAS_APSPRIESANAS: "Publiskā apspriešana",
            PublicConsultationType.SAISTOSO_NOTEIKUMU_PROJEKTI: "Saistošo noteikumu projekts",
        }[self]

    @property
    def dates_field_name(self) -> str:
        DATES_FIELD_NAMES = {
            PublicConsultationType.ATTISTIBAS_PLANOSANAS_DOKUMENTI: "Publicēšanas datums",
            PublicConsultationType.PUBLISKAS_APSPRIESANAS: "Apspriešanas periods",
            PublicConsultationType.SAISTOSO_NOTEIKUMU_PROJEKTI: "Termiņš viedokļa izteikšanai",
        }
        return DATES_FIELD_NAMES[self]
