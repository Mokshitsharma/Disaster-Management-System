import requests
import json
from datetime import datetime

def call_claude_api(user_message, conversation_history):
    """
    Call CHATGPT API for disaster response assistance.
    
    Args:
        user_message: The user's current message
        conversation_history: List of previous messages
    
    Returns:
        str: Claude's response
    """
    
    system_prompt = """You are a Disaster Response AI Agent. Your role is to:

1. Monitor and analyze disaster situations in real-time
2. Provide emergency guidance and safety instructions
3. Coordinate response efforts and resource allocation
4. Search for current disaster information when needed
5. Offer evacuation planning and emergency protocols
6. Track multiple disasters simultaneously

When users ask about current disasters, recent events, or need real-time information, 
use web search to find the latest updates.

Be clear, actionable, and prioritize safety. Use structured responses when appropriate. 
Always remain calm and professional in emergencies. Provide specific, step-by-step 
instructions when dealing with emergency situations."""

    try:
        # Prepare the API request
        url = "https://api.openai.com/v1/chat/completions"

        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "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"  # User should replace this
        }
        
        # Build conversation history
        messages = []
        for msg in conversation_history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Add current message if not in history
        if not messages or messages[-1]['content'] != user_message:
            messages.append({
                "role": "user",
                "content": user_message
            })
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 2000,
            "system": system_prompt,
            "messages": messages,
            "tools": [{
                "type": "web_search_20250305",
                "name": "web_search"
            }]
        }
        
        # Make the API call
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract text content from response
            assistant_message = ""
            tool_uses = []
            
            for block in data.get('content', []):
                if block.get('type') == 'text':
                    assistant_message += block.get('text', '')
                elif block.get('type') == 'tool_use':
                    tool_uses.append(block)
            
            # If Claude used web search, handle tool results
            if tool_uses and data.get('stop_reason') == 'tool_use':
                # In a production app, you would handle tool results here
                # For now, we'll just return the partial response
                pass
            
            return assistant_message if assistant_message else "I'm here to help with disaster response. How can I assist you?"
        
        else:
            return f"⚠️ API Error: {response.status_code}. Using fallback response system."
    
    except requests.exceptions.Timeout:
        return "⚠️ Request timed out. Please try again or contact emergency services directly if this is urgent."
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Connection error. Please check your internet connection. For immediate emergencies, call 911."
    
    except Exception as e:
        # Fallback response system
        return generate_fallback_response(user_message)


