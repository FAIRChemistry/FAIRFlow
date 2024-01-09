import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator
from .keyword import Keyword
from .relatedpublication import RelatedPublication
from .topicclassification import TopicClassification
from .author import Author
from .contact import Contact


@forge_signature
class GeneralInformation(sdRDM.DataModel):
    """"""

    id: Optional[str] = Field(
        description="Unique identifier of the given object.",
        default_factory=IDGenerator("generalinformationINDEX"),
        xml="@id",
    )

    title: Optional[str] = Field(
        default=None,
        description="title of the work.",
    )

    project: Optional[str] = Field(
        default=None,
        description="Name of the project this work is related to.",
    )

    description: Optional[str] = Field(
        default=None,
        description="describes the content of the dataset.",
    )

    authors: List[Author] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="authors of this dataset.",
    )

    contact: Optional[Contact] = Field(
        description="point of contact for this projecet",
        default_factory=Contact,
    )

    subject: List[str] = Field(
        default_factory=ListPlus,
        multiple=True,
        description=(
            "Domain-specific Subject Categories that are topically relevant to the"
            " Dataset."
        ),
    )

    related_publication: Optional[RelatedPublication] = Field(
        description="Related publication to the dataset.",
        default_factory=RelatedPublication,
    )

    keywords: List[Keyword] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Keywords and url related to the project.",
    )

    topic_classification: List[TopicClassification] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="Topic classification.",
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRFlowChemistry"
    )
    _commit: Optional[str] = PrivateAttr(
        default="e456339bee79514bdb0b05626b283e99762b3e06"
    )

    def add_to_authors(
        self,
        name: Optional[str] = None,
        affiliation: Optional[str] = None,
        identifier_scheme: Optional[str] = None,
        identifier: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
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
    ) -> None:
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
    ) -> None:
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
