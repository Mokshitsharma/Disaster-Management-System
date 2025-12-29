# 🚨 Disaster Response AI Agent

A cutting-edge, AI-powered disaster monitoring and emergency response coordination system built with Python, Streamlit, and Claude AI.

## ✨ Features

### 🤖 AI-Powered Capabilities
- **Intelligent Chat Interface** - Natural language disaster assistance powered by Claude Sonnet 4
- **Real-time Web Search** - Automatically searches for current disaster information
- **Emergency Guidance** - Step-by-step safety instructions for various disasters
- **Context Memory** - Maintains conversation history and disaster tracking

### 🌍 Disaster Monitoring
- **Live Disaster Tracking** - Monitor active disasters worldwide
- **Interactive Map View** - Visualize disasters geographically
- **Multi-disaster Support** - Track earthquakes, wildfires, floods, hurricanes, and more
- **Severity Classification** - Automatic prioritization of critical events

### 📊 Analytics & Insights
- **Real-time Statistics** - Active disasters, monitoring counts, response metrics
- **Emergency Prioritization** - AI-driven severity and urgency scoring
- **Data Deduplication** - Prevent duplicate disaster entries
- **Export Reports** - Generate formatted disaster reports

### 🎨 Modern UI/UX
- **3D Effects** - Depth and shadow effects for immersive experience
- **Light Theme** - Clean, professional light color scheme
- **Responsive Design** - Works on desktop and mobile
- **Smooth Animations** - Hover effects and transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Anthropic API key (get one at https://console.anthropic.com)

### Installation

1. **Create project directory and navigate to it:**
```bash
mkdir disaster-ai-agent
cd disaster-ai-agent
```

2. **Create all the Python files:**

Save each file with its content:
- `main.py` - Main Streamlit application
- `tools.py` - AI API integration and tools
- `memory.py` - Conversation memory management
- `utils.py` - Utility functions
- `dedupe.py` - Data deduplication logic
- `requirements.txt` - Python dependencies

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your API key:**

Open `tools.py` and replace `YOUR_API_KEY_HERE` with your actual Anthropic API key on line 45:

```python
"x-api-key": "sk-ant-your-actual-api-key-here"
```

**Alternative (Recommended):** Create a `.env` file:
```bash
echo "ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here" > .env
```

Then modify `tools.py` to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

5. **Run the application:**
```bash
streamlit run main.py
```

6. **Open your browser:**

The app will automatically open at `http://localhost:8501`

## 📖 Usage Guide

### Chat Interface

1. **Quick Actions** - Click pre-configured buttons for common queries
2. **Natural Language** - Type any disaster-related question
3. **Real-time Search** - AI automatically searches for current information
4. **Emergency Protocols** - Get step-by-step safety instructions

### Example Queries

```
"What disasters are currently active worldwide?"
"What should I do during an earthquake?"
"Help me create an evacuation plan"
"Search for recent wildfire news in California"
"What should be in my emergency kit?"
```

### Map View

- View all active disasters on an interactive map
- Click disasters for detailed information
- Filter by severity and type
- Track disaster progression

### Analytics Dashboard

- Monitor active disasters and responses
- View real-time statistics
- Track system performance
- Generate reports

## 🛠️ Configuration

### Customize Settings

Edit `main.py` to customize:

```python
# Maximum conversation messages to keep
max_messages = 100

# Disaster refresh interval
refresh_interval = 300  # seconds

# Theme colors
primary_color = "#667eea"
secondary_color = "#764ba2"
```

### API Configuration

In `tools.py`, adjust:

```python
# Claude model selection
model = "claude-sonnet-4-20250514"

# Max response tokens
max_tokens = 2000

# Enable web search
tools = [{
    "type": "web_search_20250305",
    "name": "web_search"
}]
```

## 🔐 Security Notes

1. **Never commit API keys** - Add `.env` to `.gitignore`
2. **Use environment variables** - Don't hardcode sensitive data
3. **Validate user input** - Already implemented in `utils.py`
4. **HTTPS only** - Use secure connections in production

## 📦 Project Structure

```
disaster-ai-agent/
├── main.py              # Main Streamlit application
├── tools.py             # AI API integration
├── memory.py            # Conversation memory
├── utils.py             # Utility functions
├── dedupe.py            # Data deduplication
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## 🌟 Key Features Explained

### AI Integration
- Uses Claude Sonnet 4 for intelligent responses
- Automatic web search for current information
- Context-aware conversation management
- Fallback responses when API is unavailable

### Disaster Tracking
- Real-time monitoring of global disasters
- Severity classification (Critical, High, Medium, Low)
- Geographic coordinate tracking
- Status updates (Active, Monitoring, Resolved)

### Safety Features
- Emergency contact numbers by region
- Step-by-step safety protocols
- Evacuation planning assistance
- Resource allocation guidance

## 🔧 Troubleshooting

### API Connection Issues

**Problem:** "Connection error" message
**Solution:** 
- Check your API key is correct
- Verify internet connection
- Ensure API key has proper permissions

### Import Errors

**Problem:** `ModuleNotFoundError`
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Streamlit Not Running

**Problem:** Command not found
**Solution:**
```bash
python -m pip install --upgrade streamlit
python -m streamlit run main.py
```

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Add API key to Secrets in deployment settings
5. Deploy!

### Environment Variables for Cloud

In Streamlit Cloud secrets:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

## 🤝 Contributing

Contributions welcome! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Emergency Contacts

**Always call emergency services directly for immediate help:**

- 🇺🇸 USA: 911
- 🇪🇺 Europe: 112
- 🇬🇧 UK: 999
- 🇦🇺 Australia: 000
- 🇮🇳 India: 112
- 🇨🇦 Canada: 911

## 📞 Support

For technical support:
- Open an issue on GitHub
- Check the documentation
- Contact the development team

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Claude AI](https://anthropic.com)
- Disaster data visualization concepts
- Emergency response protocols

## 🔮 Future Enhancements

- [ ] Real-time disaster API integration
- [ ] SMS/Email alerts system
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Advanced mapping with Folium/Plotly
- [ ] Historical disaster analysis
- [ ] Predictive modeling

---

**Built with ❤️ for emergency response and disaster preparedness**

*Remember: This tool is for information and coordination. Always follow official emergency guidance and call emergency services when needed.*