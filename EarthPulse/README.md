# Earth Observation Visualizer

An interactive visualization platform for environmental and geographic data analysis, focusing on the Himalayan region.

## Features

- Interactive environmental data visualization
- Real-time map-based interface
- Multiple region support (Nepal Himalayas, Kathmandu Valley, Annapurna Region, Everest Region)
- Time-series analysis (2000-2025)
- Environmental indicators tracking:
  - NDVI (Normalized Difference Vegetation Index)
  - Glacier coverage
  - Urban development
  - Temperature patterns

## Demo & Screenshots

### Application Demo
[▶️ Watch Demo Video](assets/screenshots/demo.mp4)

### Screenshots
<img width="1451" height="769" alt="{85CDEA41-4C32-4F6D-B65F-5FED5A39B243}" src="https://github.com/user-attachments/assets/d2a2d623-52e3-4c0c-8901-b272a698f2cc" />





<img width="1162" height="569" alt="{BE58627F-F274-402B-8906-F11309DE4D63}" src="https://github.com/user-attachments/assets/16b9f7a2-a803-4017-91b3-3e6a73c8ec8e" />



<img width="1171" height="632" alt="{81E0F3B7-911B-43E4-96B8-6D6D4C5AC7D7}" src="https://github.com/user-attachments/assets/a701e175-b0b8-481f-81c3-9f5711e1caa8" />


<img width="1294" height="760" alt="{B02B7FE6-69E1-497E-89FE-D95FFA170453}" src="https://github.com/user-attachments/assets/65f29d88-dbe9-4e41-ba19-9a8a7b2bc9bc" />


## Tech Stack

### Frontend
- React with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Framer Motion for animations
- MapBox for interactive maps

### Backend
- FastAPI (Python)
- Async support
- Environmental data simulation
- NASA Earth Observation API integration
- Report generation capabilities

## Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv
On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python run_dev.py
```

### Frontend Setup
```bash
npm install
npm run dev
```

## Usage

1. Start the backend server
2. Launch the frontend application
3. Access the application at `http://localhost:3000`

## Features in Detail

- **Environmental Data Analysis**: Track changes in vegetation, glaciers, urban development, and temperature
- **Interactive Maps**: Explore different regions with detailed geographic visualization
- **Time Series Analysis**: Compare environmental changes over time
- **Data Export**: Download data in various formats (JSON, CSV, XLSX)
- **Report Generation**: Create detailed PDF reports with visualizations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[Add your license here]

## Acknowledgments

- NASA Earth Observation APIs
- MapBox for mapping services
- [Add other acknowledgments]
