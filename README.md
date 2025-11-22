# Turkey Water Risk Atlas

A static web application visualizing water risk indicators for Turkey using WRI Aqueduct 4.0 data.

## Overview

This project provides an interactive water risk atlas for Turkey using WRI Aqueduct 4.0 data. The application displays catchment-level (HydroBASINS L6) water risk indicators with hydrology overlays (rivers and lakes), matching the visual style of WRI's global Aqueduct atlas. The map shows baseline and future water risk metrics including water stress, interannual variability, seasonal variability, and drought severity.

## Data Sources

### Primary Data Source
- **WRI Aqueduct 4.0**: Current and Future Global Maps Data
  - URL: https://www.wri.org/data/aqueduct-global-maps-40-data
  - License: Creative Commons Attribution 4.0 International
  - Coverage: Global baseline and future projections (2030, 2050, 2080) under SSP2-RCP4.5 scenario

### Technical Documentation
- **Aqueduct 4.0 Technical Note** (Kuzma et al.) - Methods and indicator definitions
- **Aqueduct40 GitHub Repository** - Data dictionary and production scripts
  - URL: https://github.com/wri/Aqueduct40

### Administrative Boundaries
- Derived from Aqueduct 4.0 administrative unit aggregations
- 81 provinces (ADM1 level) covering Turkey (used for labels only)

### Hydrology Data
- **HydroRIVERS**: Global river network from HydroSHEDS (clipped to Turkey)
- **HydroLAKES**: Global lake polygons from HydroSHEDS (clipped to Turkey)
- Used as visual overlays to provide geographic context

## Indicators Available

### Baseline Metrics (2010)
- **Water Stress**: Pressure on water resources (0-5 scale)
- **Interannual Variability**: Year-to-year variation in water availability
- **Seasonal Variability**: Within-year variation in water availability
- **Drought Severity**: Frequency and intensity of droughts

### Future Projections
- **Years**: 2030, 2050, 2080
- **Scenarios**:
  - **BAU (Business As Usual)**: ssp3-rcp7.0 pathway
  - **Optimistic**: ssp1-rcp2.6 pathway
  - **Pessimistic**: ssp5-rcp8.5 pathway
- All future data is provincial-level aggregations directly from WRI

## Technical Implementation

### Data Processing
1. **Data Acquisition**: Download Aqueduct 4.0 ZIP from WRI
2. **Preprocessing**: Extract Turkey province data using Python scripts
3. **Format Conversion**: Generate CSV and GeoJSON for web consumption

### Frontend Architecture
- **Framework**: React + TypeScript with Vite
- **Mapping**: React-Leaflet for interactive maps
- **Data Loading**: Native fetch for GeoJSON, PapaParse for CSV
- **Visualization**: 
  - Catchment-level risk polygons (colored by selected metric)
  - River network overlay (blue lines)
  - Lake polygons overlay (blue fill)
  - Province borders (subtle, for labels only)
  - Neutral basemap (CartoDB light nolabels)
- **Deployment**: Static build hosted on GitHub Pages

### File Structure
```
turkey-watermaps/
├── data/                    # Raw data storage
│   └── aqueduct_raw/       # Aqueduct 4.0 downloads
├── output/                 # Processed data
│   ├── city_water_metrics_long.csv
│   └── turkey_provinces_clean.geojson
├── scripts/               # Processing scripts
│   └── process_aqueduct_data.py
├── docs/                  # GitHub Pages deployment
│   ├── index.html
│   └── data/
└── web/                   # React/Vite source (alternative)
```

## Development Setup

### Prerequisites
- Python 3.7+
- Git

### Python Environment Setup
1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start
1. Clone repository: `git clone https://github.com/yourusername/turkey-watermaps.git`
2. Set up Python environment (see above)
3. Run preprocessing: `python scripts/process_aqueduct_data.py`
4. Open `docs/index.html` in a web browser

### Data Processing

#### 1. Setup Python Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Extract Catchment Data from Aqueduct GDB
```bash
# Ensure Aqueduct GDB is in data/aqueduct_raw/Aqueduct40_waterrisk_download_Y2023M07D05/GDB/
python scripts/extract_catchments.py
```

#### 3. Download and Process HydroRIVERS
```bash
# Downloads from HydroSHEDS (large file ~500MB)
python scripts/download_hydrorivers.py
```

#### 4. Download and Process HydroLAKES
```bash
# Downloads from HydroSHEDS (large file ~200MB)
python scripts/download_hydrolakes.py
```

#### 5. Copy Processed Data to Web Directory
```bash
python scripts/copy_data_to_web.py
```

#### 6. Process Province-Level Metrics (Optional)
```bash
# For province-level aggregations (used as fallback)
python scripts/process_aqueduct_data.py
```

## Deployment

The site is configured for GitHub Pages deployment:

1. Push code to GitHub repository
2. Enable Pages in repository settings
3. Set source to `main` branch and `/docs` folder
4. Site will be available at `https://yourusername.github.io/turkey-watermaps/`

## Usage

1. **Select Metric**: Choose from water stress, variability, or drought indicators
2. **Choose Scenario**:
   - **Baseline**: Historical data (2010 only)
   - **BAU**: Business As Usual future projections
   - **Optimistic**: Low emissions pathway
   - **Pessimistic**: High emissions pathway
3. **Pick Year**: Select 2010 (baseline), 2030, 2050, or 2080
4. **Explore Map**: Click provinces to view detailed metrics
5. **Color Scale**: Darker green indicates higher water risk (0-5 scale)

## Data Source Correction

**Important**: Initially used incorrect dataset (Global Maps) which only provided baseline administrative data. Corrected to use "Aqueduct 4.0 Current and Future Country Rankings" which includes provincial future projections for 2010, 2030, 2050, 2080 across multiple scenarios.

## Limitations

- **Annual Timeseries**: Aqueduct provides discrete snapshots (2010, 2030, 2050, 2080) rather than continuous annual data
- **Boundary Accuracy**: Simplified point-based representation for mapping
- **Resolution**: Province-level aggregation only
- **Interpolation**: No synthetic years between Aqueduct milestones

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add future projection data processing
4. Implement accurate boundary geometries
5. Submit pull request

## License

This project is licensed under MIT. Data sources maintain their respective licenses:

- WRI Aqueduct 4.0: Creative Commons Attribution 4.0 International
- Administrative boundaries: Derived from public domain sources

## Acknowledgments

- World Resources Institute (WRI) for Aqueduct 4.0 dataset
- OpenStreetMap contributors for base map tiles
- Leaflet.js and PapaParse libraries for web functionality

## Contact

For questions about the data or methodology, refer to:
- WRI Aqueduct: https://www.wri.org/aqueduct
- Technical documentation: Aqueduct 4.0 Technical Note
