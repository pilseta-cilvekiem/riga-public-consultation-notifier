from functools import partial
from types import TracebackType
from typing import Any, Optional, Type

import requests
from bs4 import BeautifulSoup, Tag
from fake_useragent import UserAgent

from ..enums.public_consultation_type import PublicConsultationType
from ..models.public_consultation import PublicConsultation
from ..parameters import ROOT_URL


class PublicConsultationFetcher:
    def __init__(self) -> None:
        pass

    def __enter__(self):
        self.requests_session = requests.Session()
        self.requests_session.headers["User-Agent"] = UserAgent().random
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.requests_session.close()

    def fetch_public_consultations(
        self, public_consultation_type: PublicConsultationType
    ) -> list[PublicConsultation]:
        http_response = self.requests_session.get(
            f"{ROOT_URL}/lv/{public_consultation_type.value}", timeout=5
        )
        http_response.raise_for_status()
        soup = BeautifulSoup(http_response.text, "html.parser")
        content_area_div = _find_required_tag(
            soup, "div", recursive=True, id="content-area"
        )
        article_divs = _find_all_tags(
            content_area_div, "div", recursive=True, role="article"
        )
        pager_nav = _find_optional_tag(
            content_area_div, "nav", recursive=True, class_="pager"
        )
        create_public_consultation = partial(
            _create_public_consultation, public_consultation_type
        )
        public_consultations = list(map(create_public_consultation, article_divs))
        if pager_nav is not None and not public_consultations[-1].is_closed:
            raise NotImplementedError(
                "There are more public consultations to fetch on the next page, multiple page fetching is not implemented"
            )
        return public_consultations


def _create_public_consultation(
    public_consultation_type: PublicConsultationType, article_div: Tag
) -> PublicConsultation:
    link_div = _find_required_tag(
        article_div, "div", recursive=False, class_="catalog-card-top"
    )
    link_h3 = _find_required_tag(link_div, "h3", recursive=False)
    link_a = _find_required_tag(link_h3, "a", recursive=False)
    fields_div = _find_required_tag(
        article_div, "div", recursive=True, class_="classifier-row"
    )
    field_divs = _find_all_tags(fields_div, "div", recursive=False)
    fields = dict(map(_create_field, field_divs))
    return PublicConsultation(
        _get_attribute_value(link_a, "href"),
        link_a.text,
        fields,
        public_consultation_type,
    )


def _create_field(field_element: Tag) -> tuple[str, str]:
    field_label_div = _find_required_tag(
        field_element, "div", recursive=False, class_="field-label"
    )
    field_value_div = _find_required_tag(
        field_element, "div", recursive=False, class_=None
    )
    field_value_span = _find_required_tag(field_value_div, "span", recursive=False)
    return (field_label_div.text, field_value_span.text)


def _find_optional_tag(
    tag: Tag, name: str, recursive: bool, **kwargs: Any
) -> Tag | None:
    find_result = tag.find(name, recursive=recursive, **kwargs)
    if find_result is not None and not isinstance(find_result, Tag):
        raise TypeError(f"Expected a Tag object, got {type(find_result)}")
    return find_result


def _find_required_tag(tag: Tag, name: str, recursive: bool, **kwargs: Any) -> Tag:
    find_result = tag.find(name, recursive=recursive, **kwargs)
    if not isinstance(find_result, Tag):
        raise TypeError(f"Expected a Tag object, got {type(find_result)}")
    return find_result


def _find_all_tags(tag: Tag, name: str, recursive: bool, **kwargs: Any) -> list[Tag]:
    return [
        find_result
        for find_result in tag.find_all(name, recursive=recursive, **kwargs)
        if isinstance(find_result, Tag)
    ]


def _get_attribute_value(tag: Tag, attribute_name: str) -> str:
    attribute_value = tag.get(attribute_name)
    if not isinstance(attribute_value, str):
        raise TypeError(f"Expected a string, got {type(attribute_value)}")
    return attribute_value
