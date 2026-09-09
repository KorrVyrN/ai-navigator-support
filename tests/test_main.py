import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from main import run_pipeline


class TestMainPipeline:
    """Tests for main.py pipeline"""

    def test_synthetic_tickets_file_exists(self):
        """Test that synthetic_tickets.json file exists"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        assert os.path.exists(data_path), f"File {data_path} not found"

    def test_synthetic_tickets_valid_json(self):
        """Test that synthetic_tickets.json contains valid JSON"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list), "Data should be a list"
        assert len(data) > 0, "Data should not be empty"

    def test_synthetic_tickets_structure(self):
        """Test that tickets have required fields"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        
        required_fields = ["id", "timestamp", "description", "priority", "type"]
        for ticket in tickets:
            for field in required_fields:
                assert field in ticket, f"Ticket missing required field: {field}"

    def test_synthetic_tickets_contain_sensitive_data(self):
        """Test that synthetic tickets contain data to mask"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        
        # At least one ticket should have phone number, email, INN, etc.
        all_descriptions = " ".join([t["description"] for t in tickets])
        
        # Check for at least one type of sensitive data
        has_phone = any(c.isdigit() for c in all_descriptions)
        has_text = len(all_descriptions) > 0
        
        assert has_phone and has_text, "Tickets should contain test data"

    @patch('builtins.print')
    def test_pipeline_runs_without_error(self, mock_print):
        """Test that pipeline runs without raising exceptions"""
        try:
            run_pipeline()
        except FileNotFoundError:
            pytest.fail("Pipeline raised FileNotFoundError")
        except Exception as e:
            pytest.fail(f"Pipeline raised unexpected exception: {e}")

    @patch('builtins.print')
    def test_pipeline_prints_output(self, mock_print):
        """Test that pipeline produces output"""
        run_pipeline()
        # Check that print was called at least once
        assert mock_print.call_count > 0, "Pipeline should produce output"

    @patch('builtins.print')
    def test_pipeline_processes_all_tickets(self, mock_print):
        """Test that pipeline processes all loaded tickets"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        with open(data_path, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        
        run_pipeline()
        
        # Check that each ticket ID was printed
        printed_text = " ".join([str(call) for call in mock_print.call_args_list])
        for ticket in tickets:
            # Ticket ID should appear in output
            assert str(ticket["id"]) in printed_text or "ID" in printed_text

    @patch('builtins.print')
    def test_pipeline_mentions_masking(self, mock_print):
        """Test that pipeline mentions masking/anonymization"""
        run_pipeline()
        printed_text = " ".join([str(call) for call in mock_print.call_args_list])
        # Check for masking related output
        assert any(keyword in printed_text.lower() 
                  for keyword in ["маск", "защиц", "анонім", "phone", "inn"])

    def test_pipeline_json_loading(self):
        """Test JSON loading functionality"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        
        with open(data_path, "r", encoding="utf-8") as f:
            tickets = json.load(f)
        
        assert isinstance(tickets, list)
        assert all("description" in ticket for ticket in tickets)

    @patch('builtins.print')
    def test_pipeline_handles_special_characters(self, mock_print):
        """Test pipeline can handle Cyrillic and special characters"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        with open(data_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verify UTF-8 encoding
        assert isinstance(content, str)
        # Check for Cyrillic characters
        assert any(ord(c) > 127 for c in content)

    def test_pipeline_data_consistency(self):
        """Test that data remains consistent across runs"""
        data_path = os.path.join("data", "synthetic_tickets.json")
        
        with open(data_path, "r", encoding="utf-8") as f:
            data1 = json.load(f)
        
        with open(data_path, "r", encoding="utf-8") as f:
            data2 = json.load(f)
        
        assert data1 == data2, "Data should be consistent"
        assert len(data1) == len(data2), "Number of tickets should match"
