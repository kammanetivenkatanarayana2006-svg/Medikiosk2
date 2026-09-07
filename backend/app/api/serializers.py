"""
Shared API serializers for MongoDB documents.
Converts Mongo ObjectId and datetime values to JSON-serializable types.
"""
from typing import Any, Dict, List


def serialize_doc(doc):
    """Convert a Mongo document _id (ObjectId) to a JSON-safe id string."""
    if not doc:
        return doc
    result = dict(doc)
    if "_id" in result:
        result["id"] = str(result.pop("_id"))
    return result


def serialize_docs(docs):
    """Convert a list of Mongo documents to JSON-safe dicts."""
    if not docs:
        return []
    return [serialize_doc(d) for d in docs]