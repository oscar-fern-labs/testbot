# Mass Transit Billing System Implementation

## Overview

This implementation provides a complete billing system for a mass transit network with zone-based pricing, daily caps (£15), and monthly caps (£100).

## Project Structure

```
testbot/
├── src/
│   └── mass_transit_billing.py    # Main billing system implementation
├── tests/
│   └── test_mass_transit_billing.py # Comprehensive unit tests
├── resources/
│   ├── zone_map.csv               # Station-to-zone mapping
│   ├── journey_data.csv           # Sample journey data
│   └── output.csv                 # Generated billing output
├── README.md                      # Original requirements
├── IMPLEMENTATION.md              # This file
├── requirements.txt               # Python dependencies (none required)
└── .gitignore                     # Git ignore file
```

## Key Features

1. **Zone-based Pricing**:
   - Base fee: £2.00 for all journeys
   - Zone 1: £0.80 additional
   - Zones 2-3: £0.50 additional
   - Zones 4-5: £0.30 additional
   - Zones 6+: £0.10 additional

2. **Billing Caps**:
   - Daily cap: £15.00
   - Monthly cap: £100.00

3. **Error Handling**:
   - Erroneous journeys (missing IN or OUT): £5.00 flat fee
   - All valid journeys must complete before midnight

4. **Data Processing**:
   - Reads zone mapping from CSV
   - Processes journey data chronologically
   - Outputs user billing totals to CSV

## Usage

```bash
cd src
python3 mass_transit_billing.py ../resources/zone_map.csv ../resources/journey_data.csv ../resources/output.csv
```

## Testing

Run the comprehensive test suite:

```bash
python3 -m unittest tests.test_mass_transit_billing -v
```

## Design Decisions

1. **Object-Oriented Design**: Separate classes for Station, Journey, and BillingSystem for clarity and maintainability.

2. **Efficient Cap Tracking**: Daily and monthly costs are tracked separately to efficiently apply caps without recalculating previous journeys.

3. **Incomplete Journey Handling**: The system tracks incomplete journeys per user per day, automatically marking unmatched entries as erroneous.

4. **Floating-Point Precision**: Output formatting uses `.2f` to ensure consistent monetary display.

5. **Extensibility**: The design allows for easy addition of new zones, pricing rules, or cap structures.

## Assumptions

- All timestamps are in ISO format and UTC
- Station names in journey data match exactly with zone map
- Users can only have one incomplete journey per day
- Zone numbers are positive integers starting from 1
