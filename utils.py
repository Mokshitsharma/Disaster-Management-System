import re
from datetime import datetime, timedelta
from typing import Dict, List
import random

def format_message(content: str) -> str:
    """
    Format message content for display with proper styling.
    
    Args:
        content: Raw message content
    
    Returns:
        Formatted HTML string
    """
    
    # Convert markdown-style formatting
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    
    # Convert line breaks
    content = content.replace('\n', '<br>')
    
    # Highlight emergency keywords
    emergency_keywords = {
        'CRITICAL': '<span style="color: #ff4444; font-weight: bold;">CRITICAL</span>',
        'WARNING': '<span style="color: #ff9800; font-weight: bold;">WARNING</span>',
        'ALERT': '<span style="color: #ff5722; font-weight: bold;">ALERT</span>',
        'URGENT': '<span style="color: #f44336; font-weight: bold;">URGENT</span>',
    }
    
    for keyword, replacement in emergency_keywords.items():
        content = re.sub(f'\\b{keyword}\\b', replacement, content, flags=re.IGNORECASE)
    
    return content


def get_disaster_stats(disasters: List[Dict]) -> Dict:
    """
    Calculate statistics from disaster data.
    
    Args:
        disasters: List of disaster dictionaries
    
    Returns:
        Dictionary of statistics
    """
    
    active_count = sum(1 for d in disasters if d.get('status') == 'Active')
    monitoring_count = len(disasters)
    
    # Calculate responses (simulated based on disasters)
    responses = active_count * 15 + monitoring_count * 5 + random.randint(5, 20)
    
    return {
        'active': active_count,
        'monitoring': monitoring_count,
        'responses': responses,
        'critical': sum(1 for d in disasters if d.get('severity') == 'Critical'),
        'high': sum(1 for d in disasters if d.get('severity') == 'High'),
    }


def load_mock_disasters() -> List[Dict]:
    """
    Load mock disaster data for testing/demo purposes.
    
    Returns:
        List of disaster dictionaries
    """
    
    disasters = [
        {
            'id': 1,
            'type': 'Earthquake',
            'location': 'California, USA',
            'severity': 'High',
            'status': 'Active',
            'time': '2 hours ago',
            'lat': 34.0522,
            'lng': -118.2437,
            'magnitude': '6.2',
            'depth': '10 km',
            'affected_population': '~2 million'
        },
        {
            'id': 2,
            'type': 'Wildfire',
            'location': 'New South Wales, Australia',
            'severity': 'Critical',
            'status': 'Monitoring',
            'time': '5 hours ago',
            'lat': -33.8688,
            'lng': 151.2093,
            'area': '50,000 acres',
            'containment': '25%',
            'evacuations': '15,000 people'
        },
        {
            'id': 3,
            'type': 'Flood',
            'location': 'Dhaka, Bangladesh',
            'severity': 'Medium',
            'status': 'Active',
            'time': '1 day ago',
            'lat': 23.8103,
            'lng': 90.4125,
            'water_level': '2.5 meters above normal',
            'affected_areas': '12 districts'
        },
        {
            'id': 4,
            'type': 'Hurricane',
            'location': 'Caribbean Sea',
            'severity': 'High',
            'status': 'Monitoring',
            'time': '3 hours ago',
            'lat': 18.2208,
            'lng': -66.5901,
            'category': 'Category 3',
            'wind_speed': '120 mph',
            'projected_path': 'Northward'
        },
        {
            'id': 5,
            'type': 'Tornado',
            'location': 'Oklahoma, USA',
            'severity': 'Medium',
            'status': 'Resolved',
            'time': '6 hours ago',
            'lat': 35.4676,
            'lng': -97.5164,
            'ef_scale': 'EF-2',
            'path_length': '15 miles'
        }
    ]
    
    return disasters


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula.
    
    Args:
        lat1, lon1: First coordinate
        lat2, lon2: Second coordinate
    
    Returns:
        Distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance


def format_time_ago(time_str: str) -> str:
    """
    Convert time string to human-readable "time ago" format.
    
    Args:
        time_str: Time string (e.g., "2 hours ago")
    
    Returns:
        Formatted time string
    """
    
    # If already in "X ago" format, return as is
    if 'ago' in time_str:
        return time_str
    
    # Otherwise, try to parse and format
    try:
        time_obj = datetime.fromisoformat(time_str)
        now = datetime.now()
        diff = now - time_obj
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return time_str


def get_severity_color(severity: str) -> str:
    """
    Get color code for disaster severity level.
    
    Args:
        severity: Severity level string
    
    Returns:
        Color hex code
    """
    
    colors = {
        'Critical': '#ff4444',
        'High': '#ff9800',
        'Medium': '#ffd93d',
        'Low': '#4facfe',
        'Resolved': '#6bcf7f'
    }
    
    return colors.get(severity, '#999999')


def validate_coordinates(lat: float, lng: float) -> bool:
    """
    Validate latitude and longitude coordinates.
    
    Args:
        lat: Latitude
        lng: Longitude
    
    Returns:
        True if valid, False otherwise
    """
    
    return -90 <= lat <= 90 and -180 <= lng <= 180


def generate_disaster_id() -> str:
    """
    Generate a unique disaster ID.
    
    Returns:
        Unique disaster ID string
    """
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = random.randint(1000, 9999)
    return f"DIS-{timestamp}-{random_suffix}"


def sanitize_input(user_input: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        user_input: Raw user input
    
    Returns:
        Sanitized input
    """
    
    # Remove any potentially harmful characters
    sanitized = re.sub(r'[<>\"\'%;()&+]', '', user_input)
    
    # Limit length
    max_length = 1000
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()


def format_coordinates(lat: float, lng: float) -> str:
    """
    Format coordinates for display.
    
    Args:
        lat: Latitude
        lng: Longitude
    
    Returns:
        Formatted coordinate string
    """
    
    lat_dir = 'N' if lat >= 0 else 'S'
    lng_dir = 'E' if lng >= 0 else 'W'
    
    return f"{abs(lat):.4f}°{lat_dir}, {abs(lng):.4f}°{lng_dir}"


def get_emergency_priority(severity: str, status: str) -> int:
    """
    Calculate emergency priority score.
    
    Args:
        severity: Disaster severity
        status: Disaster status
    
    Returns:
        Priority score (1-10, higher is more urgent)
    """
    
    severity_scores = {
        'Critical': 10,
        'High': 7,
        'Medium': 4,
        'Low': 2
    }
    
    status_multiplier = {
        'Active': 1.0,
        'Monitoring': 0.7,
        'Resolved': 0.3
    }
    
    base_score = severity_scores.get(severity, 1)
    multiplier = status_multiplier.get(status, 0.5)
    
    return int(base_score * multiplier)


def export_disaster_report(disasters: List[Dict]) -> str:
    """
    Export disaster data as a formatted report.
    
    Args:
        disasters: List of disaster dictionaries
    
    Returns:
        Formatted report string
    """
    
    report = "=" * 60 + "\n"
    report += "DISASTER RESPONSE REPORT\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += "=" * 60 + "\n\n"
    
    stats = get_disaster_stats(disasters)
    report += f"SUMMARY:\n"
    report += f"  Active Disasters: {stats['active']}\n"
    report += f"  Monitoring: {stats['monitoring']}\n"
    report += f"  Critical Level: {stats['critical']}\n"
    report += f"  High Level: {stats['high']}\n\n"
    
    report += "ACTIVE DISASTERS:\n"
    report += "-" * 60 + "\n"
    
    for disaster in sorted(disasters, key=lambda x: get_emergency_priority(x['severity'], x['status']), reverse=True):
        report += f"\n{disaster['type']} - {disaster['location']}\n"
        report += f"  Severity: {disaster['severity']}\n"
        report += f"  Status: {disaster['status']}\n"
        report += f"  Time: {disaster['time']}\n"
        report += f"  Coordinates: {format_coordinates(disaster['lat'], disaster['lng'])}\n"
    
    report += "\n" + "=" * 60 + "\n"
    
    return report