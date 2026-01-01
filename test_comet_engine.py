"""Unit tests for Comet-Hive-Agent deterministic shortcut engine.

Comprehensive test coverage for citation tracking, node validation,
and execution logging.
"""

import unittest
import json
from datetime import datetime
from comet_engine import (
    CometEngine,
    ShortcutNode,
    VerifiedCitation,
    create_citation
)


class TestVerifiedCitation(unittest.TestCase):
    """Test cases for VerifiedCitation dataclass."""
    
    def test_citation_creation(self):
        """Test basic citation creation."""
        citation = create_citation(
            source_id="test_source",
            content="test content"
        )
        
        self.assertEqual(citation.source_id, "test_source")
        self.assertEqual(citation.verification_method, "sha256")
        self.assertIsInstance(citation.timestamp, str)
        self.assertEqual(len(citation.content_hash), 64)  # SHA-256 produces 64 hex chars
    
    def test_citation_immutability(self):
        """Test citation hash consistency."""
        content = "deterministic test content"
        citation1 = create_citation("src1", content)
        citation2 = create_citation("src2", content)
        
        # Same content should produce same hash
        self.assertEqual(citation1.content_hash, citation2.content_hash)
    
    def test_citation_requires_hash(self):
        """Test citation validation requires content_hash."""
        with self.assertRaises(ValueError):
            VerifiedCitation(
                source_id="test",
                content_hash="",
                timestamp="2025-01-01T00:00:00",
                verification_method="sha256"
            )


class TestShortcutNode(unittest.TestCase):
    """Test cases for ShortcutNode dataclass."""
    
    def test_node_validation_success(self):
        """Test valid node passes validation."""
        node = ShortcutNode(
            node_id="test_node_1",
            pattern="github.com/notifications",
            action="bulk_mark_done",
            confidence=0.95
        )
        
        self.assertTrue(node.validate())
    
    def test_node_validation_confidence_bounds(self):
        """Test node validation rejects invalid confidence values."""
        # Confidence too high
        node_high = ShortcutNode(
            node_id="test_node_2",
            pattern="test",
            action="test",
            confidence=1.5
        )
        self.assertFalse(node_high.validate())
        
        # Confidence too low
        node_low = ShortcutNode(
            node_id="test_node_3",
            pattern="test",
            action="test",
            confidence=-0.1
        )
        self.assertFalse(node_low.validate())
    
    def test_node_validation_required_fields(self):
        """Test node validation requires node_id and pattern."""
        node_no_id = ShortcutNode(
            node_id="",
            pattern="test",
            action="test",
            confidence=0.5
        )
        self.assertFalse(node_no_id.validate())
        
        node_no_pattern = ShortcutNode(
            node_id="test",
            pattern="",
            action="test",
            confidence=0.5
        )
        self.assertFalse(node_no_pattern.validate())


class TestCometEngine(unittest.TestCase):
    """Test cases for CometEngine core functionality."""
    
    def setUp(self):
        """Set up test engine instance."""
        self.engine = CometEngine()
    
    def test_engine_initialization(self):
        """Test engine initializes with correct defaults."""
        self.assertEqual(self.engine.schema_version, "1.0.0")
        self.assertEqual(len(self.engine.shortcuts), 0)
        self.assertEqual(len(self.engine.execution_log), 0)
    
    def test_register_shortcut_success(self):
        """Test successful shortcut registration."""
        node = ShortcutNode(
            node_id="github_notifications",
            pattern="github.com/notifications",
            action="optimize_notifications",
            confidence=0.9
        )
        
        result = self.engine.register_shortcut(node)
        self.assertTrue(result)
        self.assertIn("github_notifications", self.engine.shortcuts)
    
    def test_register_shortcut_validation_failure(self):
        """Test registration fails for invalid nodes."""
        invalid_node = ShortcutNode(
            node_id="",
            pattern="test",
            action="test",
            confidence=2.0
        )
        
        result = self.engine.register_shortcut(invalid_node)
        self.assertFalse(result)
        self.assertEqual(len(self.engine.shortcuts), 0)
    
    def test_execute_shortcut_success(self):
        """Test successful shortcut execution."""
        citation = create_citation("doc_1", "optimization pattern")
        node = ShortcutNode(
            node_id="opt_1",
            pattern="optimize",
            action="execute_optimization",
            confidence=0.85,
            verified_citations=[citation],
            design_implications={"efficiency": "high"}
        )
        
        self.engine.register_shortcut(node)
        
        context = {"user": "test_user", "timestamp": "2025-01-01"}
        result = self.engine.execute_shortcut("opt_1", context)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["node_id"], "opt_1")
        self.assertEqual(result["action"], "execute_optimization")
        self.assertEqual(result["confidence"], 0.85)
        self.assertEqual(len(result["verified_citations"]), 1)
        self.assertEqual(result["design_implications"]["efficiency"], "high")
        self.assertEqual(result["context"], context)
    
    def test_execute_nonexistent_shortcut(self):
        """Test execution returns None for non-existent shortcuts."""
        result = self.engine.execute_shortcut("nonexistent", {})
        self.assertIsNone(result)
    
    def test_execution_log_tracking(self):
        """Test execution log tracks all executions."""
        node = ShortcutNode(
            node_id="log_test",
            pattern="test",
            action="test_action",
            confidence=0.5
        )
        
        self.engine.register_shortcut(node)
        
        # Execute multiple times
        self.engine.execute_shortcut("log_test", {"run": 1})
        self.engine.execute_shortcut("log_test", {"run": 2})
        self.engine.execute_shortcut("log_test", {"run": 3})
        
        log = self.engine.get_execution_log()
        self.assertEqual(len(log), 3)
        self.assertEqual(log[0]["context"]["run"], 1)
        self.assertEqual(log[2]["context"]["run"], 3)
    
    def test_generate_content_hash(self):
        """Test content hash generation is deterministic."""
        content = "test content for hashing"
        hash1 = self.engine.generate_content_hash(content)
        hash2 = self.engine.generate_content_hash(content)
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 64)
    
    def test_export_schema(self):
        """Test schema export contains all required fields."""
        node = ShortcutNode(
            node_id="export_test",
            pattern="test_pattern",
            action="test_action",
            confidence=0.75,
            design_implications={"test": "value"}
        )
        
        self.engine.register_shortcut(node)
        self.engine.execute_shortcut("export_test", {})
        
        schema = self.engine.export_schema()
        
        self.assertEqual(schema["schema_version"], "1.0.0")
        self.assertIn("export_test", schema["shortcuts"])
        self.assertEqual(schema["shortcuts"]["export_test"]["pattern"], "test_pattern")
        self.assertEqual(schema["shortcuts"]["export_test"]["confidence"], 0.75)
        self.assertEqual(schema["total_executions"], 1)
    
    def test_get_execution_log_returns_copy(self):
        """Test execution log returns copy to prevent external modification."""
        node = ShortcutNode(
            node_id="copy_test",
            pattern="test",
            action="test",
            confidence=0.5
        )
        
        self.engine.register_shortcut(node)
        self.engine.execute_shortcut("copy_test", {})
        
        log = self.engine.get_execution_log()
        original_length = len(log)
        
        # Modify returned log
        log.append({"fake": "entry"})
        
        # Original should be unchanged
        self.assertEqual(len(self.engine.get_execution_log()), original_length)


if __name__ == "__main__":
    unittest.main()
