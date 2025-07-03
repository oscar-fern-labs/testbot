"""
Tests for the Mass Transit Billing System
"""

import unittest
import os
import sys
import csv
import tempfile
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mass_transit_billing import Station, Journey, BillingSystem


class TestStation(unittest.TestCase):
    """Test cases for Station class."""
    
    def test_station_creation(self):
        station = Station("Paddington", 1)
        self.assertEqual(station.name, "Paddington")
        self.assertEqual(station.zone, 1)


class TestJourney(unittest.TestCase):
    """Test cases for Journey class."""
    
    def test_complete_journey_zone1_to_zone1(self):
        """Test journey from zone 1 to zone 1: £3.60"""
        entry_station = Station("Paddington", 1)
        exit_station = Station("Bank", 1)
        
        journey = Journey("user001", entry_station=entry_station, 
                         exit_station=exit_station)
        journey.is_complete = True
        
        cost = journey.calculate_cost()
        self.assertAlmostEqual(cost, 3.60, places=2)
    
    def test_complete_journey_zone6_to_zone4(self):
        """Test journey from zone 6 to zone 4: £2.40"""
        entry_station = Station("Woolwich", 6)
        exit_station = Station("Heathrow Terminal 5", 4)
        
        journey = Journey("user002", entry_station=entry_station, 
                         exit_station=exit_station)
        journey.is_complete = True
        
        cost = journey.calculate_cost()
        self.assertAlmostEqual(cost, 2.40, places=2)
    
    def test_complete_journey_zone2_to_zone3(self):
        """Test journey from zone 2 to zone 3: £3.00"""
        entry_station = Station("Hammersmith", 2)
        exit_station = Station("Richmond", 3)
        
        journey = Journey("user003", entry_station=entry_station, 
                         exit_station=exit_station)
        journey.is_complete = True
        
        cost = journey.calculate_cost()
        self.assertAlmostEqual(cost, 3.00, places=2)
    
    def test_incomplete_journey(self):
        """Test incomplete journey: £5.00"""
        entry_station = Station("Victoria", 1)
        
        journey = Journey("user004", entry_station=entry_station)
        journey.is_complete = False
        
        cost = journey.calculate_cost()
        self.assertAlmostEqual(cost, 5.00, places=2)


class TestBillingSystem(unittest.TestCase):
    """Test cases for BillingSystem class."""
    
    def setUp(self):
        self.billing_system = BillingSystem()
        self.temp_dir = tempfile.mkdtemp()
    
    def create_test_zone_map(self):
        """Create a simple zone map for testing."""
        zone_map_path = os.path.join(self.temp_dir, "zone_map.csv")
        with open(zone_map_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['station', 'zone'])
            writer.writerow(['Paddington', '1'])
            writer.writerow(['Bank', '1'])
            writer.writerow(['Victoria', '1'])
            writer.writerow(['Hammersmith', '2'])
            writer.writerow(['Richmond', '3'])
            writer.writerow(['Heathrow Terminal 5', '4'])
            writer.writerow(['Epping', '5'])
            writer.writerow(['Woolwich', '6'])
        return zone_map_path
    
    def test_load_zone_map(self):
        """Test loading zone map from CSV."""
        zone_map_path = self.create_test_zone_map()
        self.billing_system.load_zone_map(zone_map_path)
        
        self.assertEqual(len(self.billing_system.stations), 8)
        self.assertEqual(self.billing_system.stations['Paddington'].zone, 1)
        self.assertEqual(self.billing_system.stations['Woolwich'].zone, 6)
    
    def test_daily_cap(self):
        """Test that daily cap of £15 is applied."""
        zone_map_path = self.create_test_zone_map()
        self.billing_system.load_zone_map(zone_map_path)
        
        # Create journey data that would exceed daily cap
        journey_data_path = os.path.join(self.temp_dir, "journey_data.csv")
        with open(journey_data_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'direction', 'station', 'timestamp'])
            
            # Multiple zone 1 to zone 1 journeys (£3.60 each)
            # 5 journeys would be £18.00 without cap
            for i in range(5):
                writer.writerow(['user001', 'IN', 'Paddington', f'2024-01-15T{8+i:02d}:00:00'])
                writer.writerow(['user001', 'OUT', 'Bank', f'2024-01-15T{8+i:02d}:30:00'])
        
        results = self.billing_system.process_journey_data(journey_data_path)
        
        # Should be capped at £15.00
        self.assertAlmostEqual(results['user001'], 15.00, places=2)
    
    def test_monthly_cap(self):
        """Test that monthly cap of £100 is applied."""
        zone_map_path = self.create_test_zone_map()
        self.billing_system.load_zone_map(zone_map_path)
        
        # Create journey data that would exceed monthly cap
        journey_data_path = os.path.join(self.temp_dir, "journey_data.csv")
        with open(journey_data_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'direction', 'station', 'timestamp'])
            
            # Create journeys across multiple days
            # Each day has 4 zone 1-1 journeys = £14.40 (under daily cap)
            # 10 days = £144.00 without monthly cap
            for day in range(1, 11):
                for i in range(4):
                    writer.writerow(['user001', 'IN', 'Paddington', 
                                   f'2024-01-{day:02d}T{8+i*2:02d}:00:00'])
                    writer.writerow(['user001', 'OUT', 'Bank', 
                                   f'2024-01-{day:02d}T{8+i*2:02d}:30:00'])
        
        results = self.billing_system.process_journey_data(journey_data_path)
        
        # Should be capped at £100.00
        self.assertAlmostEqual(results['user001'], 100.00, places=2)
    
    def test_erroneous_journeys(self):
        """Test handling of erroneous journeys (missing IN or OUT)."""
        zone_map_path = self.create_test_zone_map()
        self.billing_system.load_zone_map(zone_map_path)
        
        journey_data_path = os.path.join(self.temp_dir, "journey_data.csv")
        with open(journey_data_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'direction', 'station', 'timestamp'])
            
            # Missing OUT
            writer.writerow(['user001', 'IN', 'Paddington', '2024-01-15T08:00:00'])
            
            # Missing IN
            writer.writerow(['user002', 'OUT', 'Bank', '2024-01-15T09:00:00'])
            
            # Complete journey for comparison
            writer.writerow(['user003', 'IN', 'Paddington', '2024-01-15T08:00:00'])
            writer.writerow(['user003', 'OUT', 'Bank', '2024-01-15T08:30:00'])
        
        results = self.billing_system.process_journey_data(journey_data_path)
        
        self.assertAlmostEqual(results['user001'], 5.00, places=2)  # Erroneous journey
        self.assertAlmostEqual(results['user002'], 5.00, places=2)  # Erroneous journey
        self.assertAlmostEqual(results['user003'], 3.60, places=2)  # Complete journey
    
    def test_save_results(self):
        """Test saving results to CSV."""
        results = {
            'user001': 15.00,
            'user002': 7.50,
            'user003': 3.60
        }
        
        output_path = os.path.join(self.temp_dir, "output.csv")
        self.billing_system.save_results(results, output_path)
        
        # Read back and verify
        with open(output_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]['user_id'], 'user001')
        self.assertEqual(rows[0]['total_cost'], '15.00')
        self.assertEqual(rows[1]['user_id'], 'user002')
        self.assertEqual(rows[1]['total_cost'], '7.50')
        self.assertEqual(rows[2]['user_id'], 'user003')
        self.assertEqual(rows[2]['total_cost'], '3.60')


if __name__ == '__main__':
    unittest.main()







