# Intelligent Path of Exile Craft Helper

An advanced AI-powered crafting assistant for Path of Exile that provides intelligent crafting strategies, real-time market analysis, OCR item detection, and comprehensive session tracking.

## 🚀 Features

### 🤖 AI-Powered Crafting Intelligence
- **Adaptive Strategy Optimization**: AI analyzes your crafting goals and recommends optimal methods
- **Machine Learning Recommendations**: Learns from your crafting patterns to improve suggestions
- **Probability Engine**: Calculates exact success rates and expected costs for each method
- **Budget Optimization**: AI-optimized budget allocation across different crafting strategies
- **Risk Assessment**: Comprehensive risk analysis with mitigation strategies

### 📊 Real-Time Market Intelligence
- **Live Price Updates**: Automatic currency price updates every 5 minutes
- **Market API Integration**: Real-time data from Path of Exile market APIs
- **Price Optimization**: Dynamic cost calculations based on current market conditions
- **Currency Efficiency Analysis**: Recommends most cost-effective currency combinations

### 🔍 Intelligent OCR & Item Detection
- **Screenshot Analysis**: Automatically detect and analyze items from screenshots
- **Multi-Method OCR**: Advanced text recognition with confidence scoring
- **Auto-Population**: Automatically fills crafting forms with detected item data
- **Fuzzy Matching**: Handles OCR errors and modifier variations intelligently
- **Tooltip Detection**: Automatic PoE item tooltip detection on screen

### 📈 Comprehensive Analytics & Tracking
- **Session Tracking**: Detailed tracking of all crafting sessions
- **Success Rate Analysis**: Monitor your crafting success rates over time
- **Cost Efficiency Metrics**: Track spending patterns and optimization opportunities
- **Method Performance**: Compare effectiveness of different crafting methods
- **Personalized Recommendations**: AI-generated suggestions based on your history

### 🎯 Advanced Crafting Methods
- **Chaos Spam**: High-risk, high-reward random crafting
- **Alt + Regal**: Targeted crafting for specific modifiers
- **Essence Crafting**: Guaranteed modifier crafting with essences
- **Fossil Crafting**: Biased outcomes using fossil combinations
- **Mastercraft**: Guaranteed modifiers from crafting bench
- **Hybrid Methods**: AI-recommended combinations of multiple approaches

### ⚡ Performance & Usability
- **Overlay Mode**: Always-on-top window for easy access during gameplay
- **Multi-Monitor Support**: Works across multiple displays
- **Performance Optimization**: Intelligent resource management
- **Customizable UI**: Adjustable opacity, positioning, and themes
- **League Support**: Automatic detection and configuration for current league

## 🛠️ Installation

### Prerequisites
- Python 3.8+ with tkinter
- Tesseract OCR engine (for item detection features)
- Internet connection (for market data)

### Dependencies
```bash
pip install -r requirements.txt
```

### Required System Dependencies
- **Tesseract OCR**: Install from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
- **OpenCV**: Included in requirements.txt
- **Pillow**: For image processing
- **NumPy**: For mathematical calculations

## 🎮 Usage

### Basic Usage
1. **Launch the application**:
   ```bash
   python poe_craft_helper.py
   ```

2. **Enter your item base** (e.g., "Titanium Spirit Shield")

3. **Specify target modifiers** (one per line):
   - +1 to Level of Socketed Gems
   - 70+ Life
   - 35+ Resistances

4. **Set your budget** and item level requirements

5. **Choose crafting method** or use "Auto" for AI recommendations

6. **Generate your plan** and follow the step-by-step instructions

### Advanced Features

#### AI-Enhanced Planning
- Select "Auto" method for AI-optimized strategy selection
- View confidence scores and success probabilities
- Get adaptive plans with contingency strategies
- Receive budget allocation recommendations

#### Item Detection
- Click "Item Detection" to open the OCR analyzer
- Use "Capture Screen Region" to select item tooltips
- Upload screenshot files for analysis
- Auto-populate crafting forms with detected data

#### Market Intelligence
- Real-time currency price updates
- Cost efficiency calculations
- Market volatility monitoring
- Price trend analysis

#### Session Analytics
- Track all crafting sessions automatically
- View success rates and cost efficiency
- Get personalized improvement recommendations
- Export session data for external analysis

## 🧠 AI Features Explained

### Adaptive Strategy Selection
The AI analyzes your crafting scenario using:
- **Modifier Complexity**: Evaluates difficulty of target modifiers
- **Budget Constraints**: Optimizes for your available currency
- **Market Conditions**: Considers current prices and volatility
- **Historical Data**: Learns from your previous crafting sessions
- **Risk Tolerance**: Adapts to your preferred risk level

### Probability Engine
Calculates exact probabilities for:
- **Success Rates**: Per-method success probabilities
- **Cost Expectations**: Expected currency costs
- **Time Efficiency**: Estimated time to completion
- **Risk Assessment**: Probability of budget overruns

### Learning System
Continuously improves through:
- **Session Analysis**: Learns from your crafting outcomes
- **Pattern Recognition**: Identifies successful strategies
- **Feedback Integration**: Incorporates your success/failure data
- **Market Adaptation**: Adjusts to changing market conditions

## 📊 Analytics Dashboard

### Session Tracking
- **Real-time Monitoring**: Track active crafting sessions
- **Historical Analysis**: View past sessions and outcomes
- **Success Metrics**: Monitor success rates and cost efficiency
- **Method Comparison**: Compare effectiveness of different approaches

### Performance Insights
- **Cost Analysis**: Track spending patterns and optimization opportunities
- **Time Tracking**: Monitor time spent on different crafting methods
- **Efficiency Metrics**: Identify most cost-effective approaches
- **Trend Analysis**: View performance trends over time

## ⚙️ Configuration

### User Preferences
- **Default Budget**: Set your typical crafting budget
- **Preferred Methods**: Choose your favorite crafting approaches
- **Overlay Settings**: Configure opacity and positioning
- **Auto-refresh**: Enable automatic price updates
- **League Selection**: Choose your current league

### Performance Settings
- **Resource Monitoring**: Automatic performance optimization
- **Cache Management**: Intelligent memory usage
- **Background Tasks**: Optimized background processing
- **UI Responsiveness**: Maintained smooth interface performance

## 🔧 Advanced Configuration

### League Support
The application automatically detects and configures for:
- **Secrets of the Atlas** (Current League)
- **Settlers of Kalguur**
- **Necropolis**
- **Standard League**
- **Hardcore League**

### Market API Configuration
- **Automatic Updates**: Real-time price data every 5 minutes
- **Fallback Systems**: Offline mode with cached prices
- **Error Handling**: Graceful degradation on API failures
- **Rate Limiting**: Respectful API usage patterns

## 📁 File Structure

```
poe_craft_helper/
├── poe_craft_helper.py          # Main application
├── requirements.txt             # Python dependencies
├── data/                        # User data and databases
│   ├── user_preferences.json   # User settings
│   ├── crafting_sessions.db    # Session tracking
│   ├── learning_system.db      # AI learning data
│   └── market_intelligence.db  # Market analysis data
├── ai_crafting_optimizer.py    # AI strategy optimization
├── market_api.py               # Market data integration
├── ocr_analyzer.py             # Item detection and OCR
├── session_tracker.py          # Analytics and tracking
├── probability_engine.py       # Success rate calculations
├── intelligent_recommendations.py # AI recommendations
├── adaptive_learning_system.py # Machine learning
├── performance_optimizer.py    # Performance management
└── league_config.py            # League configuration
```

## 🎯 Crafting Methods Deep Dive

### Chaos Spam
- **Best For**: Multiple good modifiers, high budget
- **Success Rate**: 15-25% (varies by complexity)
- **Cost**: 50-500+ Chaos Orbs (RNG dependent)
- **Risk Level**: High variance, can be expensive
- **AI Optimization**: Budget allocation and stop-loss strategies

### Alt + Regal
- **Best For**: Targeting 1-2 specific modifiers
- **Success Rate**: 60-80% for single targets
- **Cost**: Moderate (Alterations + Regal + potentially Exalts)
- **Risk Level**: Lower cost entry, good control
- **AI Optimization**: Optimal stopping points and backup strategies

### Essence Crafting
- **Best For**: Guaranteeing specific modifiers
- **Success Rate**: 80-95% for guaranteed mods
- **Cost**: Higher but predictable
- **Risk Level**: Lower variance than chaos spam
- **AI Optimization**: Essence selection and combination strategies

### Fossil Crafting
- **Best For**: Biasing outcomes toward desired modifier types
- **Success Rate**: 50-70% with proper fossil selection
- **Cost**: Variable based on fossil prices
- **Risk Level**: More controlled than pure RNG methods
- **AI Optimization**: Fossil combination recommendations

### Mastercraft
- **Best For**: Adding final guaranteed modifiers
- **Success Rate**: 100% (guaranteed outcomes)
- **Cost**: Fixed currency cost from crafting bench
- **Risk Level**: Very low, guaranteed outcomes
- **AI Optimization**: Optimal crafting bench usage

## 🔮 Future Features

### Planned Enhancements
- **Voice Commands**: Voice-activated crafting assistance
- **Stream Integration**: Twitch/YouTube integration for streamers
- **Mobile Companion**: Mobile app for remote monitoring
- **Advanced Analytics**: Deep learning-based trend analysis
- **Community Features**: Shared crafting strategies and success stories

### AI Improvements
- **Predictive Modeling**: Advanced success prediction algorithms
- **Market Prediction**: AI-powered price trend forecasting
- **Personalized Learning**: Individual user behavior modeling
- **Strategy Evolution**: Continuous strategy optimization

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Install Tesseract OCR
4. Run the application: `python poe_craft_helper.py`

### Testing
- Test with different item types and modifier combinations
- Verify OCR accuracy with various screenshot qualities
- Validate market data integration
- Check performance with extended usage sessions

## 📄 License

This project is provided as-is for educational and personal use. Please respect Path of Exile's terms of service and API usage guidelines.

## 🙏 Acknowledgments

- **Path of Exile Community**: For crafting knowledge and feedback
- **Open Source Libraries**: Tesseract, OpenCV, and other dependencies
- **GGG**: For creating Path of Exile and providing API access

## 📞 Support

For issues, questions, or feature requests:
- Check the analytics dashboard for usage insights
- Review the session tracking for troubleshooting
- Monitor the performance optimizer for system issues
- Use the AI recommendations for optimization suggestions

---

**Note**: This application is designed to enhance your Path of Exile crafting experience. Always verify crafting strategies and use at your own discretion. The AI recommendations are based on statistical analysis and should not be considered guaranteed outcomes.