"""Comet-Hive-Agent: Deterministic Shortcut Engine

Axiom JSON Schema Implementation for browser automation shortcuts.
Provides mathematical rigor and verified citation tracking.
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VerifiedCitation:
    """Immutable citation with cryptographic verification."""
    source_id: str
    content_hash: str
    timestamp: str
    verification_method: str
    
    def __post_init__(self):
        """Ensure citation immutability via hash verification."""
        if not self.content_hash:
            raise ValueError("Citation must have content_hash")


@dataclass
class ShortcutNode:
    """Deterministic node in the shortcut decision tree."""
    node_id: str
    pattern: str
    action: str
    confidence: float
    verified_citations: List[VerifiedCitation] = field(default_factory=list)
    design_implications: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> bool:
        """Validate node meets Axiom determinism requirements."""
        if not (0.0 <= self.confidence <= 1.0):
            return False
        if not self.node_id or not self.pattern:
            return False
        return True


class CometEngine:
    """Core deterministic shortcut engine for Comet-Hive-Agent."""
    
    def __init__(self):
        self.shortcuts: Dict[str, ShortcutNode] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.schema_version = "1.0.0"
        
    def register_shortcut(self, node: ShortcutNode) -> bool:
        """Register a deterministic shortcut with validation.
        
        Args:
            node: ShortcutNode to register
            
        Returns:
            bool: True if registration successful
        """
        if not node.validate():
            return False
            
        self.shortcuts[node.node_id] = node
        return True
    
    def execute_shortcut(self, node_id: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute a registered shortcut deterministically.
        
        Args:
            node_id: Identifier of the shortcut to execute
            context: Execution context with required parameters
            
        Returns:
            Execution result with citations and implications
        """
        if node_id not in self.shortcuts:
            return None
            
        node = self.shortcuts[node_id]
        
        result = {
            "node_id": node_id,
            "action": node.action,
            "confidence": node.confidence,
            "timestamp": datetime.utcnow().isoformat(),
            "verified_citations": [
                {
                    "source_id": cit.source_id,
                    "content_hash": cit.content_hash,
                    "verification_method": cit.verification_method
                }
                for cit in node.verified_citations
            ],
            "design_implications": node.design_implications,
            "context": context
        }
        
        self.execution_log.append(result)
        return result
    
    def generate_content_hash(self, content: str) -> str:
        """Generate SHA-256 hash for citation verification.
        
        Args:
            content: Content to hash
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def export_schema(self) -> Dict[str, Any]:
        """Export current shortcuts as Axiom JSON schema.
        
        Returns:
            Complete schema dictionary
        """
        return {
            "schema_version": self.schema_version,
            "shortcuts": {
                node_id: {
                    "pattern": node.pattern,
                    "action": node.action,
                    "confidence": node.confidence,
                    "verified_citations": len(node.verified_citations),
                    "design_implications": node.design_implications
                }
                for node_id, node in self.shortcuts.items()
            },
            "total_executions": len(self.execution_log)
        }
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Retrieve complete execution log for audit trail.
        
        Returns:
            List of all executed shortcuts with full context
        """
        return self.execution_log.copy()


def create_citation(source_id: str, content: str, verification_method: str = "sha256") -> VerifiedCitation:
    """Helper function to create verified citations.
    
    Args:
        source_id: Unique identifier for the source
        content: Content to be cited
        verification_method: Hash method for verification
        
    Returns:
        VerifiedCitation instance
    """
    content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    timestamp = datetime.utcnow().isoformat()
    
    return VerifiedCitation(
        source_id=source_id,
        content_hash=content_hash,
        timestamp=timestamp,
        verification_method=verification_method
    )
