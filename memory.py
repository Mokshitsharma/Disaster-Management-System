from datetime import datetime
from typing import List, Dict
import json

class ConversationMemory:
    """
    Manages conversation history and context for the disaster AI agent.
    Stores messages, user preferences, and disaster tracking information.
    """
    
    def __init__(self):
        """Initialize conversation memory."""
        self.messages = []
        self.user_context = {}
        self.disaster_context = {}
        self.max_messages = 100  # Maximum messages to keep in memory
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            role: Either 'user' or 'assistant'
            content: The message content
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().strftime('%I:%M %p')
        }
        
        self.messages.append(message)
        
        # Keep only the most recent messages to prevent memory overflow
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[Dict]:
        """
        Get all messages in the conversation.
        
        Returns:
            List of message dictionaries
        """
        return self.messages
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get conversation history formatted for Claude API.
        
        Returns:
            List of messages with role and content only
        """
        return [
            {
                'role': msg['role'],
                'content': msg['content']
            }
            for msg in self.messages
        ]
    
    def clear_messages(self) -> None:
        """Clear all messages from memory."""
        self.messages = []
    
    def set_user_context(self, key: str, value: any) -> None:
        """
        Store user-specific context information.
        
        Args:
            key: Context key (e.g., 'location', 'preferences')
            value: Context value
        """
        self.user_context[key] = value
    
    def get_user_context(self, key: str, default=None) -> any:
        """
        Retrieve user context information.
        
        Args:
            key: Context key
            default: Default value if key doesn't exist
        
        Returns:
            Context value or default
        """
        return self.user_context.get(key, default)
    
    def update_disaster_context(self, disaster_id: str, data: Dict) -> None:
        """
        Update context for a specific disaster.
        
        Args:
            disaster_id: Unique disaster identifier
            data: Disaster data dictionary
        """
        self.disaster_context[disaster_id] = {
            **data,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_disaster_context(self, disaster_id: str) -> Dict:
        """
        Get context for a specific disaster.
        
        Args:
            disaster_id: Unique disaster identifier
        
        Returns:
            Disaster context dictionary
        """
        return self.disaster_context.get(disaster_id, {})
    
    def get_recent_disasters(self, limit: int = 5) -> List[Dict]:
        """
        Get most recently updated disasters.
        
        Args:
            limit: Maximum number of disasters to return
        
        Returns:
            List of disaster context dictionaries
        """
        disasters = sorted(
            self.disaster_context.values(),
            key=lambda x: x.get('last_updated', ''),
            reverse=True
        )
        return disasters[:limit]
    
    def export_conversation(self) -> str:
        """
        Export conversation history as JSON string.
        
        Returns:
            JSON string of conversation
        """
        export_data = {
            'messages': self.messages,
            'user_context': self.user_context,
            'disaster_context': self.disaster_context,
            'exported_at': datetime.now().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def import_conversation(self, json_data: str) -> bool:
        """
        Import conversation history from JSON string.
        
        Args:
            json_data: JSON string containing conversation data
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = json.loads(json_data)
            self.messages = data.get('messages', [])
            self.user_context = data.get('user_context', {})
            self.disaster_context = data.get('disaster_context', {})
            return True
        except Exception as e:
            print(f"Error importing conversation: {e}")
            return False
    
    def get_summary(self) -> Dict:
        """
        Get a summary of the conversation and context.
        
        Returns:
            Summary dictionary
        """
        return {
            'total_messages': len(self.messages),
            'user_messages': len([m for m in self.messages if m['role'] == 'user']),
            'assistant_messages': len([m for m in self.messages if m['role'] == 'assistant']),
            'tracked_disasters': len(self.disaster_context),
            'user_context_keys': list(self.user_context.keys())
        }
    
    def search_messages(self, keyword: str) -> List[Dict]:
        """
        Search for messages containing a specific keyword.
        
        Args:
            keyword: Keyword to search for
        
        Returns:
            List of matching messages
        """
        keyword_lower = keyword.lower()
        return [
            msg for msg in self.messages
            if keyword_lower in msg['content'].lower()
        ]
    
    def get_message_count(self) -> int:
        """
        Get the total number of messages.
        
        Returns:
            Message count
        """
        return len(self.messages)
    
    def __repr__(self) -> str:
        """String representation of conversation memory."""
        summary = self.get_summary()
        return f"ConversationMemory(messages={summary['total_messages']}, disasters={summary['tracked_disasters']})"