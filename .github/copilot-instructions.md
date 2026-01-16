# AI Coding Agent Instructions for data-engineering-workshop

## Project Overview
This is a **data engineering workshop** focused on practical ETL (Extract, Transform, Load) pipelines using Docker, Terraform, and PostgreSQL. The primary module demonstrates ingesting NYC taxi data from public sources into a PostgreSQL database.

## Architecture & Key Components

### Data Pipeline Pattern (`01-Docker_Post_Terraform/testdoc/pipeline/`)
- **Primary Workflow**: Remote CSV → Pandas DataFrame → PostgreSQL
  - `ingest_data.py`: Main entry point for data ingestion with chunked CSV processing
  - Downloads NYC yellow taxi data from: `https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/`
  - Uses SQLAlchemy for database connection management
  - Processes data in chunks (default: 100k rows) to manage memory
  - Creates table schema on first chunk, then appends remaining chunks

### Infrastructure
- **Docker**: Containerizes Python pipeline with uv for deterministic dependency management
  - Base image: `python:3.13.11-slim`
  - Uses `uv sync --locked` for reproducible builds
- **Terraform** (`01-Docker_Post_Terraform/terraform/`): Infrastructure-as-code (templates present but not yet implemented)
- **PostgreSQL**: Persistent data store for taxi trip data

## Critical Developer Workflows

### Running the Ingest Pipeline
```bash
# From pipeline directory
uv run python ingest_data.py \
  --pg-user=root \
  --pg-password=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --pg-table=yellow_taxi_trips_2021_1
```

### Dependency Management
- **Tool**: `uv` (modern Python package manager - see `pyproject.toml`)
- **Python**: 3.13+ (specified in `.python-version`)
- **Key Dependencies**:
  - `pandas>=2.3.3`: Data manipulation
  - `sqlalchemy>=2.0.45`: Database ORM
  - `psycopg2-binary>=2.9.11`: PostgreSQL adapter
  - `pyarrow>=22.0.0`: Columnar data format
  - `tqdm>=4.67.1`: Progress bars
- **Dev Dependencies**: `jupyter`, `pgcli` (for interactive development/debugging)

### Docker Build & Run
```bash
# Build pipeline image
docker build -t pipeline:latest 01-Docker_Post_Terraform/testdoc/pipeline/

# Run (requires PostgreSQL service running)
docker run pipeline:latest
```

## Project-Specific Conventions

### Data Type Handling
The `ingest_data.py` defines a `dtype` dictionary for schema enforcement:
- Integer columns use nullable `Int64` (not `int64`) to allow NULLs
- Temporal columns: `tpep_pickup_datetime`, `tpep_dropoff_datetime` parsed as datetime
- Example: `"VendorID": "Int64"`, `"fare_amount": "float64"`

### Chunked Data Processing
Always process large datasets in chunks to prevent memory exhaustion:
```python
df_iter = pd.read_csv(url, chunksize=100000, iterator=True)
for df_chunk in tqdm(df_iter):
    # Process chunk
    df_chunk.to_sql(name='target_table', con=engine, if_exists='append')
```

### Database Connection String Format
PostgreSQL URIs follow: `postgresql://{user}:{password}@{host}:{port}/{database}`

## Integration Points & External Dependencies

### NYC-TLC Open Data
- Source: `github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/`
- File format: Gzipped CSV (pandas handles decompression automatically)
- Data contains: Vendor ID, passenger count, trip distance, fare/tip amounts, location IDs, timestamps, etc.

### Cross-Module Relationships
- **01-Docker_Post_Terraform/**: Core ETL + infrastructure (primary module)
- **02-06/**: Additional workshop modules (Module-2 through Module-6) with solution documentation
- **Notebooks** (`notebook.ipynb`, `solution.ipynb`): Interactive exploration & testing of pipeline logic

## Important Conventions

1. **Table Naming**: Use descriptive names with year/month suffix (e.g., `yellow_taxi_trips_2021_1`)
2. **Progress Tracking**: Always wrap data loops with `tqdm` for visibility into long-running operations
3. **Error Handling**: Currently minimal; enhance with retry logic for network downloads and database failures
4. **Configuration**: CLI arguments or environment variables for database credentials (seen in workflow examples)
5. **Jupyter Notebooks**: Used for development/testing before production pipeline code

## Common Development Tasks

- **Modify data schema**: Update `dtype` and `parse_dates` dictionaries in `ingest_data.py`
- **Change data source**: Modify `prefix` and `url` variables (supports different years/months)
- **Adjust chunk size**: Change `chunksize` parameter (trade-off: memory vs. I/O)
- **Add columns**: Extend `dtype` dict and ensure PostgreSQL schema compatibility
- **Debug locally**: Use `pgcli` (in dev dependencies) to query results; use Jupyter notebooks for exploratory analysis
