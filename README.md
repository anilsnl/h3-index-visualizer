# H3 Index Visualizer

An interactive web application for visualizing and exploring Uber's H3 hexagonal hierarchical geospatial indexing system. Built with vanilla JavaScript and featuring a modern dark-themed UI.

**Live Demo:** [https://h3-map.senel.tr](https://h3-map.senel.tr)

![H3 Index Visualizer](images/screenshot-main.png)

## Features

### Core Functionality
- **Dual Input Modes**
  - Search by H3 ID (Hexadecimal or Decimal format)
  - Search by Latitude/Longitude coordinates
- **Interactive Map**
  - Click anywhere on the map to visualize H3 cells
  - Dynamic resolution based on zoom level
  - Centered on Anıtkabir, Ankara, Turkey (default view at Resolution 11)

### Visualization
- Real-time hexagon boundary rendering
- Cell center point markers
- Color-coded visualization with dark theme
- Parent layer hierarchy (zoom out to see larger cells)
- Detailed cell information display

### Advanced Features
- **Multi-Language Support**
  - Automatic browser language detection
  - Supported languages: English, Turkish, German
  - Defaults to English for unsupported languages
- **"Locate Me" Functionality**
  - Uses browser geolocation to find your current H3 cell
  - Automatically calculates at Resolution 15 (maximum detail)
- **Resolution Reference Table**
  - Complete H3 resolution statistics (Res 0-15)
  - Hexagon counts, edge lengths, areas
- **Format Support**
  - Hexadecimal H3 IDs
  - Decimal (64-bit) H3 IDs with BigInt support
  - Directed Edges and Vertex handling

### User Experience
- **Auto-Synchronization**: Input fields automatically sync between tabs
  - Enter H3 ID → see coordinates
  - Enter coordinates → see H3 ID
- **Smart Resolution Selection**
  - Coordinate lookups use Resolution 15 for maximum detail
  - Map clicks use zoom-appropriate resolution
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Eye-friendly interface with inverted map tiles

## Screenshots

### Main Interface
![Main Interface](images/screenshot-main.png)

### By H3 ID Tab
![Search by H3 ID](images/screenshot-h3-id.png)

### By Coordinates Tab
![Search by Coordinates](images/screenshot-coordinates.png)

### Cell Details
![Cell Details Panel](images/screenshot-details.png)

### Reference Table
![H3 Resolution Table](images/screenshot-table.png)

## Technologies Used

- **Mapping**: [Leaflet.js](https://leafletjs.com/) v1.9.4
- **H3 Library**: [h3-js](https://github.com/uber/h3-js) v4.1.0
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) (CDN)
- **Icons**: [Lucide Icons](https://lucide.dev/)
- **Base Maps**: CartoDB Light tiles with inverted colors for dark mode

## How to Use

### Search by H3 ID
1. Click the **"By H3 ID"** tab
2. Select format (Hexadecimal or Decimal)
3. Enter an H3 index (e.g., `8928308280fffff`)
4. Click search or press Enter
5. View the hexagon on the map and detailed information

### Search by Coordinates
1. Click the **"By Lat/Lon"** tab
2. Enter latitude and longitude (e.g., `39.925`, `32.836944`)
3. Click **"Find H3 Cell"**
4. The app calculates the H3 cell at Resolution 15

### Interactive Features
- **Click on Map**: Instantly get the H3 cell for any location
- **Locate Me**: Click to find your current location's H3 cell
- **Parent Layers**: Click any parent cell to zoom out and explore larger hexagons
- **Swap Lat/Lon**: Debug button to swap coordinates if needed

### Language Switching
- Use the language switcher in the header (TR/EN/DE)
- Language is auto-detected on first visit

## Installation

### Option 1: Direct Use
Simply open `index.html` in a modern web browser. All dependencies are loaded via CDN.

### Option 2: Local Server
For better development experience:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js
npx http-server

# Using PHP
php -S localhost:8000
```

Then visit `http://localhost:8000`

## Project Structure

```
h3-index-visualizer/
├── index.html          # Main application (single-file)
├── images/             # Screenshots and assets
│   ├── screenshot-main.png
│   ├── screenshot-h3-id.png
│   └── ...
└── README.md          # This file
```

## Configuration

### Default Settings
You can modify these settings in `index.html`:

- **Default Location**: Line 887-888 (currently Anıtkabir, Ankara)
- **Default Resolution**: Line 889 (currently Res 11)
- **Coordinate Resolution**: Line 586 (Res 15 for max detail)
- **Locate Me Resolution**: Line 832 (Res 15)

### Language Settings
- **Supported Languages**: `tr`, `en`, `de` (Line 347-350)
- **Default Language**: English with auto-detection (Line 356)

## H3 Resolution Reference

| Resolution | Avg Area    | Edge Length | Use Case                |
|------------|-------------|-------------|-------------------------|
| 0          | 4,250,546 km² | 1,107 km    | Continental             |
| 5          | 252.9 km²   | 8.5 km      | Large cities            |
| 8          | 0.73 km²    | 461 m       | Neighborhoods           |
| 11         | 2,150 m²    | 24.9 m      | Buildings (default)     |
| 12         | 307 m²      | 9.4 m       | Building level          |
| 15         | 0.9 m²      | 0.5 m       | Maximum detail          |

## Browser Support

- Modern browsers with ES6+ support
- Geolocation API for "Locate Me" feature
- BigInt support for decimal H3 IDs

### Recommended Browsers
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Contributing

Contributions are welcome! Feel free to:
- Report bugs via GitHub Issues
- Submit pull requests
- Suggest new features
- Improve documentation

## About H3

H3 is a hexagonal hierarchical geospatial indexing system developed by Uber. It provides:
- Efficient spatial indexing
- Multiple resolutions (0-15)
- Consistent hexagonal grid
- Fast neighbor lookups
- Global coverage

Learn more at [H3 Documentation](https://h3geo.org/docs/)

## License

This project is open source and available under the MIT License.

## Author

**Anil Dursun Senel**
- Website: [senel.tr](https://senel.tr)
- GitHub: [@anilsnl](https://github.com/anilsnl)
- Live Demo: [h3-map.senel.tr](https://h3-map.senel.tr)

## Acknowledgments

- [Uber H3 Team](https://github.com/uber/h3) for the amazing geospatial indexing system
- [Leaflet](https://leafletjs.com/) for the mapping library
- [CartoDB](https://carto.com/) for the base map tiles
- [Lucide](https://lucide.dev/) for the beautiful icons

---

**Star this repository** if you find it useful! ⭐
