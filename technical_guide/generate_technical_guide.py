"""
Generate the STE Mapbook Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: ste_mapbook_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from datetime import date

OUTPUT_FILE = "ste_mapbook_technical_guide.pdf"

# ── Colour palette ────────────────────────────────────────────────────────────
GREEN_DARK   = colors.HexColor("#115631")
GREEN_MID    = colors.HexColor("#2d6a4f")
GREEN_LIGHT  = colors.HexColor("#d8f3dc")
AMBER        = colors.HexColor("#e7a553")
SLATE        = colors.HexColor("#3d3d3d")
LIGHT_GREY   = colors.HexColor("#f5f5f5")
MID_GREY     = colors.HexColor("#cccccc")
WHITE        = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE     = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                   spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE  = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                   spaceAfter=4,  alignment=TA_CENTER)
META      = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                   alignment=TA_CENTER, spaceAfter=2)

H1        = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                   spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold",
                   borderPad=0)
H2        = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                   spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3        = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                   spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")

BODY      = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                   spaceAfter=6, alignment=TA_JUSTIFY)
BULLET    = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                   spaceAfter=3, leftIndent=14, firstLineIndent=-10,
                   bulletIndent=4)
CODE      = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                   backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                   spaceAfter=4, leftIndent=10, rightIndent=10,
                   borderPad=3)
NOTE      = _style("Note", fontSize=8.5, leading=13, textColor=colors.HexColor("#555555"),
                   backColor=colors.HexColor("#fff8e1"), leftIndent=10,
                   rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):
    return Paragraph(text, style)

def h1(text): return Paragraph(text, H1)
def h2(text): return Paragraph(text, H2)
def h3(text): return Paragraph(text, H3)
def sp(n=6):  return Spacer(1, n)
def bullet(text): return Paragraph(f"• {text}", BULLET)  # noqa: uses BulletItem style
def note(text):   return Paragraph(f"<b>Note:</b> {text}", NOTE)
def code(text):   return Paragraph(text, CODE)

def table(data, col_widths, header_row=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header_row else 0)
    style = [
        ("BACKGROUND",  (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",   (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",        (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",(0, 0), (-1, -1), 6),
        ("TOPPADDING",  (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",(0,0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Footer bar
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "STE Mapbook — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    # Top accent line
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="STE Mapbook — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover / Title ─────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("STE Mapbook", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Elephant Movescape Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"),
        hr(),
        p(
            "The <b>STE Mapbook</b> workflow is a data-to-report pipeline purpose-built for "
            "analysing African elephant (<i>Loxodonta africana</i>) movement ecology. "
            "It ingests GPS telemetry data from <b>EarthRanger</b>, performs a sequence of "
            "spatial and statistical computations, and delivers six map products, summary "
            "statistics, an interactive dashboard, and a print-ready Word mapbook — all "
            "organised per individual elephant."
        ),
        p(
            "The workflow is implemented as an <b>Ecoscope Workflow</b> (YAML spec) and "
            "executes within the <code>ecoscope-workflows</code> runtime. Each task in the "
            "spec is a composable, versioned function; tasks are chained via data references "
            "(<code>${{ workflow.&lt;id&gt;.return }}</code>) and the engine resolves "
            "execution order automatically."
        ),
        sp(4),
        note(
            "Although the trajectory segment filter defaults are tuned for elephants "
            "(max speed 9 km/h, max gap 6 h), every threshold is user-configurable at "
            "run time through the workflow form."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All telemetry data is sourced from an <b>EarthRanger</b> instance "
            "(<code>set_er_connection</code> task). The user must select a pre-configured "
            "EarthRanger data source. The workflow calls "
            "<code>get_subjectgroup_observations</code> twice — once for the current "
            "analysis period and once for the comparison (previous) period."
        ),
        bullet("The connection is passed as <code>client</code> to every EarthRanger fetch task."),
        bullet("Authentication is handled by the Ecoscope EarthRanger client; no credentials are stored in the spec."),
        bullet("The <code>filter: clean</code> parameter discards any observation already flagged as junk in EarthRanger before the data even reaches the workflow."),

        sp(4), h2("2.2 Subject Group"),
        p(
            "The user specifies a <b>Subject Group Name</b> (default: <code>Elephants</code>) "
            "that must match exactly — case-sensitively — the name of a subject group in "
            "the connected EarthRanger instance. The workflow fetches every observation for "
            "all subjects within that group over the configured time range."
        ),
        note(
            "If the subject group name is wrong or the group contains no observations in "
            "the requested period, the workflow skips all downstream tasks gracefully via "
            "the <code>any_is_empty_df</code> skipif condition."
        ),

        sp(4), h2("2.3 Google Earth Engine Project"),
        p(
            "A <b>Google Earth Engine (GEE)</b> project is required for the seasonal "
            "analysis component. The task <code>custom_determine_season_windows</code> "
            "queries NDVI time-series data from GEE to classify the analysis period into "
            "wet and dry seasons. The GEE project name is supplied by the user via "
            "<code>set_gee_connection</code>."
        ),

        sp(4), h2("2.4 landDx Geodatabase"),
        p(
            "All six maps share a common base of protected-area polygons sourced from the "
            "<b>landDx</b> geodatabase (<code>landDx.gpkg</code>). By default, the file is "
            "downloaded automatically from a Dropbox URL. Users may also supply a local path."
        ),
        p("The database is filtered to include only three land-use categories:"),
        bullet("Community Conservancy"),
        bullet("National Reserve"),
        bullet("National Park"),
        p(
            "Only three columns are retained after loading: <code>type</code>, "
            "<code>name</code>, and <code>geometry</code>. The layer is then split by "
            "<code>type</code> and each category is styled independently:"
        ),
        table(
            [
                ["Land-use Type", "Fill / Line Colour", "Opacity"],
                ["Community Conservancy", "RGB(166, 182, 151)  #a6b697", "17.5 %"],
                ["National Reserve",     "RGB(136, 167, 142)  #88a78e", "17.5 %"],
                ["National Park",        "RGB(17,  86,  49)   #115631", "17.5 %"],
            ],
            [5.5*cm, 8*cm, 3*cm],
        ),
        p(
            "A text label layer (centroid-anchored, Arial, 1 000 m base size, "
            "40–75 px clamp) shows protected-area names at appropriate zoom levels."
        ),

        sp(4), h2("2.5 Base Map Tile Layer"),
        p(
            "Every map uses the <b>ArcGIS World Hillshade</b> tile service as the "
            "background raster:"
        ),
        code("https://server.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"),
        p("Opacity is set to 1.0 (fully opaque) with a max zoom of 20."),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Observations → Relocations"),
        p(
            "Raw EarthRanger observations are converted to a standardised "
            "<b>relocations GeoDataFrame</b> via <code>process_relocations</code>. "
            "The following columns are extracted and retained:"
        ),
        table(
            [
                ["Column", "Source field", "Description"],
                ["groupby_col",                   "internal",                   "Subject identifier used for grouping"],
                ["fixtime",                        "observation timestamp",       "UTC datetime of the GPS fix"],
                ["junk_status",                    "EarthRanger flag",            "True if fix is marked junk"],
                ["geometry",                       "lat/lon",                    "Point geometry (WGS 84)"],
                ["extra__subject__name",           "subject.name",               "Elephant display name"],
                ["extra__subject__hex",            "subject.hex_color",          "Subject colour used in maps"],
                ["extra__subject__sex",            "subject.sex",                "Subject sex (M / F / unknown)"],
                ["extra__created_at",              "observation.created_at",     "Record creation timestamp"],
                ["extra__subject__subject_subtype","subject.subject_subtype",    "Subject subtype (e.g. elephant)"],
            ],
            [3.5*cm, 4.5*cm, 8.5*cm],
        ),
        p(
            "Three known-bad coordinate pairs are filtered out unconditionally:"
        ),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),

        sp(4), h2("3.2 Day / Night Annotation"),
        p(
            "Each relocation is labelled as day or night by "
            "<code>classify_is_night</code>. The function calculates solar elevation "
            "at the fix's location and UTC timestamp using the <b>ephem</b> library. "
            "A fix is classified as night (<code>is_night = True</code>) when the "
            "sun is below the horizon. This boolean is later used as a colour key "
            "in the Day/Night map."
        ),

        sp(4), h2("3.3 Trajectory Segment Filter"),
        p(
            "Before trajectory construction, a <b>trajectory segment filter</b> "
            "is defined by the user (<code>custom_trajectory_segment_filter</code>). "
            "The same filter object is applied to <i>both</i> the current period "
            "and the previous period trajectories, ensuring methodological consistency "
            "in comparisons."
        ),
        table(
            [
                ["Parameter", "Default", "Unit", "Purpose"],
                ["min_length_meters", "0.001",  "m",   "Remove sub-centimetre GPS noise"],
                ["max_length_meters", "5 000",  "m",   "Remove implausible long jumps"],
                ["min_time_secs",     "1",      "s",   "Remove zero-duration segments"],
                ["max_time_secs",     "21 600", "s",   "Remove gaps > 6 h (fix dropout)"],
                ["min_speed_kmhr",    "0.01",   "km/h","Remove near-stationary fixes"],
                ["max_speed_kmhr",    "9",      "km/h","Remove biologically impossible speeds for elephants"],
            ],
            [4*cm, 2.5*cm, 1.8*cm, 8.2*cm],
        ),
        note(
            "9 km/h is used as the elephant speed ceiling because sustained travel "
            "above this threshold is not observed in the wild under normal conditions. "
            "Segments exceeding this value typically indicate GPS multipath, collar "
            "store-and-forward artefacts, or data-entry errors."
        ),

        sp(4), h2("3.4 Relocations → Trajectories"),
        p(
            "Filtered relocations are connected into <b>linear trajectory segments</b> "
            "by <code>relocations_to_trajectory</code>. Each segment joins two consecutive "
            "fixes for the same subject and records:"
        ),
        bullet("<b>dist_meters</b> — straight-line distance between the two fixes"),
        bullet("<b>speed_kmhr</b> — dist_meters ÷ elapsed time × 3.6"),
        bullet("<b>segment_start / segment_end</b> — timestamps of the bounding fixes"),
        bullet("<b>geometry</b> — LineString in WGS 84"),
        p(
            "A temporal index is then added (<code>add_temporal_index</code>) keyed "
            "to <code>segment_start</code> and grouped by subject name, enabling "
            "efficient per-subject iteration in all downstream tasks."
        ),
    ]

    # ── 4. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Map Outputs — Methodology"), hr(),
    ]

    # 4.1 Movement Tracks
    story += [
        h2("4.1 Movement Tracks Map"),
        p(
            "The Movement Tracks map overlays <b>current period</b> and "
            "<b>previous period</b> trajectories for each subject, allowing "
            "rangers to assess range shifts across time."
        ),
        h3("How the dual-period display is constructed"),
        p(
            "After trajectories for both periods are built independently (both filtered "
            "by the same segment filter), a <code>duration_status</code> column is "
            "appended — <code>'Current tracks'</code> or <code>'Previous tracks'</code>. "
            "The two GeoDataFrames are merged (<code>merge_multiple_df</code>) and "
            "then filtered by <code>filter_groups_by_value_criteria</code> with "
            "<code>criteria: priority</code> and "
            "<code>priority_value: 'Current tracks'</code>. "
            "This step removes subject–periods for which only previous-period data "
            "exists but no current data — preventing orphaned previous tracks from "
            "appearing for subjects no longer in the group."
        ),
        h3("Colour assignment"),
        p(
            "<code>modify_status_colors</code> maps each unique "
            "<code>duration_status</code> value to an RGBA colour. Current tracks "
            "receive a vivid colour derived from the subject's own "
            "<code>hex_color</code> field; previous tracks receive a muted variant. "
            "Trajectories are sorted descending by <code>duration_status</code> so "
            "current tracks are always rendered on top."
        ),
        h3("Line styling"),
        table(
            [
                ["Property",       "Value"],
                ["Width",          "2.85 px (min 2, max 8)"],
                ["Opacity",        "55 %"],
                ["Cap / Join",     "Rounded"],
                ["Width units",    "pixels (screen-space, zoom-independent)"],
            ],
            [5*cm, 11.5*cm],
        ),
    ]

    # 4.2 Speed Map
    story += [
        sp(4), h2("4.2 Speed Map"),
        p(
            "The Speed Map colours each trajectory segment by its average speed, "
            "making it easy to identify corridors of fast travel versus slow "
            "foraging areas."
        ),
        h3("Classification"),
        p(
            "<code>apply_classification</code> bins the <code>speed_kmhr</code> "
            "column using the <b>Equal Interval</b> scheme with <b>k = 6</b> classes. "
            "Equal interval divides the observed speed range into six bins of equal "
            "width. Labels are formatted to one decimal place with the suffix "
            "<code>km/h</code>."
        ),
        note(
            "Equal interval is chosen here (rather than natural breaks) to produce "
            "classes with intuitive, evenly spaced boundaries that are easy to "
            "communicate to non-technical readers."
        ),
        h3("Colour ramp"),
        table(
            [
                ["Bin (low → high)", "Hex colour", "Perception"],
                ["1 (slowest)", "#1a9850", "Dark green — resting / foraging"],
                ["2",           "#91cf60", "Light green"],
                ["3",           "#d9ef8b", "Yellow-green"],
                ["4",           "#fee08b", "Yellow — moderate travel"],
                ["5",           "#fc8d59", "Orange"],
                ["6 (fastest)", "#d73027", "Red — fast directional movement"],
            ],
            [4*cm, 3.5*cm, 9*cm],
        ),
        p(
            "This is a diverging green-to-red ramp (adapted from ColorBrewer "
            "<i>RdYlGn</i>) — perceptually ordered from cool/slow to warm/fast."
        ),
    ]

    # 4.3 Day/Night Map
    story += [
        sp(4), h2("4.3 Day / Night Map"),
        p(
            "Segments are coloured by the <code>is_night</code> boolean computed "
            "during relocation annotation (Section 3.2)."
        ),
        table(
            [
                ["Value",             "Colour",  "Hex"],
                ["Day  (is_night = 0)", "Amber",   "#e7a553"],
                ["Night (is_night = 1)","Dark blue","#292965"],
            ],
            [5*cm, 4*cm, 7.5*cm],
        ),
        p(
            "Trajectories are sorted ascending by <code>is_night</code> so that "
            "night segments (value 1) are rendered last and appear on top of day "
            "segments where they overlap."
        ),
    ]

    # 4.4 Home Range
    story += [
        sp(4), h2("4.4 Home Range Map (ETD + MCP)"),
        p(
            "The Home Range map combines two complementary estimators: "
            "Elliptical Time Density (ETD) contours, which capture the probability "
            "density of space use, and a Minimum Convex Polygon (MCP), which shows "
            "the total bounding extent of all observed locations."
        ),

        h3("4.4.1 Elliptical Time Density (ETD)"),
        p(
            "ETD is a bivariate kernel density estimator that accounts for "
            "the temporal autocorrelation inherent in GPS telemetry. Instead of "
            "treating each fix as an independent observation, it weights space use "
            "by the time spent in each area, producing more ecologically realistic "
            "home range estimates."
        ),
        p("Key parameters used in <code>calculate_elliptical_time_density</code>:"),
        table(
            [
                ["Parameter",              "Value",        "Meaning"],
                ["CRS",                    "ESRI:53042",   "World Azimuthal Equidistant — equal-area, minimises distortion for range-wide computations"],
                ["cell_size",              "Auto-scale",   "Cell size is derived automatically from the data extent and trajectory density"],
                ["max_speed_factor",       "1.05",         "Segments with speed > 1.05 × median are down-weighted (reduces motorway artefacts)"],
                ["expansion_factor",       "1.3",          "Raster extent is expanded 30 % beyond the data envelope to capture edge usage"],
                ["band_count",             "1",            "Single density band output"],
                ["nodata_value",           "NaN",          "Cells outside the probability mass are set to NaN (transparent)"],
                ["percentiles",            "50, 60, 70, 80, 90, 95, 99.9", "Contours at these probability thresholds are extracted as polygons"],
            ],
            [4*cm, 2.8*cm, 9.7*cm],
        ),
        p(
            "The resulting raster is reprojected back to <b>EPSG:4326 (WGS 84)</b> "
            "before visualisation. Contour polygons are coloured using the "
            "<b>RdYlGn</b> diverging colormap — innermost (50th percentile core) "
            "in red, outermost (99.9th percentile) in green — providing an "
            "intuitive density gradient."
        ),

        h3("4.4.2 Minimum Convex Polygon (MCP)"),
        p(
            "<code>generate_mcp_gdf</code> computes the convex hull of all "
            "fix locations in the planar CRS <b>ESRI:53042</b> and reports the "
            "polygon area in km². The MCP is displayed as a hot-pink outline "
            "(RGB 255, 20, 147) with no fill, so the ETD contours remain visible "
            "beneath it."
        ),
        note(
            "ESRI:53042 (World Azimuthal Equidistant, centred at the equator) is "
            "used for all area calculations in this workflow because it preserves "
            "distances from the centre point and produces consistent area metrics "
            "across the African continent without the distortion of geographic "
            "coordinate systems."
        ),
    ]

    # 4.5 Mean Speed Raster
    story += [
        sp(4), h2("4.5 Mean Speed Raster"),
        p(
            "The Mean Speed Raster aggregates segment-level speeds onto a "
            "regular hexagonal grid, revealing landscape-scale patterns in "
            "elephant movement intensity."
        ),

        h3("Raster generation — ecograph parameters"),
        p(
            "The raster is computed by <code>generate_ecograph_raster</code> "
            "(the <i>ecograph</i> algorithm from the Ecoscope library):"
        ),
        table(
            [
                ["Parameter",          "Value",   "Effect"],
                ["step_length",        "2 000 m", "Trajectories are resampled to 2 km steps before aggregation; this regularises the contribution of each segment regardless of fix rate"],
                ["movement_covariate", "speed",   "The metric being aggregated is speed (km/h)"],
                ["interpolation",      "mean",    "Within each hex cell, values are averaged across all contributing steps"],
                ["radius",             "2",       "Each hex cell also incorporates contributions from its 2-ring neighbourhood (smoothing)"],
                ["dist_col",           "dist_meters", "Source column for step-length weighting"],
                ["cutoff",             "null",    "No hard cutoff on contributing distance"],
                ["tortuosity_length",  "3",       "Path sinuosity is computed over 3-step windows"],
                ["resolution",         "null",    "Hex cell size is auto-derived from data density"],
            ],
            [3.8*cm, 2.8*cm, 9.9*cm],
        ),

        h3("Classification and colouring"),
        p(
            "The raw per-cell mean speed values are classified using "
            "<b>Natural Breaks (Jenks)</b> with <b>k = 6</b> classes. "
            "Natural breaks minimises within-class variance and maximises "
            "between-class variance — well-suited to speed rasters where the "
            "distribution is typically right-skewed (many slow cells, few fast ones)."
        ),
        p(
            "The same six-colour green-to-red ramp used on the Speed Map is "
            "applied here, so readers can intuitively compare the two products. "
            "Labels are formatted to one decimal place in km/h."
        ),
        note(
            "The key distinction between the Speed Map and the Mean Speed Raster: "
            "the Speed Map colours individual trajectory segments (showing routes), "
            "whereas the Mean Speed Raster aggregates all movement across a spatial "
            "grid (showing landscape-level patterns). Areas used by fast-moving "
            "elephants appear as red hex cells even if no single track crosses them."
        ),
    ]

    # 4.6 Seasonal Home Range
    story += [
        sp(4), h2("4.6 Seasonal Home Range Map"),
        p(
            "The Seasonal Home Range map shows how elephant space use shifts "
            "between the <b>wet</b> and <b>dry</b> seasons — a key indicator of "
            "resource availability and migratory behaviour."
        ),

        h3("Season determination — GEE NDVI"),
        p(
            "<code>custom_determine_season_windows</code> queries the Google Earth "
            "Engine NDVI time series for the region of interest (derived from the "
            "ETD extent) over the analysis period. Wet and dry season windows are "
            "identified from the NDVI phenology curve: periods where NDVI exceeds "
            "a threshold are classified as <i>wet</i>; periods below are "
            "classified as <i>dry</i>. The function returns a DataFrame of dated "
            "season intervals (persisted as a CSV for auditability)."
        ),
        note(
            "The season boundaries are data-driven — they reflect the actual green-up "
            "and senescence pattern for the specific landscape and year, rather than "
            "fixed calendar dates. This is critical in East African ecosystems where "
            "rainfall timing can vary considerably year to year."
        ),

        h3("Season labelling on trajectories"),
        p(
            "<code>create_seasonal_labels</code> joins the season windows to the "
            "trajectory GeoDataFrame on timestamp, adding a <code>season</code> "
            "column (e.g. <code>'wet'</code> or <code>'dry'</code>) to each segment."
        ),

        h3("ETD calculation per season"),
        p(
            "<code>calculate_seasonal_home_range</code> groups the labelled "
            "trajectories by <code>season</code> and runs an ETD calculation for "
            "each season group. Only the <b>99.9th percentile</b> contour is "
            "extracted, giving a near-total home range boundary per season. "
            "Cell size is auto-scaled for each season independently."
        ),

        h3("Colour assignment"),
        p(
            "<code>assign_season_colors</code> maps each season label to a "
            "fixed colour palette (wet = blue family, dry = orange/brown family). "
            "Polygons are rendered as filled, semi-transparent GeoJSON layers "
            "(opacity 55 %) so both seasons are visible when overlapping."
        ),
    ]

    # ── 5. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Summary Metrics"), hr(),
        p(
            "Three scalar metrics are computed per subject and displayed as "
            "widgets in the dashboard and mapbook."
        ),
        table(
            [
                ["Metric",         "Source task",              "How it is calculated"],
                ["Total MCP Area (km²)",
                 "dataframe_column_sum → total_mcp_area",
                 "Sums the area_km2 column of the MCP GeoDataFrame (calculated in ESRI:53042)"],
                ["Total Grid Area (km²)",
                 "dataframe_column_sum → total_grid_area",
                 "Sums the area_sqkm column of the ETD GeoDataFrame (grid cell areas in ESRI:53042)"],
                ["Gender",
                 "dataframe_column_first_unique_str → subject_gender",
                 "Returns the first unique value in the subject_sex column (M, F, or unknown)"],
            ],
            [3.8*cm, 5.5*cm, 7.2*cm],
        ),
        p(
            "The report duration (in months, rounded to 2 decimal places) is also "
            "computed from the analysis time range and included in the mapbook "
            "context page."
        ),
    ]

    # ── 6. Mapbook Report ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Mapbook Report (.docx)"), hr(),
        p(
            "The final deliverable is a <b>multi-section Word document</b> "
            "assembled from a cover page and one section per subject."
        ),

        h2("6.1 Cover Page"),
        p(
            "A Word template (<code>mapbook_cover_page.docx</code>) is downloaded "
            "from a Dropbox URL and populated with:"
        ),
        bullet("Total subject count"),
        bullet("Analysis time range (since / until)"),
        bullet("Prepared by: Ecoscope"),
        bullet("Organisation logo (user-supplied PNG or JPG)"),

        h2("6.2 Per-Subject Section"),
        p(
            "For each subject a section template "
            "(<code>mapbook_grouper_template.docx</code>) is rendered with:"
        ),
        bullet("Subject name and sex"),
        bullet("Current and previous period dates"),
        bullet("Report duration in months"),
        bullet("MCP area and ETD grid area (km²)"),
        bullet("Six map images (PNG, rendered via headless Playwright screenshot at 2× device scale factor)"),
        p(
            "Map images are generated by <code>adjust_map_zoom_and_screenshot</code>, "
            "which loads each interactive HTML map, adjusts the view state to the "
            "pre-computed GDF extent, waits 40 seconds for tiles to load, then "
            "captures a full-resolution screenshot. Image boxes are 11.11 × 6.5 cm."
        ),

        h2("6.3 Document Merge"),
        p(
            "<code>merge_mapbook_files</code> concatenates the cover page document "
            "and all per-subject sections into a single Word file, maintaining "
            "correct page ordering and section breaks."
        ),
    ]

    # ── 7. Dashboard ──────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Interactive Dashboard"), hr(),
        p(
            "An interactive dashboard is assembled from all widget outputs via "
            "<code>gather_dashboard</code>. The dashboard contains:"
        ),
        table(
            [
                ["Widget",                "Type",          "Source"],
                ["Gender",                "Text",          "subject_sex first unique value"],
                ["Total MCP Area",        "Single value",  "MCP area in km²"],
                ["Total Grid Area",       "Single value",  "ETD grid area in km²"],
                ["Movement Tracks",       "Map",           "Interactive DeckGL HTML per subject"],
                ["Home Range",            "Map",           "ETD + MCP DeckGL HTML per subject"],
                ["Speed Map",             "Map",           "Speed-coloured DeckGL HTML per subject"],
                ["Mean Speed Raster",     "Map",           "Ecograph hex raster DeckGL HTML"],
                ["Day / Night Tracks",    "Map",           "Day/night coloured DeckGL HTML"],
                ["Seasonal Home Range",   "Map",           "Season-coloured ETD DeckGL HTML"],
            ],
            [4.5*cm, 3*cm, 9*cm],
        ),
    ]

    # ── 8. Output Files ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Output Files"), hr(),
        p(
            "All outputs are written to the directory defined by the "
            "<code>ECOSCOPE_WORKFLOWS_RESULTS</code> environment variable."
        ),
        table(
            [
                ["File pattern",                         "Format",       "Content"],
                ["trajectories.geoparquet",              "GeoParquet",   "Current period trajectory segments with speed bins"],
                ["previous_period_trajectories.geoparquet","GeoParquet", "Previous period trajectory segments"],
                ["relocations.geoparquet",               "GeoParquet",   "Current period GPS fix locations"],
                ["previous_period_relocations.geoparquet","GeoParquet",  "Previous period GPS fix locations"],
                ["<subject>_etd.geoparquet",             "GeoParquet",   "ETD contour polygons (WGS 84) per subject"],
                ["<subject>_mcp.geoparquet",             "GeoParquet",   "MCP polygon per subject"],
                ["<subject>_seasonal_etd.geoparquet",    "GeoParquet",   "Seasonal ETD contours per subject"],
                ["<subject>_ndvi_seasons.csv",           "CSV",          "GEE-derived season windows with NDVI values"],
                ["<subject>_movement_tracks.html",       "HTML",         "Interactive movement tracks map"],
                ["<subject>_speedmap.html",              "HTML",         "Interactive speed map"],
                ["<subject>_day_night.html",             "HTML",         "Interactive day/night map"],
                ["<subject>_homerange.html",             "HTML",         "Interactive home range map"],
                ["<subject>_mean_speed_raster.html",     "HTML",         "Interactive mean speed raster map"],
                ["<subject>_seasonal_home_range.html",   "HTML",         "Interactive seasonal home range map"],
                ["mapbook_context_page.docx",            "Word",         "Mapbook cover page"],
                ["<subject>.docx",                       "Word",         "Per-subject mapbook section"],
                ["<merged_mapbook>.docx",                "Word",         "Final combined mapbook"],
            ],
            [5.5*cm, 2.5*cm, 8.5*cm],
        ),
    ]

    # ── 9. Workflow Execution Logic ───────────────────────────────────────────
    story += [
        sp(4), h1("9. Workflow Execution Logic"), hr(),

        h2("9.1 Grouping Strategy"),
        p(
            "The grouper is set to <code>subject_name</code> (the individual elephant's "
            "display name from EarthRanger). All map and metric tasks that use "
            "<code>mapvalues</code> iterate over the split-by-group data — producing "
            "one output per subject."
        ),

        h2("9.2 Skip Conditions"),
        p(
            "Every task in the workflow has two default skip conditions:"
        ),
        bullet("<b>any_is_empty_df</b> — if any input DataFrame is empty, the task and all its dependants are skipped rather than raising an error."),
        bullet("<b>any_dependency_skipped</b> — if an upstream task was skipped, all downstream tasks that depend on it are also skipped automatically."),
        p(
            "Widget creation tasks additionally have "
            "<code>skipif: conditions: [never]</code>, meaning they always run "
            "even if their input data would normally trigger a skip — this ensures "
            "the dashboard assembles correctly with partial data."
        ),

        h2("9.3 Previous Period Logic"),
        p(
            "The previous period is determined by "
            "<code>determine_previous_period</code>. Options include:"
        ),
        table(
            [
                ["Option",               "Behaviour"],
                ["Same as current period","Shifts the current period backwards by its own duration"],
                ["Previous month",       "Calendar month immediately before the current period"],
                ["Previous 3 months",    "Three calendar months before the current period start"],
                ["Previous 6 months",    "Six calendar months before the current period start"],
                ["Previous year",        "One calendar year before the current period start"],
                ["Enter start date",     "User supplies an explicit start date; duration matches current period"],
            ],
            [5*cm, 11.5*cm],
        ),
        p(
            "Default is <b>Same as current period</b>, which is the most common "
            "use case for month-on-month comparisons."
        ),
    ]

    # ── 10. Package Versions ──────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Software Versions"), hr(),
        table(
            [
                ["Package",                          "Version",   "Role"],
                ["ecoscope-workflows-core",          "0.22.17.*", "Core task library and workflow engine"],
                ["ecoscope-workflows-ext-ecoscope",  "0.22.17.*", "Ecoscope spatial analysis tasks (ETD, MCP, relocations)"],
                ["ecoscope-workflows-ext-custom",    "0.0.39.*",  "Custom STE utility tasks"],
                ["ecoscope-workflows-ext-big-life",  "0.0.8.*",   "Big Life Foundation domain tasks"],
                ["ecoscope-workflows-ext-ste",       "0.0.18.*",  "STE-specific tasks (mapbook, seasonal analysis)"],
            ],
            [5.5*cm, 3*cm, 8*cm],
        ),
        p(
            "Packages are distributed via the <code>prefix.dev</code> conda channel "
            "and pinned to patch-compatible versions (<code>.*</code> suffix). "
            "The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build PDF ─────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
