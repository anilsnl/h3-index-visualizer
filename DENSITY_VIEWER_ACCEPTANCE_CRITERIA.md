# Density Viewer Feature - Acceptance Criteria

## Overview
Add a density visualization tool that allows users to upload CSV data containing H3 cell densities (e.g., user counts, population, sales) and visualize them on the map with automatic aggregation when zooming out to parent cells.

---

## User Stories

### Primary User Story
**As a** data analyst
**I want to** upload a CSV file with H3 cell densities
**So that** I can visualize spatial distribution patterns on the map

### Secondary User Stories
1. **As a** user, **I want to** see density values displayed on each hexagon **so that** I can quickly identify high/low density areas
2. **As a** user, **I want to** zoom out and see aggregated parent cell values **so that** I can analyze data at different resolution levels
3. **As a** user, **I want to** clear the density data **so that** I can load a different dataset or return to normal view
4. **As a** user, **I want to** see visual feedback for different density ranges **so that** I can easily identify patterns

---

## Functional Requirements

### FR1: File Upload
- **FR1.1**: Button placed in a visible location on the sidebar
- **FR1.2**: Button labeled clearly (e.g., "Load Density Data" or "Import CSV")
- **FR1.3**: Clicking button opens native file picker dialog
- **FR1.4**: Only accept `.csv` file extensions
- **FR1.5**: Provide visual feedback during file loading (loading spinner/indicator)

### FR2: CSV Format
- **FR2.1**: CSV format must be: `h3code,density` (two columns)
- **FR2.2**: Header row is optional (auto-detect if present)
- **FR2.3**: H3 code column: valid H3 hexadecimal index
- **FR2.4**: Density column: positive integer or decimal number
- **FR2.5**: Example valid rows:
  ```
  8928308280fffff,150
  8928308281fffff,230
  8928308282fffff,89
  ```

### FR3: Data Validation
- **FR3.1**: All H3 codes must be the same resolution
- **FR3.2**: Detect resolution from first valid H3 code
- **FR3.3**: Reject file if mixed resolutions detected
- **FR3.4**: Show clear error message if validation fails
- **FR3.5**: Validate each H3 code using `h3.isValidCell()`
- **FR3.6**: Skip/warn on invalid rows but continue processing valid rows
- **FR3.7**: Density values must be non-negative numbers
- **FR3.8**: Handle edge cases:
  - Empty file
  - No valid rows
  - Duplicate H3 codes (use last occurrence or sum)
  - Missing values (skip row)

### FR4: Density Visualization
- **FR4.1**: Display density values as text labels on each hexagon
- **FR4.2**: Color hexagons based on density (heat map gradient)
- **FR4.3**: Use color scale from low density (cool colors) to high density (hot colors)
- **FR4.4**: Suggested gradient: Blue → Green → Yellow → Orange → Red
- **FR4.5**: Calculate percentile-based thresholds (not absolute values) for color mapping
- **FR4.6**: Make text labels readable:
  - White text on dark backgrounds
  - Black text on light backgrounds
  - Font size proportional to zoom level
- **FR4.7**: Format large numbers with abbreviations (e.g., 1.5K, 2.3M)

### FR5: Parent Cell Aggregation
- **FR5.1**: When user clicks parent cell (from parent list), aggregate child densities
- **FR5.2**: Aggregation method: **SUM** all child cell densities
- **FR5.3**: Display aggregated value on parent cell
- **FR5.4**: Maintain color scale consistency across resolutions
- **FR5.5**: Cache aggregated values for performance
- **FR5.6**: Handle partial coverage (some children have data, some don't)
- **FR5.7**: If parent has no child data, don't display it

### FR6: Data Management
- **FR6.1**: Provide "Clear Density Data" button to remove visualization
- **FR6.2**: When cleared, return to normal visualization mode
- **FR6.3**: Allow loading new file (replaces current data)
- **FR6.4**: Show active dataset indicator (filename, resolution, cell count)
- **FR6.5**: Preserve density visualization when toggling other features (k-factor, swap mode)

### FR7: User Interface
- **FR7.1**: Add "Density Viewer" section in sidebar
- **FR7.2**: Show file upload button
- **FR7.3**: Display dataset info when loaded:
  - Filename
  - Resolution
  - Total cells loaded
  - Min/max/average density
  - Total sum
- **FR7.4**: Show color scale legend
- **FR7.5**: Add "Clear Data" button (only visible when data loaded)
- **FR7.6**: Provide download template CSV button for user reference

---

## Technical Requirements

### TR1: Data Structure
```javascript
let densityData = {
    resolution: 11,              // Resolution of loaded data
    filename: "users.csv",       // Original filename
    cells: {                     // Map of H3 code -> density
        "8928308280fffff": 150,
        "8928308281fffff": 230,
        // ...
    },
    stats: {
        min: 10,
        max: 5000,
        avg: 250,
        total: 125000,
        count: 500
    },
    parentCache: {}              // Cache for aggregated parent values
};
```

### TR2: Color Scale
- **TR2.1**: Use 5-tier color gradient
- **TR2.2**: Calculate percentile thresholds (20th, 40th, 60th, 80th, 100th)
- **TR2.3**: Color palette example:
  ```javascript
  const colors = [
      { threshold: 0.2, color: '#3b82f6', label: 'Very Low' },
      { threshold: 0.4, color: '#10b981', label: 'Low' },
      { threshold: 0.6, color: '#fbbf24', label: 'Medium' },
      { threshold: 0.8, color: '#f97316', label: 'High' },
      { threshold: 1.0, color: '#ef4444', label: 'Very High' }
  ];
  ```

### TR3: Performance
- **TR3.1**: Handle up to 10,000 cells without performance degradation
- **TR3.2**: Use efficient lookups (object/Map)
- **TR3.3**: Debounce parent aggregation calculations
- **TR3.4**: Render only visible cells on map viewport (optional optimization)

### TR4: CSV Parsing
- **TR4.1**: Use native JavaScript FileReader API
- **TR4.2**: Parse CSV manually (no external libraries needed for simple format)
- **TR4.3**: Handle different line endings (CRLF, LF)
- **TR4.4**: Trim whitespace from values
- **TR4.5**: Support both comma and semicolon as delimiter (auto-detect)

### TR5: Aggregation Algorithm
```javascript
function aggregateParent(parentHex, childResolution) {
    // Get all children at the loaded data resolution
    const children = h3.cellToChildren(parentHex, childResolution);

    // Sum densities of children that exist in dataset
    let sum = 0;
    let count = 0;
    children.forEach(childHex => {
        if (densityData.cells[childHex] !== undefined) {
            sum += densityData.cells[childHex];
            count++;
        }
    });

    return count > 0 ? sum : null;
}
```

---

## UI/UX Specifications

### Location
- **Primary**: Add section after "K-Factor Selection" in sidebar (around line 122)
- **Alternative**: Add as collapsible panel at bottom of sidebar

### UI Elements
```
┌─────────────────────────────────────┐
│  DENSITY VIEWER                     │
├─────────────────────────────────────┤
│  [📊 Load Density Data]  [📄 Template]│
│                                     │
│  ✓ Dataset Loaded: users.csv       │
│  • Resolution: 11                   │
│  • Cells: 1,250                     │
│  • Range: 10 - 5,000                │
│  • Total: 125,000                   │
│                                     │
│  Color Scale:                       │
│  [█████] 0-250   Very Low           │
│  [█████] 251-500  Low               │
│  [█████] 501-750  Medium            │
│  [█████] 751-1000 High              │
│  [█████] 1001+    Very High         │
│                                     │
│  [🗑️ Clear Data]                    │
└─────────────────────────────────────┘
```

### Label Display
- **Position**: Center of each hexagon
- **Font**: Monospace, bold
- **Size**: 10-14px based on zoom level
- **Background**: Semi-transparent background for readability
- **Format**: Abbreviated (1.2K, 3.5M, etc.)

---

## Error Handling

### E1: File Validation Errors
| Error | Message | Action |
|-------|---------|--------|
| No file selected | "Please select a CSV file" | Show alert |
| Wrong file type | "Please upload a .csv file" | Reject file |
| Empty file | "CSV file is empty" | Reject file |
| No valid rows | "No valid data rows found in CSV" | Reject file |

### E2: Data Validation Errors
| Error | Message | Action |
|-------|---------|--------|
| Mixed resolutions | "All H3 codes must be the same resolution. Found: Res 10, Res 11" | Reject file |
| Invalid H3 code | "Row X: Invalid H3 code: [code]" | Skip row, warn |
| Invalid density | "Row X: Invalid density value: [value]" | Skip row, warn |
| Negative density | "Row X: Density cannot be negative: [value]" | Skip row, warn |

### E3: User Feedback
- Show error summary after parsing: "Loaded 950 cells, skipped 50 invalid rows"
- Highlight validation errors in console for debugging
- Provide clear actionable error messages

---

## Edge Cases

### EC1: Duplicate H3 Codes
- **Scenario**: Same H3 code appears multiple times in CSV
- **Behavior**: Sum all values for that cell
- **Alternative**: Use last occurrence (document in UI)

### EC2: Partial Coverage
- **Scenario**: Parent cell has only some children with data
- **Behavior**: Sum available children, show partial coverage indicator

### EC3: Interaction with K-Factor
- **Scenario**: Density data loaded + k-factor enabled
- **Behavior**: Show density on main cell and neighbors (if they have data)

### EC4: Interaction with Swap Mode
- **Scenario**: Swap mode enabled with density data
- **Behavior**: Maintain density labels and colors correctly

### EC5: Map Click with Density Data
- **Scenario**: User clicks map while density data is active
- **Behavior**: Show clicked cell's density if available, otherwise show "No data"

### EC6: Very Large Numbers
- **Scenario**: Density values > 1 billion
- **Behavior**: Format as "1.2B", ensure labels fit in hexagons

### EC7: Very Small Hexagons
- **Scenario**: High resolution with many small hexagons
- **Behavior**: Hide labels at certain zoom levels, show on hover/click

---

## Multi-Language Support

### Translations Needed
- **English**: "Load Density Data", "Clear Data", "Download Template", "Dataset Info", "Color Scale"
- **Turkish**: "Yoğunluk Verisi Yükle", "Veriyi Temizle", "Şablon İndir", "Veri Seti Bilgisi", "Renk Skalası"
- **German**: "Dichtedaten laden", "Daten löschen", "Vorlage herunterladen", "Datensatzinfo", "Farbskala"

---

## Testing Scenarios

### TS1: Basic Flow
1. Load valid CSV with 100 cells at Res 11
2. Verify all cells displayed with colors and labels
3. Click parent cell at Res 10
4. Verify aggregated sum displayed
5. Clear data
6. Verify return to normal mode

### TS2: Validation
1. Upload CSV with mixed resolutions → Reject
2. Upload empty CSV → Reject
3. Upload CSV with invalid H3 codes → Skip invalid, load valid
4. Upload CSV with negative values → Skip invalid rows

### TS3: Large Dataset
1. Load CSV with 5,000 cells
2. Verify performance is acceptable
3. Test parent aggregation at multiple levels

### TS4: Integration
1. Load density data
2. Enable k-factor → Verify both features work
3. Toggle swap mode → Verify density persists
4. Switch languages → Verify translations

---

## Sample CSV Template

```csv
h3code,density
8928308280fffff,150
8928308281fffff,230
8928308282fffff,89
8928308283fffff,450
8928308284fffff,12
8928308285fffff,678
8928308286fffff,234
8928308287fffff,567
```

---

## Success Criteria

The feature is complete when:
- ✅ User can upload CSV and see density visualization
- ✅ Colors accurately represent density ranges
- ✅ Labels are readable and properly formatted
- ✅ Parent aggregation works correctly when navigating hierarchy
- ✅ Data validation catches all error cases
- ✅ Performance is acceptable for 10,000+ cells
- ✅ Clear data functionality works
- ✅ Multi-language support implemented
- ✅ Error messages are clear and helpful
- ✅ Feature integrates smoothly with existing features (k-factor, swap mode)

---

## Future Enhancements (Out of Scope)

- Custom color scales
- Multiple density columns (switch between metrics)
- Export aggregated data
- Filter by density range
- Time-series animation
- 3D height visualization based on density
- Clustering for performance optimization

---

## Questions to Resolve Before Implementation

1. **Duplicate H3 codes**: Sum values or use last occurrence?
2. **Color scale**: Percentile-based or absolute thresholds?
3. **Label visibility**: Always show or hide at certain zoom levels?
4. **Number format**: Always abbreviate or show full numbers with tooltip?
5. **Parent navigation**: Automatic update on zoom or manual button click?
6. **CSV delimiter**: Support only comma or also semicolon/tab?

---

**Document Version**: 1.0
**Created**: 2025-12-14
**Status**: Draft - Awaiting Approval
