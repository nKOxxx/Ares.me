# Testing Ares.me Sessions

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest


class TestSession01:
    """Tests for Session 01: Tool Loop"""
    
    def test_import(self):
        """Test that s01 module imports"""
        from sessions.s01_tool_loop import agent
        assert agent is not None
    
    def test_mock_llm_exists(self):
        """Test that mock_llm function exists"""
        from sessions.s01_tool_loop.agent import mock_llm
        assert callable(mock_llm)
    
    def test_get_weather_exists(self):
        """Test that get_weather function exists"""
        from sessions.s01_tool_loop.agent import get_weather
        assert callable(get_weather)
        result = get_weather("London")
        assert "London" in result


class TestSession02:
    """Tests for Session 02: Multi-Tool"""
    
    def test_import(self):
        """Test that s02 module imports"""
        from sessions.s02_multi_tool import agent
        assert agent is not None
    
    def test_tool_handlers_exist(self):
        """Test that TOOL_HANDLERS exists"""
        from sessions.s02_multi_tool.agent import TOOL_HANDLERS
        assert isinstance(TOOL_HANDLERS, dict)
        assert len(TOOL_HANDLERS) >= 4
    
    def test_calculator_works(self):
        """Test calculator tool"""
        from sessions.s02_multi_tool.agent import calculator
        result = calculator("2 + 2")
        assert "4" in result


class TestSession04:
    """Tests for Session 04: Memory Bridge"""
    
    def test_import(self):
        """Test that s04 module imports"""
        from sessions.s04_memory_bridge import agent
        assert agent is not None
    
    def test_memory_bridge_exists(self):
        """Test MemoryBridge class"""
        from sessions.s04_memory_bridge.agent import MemoryBridge
        mb = MemoryBridge(memory_dir="/tmp/test_memory")
        assert mb is not None
        
        # Test remember/recall
        mb.remember("test_key", "test_value")
        assert mb.recall("test_key") == "test_value"


class TestExamples:
    """Tests for example agents"""
    
    def test_mini_ares_imports(self):
        """Test that mini-ares imports"""
        from examples import mini_ares
        assert mini_ares is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
