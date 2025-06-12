# T-SQL to Spark SQL Conversion Application Requirements

## Application Overview
Build a comprehensive Python-based solution with CLI and web interfaces that converts Microsoft SQL Server T-SQL to Spark SQL, with verification capabilities to ensure the accuracy of conversions.

## User Personas
1. **Developers** - Primary users of the CLI tools for batch processing and automation
2. **Implementation Team** - Uses the web application for manual verification and approval workflow

## Core Components

### Configuration System
- All application settings stored in YAML format at the root directory
- Required file: `config.yaml` (active configuration)
- Sample file: `config_sample.yaml` (reference configuration)
- Configuration should include:
  - Database connection parameters
  - API keys for Claude integration
  - Logging preferences
  - Output directory settings

### Logging System
- JSON-based structured logging to `output/<schema>_<object name>/logs.json`
- Each log entry must contain:
  - Timestamp (ISO 8601 format)
  - Type (info, warning, error, api-request, api-response)
  - Message (Markdown formatted content)
- Log rotation and archiving capabilities

### CLI Interface
Implement a shell script (`run.sh`) as the entry point with the following commands:

1. **Setup Command**
   ```
   ./run.sh setup
   ```
   - Downloads SQL objects from the source database
   - Saves original T-SQL to `output/<schema>_<object name>/1-original.sql`
   - Extracts table schemas and data to CSV files in `output/data/`

2. **Conversion Command**
   ```
   ./run.sh convert
   ```
   - Processes all SQL objects needing conversion
   - Sends T-SQL to Claude API with appropriate prompts
   - Records API interactions in logs
   - Saves converted Spark SQL to `output/<schema>_<object name>/2-converted.sql`

3. **Syntax Verification Command**
   ```
   ./run.sh verify-syntax <schema>_<object name>
   ```
   - Runs PySpark EXPLAIN on the converted SQL
   - Logs results with appropriate status indicators

4. **Data Verification Command**
   ```
   ./run.sh verify-data <schema>_<object name>
   ```
   - Loads data from the extracted CSV files
   - Executes the converted Spark SQL against loaded data
   - Logs execution results and any errors

5. **Status Management Command**
   ```
   ./run.sh set-status <schema>_<object name> <status>
   ```
   - Updates the status field in `metadata.json`
   - Valid statuses: review, approve, reject

6. **Listing Command**
   ```
   ./run.sh list [--status=<status>] [--schema=<schema>] [--search=<term>]
   ```
   - Displays a tabular view of all SQL objects
   - Supports filtering by status, schema, and search terms

### Web Application

#### Architecture
- Backend: Python + Flask
- Frontend: Alpine.js (minimal JavaScript framework) + Tailwind CSS
- RESTful API endpoints for all CLI operations

#### Dashboard Screen
- Main navigation hub with:
  - Action buttons for global operations (Setup, Convert All)
  - SQL objects table with:
    - Schema and object name columns
    - Type indicator (view, procedure, function)
    - Status indicator with color coding
    - Last modified timestamp
    - Action buttons for individual operations
  - Filtering controls:
    - Dropdown for status selection
    - Text input for search
    - Schema selection
  - Sorting capabilities on all columns

#### Verification Screen
- Object details header showing schema, name, and type
- Action toolbar with:
  - Verification buttons (Verify Syntax, Verify Data)
  - Status buttons (Approve, Reject, Set to Review)
- Tab-based interface:
  1. **Comparison Tab**:
     - Side-by-side editor showing original T-SQL and converted Spark SQL
     - Line numbering and syntax highlighting
     - Editable converted SQL with save functionality
  2. **Logs Tab**:
     - Chronological list of all operations on this object
     - Filter controls for log types
     - Rendered markdown for selected log entries
     - Search functionality within logs

## File Structure
```
project-root/
├── .gitignore                    # Git ignore patterns
├── config_sample.yaml            # Sample configuration
├── config.yaml                   # Active configuration
├── run.sh                        # CLI entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Documentation
├── convert/                      # Python module for conversion logic
│   ├── __init__.py
│   ├── api.py                    # Claude API integration
│   ├── cli.py                    # CLI command implementations
│   ├── db.py                     # Database operations
│   ├── spark.py                  # Spark SQL validation
│   └── utils.py                  # Utility functions
├── web/                          # Web application
│   ├── __init__.py
│   ├── app.py                    # Flask application
│   ├── routes.py                 # API endpoints
│   ├── static/                   # Static assets
│   └── templates/                # HTML templates
├── test/                         # Test suite
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_cli.py
│   ├── test_conversion.py
│   └── fixtures/                 # Test data
└── output/                       # Generated outputs
    ├── data/                     # Extracted table data (CSV)
    └── <schema>_<object name>/   # Per-object output
        ├── metadata.json         # Object metadata
        ├── logs.json             # Operation logs
        ├── 1-original.sql        # Original T-SQL
        └── 2-converted.sql       # Converted Spark SQL
```

## Technical Requirements

### API Integration
- Implement Claude API integration with:
  - Proper error handling and retries
  - Rate limiting compliance
  - Context management for large SQL objects
  - Prompt engineering for optimal conversion

### Data Handling
- Support for all common SQL data types
- CSV parsing and generation with proper escaping
- Data validation before and after conversion

### Error Handling
- Graceful failure modes with informative error messages
- Recovery mechanisms for interrupted operations
- Detailed logging for debugging purposes

### Security
- Secure credential management
- Input validation to prevent injection attacks
- Proper file permissions for output directory

### Testing
- Unit tests for all core functions
- Integration tests for end-to-end workflows
- Test fixtures for various SQL object types

## Deployment Considerations
- Docker containerization support
- Environment variable configuration for sensitive data
- Documentation for installation and usage

This specification provides a comprehensive foundation for generating a complete T-SQL to Spark SQL conversion application with both CLI and web interfaces.