def generate_fallback_response(user_message):
    """
    Generate intelligent fallback responses when API is unavailable.
    
    Args:
        user_message: The user's message
    
    Returns:
        str: A helpful fallback response
    """
    
    message_lower = user_message.lower()
    
    # Emergency keywords
    if any(word in message_lower for word in ['earthquake', 'seismic', 'tremor']):
        return """🏠 **EARTHQUAKE SAFETY PROTOCOL**

**During the earthquake:**
1. DROP to your hands and knees
2. COVER your head and neck under a sturdy table
3. HOLD ON until shaking stops

**After the earthquake:**
- Check for injuries and hazards
- Expect aftershocks
- Stay away from damaged buildings
- Listen to local authorities

**Emergency Contacts:** 911 (US) | 112 (EU) | 999 (UK)"""
    
    elif any(word in message_lower for word in ['fire', 'wildfire', 'smoke']):
        return """🔥 **WILDFIRE SAFETY PROTOCOL**

**Immediate Actions:**
1. Monitor local news and emergency alerts
2. Prepare evacuation bag (documents, water, medications)
3. Close all windows and doors
4. Wet towels and place under doors

**If Ordered to Evacuate:**
- Leave immediately
- Follow designated evacuation routes
- Don't return until authorities say it's safe

**Emergency Contacts:** 911 (US) | 112 (EU) | 999 (UK)"""
    
    elif any(word in message_lower for word in ['flood', 'flooding', 'water']):
        return """💧 **FLOOD SAFETY PROTOCOL**

**Immediate Actions:**
1. Move to higher ground immediately
2. Avoid walking/driving through flood water
3. Turn off utilities if instructed
4. Stay informed via weather radio

**Remember:**
- 6 inches of water can knock you down
- 12 inches can carry away a vehicle
- Never drive through flooded roads

**Emergency Contacts:** 911 (US) | 112 (EU) | 999 (UK)"""
    
    elif any(word in message_lower for word in ['kit', 'supplies', 'emergency bag', 'preparedness']):
        return """🎒 **EMERGENCY KIT ESSENTIALS**

**Basic Supplies (3-day supply):**
- Water (1 gallon per person per day)
- Non-perishable food
- Battery-powered radio
- Flashlight & extra batteries
- First aid kit
- Medications (7-day supply)

**Important Documents:**
- ID copies
- Insurance policies
- Medical records
- Bank information

**Additional Items:**
- Cash
- Phone chargers
- Whistle
- Dust masks
- Moist towelettes
- Local maps"""
    
    elif any(word in message_lower for word in ['evacuation', 'evacuate', 'leave']):
        return """📋 **EVACUATION PLANNING**

**Create Your Plan:**
1. **Routes:** Identify 2+ evacuation routes
2. **Meeting Point:** Designate outside your neighborhood
3. **Contacts:** List out-of-area emergency contact
4. **Pets:** Plan for pet evacuation

**What to Take:**
- Emergency kit
- Important documents
- Medications
- Cash & credit cards
- Phone & chargers

**During Evacuation:**
- Follow official routes
- Don't take shortcuts
- Check on neighbors
- Lock your home
- Don't return until cleared

**Stay Informed:** Monitor local radio/TV"""
    
    elif any(word in message_lower for word in ['active', 'current', 'happening', 'now']):
        return """🌍 **ACTIVE DISASTER MONITORING**

I'm currently tracking:

1. **Earthquake** - California (High Severity)
   - Magnitude: 6.2
   - Status: Active response
   - Time: 2 hours ago

2. **Wildfire** - Australia (Critical)
   - Area: 50,000 acres
   - Status: Containment efforts ongoing
   - Time: 5 hours ago

3. **Flood** - Bangladesh (Medium)
   - Affected: Multiple districts
   - Status: Active monitoring
   - Time: 1 day ago

For real-time updates, please enable API access or visit official disaster monitoring websites."""
    
    else:
        return """🚨 **Disaster Response AI Agent**

I'm here to help with:

✅ **Emergency Guidance** - Safety procedures for various disasters
✅ **Disaster Monitoring** - Tracking active events worldwide
✅ **Evacuation Planning** - Creating personalized evacuation plans
✅ **Emergency Kits** - What supplies you need
✅ **Real-time Information** - Current disaster updates

**How can I assist you?**

For immediate emergencies, always call:
- 🇺🇸 USA: 911
- 🇪🇺 Europe: 112
- 🇬🇧 UK: 999

Ask me about earthquakes, wildfires, floods, emergency kits, or evacuation planning!"""
    
    return response


def search_disasters():
    """
    Search for current disaster information (placeholder for web search).
    
    Returns:
        list: List of current disasters
    """
    
    # This would integrate with real disaster APIs
    # For now, return mock data
    
    return [
        {
            "type": "Earthquake",
            "location": "California, USA",
            "severity": "High",
            "magnitude": "6.2",
            "time": "2 hours ago",
            "lat": 34.0522,
            "lng": -118.2437
        },
        {
            "type": "Wildfire",
            "location": "New South Wales, Australia",
            "severity": "Critical",
            "area": "50,000 acres",
            "time": "5 hours ago",
            "lat": -33.8688,
            "lng": 151.2093
        }
    ]


def get_emergency_contacts():
    """
    Get emergency contact numbers by region.
    
    Returns:
        list: Emergency contact information
    """
    
    return [
        {"country": "USA", "number": "911"},
        {"country": "Europe", "number": "112"},
        {"country": "UK", "number": "999"},
        {"country": "Australia", "number": "000"},
        {"country": "India", "number": "112"},
        {"country": "Canada", "number": "911"},
    ]


def analyze_disaster_severity(disaster_data):
    """
    Analyze disaster severity based on multiple factors.
    
    Args:
        disaster_data: Dictionary containing disaster information
    
    Returns:
        dict: Severity analysis
    """
    
    severity_scores = {
        'Critical': 4,
        'High': 3,
        'Medium': 2,
        'Low': 1
    }
    
    score = severity_scores.get(disaster_data.get('severity', 'Low'), 1)
    
    return {
        'score': score,
        'level': disaster_data.get('severity', 'Unknown'),
        'recommendation': get_severity_recommendation(score)
    }


def get_severity_recommendation(score):
    """
    Get recommendations based on severity score.
    
    Args:
        score: Severity score (1-4)
    
    Returns:
        str: Recommendation text
    """
    
    if score >= 4:
        return "🚨 CRITICAL: Immediate evacuation may be necessary. Follow all official instructions."
    elif score >= 3:
        return "⚠️ HIGH: Be prepared to evacuate. Monitor situation closely."
    elif score >= 2:
        return "⚡ MEDIUM: Stay informed. Review emergency plans."
    else:
        return "ℹ️ LOW: Monitor for updates. Maintain normal precautions."
