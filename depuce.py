from typing import List, Dict, Set
from datetime import datetime
import hashlib

class DisasterDeduplicator:
    """
    Handles deduplication of disaster data to prevent duplicate entries
    and ensure data integrity in the disaster monitoring system.
    """
    
    def __init__(self):
        """Initialize the deduplicator with tracking sets."""
        self.seen_hashes: Set[str] = set()
        self.disaster_signatures: Dict[str, Dict] = {}
    
    def generate_signature(self, disaster: Dict) -> str:
        """
        Generate a unique signature for a disaster based on key attributes.
        
        Args:
            disaster: Disaster data dictionary
        
        Returns:
            Unique signature string
        """
        
        # Create signature from key fields
        signature_parts = [
            disaster.get('type', '').lower(),
            disaster.get('location', '').lower(),
            str(disaster.get('lat', 0)),
            str(disaster.get('lng', 0)),
            disaster.get('time', '').split()[0]  # Use date part only
        ]
        
        signature_string = '|'.join(signature_parts)
        
        # Create hash
        signature_hash = hashlib.md5(signature_string.encode()).hexdigest()
        
        return signature_hash
    
    def is_duplicate(self, disaster: Dict, threshold: float = 0.9) -> bool:
        """
        Check if a disaster is a duplicate of an existing entry.
        
        Args:
            disaster: Disaster data dictionary
            threshold: Similarity threshold (0.0-1.0)
        
        Returns:
            True if duplicate, False otherwise
        """
        
        signature = self.generate_signature(disaster)
        
        # Check exact match
        if signature in self.seen_hashes:
            return True
        
        # Check similar disasters
        for existing_sig, existing_disaster in self.disaster_signatures.items():
            similarity = self.calculate_similarity(disaster, existing_disaster)
            if similarity >= threshold:
                return True
        
        return False
    
    def add_disaster(self, disaster: Dict) -> bool:
        """
        Add a disaster to the tracking system if it's not a duplicate.
        
        Args:
            disaster: Disaster data dictionary
        
        Returns:
            True if added, False if duplicate
        """
        
        if self.is_duplicate(disaster):
            return False
        
        signature = self.generate_signature(disaster)
        self.seen_hashes.add(signature)
        self.disaster_signatures[signature] = disaster
        
        return True
    
    def calculate_similarity(self, disaster1: Dict, disaster2: Dict) -> float:
        """
        Calculate similarity score between two disasters.
        
        Args:
            disaster1: First disaster dictionary
            disaster2: Second disaster dictionary
        
        Returns:
            Similarity score (0.0-1.0)
        """
        
        score = 0.0
        total_weight = 0.0
        
        # Type similarity (weight: 0.3)
        if disaster1.get('type', '').lower() == disaster2.get('type', '').lower():
            score += 0.3
        total_weight += 0.3
        
        # Location similarity (weight: 0.3)
        if disaster1.get('location', '').lower() == disaster2.get('location', '').lower():
            score += 0.3
        total_weight += 0.3
        
        # Coordinate proximity (weight: 0.2)
        coord_similarity = self.calculate_coordinate_similarity(
            disaster1.get('lat', 0), disaster1.get('lng', 0),
            disaster2.get('lat', 0), disaster2.get('lng', 0)
        )
        score += coord_similarity * 0.2
        total_weight += 0.2
        
        # Time similarity (weight: 0.2)
        time_similarity = self.calculate_time_similarity(
            disaster1.get('time', ''), 
            disaster2.get('time', '')
        )
        score += time_similarity * 0.2
        total_weight += 0.2
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def calculate_coordinate_similarity(self, lat1: float, lng1: float, 
                                       lat2: float, lng2: float) -> float:
        """
        Calculate similarity based on coordinate proximity.
        
        Args:
            lat1, lng1: First coordinate pair
            lat2, lng2: Second coordinate pair
        
        Returns:
            Similarity score (0.0-1.0)
        """
        
        from math import radians, sin, cos, sqrt, atan2
        
        # Haversine formula for distance
        R = 6371  # Earth radius in km
        
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        # Consider disasters within 50km as similar
        if distance < 50:
            return 1.0 - (distance / 50)
        else:
            return 0.0
    
    def calculate_time_similarity(self, time1: str, time2: str) -> float:
        """
        Calculate similarity based on time proximity.
        
        Args:
            time1: First time string
            time2: Second time string
        
        Returns:
            Similarity score (0.0-1.0)
        """
        
        # Parse time strings (handle "X hours ago" format)
        try:
            # Simple hour extraction
            if 'hour' in time1 and 'hour' in time2:
                hours1 = int(time1.split()[0])
                hours2 = int(time2.split()[0])
                diff = abs(hours1 - hours2)
                
                # Consider within 6 hours as similar
                if diff < 6:
                    return 1.0 - (diff / 6)
            
            return 0.0
        except:
            return 0.0
    
    def deduplicate_list(self, disasters: List[Dict]) -> List[Dict]:
        """
        Remove duplicates from a list of disasters.
        
        Args:
            disasters: List of disaster dictionaries
        
        Returns:
            Deduplicated list
        """
        
        unique_disasters = []
        
        for disaster in disasters:
            if not self.is_duplicate(disaster):
                self.add_disaster(disaster)
                unique_disasters.append(disaster)
        
        return unique_disasters
    
    def merge_similar_disasters(self, disasters: List[Dict], 
                                threshold: float = 0.8) -> List[Dict]:
        """
        Merge similar disasters into single entries with combined data.
        
        Args:
            disasters: List of disaster dictionaries
            threshold: Similarity threshold for merging
        
        Returns:
            List of merged disasters
        """
        
        if not disasters:
            return []
        
        merged = []
        processed = set()
        
        for i, disaster1 in enumerate(disasters):
            if i in processed:
                continue
            
            # Start with current disaster
            merged_disaster = disaster1.copy()
            similar_disasters = [disaster1]
            
            # Find similar disasters
            for j, disaster2 in enumerate(disasters[i+1:], start=i+1):
                if j in processed:
                    continue
                
                similarity = self.calculate_similarity(disaster1, disaster2)
                if similarity >= threshold:
                    similar_disasters.append(disaster2)
                    processed.add(j)
            
            # Merge data if multiple similar disasters found
            if len(similar_disasters) > 1:
                merged_disaster['merged_count'] = len(similar_disasters)
                merged_disaster['sources'] = [
                    d.get('source', 'Unknown') for d in similar_disasters
                ]
            
            merged.append(merged_disaster)
            processed.add(i)
        
        return merged
    
    def get_statistics(self) -> Dict:
        """
        Get deduplication statistics.
        
        Returns:
            Dictionary of statistics
        """
        
        return {
            'unique_disasters': len(self.disaster_signatures),
            'total_signatures': len(self.seen_hashes),
            'duplicates_prevented': len(self.seen_hashes) - len(self.disaster_signatures)
        }
    
    def clear(self):
        """Clear all tracking data."""
        self.seen_hashes.clear()
        self.disaster_signatures.clear()


