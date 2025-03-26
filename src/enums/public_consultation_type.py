from enum import Enum


class PublicConsultationType(Enum):
    ATTISTIBAS_PLANOSANAS_DOKUMENTI = "attistibas-planosanas-dokumenti"
    PUBLISKAS_APSPRIESANAS = "publiskas-apspriesanas"
    SAISTOSO_NOTEIKUMU_PROJEKTI = "saistoso-noteikumu-projekti"

    @property
    def display_name(self) -> str:
        return {
            self.ATTISTIBAS_PLANOSANAS_DOKUMENTI: "Attīstības plānošanas dokuments",
            self.PUBLISKAS_APSPRIESANAS: "Publiskā apspriešana",
            self.SAISTOSO_NOTEIKUMU_PROJEKTI: "Saistošo noteikumu projekts",
        }[self]

    @property
    def dates_field_name(self) -> str:
        return {
            self.ATTISTIBAS_PLANOSANAS_DOKUMENTI: "Publicēšanas datums",
            self.PUBLISKAS_APSPRIESANAS: "Apspriešanas periods",
            self.SAISTOSO_NOTEIKUMU_PROJEKTI: "Termiņš viedokļa izteikšanai",
        }[self]
