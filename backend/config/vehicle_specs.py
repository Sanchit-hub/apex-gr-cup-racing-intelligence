"""Toyota GR86 Cup Car Specifications and Track Data."""

# Toyota GR86 Cup Car Specifications
GR86_CUP_SPECS = {
    "engine": {
        "type": "2.4L Flat-4 Boxer",
        "horsepower": 228,
        "torque_nm": 249,
        "redline_rpm": 7400,
        "max_rpm": 7500
    },
    "performance": {
        "top_speed_kmh": 225,
        "top_speed_mph": 140,
        "weight_kg": 1270,
        "weight_lbs": 2800,
        "power_to_weight": 0.179,  # hp/kg
        "0_to_60_mph": 6.1
    },
    "dimensions": {
        "wheelbase_mm": 2575,
        "length_mm": 4240,
        "width_mm": 1775,
        "height_mm": 1310
    },
    "drivetrain": {
        "type": "RWD",
        "transmission": "6-speed manual",
        "final_drive": 4.3
    },
    "suspension": {
        "front": "MacPherson strut",
        "rear": "Double wishbone",
        "adjustable_dampers": True
    },
    "brakes": {
        "front": "Brembo 4-piston",
        "rear": "Brembo 2-piston",
        "abs": True
    },
    "tires": {
        "compound": "Michelin Pilot Sport Cup 2",
        "front_size": "215/45R17",
        "rear_size": "215/45R17",
        "optimal_temp_c": 85,
        "optimal_pressure_psi": 32
    }
}

# Track-specific data
TRACK_DATA = {
    "barber_motorsports_park": {
        "name": "Barber Motorsports Park",
        "location": "Birmingham, Alabama",
        "length_km": 3.7,
        "length_miles": 2.3,
        "turns": 17,
        "direction": "Clockwise",
        "elevation_change_m": 24,
        "track_record": {
            "time": 89.5,  # seconds
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3,
        "key_corners": {
            "Turn 1": {"type": "Heavy braking", "speed_kmh": 80},
            "Turn 5": {"type": "High-speed", "speed_kmh": 140},
            "Turn 15": {"type": "Technical", "speed_kmh": 95}
        }
    },
    "circuit_of_the_americas": {
        "name": "Circuit of the Americas",
        "location": "Austin, Texas",
        "length_km": 5.513,
        "length_miles": 3.426,
        "turns": 20,
        "direction": "Counter-clockwise",
        "elevation_change_m": 41,
        "track_record": {
            "time": 125.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3,
        "key_corners": {
            "Turn 1": {"type": "Uphill heavy braking", "speed_kmh": 70},
            "Turn 11": {"type": "High-speed", "speed_kmh": 160},
            "Turn 19": {"type": "Fast chicane", "speed_kmh": 120}
        }
    },
    "indianapolis": {
        "name": "Indianapolis Motor Speedway Road Course",
        "location": "Indianapolis, Indiana",
        "length_km": 3.925,
        "length_miles": 2.439,
        "turns": 14,
        "direction": "Clockwise",
        "elevation_change_m": 8,
        "track_record": {
            "time": 95.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3
    },
    "road_america": {
        "name": "Road America",
        "location": "Elkhart Lake, Wisconsin",
        "length_km": 6.515,
        "length_miles": 4.048,
        "turns": 14,
        "direction": "Clockwise",
        "elevation_change_m": 45,
        "track_record": {
            "time": 145.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3
    },
    "sebring": {
        "name": "Sebring International Raceway",
        "location": "Sebring, Florida",
        "length_km": 6.019,
        "length_miles": 3.74,
        "turns": 17,
        "direction": "Clockwise",
        "elevation_change_m": 9,
        "track_record": {
            "time": 135.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3
    },
    "sonoma": {
        "name": "Sonoma Raceway",
        "location": "Sonoma, California",
        "length_km": 4.052,
        "length_miles": 2.52,
        "turns": 12,
        "direction": "Clockwise",
        "elevation_change_m": 52,
        "track_record": {
            "time": 105.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3
    },
    "virginia_international_raceway": {
        "name": "Virginia International Raceway",
        "location": "Alton, Virginia",
        "length_km": 5.263,
        "length_miles": 3.27,
        "turns": 18,
        "direction": "Clockwise",
        "elevation_change_m": 30,
        "track_record": {
            "time": 120.0,
            "driver": "Professional",
            "year": 2024
        },
        "sectors": 3
    }
}

# Performance thresholds for analysis
PERFORMANCE_THRESHOLDS = {
    "excellent_consistency": 0.5,  # Within 0.5s of best lap
    "good_consistency": 1.0,
    "average_consistency": 2.0,
    "max_lateral_g": 1.2,  # GR86 Cup car limit
    "max_braking_g": 1.4,
    "max_acceleration_g": 0.8,
    "optimal_brake_temp_c": 450,
    "max_brake_temp_c": 650,
    "tire_deg_rate_normal": 0.1,  # seconds per lap
    "tire_deg_rate_aggressive": 0.2
}
