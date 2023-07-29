import sdRDM

from typing import List, Optional
from pydantic import Field, PrivateAttr
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature, IDGenerator


from .author import Author


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

    description: Optional[str] = Field(
        default=None,
        description="describes the content of the dataset.",
    )

    authors: List[Author] = Field(
        default_factory=ListPlus,
        multiple=True,
        description="authors of this dataset.",
    )

    __repo__: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/datamodel_b07_tc.git"
    )
    __commit__: Optional[str] = PrivateAttr(
        default="941a1c1d9c93cf7b4c0395591b1fd7eddbff7406"
    )

    def add_to_authors(
        self,
        name: Optional[str] = None,
        affiliation: Optional[str] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        This method adds an object of type 'Author' to attribute authors

        Args:
            id (str): Unique identifier of the 'Author' object. Defaults to 'None'.
            name (): full name including given and family name.. Defaults to None
            affiliation (): organization the author is affiliated to.. Defaults to None
        """

        params = {
            "name": name,
            "affiliation": affiliation,
        }

        if id is not None:
            params["id"] = id

        self.authors.append(Author(**params))
