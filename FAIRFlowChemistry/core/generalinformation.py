import sdRDM

from typing import List, Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element, wrapped
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from .relatedpublication import RelatedPublication
from .topicclassification import TopicClassification
from .keyword import Keyword
from .author import Author


@forge_signature
class Contact(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@46cef31442ba9e52c957dc3a77a7bf5a64326c1e#Contact"
    },
):
    """Small type for attribute 'contact'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )
    name: Optional[str] = element(default=None, tag="name", json_schema_extra=dict())
    affiliation: Optional[str] = element(
        default=None, tag="affiliation", json_schema_extra=dict()
    )
    email: Optional[str] = element(default=None, tag="email", json_schema_extra=dict())
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="46cef31442ba9e52c957dc3a77a7bf5a64326c1e"
    )


@forge_signature
class GeneralInformation(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRFlowChemistry@46cef31442ba9e52c957dc3a77a7bf5a64326c1e#GeneralInformation"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    title: Optional[str] = element(
        description="title of the work.",
        default=None,
        tag="title",
        json_schema_extra=dict(),
    )

    project: Optional[str] = element(
        description="Name of the project this work is related to.",
        default=None,
        tag="project",
        json_schema_extra=dict(),
    )

    description: Optional[str] = element(
        description="describes the content of the dataset.",
        default=None,
        tag="description",
        json_schema_extra=dict(),
    )

    authors: List[Author] = wrapped(
        "authors",
        element(
            description="authors of this dataset.",
            default_factory=ListPlus,
            tag="Author",
            json_schema_extra=dict(multiple=True),
        ),
    )

    contact: Optional[Contact] = element(
        description="point of contact for this projecet",
        default_factory=Contact,
        tag="contact",
        json_schema_extra=dict(),
    )

    subject: List[str] = wrapped(
        "subject",
        element(
            description=(
                "Domain-specific Subject Categories that are topically relevant to the"
                " Dataset."
            ),
            default_factory=ListPlus,
            tag="string",
            json_schema_extra=dict(multiple=True),
        ),
    )

    related_publication: Optional[RelatedPublication] = element(
        description="Related publication to the dataset.",
        default_factory=RelatedPublication,
        tag="related_publication",
        json_schema_extra=dict(),
    )

    keywords: List[Keyword] = wrapped(
        "keywords",
        element(
            description="Keywords and url related to the project.",
            default_factory=ListPlus,
            tag="Keyword",
            json_schema_extra=dict(multiple=True),
        ),
    )

    topic_classification: List[TopicClassification] = wrapped(
        "topic_classification",
        element(
            description="Topic classification.",
            default_factory=ListPlus,
            tag="TopicClassification",
            json_schema_extra=dict(multiple=True),
        ),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="46cef31442ba9e52c957dc3a77a7bf5a64326c1e"
    )

    def add_to_authors(
        self,
        name: Optional[str] = None,
        affiliation: Optional[str] = None,
        identifier_scheme: Optional[str] = None,
        identifier: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Author:
        """
        This method adds an object of type 'Author' to attribute authors

        Args:
            id (str): Unique identifier of the 'Author' object. Defaults to 'None'.
            name (): full name including given and family name.. Defaults to None
            affiliation (): organization the author is affiliated to.. Defaults to None
            identifier_scheme (): Name of the identifier scheme (ORCID, ISNI).. Defaults to None
            identifier (): Uniquely identifies an individual author or organization, according to various schemes.. Defaults to None
        """
        params = {
            "name": name,
            "affiliation": affiliation,
            "identifier_scheme": identifier_scheme,
            "identifier": identifier,
        }
        if id is not None:
            params["id"] = id
        self.authors.append(Author(**params))
        return self.authors[-1]

    def add_to_keywords(
        self,
        value: Optional[str] = None,
        vocabulary: Optional[str] = None,
        vocabulary_uri: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Keyword:
        """
        This method adds an object of type 'Keyword' to attribute keywords

        Args:
            id (str): Unique identifier of the 'Keyword' object. Defaults to 'None'.
            value (): Key terms that describe important aspects of the Dataset.. Defaults to None
            vocabulary (): For the specification of the keyword controlled vocabulary in use, such as LCSH, MeSH, or others.. Defaults to None
            vocabulary_uri (): Keyword vocabulary URI points to the web presence that describes the keyword vocabulary, if appropriate.. Defaults to None
        """
        params = {
            "value": value,
            "vocabulary": vocabulary,
            "vocabulary_uri": vocabulary_uri,
        }
        if id is not None:
            params["id"] = id
        self.keywords.append(Keyword(**params))
        return self.keywords[-1]

    def add_to_topic_classification(
        self,
        value: Optional[str] = None,
        vocab: Optional[str] = None,
        vocab_uri: Optional[str] = None,
        id: Optional[str] = None,
    ) -> TopicClassification:
        """
        This method adds an object of type 'TopicClassification' to attribute topic_classification

        Args:
            id (str): Unique identifier of the 'TopicClassification' object. Defaults to 'None'.
            value (): Topic or Subject term that is relevant to this Dataset.. Defaults to None
            vocab (): Provided for specification of the controlled vocabulary in use, e.g., LCSH, MeSH, etc.. Defaults to None
            vocab_uri (): Specifies the URI location for the full controlled vocabulary.. Defaults to None
        """
        params = {"value": value, "vocab": vocab, "vocab_uri": vocab_uri}
        if id is not None:
            params["id"] = id
        self.topic_classification.append(TopicClassification(**params))
        return self.topic_classification[-1]
