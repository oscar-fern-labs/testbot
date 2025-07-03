"""
Mass Transit Billing System

A billing system for a mass transit network that calculates journey costs
based on zones with daily and monthly caps.
"""

import csv
import sys
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


class Station:
    """Represents a station with its zone information."""
    
    def __init__(self, name: str, zone: int):
        self.name = name
        self.zone = zone


class Journey:
    """Represents a journey with entry and exit information."""
    
    def __init__(self, user_id: str, entry_station: Optional[Station] = None, 
                 entry_time: Optional[datetime] = None, exit_station: Optional[Station] = None, 
                 exit_time: Optional[datetime] = None):
        self.user_id = user_id
        self.entry_station = entry_station
        self.entry_time = entry_time
        self.exit_station = exit_station
        self.exit_time = exit_time
        self.cost = 0.0
        self.is_complete = False
    
    def calculate_cost(self) -> float:
        """Calculate the cost of the journey based on zones."""
        if not self.is_complete:
            # Erroneous journey (missing IN or OUT)
            self.cost = 5.00
            return self.cost
        
        # Base fee
        base_fee = 2.00
        
        # Zone-based additional costs
        entry_zone_cost = self._get_zone_cost(self.entry_station.zone)
        exit_zone_cost = self._get_zone_cost(self.exit_station.zone)
        
        self.cost = base_fee + entry_zone_cost + exit_zone_cost
        return self.cost
    
    def _get_zone_cost(self, zone: int) -> float:
        """Get additional cost based on zone."""
        if zone == 1:
            return 0.80
        elif 2 <= zone <= 3:
            return 0.50
        elif 4 <= zone <= 5:
            return 0.30
        else:  # zone >= 6
            return 0.10


class BillingSystem:
    """Main billing system that processes journeys and calculates costs."""
    
    def __init__(self):
        self.stations: Dict[str, Station] = {}
        self.daily_cap = 15.00
        self.monthly_cap = 100.00
    
    def load_zone_map(self, filepath: str) -> None:
        """Load station zone mapping from CSV file."""
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                station_name = row['station']
                zone = int(row['zone'])
                self.stations[station_name] = Station(station_name, zone)
    
    def process_journey_data(self, filepath: str) -> Dict[str, float]:
        """Process journey data and calculate total costs per user."""
        # Track incomplete journeys per user per day
        incomplete_journeys: Dict[str, Dict[str, Journey]] = defaultdict(lambda: defaultdict(lambda: None))
        
        # Track costs per user per day and month
        daily_costs: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        monthly_costs: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        total_costs: Dict[str, float] = defaultdict(float)
        
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                user_id = row['user_id']
                direction = row['direction']
                station_name = row['station']
                timestamp = datetime.fromisoformat(row['timestamp'])
                
                date_key = timestamp.strftime('%Y-%m-%d')
                month_key = timestamp.strftime('%Y-%m')
                user_date_key = f"{user_id}_{date_key}"
                
                station = self.stations.get(station_name)
                if not station:
                    continue
                
                if direction == 'IN':
                    # Check if there's already an incomplete journey for this user on this day
                    if incomplete_journeys[user_id][date_key]:
                        # Previous journey was incomplete
                        prev_journey = incomplete_journeys[user_id][date_key]
                        prev_journey.cost = 5.00
                        self._apply_journey_cost(prev_journey, daily_costs, monthly_costs, 
                                                total_costs, date_key, month_key)
                    
                    # Start new journey
                    journey = Journey(user_id, entry_station=station, entry_time=timestamp)
                    incomplete_journeys[user_id][date_key] = journey
                
                elif direction == 'OUT':
                    # Complete the journey if there's a matching IN
                    if incomplete_journeys[user_id][date_key]:
                        journey = incomplete_journeys[user_id][date_key]
                        journey.exit_station = station
                        journey.exit_time = timestamp
                        journey.is_complete = True
                        journey.calculate_cost()
                        
                        self._apply_journey_cost(journey, daily_costs, monthly_costs, 
                                               total_costs, date_key, month_key)
                        
                        # Remove completed journey
                        incomplete_journeys[user_id][date_key] = None
                    else:
                        # OUT without IN - erroneous journey
                        journey = Journey(user_id, exit_station=station, exit_time=timestamp)
                        journey.cost = 5.00
                        self._apply_journey_cost(journey, daily_costs, monthly_costs, 
                                               total_costs, date_key, month_key)
        
        # Handle remaining incomplete journeys
        for user_id, user_journeys in incomplete_journeys.items():
            for date_key, journey in user_journeys.items():
                if journey:
                    journey.cost = 5.00
                    month_key = datetime.strptime(date_key, '%Y-%m-%d').strftime('%Y-%m')
                    self._apply_journey_cost(journey, daily_costs, monthly_costs, 
                                           total_costs, date_key, month_key)
        
        return dict(total_costs)
    
    def _apply_journey_cost(self, journey: Journey, daily_costs: Dict, monthly_costs: Dict,
                           total_costs: Dict, date_key: str, month_key: str) -> None:
        """Apply journey cost with daily and monthly caps."""
        user_id = journey.user_id
        
        # Check daily cap
        if daily_costs[user_id][date_key] >= self.daily_cap:
            # Daily cap reached, no additional cost
            return
        
        # Check monthly cap
        if monthly_costs[user_id][month_key] >= self.monthly_cap:
            # Monthly cap reached, no additional cost
            return
        
        # Apply cost up to caps
        remaining_daily = self.daily_cap - daily_costs[user_id][date_key]
        remaining_monthly = self.monthly_cap - monthly_costs[user_id][month_key]
        
        actual_cost = min(journey.cost, remaining_daily, remaining_monthly)
        
        daily_costs[user_id][date_key] += actual_cost
        monthly_costs[user_id][month_key] += actual_cost
        total_costs[user_id] += actual_cost
    
    def save_results(self, results: Dict[str, float], filepath: str) -> None:
        """Save billing results to CSV file."""
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['user_id', 'total_cost']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for user_id, total_cost in sorted(results.items()):
                writer.writerow({
                    'user_id': user_id,
                    'total_cost': f"{total_cost:.2f}"
                })


def main():
    """Main entry point for the billing system."""
    if len(sys.argv) != 4:
        print("Usage: python mass_transit_billing.py <zone_map_file> <journey_data_file> <output_file>")
        sys.exit(1)
    
    zone_map_file = sys.argv[1]
    journey_data_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Initialize billing system
    billing_system = BillingSystem()
    
    try:
        # Load zone map
        billing_system.load_zone_map(zone_map_file)
        
        # Process journey data
        results = billing_system.process_journey_data(journey_data_file)
        
        # Save results
        billing_system.save_results(results, output_file)
        
        print(f"Billing calculation complete. Results saved to {output_file}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
