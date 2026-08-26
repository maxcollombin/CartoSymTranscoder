"""
Base Pydantic models and utilities for CartoSym.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from abc import ABC


class BaseCartoSymModel(BaseModel):
    """
    Base class for all CartoSym models.
    
    Provides common configuration and utilities for validation,
    serialization, and documentation generation.
    """
    
    model_config = ConfigDict(
        # Allow extra fields for extensibility
        extra="forbid",
        # Validate on assignment  
        validate_assignment=True,
        # Use enum values in serialization
        use_enum_values=True,
        # Populate by name (for JSON Schema compatibility)
        populate_by_name=True,
        # Use aliases in serialization
        serialize_by_alias=True,
        # Strict validation by default
        strict=False,
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary, excluding None values."""
        return self.model_dump(exclude_none=True)
    
    def to_json(self) -> str:
        """Convert model to JSON string."""
        return self.model_dump_json(exclude_none=True)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create model instance from dictionary."""
        return cls.model_validate(data)
    
    @classmethod 
    def from_json(cls, json_str: str):
        """Create model instance from JSON string."""
        return cls.model_validate_json(json_str)


class CommentMixin(BaseModel):
    """Mixin for models that can have comments."""
    comment: Optional[str] = Field(None, alias="$comment", description="Optional comment")


class AlterMixin(BaseModel):
    """Mixin for models that can have alter flag."""
    alter: Optional[bool] = Field(None, description="Whether this overrides a previous definition")
