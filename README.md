
<div align="center">
  <img src="public/scrapper-icon.png" alt="UFRGS Scraper" width="200"/>
</div>

# UFRGS Admissions Data Scraper

A Python-based web scraping tool that collects and processes admissions data from UFRGS (Universidade Federal do Rio Grande do Sul) for both Vestibular and SISU selection processes.

## Features

- 🎓 Scrapes admissions data from UFRGS portal
- 📊 Supports both Vestibular and SISU selection processes
- 🗄️ Automatic database storage with batch processing
- 🐳 Fully containerized with Docker
- 📅 Historical data collection (2016-2025)
- 🔍 Course filtering capabilities
- 🔄 Data transformation and normalization

## Project Structure

```
├── services/
│   ├── api_wrapper.py       # HTTP request handling
│   └── database_service.py  # Database operations
├── main.py                  # Main scraper script
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Multi-container setup
├── requirements.txt        # Python dependencies
├── run.sh                  # Execution script
└── .env                    # Environment variables
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+ (if running locally)

## Installation & Setup

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ufrgs-scraper
   ```

2. **Build the Docker image**
   ```bash
   docker build -t scraper .
   ```

3. **Configure environment variables**
   Create a `.env` file with your database configuration:
   ```env
   DATABASE_URL=your_database_url_here
   # Add other required environment variables
   ```

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage

### Using the Shell Script (Recommended)

The easiest way to run the scraper is using the provided shell script:

### Manual Docker Execution

```bash
# Scrape data for a specific course across all years
docker run --rm scraper python main.py "course_name" 2016 2017 2018 2019 2020 2021 2022 2023 2024 2025

# Scrape data for specific years only
docker run --rm scraper python main.py "psicologia" 2023 2024 2025

# Scrape all courses for specific years
docker run --rm scraper python main.py "" 2024 2025
```

### Local Execution

```bash
# Run with course filter and specific years
python main.py "course_name" 2023 2024 2025

# Run with course filter for all years
python main.py "psicologia"
```

## How It Works

1. **Course Discovery**: The scraper first fetches available courses for each year and selection type (Vestibular/SISU)
2. **Data Extraction**: For each course, it retrieves candidate data including rankings, scores, and status information
3. **Data Processing**: Raw HTML tables are parsed and converted to structured data
4. **Data Storage**: Processed data is stored in the database using batch operations

## Data Fields

The scraper collects and normalizes the following candidate information:

| Original Field | Normalized Field | Description |
|----------------|------------------|-------------|
| Classificação | classification | Candidate ranking |
| Média | score | Average score |
| Vaga(s) de Concorrência | concurrence_type | Competition type |
| Período Vaga | period | Period/shift |
| Vaga de Ingresso | enter_type | Entry type |
| Situação | status | Current status |
| Data Situação | date | Status date |
| Candidato | name | Candidate name |

Additional fields added during processing:
- `year`: Selection year
- `course_name`: Full course name
- `exam_type`: Selection type (vest/sisu)

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://user:password@host:port/database
# Add other configuration as needed
```

### Docker Compose

For development with database included:

```bash
docker-compose up -d
```
## Performance Considerations

- **Rate Limiting**: The scraper respects the target server by implementing appropriate delays
- **Batch Processing**: Database operations are batched for efficiency
- **Memory Management**: Large datasets are processed in chunks
- **Caching**: Course data is cached to avoid redundant requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and research purposes only. Please respect the target website's robots.txt and terms of service. The authors are not responsible for any misuse of this tool.