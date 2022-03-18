"""v1.schemas namespace."""

from typing import AbstractSet, Any, Dict, Mapping, Union

from pydantic import BaseModel


class PropertyBaseModel(BaseModel):
    """Workaround for serializing properties with pydantic."""

    @classmethod
    def get_properties(cls):
        """Override properties."""
        return [
            prop
            for prop in dir(cls)
            if isinstance(getattr(cls, prop), property) and prop not in ("__values__", "fields")
        ]

    def dict(
        self,
        *,
        include: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]] = None,
        exclude: Union[AbstractSet[Union[int, str]], Mapping[Union[int, str], Any]] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> Dict[str, Any]:
        """Override dict."""
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs
