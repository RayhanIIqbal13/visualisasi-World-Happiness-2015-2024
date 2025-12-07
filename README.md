# 🌍 World Happiness Report Dashboard (2015-2024)

A comprehensive Streamlit dashboard for analyzing World Happiness Report data across 175+ countries from 2015 to 2024.

## 📊 Features

- **🌐 Region Analysis**: Interactive map and distribution charts of world regions
- **🗺️ Country Data**: Detailed country profiles with regional filtering
- **😊 Happiness Report**: Ranking, trends, and statistical analysis
- **💰 Economic Indicator**: GDP correlation with happiness scores
- **👥 Social Indicator**: Social support, life expectancy, and freedom metrics
- **🤝 Perception Indicator**: Generosity and corruption perception analysis

## 🎯 Key Metrics

- **175+ Countries** covered across 10 geographic regions
- **10 Years of Data** (2015-2024) with 1,500+ happiness records
- **Interactive Visualizations** with Plotly and Folium maps
- **Multi-dimensional Analysis** across economic, social, and perception indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RayhanIIqbal13/visualisasi-World-Happiness-2015-2024.git
   cd visualisasi-World-Happiness-2015-2024
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL Database:**
   ```bash
   psql -U postgres -f DDL_whr_v2.sql
   ```

5. **Configure database credentials** in `config_whr.py`:
   ```python
   DB_HOST = "localhost"
   DB_PORT = 5432
   DB_NAME = "world_happines_v2"
   DB_USER = "postgres"
   DB_PASSWORD = "your_password"
   ```

6. **Run the application:**
   ```bash
   streamlit run app_whr.py
   ```

   The app will open at `http://localhost:8501`

## 📁 Project Structure

```
.
├── app_whr.py                 # Main Streamlit application
├── config_whr.py              # Database configuration & query functions
├── requirements.txt           # Python dependencies
├── DDL_whr_v2.sql            # Database schema
├── Data/
│   ├── Csv/                   # CSV source files (2015-2024)
│   ├── Json/                  # JSON data files (2015-2024)
│   └── sql document/          # SQL insert scripts
└── README.md                  # This file
```

## 🗄️ Database Schema

### Tables
- **region**: Geographic regions (10 regions)
- **country**: 175+ countries with region assignments
- **happiness_report**: Main happiness metrics by year and country
- **economic_indicator**: GDP per capita data
- **social_indicator**: Social support, life expectancy, freedom
- **perception_indicator**: Generosity and corruption perception

### Key Relationships
```
country → region
happiness_report → country (foreign key)
economic_indicator → happiness_report
social_indicator → happiness_report
perception_indicator → happiness_report
```

## 📊 Dashboard Pages

### 1. 🏠 Beranda (Home)
- Overview statistics
- Database summary
- Navigation guide

### 2. 🌐 Region
- Regional distribution map
- Country count per region
- Regional statistics
- Region filtering

### 3. 🗺️ Country
- Country choropleth map
- Country-level data
- Regional filtering
- Country details table

### 4. 😊 Happiness Report
- Country rankings
- Happiness score trends
- Distribution analysis
- Year and region filters

### 5. 💰 Economic Indicator
- GDP per capita analysis
- GDP-Happiness correlation
- Economic trends
- Top GDP countries

### 6. 👥 Social Indicator
- Social support analysis
- Life expectancy metrics
- Freedom to make life choices
- Regional comparisons

### 7. 🤝 Perception Indicator
- Generosity metrics
- Corruption perception
- Top/bottom rankings
- Year and region analysis

## 🔍 Key Features

### Filters
- **Year Filter**: Compare across 2015-2024
- **Region Filter**: Analyze specific geographic regions
- **Country Filter**: Focus on individual countries

### Visualizations
- 📍 Interactive choropleth maps with Folium
- 📊 Bar charts, pie charts, and histograms
- 📈 Trend analysis with line plots
- 📋 Detailed data tables with sorting/filtering
- 🔗 Correlation heatmaps

### Data Export
- Download data as CSV
- Full data table views with pagination
- Statistical summaries

## 📈 Data Insights

**Top 5 Happiest Countries (2015-2024 avg):**
- Denmark, Iceland, Switzerland, Netherlands, Finland

**Top 5 Least Happy Countries (2015-2024 avg):**
- Afghanistan, Burundi, South Sudan, Central African Republic, Syria

**Happiest Region:**
- North America and ANZ (avg score: 7.16)

**Least Happy Region:**
- Sub-Saharan Africa (avg score: 4.28)

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit 1.28+ |
| Backend | Python 3.8+ |
| Database | PostgreSQL 12+ |
| Visualization | Plotly, Folium |
| Data Processing | Pandas, NumPy |
| Mapping | GeoJSON, Folium, Streamlit-folium |

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub repository
4. Deploy with one click

**Requires**: Cloud PostgreSQL (Render, Supabase, AWS RDS)

### Option 2: Docker
```bash
docker build -t whr-dashboard .
docker run -p 8501:8501 whr-dashboard
```

### Option 3: VPS (DigitalOcean, AWS, Google Cloud)
1. Deploy Python application
2. Setup PostgreSQL database
3. Configure Nginx reverse proxy
4. Enable HTTPS with Let's Encrypt

## 📝 Configuration

### Environment Variables (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/world_happines_v2
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Config (.streamlit/config.toml)
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
headless = true
port = 8501
```

## 🐛 Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check credentials in `config_whr.py`
- Ensure database schema is created with `DDL_whr_v2.sql`

### Missing Data
- Run data import scripts in `Data/sql document/`
- Check JSON files are properly formatted
- Verify all 10 years (2015-2024) are present

### Map Display Issues
- Ensure Folium is installed: `pip install folium streamlit-folium`
- Check internet connection for GeoJSON loading
- Verify 175 countries are in database

## 📚 Data Sources

- **World Happiness Report**: Official World Happiness Report (2015-2024)
- **GeoJSON**: Natural Earth Data for geographic boundaries
- **Economic Data**: World Bank GDP indicators
- **Social Data**: UN Development Programme indicators

## 👨‍💼 Author

**Rayhan IIqbal**
- GitHub: [@RayhanIIqbal13](https://github.com/RayhanIIqbal13)
- Repository: [visualisasi-World-Happiness-2015-2024](https://github.com/RayhanIIqbal13/visualisasi-World-Happiness-2015-2024)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📞 Support

For issues or questions, please:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new GitHub issue with details

## 🙏 Acknowledgments

- World Happiness Report team
- Streamlit community
- Open source contributors

---

**Last Updated**: December 2025  
**Status**: Active Development ✅
