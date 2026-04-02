# STE Mapbook Workflow

Generates a multi-section mapbook report for wildlife tracking data sourced from EarthRanger. For each subject, the workflow produces six map visualizations, a Word document report, and an interactive dashboard.

## What it produces

| Output | Description |
|--------|-------------|
| **Movement Tracks map** | Current vs. previous period tracks, color-coded by period |
| **Speed Map** | Trajectories colored by speed bins (km/h) |
| **Day/Night Map** | Trajectories colored by day (orange) or night (dark blue) |
| **Home Range map** | Elliptical Time Density (ETD) contours + Minimum Convex Polygon (MCP) |
| **Mean Speed Raster** | Hexagonal raster of mean movement speed |
| **Seasonal Home Range** | ETD contours split by wet/dry season |
| **Mapbook (.docx)** | Word document with a cover page and one section per subject |
| **Dashboard** | Interactive widget dashboard with all maps and summary metrics |

---

## Requirements

- Access to an **EarthRanger** instance with a configured data source
- Access to a **Google Earth Engine** project
- The `landDx` geodatabase (downloaded automatically from Dropbox by default)

---

## Configuration Parameters

When running the workflow you will be prompted to fill in the following:

### Workflow Details
| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional description |

### Define Analysis Time Range
| Field | Description |
|-------|-------------|
| Since | Start date/time of the analysis period |
| Until | End date/time of the analysis period |

### Set Previous Period Range
Defines the comparison period shown on the Movement Tracks map.

| Option | Description |
|--------|-------------|
| Same as current period | Mirror the current period length ending at the current start |
| Previous month | Calendar month before the current period |
| Previous 3 months | Three calendar months before the current period |
| Previous 6 months | Six calendar months before the current period |
| Previous year | One calendar year before the current period |
| Enter start date | Manually specify a start date for the previous period |

### Data Sources
| Field | Description |
|-------|-------------|
| Connect to EarthRanger | Select the EarthRanger data source to pull observations from |
| Connect to Earth Engine | Select the Google Earth Engine project for seasonal analysis |

### Subject Group
| Field | Description | Default |
|-------|-------------|---------|
| Subject Group Name | Name of the subject group in EarthRanger (case-sensitive) | `Elephants` |

### Load landDx Database
The landDx geodatabase contains protected area boundaries (Community Conservancies, National Reserves, National Parks) used as base layers on all maps.

| Option | Description | Default |
|--------|-------------|---------|
| Download from URL | Provide a URL to download the `.gpkg` file | Pre-filled Dropbox URL |
| Use local file | Provide a path to a local `.gpkg` file | — |

### Trajectory Segment Filter
Filters out GPS noise and unrealistic movements before trajectory analysis. The same filter is applied to both current and previous period trajectories.

| Field | Default | Description |
|-------|---------|-------------|
| Minimum Segment Length (m) | `0.001` | Discard segments shorter than this distance |
| Maximum Segment Length (m) | `5000` | Discard segments longer than this distance |
| Minimum Segment Duration (s) | `1` | Discard segments shorter than this duration |
| Maximum Segment Duration (s) | `21600` | Discard segments longer than this duration (default = 6 h) |
| Minimum Speed (km/h) | `0.01` | Discard segments below this average speed |
| Maximum Speed (km/h) | `9` | Discard segments above this average speed |

### Zoom to gdf extent
| Field | Default | Description |
|-------|---------|-------------|
| Expansion Factor | `1.05` | Padding around the map boundary. `1.0` = tight fit, `1.2` = 20% padding |

### Report Logo
The logo appears on the mapbook cover page.

| Option | Description |
|--------|-------------|
| Download from URL | Provide a URL to a PNG or JPG logo |
| Use local file | Provide a path to a local image file |

---

## Output Files

All outputs are written to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`:

| File | Description |
|------|-------------|
| `trajectories.geoparquet` | Current period trajectories |
| `previous_period_trajectories.geoparquet` | Previous period trajectories |
| `relocations.geoparquet` | Current period relocations |
| `previous_period_relocations.geoparquet` | Previous period relocations |
| `*.geoparquet` (ETD, MCP, seasonal) | Home range polygons per subject |
| `*_movement_tracks.html` | Interactive movement tracks map per subject |
| `*_speedmap.html` | Interactive speed map per subject |
| `*_day_night.html` | Interactive day/night map per subject |
| `*_homerange.html` | Interactive home range map per subject |
| `*_mean_speed_raster.html` | Interactive mean speed raster map per subject |
| `*_seasonal_home_range.html` | Interactive seasonal home range map per subject |
| `mapbook_context_page.docx` | Cover page document |
| `*.docx` (per subject) | Individual subject report sections |
| Merged mapbook `.docx` | Final combined Word report |

---