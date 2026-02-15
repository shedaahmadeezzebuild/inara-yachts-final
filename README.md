# Inara Yachts - AI Charter & Sales Bot

A sophisticated AI-powered chatbot for yacht charter and sales inquiries, built with Streamlit and powered by Mistral Large AI.

## Features

✨ **Professional 3D UI**: Modern gradient design with enterprise-grade styling
🤖 **AI-Powered**: Mistral Large AI model with knowledge base integration
📚 **Comprehensive Knowledge Base**: 1000+ FAQ items for charter and sales services
🎯 **Multiple Service Modes**: 
  - General Inquiry
  - Charter Booking
  - Yacht Sales
  - Fleet Information
  - Contact & Support

💾 **Persistent Chat History**: Maintains conversation context throughout sessions
📊 **Real-time Analytics**: Knowledge base statistics and model information

## Project Structure

```
Inara Yachts/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── logo.jpg                        # Sidebar logo
├── header_logo.jpg                 # Main header logo
├── user_avatar.jpg                 # User chat avatar
├── inara_charter_batch_1.json      # Charter data batch 1
├── inara_charter_batch_2.json      # Charter data batch 2
├── inara_charter_batch_3.json      # Charter data batch 3
├── inara_charter_batch_4.json      # Charter data batch 4
├── inara_sales_batch_1.json        # Sales data batch 1
├── inara_sales_batch_2.json        # Sales data batch 2
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Installation

### Requirements
- Python 3.8+
- Virtual Environment (venv)

### Setup

1. **Create and activate a virtual environment**:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Configuration

### API Keys
The bot uses the Mistral AI API. The API key is embedded in `app.py`:
```python
MISTRAL_API_KEY = "SsDvv0v2AToQqVj1pDOZSUAFyd0VtnXa"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-large-latest"
```

## Running the Application

```bash
streamlit run app.py
```

The application will be available at: `http://localhost:8501`

## Features in Detail

### Service Modes
Each mode provides specialized responses based on the context:

- **General Inquiry**: General information about Inara Yachts services
- **Charter Booking**: Help with booking luxury yacht charters
- **Yacht Sales**: Assistance with yacht purchasing and sales
- **Fleet Information**: Details about available yachts
- **Contact & Support**: Customer support and contact information

### Knowledge Base
The application includes a comprehensive knowledge base with:
- 1000+ FAQ items
- Structured charter and sales information
- Real-time FAQ statistics displayed in the sidebar

### Professional UI
- Blue gradient background with cyan accents
- 3D-like shadows and hover effects
- Responsive design with professional typography
- Smooth animations and transitions

## API Integration

### Mistral AI Integration
The bot communicates with Mistral AI API v1:
- **Model**: mistral-large-latest
- **Response Format**: Streaming chat completions
- **Context Window**: Maintains full conversation history
- **Knowledge Injection**: Dynamic context based on service mode

## Data Files

### Charter Data
- `inara_charter_batch_1-4.json`: Contains charter FAQs, routing rules, and lead scoring

### Sales Data
- `inara_sales_batch_1-2.json`: Contains sales FAQs and business logic

Each file includes:
- FAQ items with questions and answers
- Trigger keywords for smart matching
- Upsell prompts and escalation rules
- Channel-specific formatting

## Customization

### Modifying System Prompts
Edit the `system_prompts` dictionary in `app.py` to customize AI responses for each service mode.

### Updating Logos
Replace image files:
- `logo.jpg` - Sidebar logo
- `header_logo.jpg` - Main header logo
- `user_avatar.jpg` - User chat avatar

### Styling
CSS customization is available in the `<style>` section of the HTML markdown in `app.py`.

## Error Handling

The application includes robust error handling for:
- Missing data files (graceful degradation)
- API connection failures
- Invalid user input
- File I/O errors

## Performance Considerations

- Knowledge base is cached with `@st.cache_resource`
- JSON files are loaded once at startup
- Conversation history is maintained in session state
- Streamlit handles UI updates efficiently

## Security Notes

- API keys are embedded in the code (not recommended for production)
- For production deployment, use environment variables
- Implement proper authentication for public deployments

## Future Enhancements

- Multi-language support
- Database integration for persistent storage
- Advanced analytics dashboard
- Voice input/output capabilities
- Integration with booking systems
- CRM integration

## Support

For issues or questions, contact: info@inarayachts.com

## License

© 2026 Inara Yachts. All rights reserved.

---

**Built with ❤️ using Streamlit and Mistral AI**