def deduplicate_disasters(disasters: List[Dict], 
                         merge: bool = False,
                         threshold: float = 0.9) -> List[Dict]:
    """
    Convenience function to deduplicate a list of disasters.
    
    Args:
        disasters: List of disaster dictionaries
        merge: Whether to merge similar disasters
        threshold: Similarity threshold
    
    Returns:
        Deduplicated list
    """
    
    deduplicator = DisasterDeduplicator()
    
    if merge:
        return deduplicator.merge_similar_disasters(disasters, threshold)
    else:
        return deduplicator.deduplicate_list(disasters)


# Example usage
if __name__ == "__main__":
    # Test deduplication
    test_disasters = [
        {
            'type': 'Earthquake',
            'location': 'California',
            'lat': 34.05,
            'lng': -118.24,
            'time': '2 hours ago'
        },
        {
            'type': 'Earthquake',
            'location': 'California',
            'lat': 34.06,
            'lng': -118.25,
            'time': '2 hours ago'
        },
        {
            'type': 'Wildfire',
            'location': 'Australia',
            'lat': -33.87,
            'lng': 151.21,
            'time': '5 hours ago'
        }
    ]
    
    deduped = deduplicate_disasters(test_disasters)
    print(f"Original: {len(test_disasters)} disasters")
    print(f"After deduplication: {len(deduped)} disasters")