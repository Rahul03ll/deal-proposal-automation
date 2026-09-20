#!/usr/bin/env python3
"""
Unit tests for VelocityOps Instant Proposal & SOW Generator
Tests deterministic heuristic extraction, rate card loading, HTML rendering, and pipeline flow.
"""

import os
import sys
import unittest
from pathlib import Path

# Ensure proposal_generator is on python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from proposal_generator import (
    load_rate_card,
    parse_deal_notes_heuristic,
    render_html_proposal,
    process_deals_pipeline,
    RATE_CARD_PATH,
    TRACKER_PATH,
)


class TestProposalGenerator(unittest.TestCase):
    def setUp(self):
        self.sample_deal = {
            "deal_id": "DEAL-TEST-99",
            "company": "Nexus Logistics Global",
            "contact_name": "Jordan Smith",
            "contact_email": "jsmith@nexuslogistics.com",
            "deal_title": "Automated Manifest Extraction Pipeline",
            "region": "North America (US)",
            "estimated_budget": "$40000",
            "currency": "USD",
            "meeting_notes": "Logistics hub managing 500 bills of lading per day. Manual entry causes 6 hours of lag. 6 weeks timeline required. Needs PostgreSQL and webhook integration.",
            "status": "READY"
        }
        self.rate_card = load_rate_card()

    def test_load_rate_card(self):
        """Test rate card loads correctly with required enterprise fields."""
        card = load_rate_card()
        self.assertIsInstance(card, dict)
        self.assertIn("company_name", card)
        self.assertIn("founder", card)
        self.assertIn("standard_payment_terms", card)
        self.assertIn("sla_support_period", card)

    def test_parse_deal_notes_heuristic(self):
        """Test rule-based deterministic heuristic extraction."""
        extracted = parse_deal_notes_heuristic(self.sample_deal, self.rate_card)
        self.assertEqual(extracted["deal_id"], "DEAL-TEST-99")
        self.assertEqual(extracted["company_name"], "Nexus Logistics Global")
        self.assertEqual(extracted["client_name"], "Jordan Smith")
        self.assertEqual(extracted["project_title"], "Automated Manifest Extraction Pipeline")
        self.assertEqual(extracted["investment_total"], "$40000")
        self.assertIn("6 Weeks", extracted["executive_summary"] + extracted["email_draft"])
        self.assertTrue(len(extracted["milestones"]) >= 3)
        self.assertIn("email_draft", extracted)
        self.assertIn("Hi Jordan", extracted["email_draft"])

    def test_render_html_proposal(self):
        """Test HTML rendering produces valid markup with key sections and styling."""
        extracted = parse_deal_notes_heuristic(self.sample_deal, self.rate_card)
        html = render_html_proposal(extracted)
        self.assertIsInstance(html, str)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("Nexus Logistics Global", html)
        self.assertIn("Automated Manifest Extraction Pipeline", html)
        self.assertIn("$40000", html)
        self.assertIn("Authorized Signatory", html)
        self.assertIn("CONFIDENTIAL & PROPRIETARY", html)
        self.assertIn("Phased Milestones & Key Deliverables", html)

    def test_process_deals_pipeline_dry_run(self):
        """Test dry-run processing succeeds without modifying state."""
        success = process_deals_pipeline(deal_id_filter="DEAL-401", dry_run=True)
        self.assertTrue(success)

    def test_process_deals_pipeline_invalid_deal(self):
        """Test pipeline returns False gracefully when non-existent deal ID requested."""
        success = process_deals_pipeline(deal_id_filter="DEAL-NONEXISTENT", dry_run=True)
        self.assertFalse(success)

    def test_process_deals_pipeline_invalid_tracker(self):
        """Test pipeline returns False gracefully when tracker file does not exist."""
        non_existent_path = Path(__file__).resolve().parent / "does_not_exist_tracker.csv"
        success = process_deals_pipeline(tracker_path=non_existent_path, dry_run=True)
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main()
