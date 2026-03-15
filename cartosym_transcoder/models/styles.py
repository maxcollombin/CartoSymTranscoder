"""
Core style and rule models for CartoSym.

Based on the JSON Schema definitions for style, stylingRule, and metadata.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import Field, field_validator, model_validator
from .base import BaseCartoSymModel, CommentMixin

# Import symbolizers
from .symbolizers import Symbolizer


class Metadata(BaseCartoSymModel, CommentMixin):
    """
    Metadata for a CartoSym style.
    
    Based on the 'metadata' definition in the JSON schema.
    """
    title: Optional[str] = Field(None, description="Style title")
    abstract: Optional[str] = Field(None, description="Style abstract/summary")
    description: Optional[str] = Field(None, description="Style description") 
    authors: Optional[List[str]] = Field(None, description="List of authors")
    keywords: Optional[List[str]] = Field(None, description="Keywords for the style")
    geo_data_classes: Optional[List[str]] = Field(
        None, 
        alias="geoDataClasses",
        description="Geographic data classes (URIs)"
    )


class Variable(BaseCartoSymModel):
    """
    Represents a variable definition in CartoSym CSS.
    """
    name: str = Field(..., description="Variable name")
    value: Any = Field(..., description="Variable value")
    type: Optional[str] = Field(None, description="Variable type (optional)")


class StylingRule(BaseCartoSymModel, CommentMixin):
    """
    Individual styling rule with optional selector and symbolizer.
    Now supports explicit stylingRuleName.
    """
    name: Optional[str] = Field(None, description="Rule name (legacy or fallback)")
    styling_rule_name: Optional[str] = Field(
        None,
        alias="stylingRuleName",
        description="Explicit styling rule name (from grammar)"
    )
    nested_rules: Optional[List['StylingRule']] = Field(
        None,
        alias="nestedRules", 
        description="Nested rules within this rule"
    )
    selector: Optional[Union[Dict[str, Any], List[str], str]] = Field(
        None, 
        description="Selector expression (flexible - can be dict, list, or string)"
    )
    symbolizer: Optional[Union[Symbolizer, Dict[str, Any]]] = Field(
        None, 
        description="Symbolizer for this rule"
    )

    @field_validator('symbolizer', mode='before')
    def ensure_symbolizer_model(cls, v):
        if isinstance(v, dict):
            return Symbolizer.from_dict(v)
        return v

    @model_validator(mode='after')
    def recursively_validate_nested_rules(self):
        if self.nested_rules:
            for i, rule in enumerate(self.nested_rules):
                if isinstance(rule, dict):
                    self.nested_rules[i] = StylingRule.model_validate(rule)
        return self



class Style(BaseCartoSymModel, CommentMixin):
    """
    Root CartoSym style definition.
    Now supports explicit variable objects.
    """
    include: Optional[Union[str, List[str]]] = Field(
        None,
        alias="$include", 
        description="Included style files"
    )
    metadata: Optional[Metadata] = Field(None, description="Style metadata")
    styling_rules: List[StylingRule] = Field(
        ..., 
        alias="stylingRules",
        description="List of styling rules"
    )
    variables: Optional[List[Variable]] = Field(
        None,
        alias="$variables",
        description="Style variables (as objects)"
    )


# Enable forward references
StylingRule.model_rebuild()
