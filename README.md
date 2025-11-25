# Google Drive MCP Server

A server that provides MCP (Machine Control Protocol) interface to interact with Google Drive files and folders.

## Features

- Search for files in Google Drive
- Get file content and metadata
- OAuth authentication with token persistence
- HTTP and stdio transport modes

## Quick Start with Docker Compose

The easiest way to get started is using Docker Compose:

### Prerequisites

1. **Docker and Docker Compose** installed on your system
2. **Google Drive API credentials** - Download `credentials.json` from [Google Cloud Console](https://console.cloud.google.com/)
3. **Authentication token** - Generate `tokens.json` by running auth setup (see below)

### Setup Steps

1. **Place your files in the project root:**
   - `credentials.json` - Your Google Drive API credentials
   - `tokens.json` - Your authentication token (generate if you don't have it)

2. **Generate authentication token (if needed):**
   ```bash
   # First, set up a local environment
   python -m venv venv
   source venv/bin/activate
   pip install -e .
   
   # Run authentication setup
   python -m gdrive_mcp_server.auth_setup --credentials credentials.json --token tokens.json
   ```

3. **Start the server:**
   ```bash
   docker-compose up -d
   ```

4. **Verify it's running:**
   ```bash
   docker-compose logs -f
   # You should see: "Starting Google Drive MCP server!"
   ```

5. **Test the connection:**
   ```bash
   curl -X POST http://localhost:8000/mcp/v1/initialize \
     -H "Content-Type: application/json" \
     -d '{"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}'
   ```

6. **Stop the server:**
   ```bash
   docker-compose down
   ```

### Configuration

- **Custom port:** Create a `.env` file with `HTTP_PORT=8000` (or your preferred port)
- **View logs:** `docker-compose logs -f`
- **Restart:** `docker-compose restart`

The server will be available at `http://localhost:8000` (or your configured port).

## Requirements

- Python 3.11 or higher
- Google Drive API credentials

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the package in editable mode:
```bash
pip install -e .
```

3. Set up Google Drive API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Drive API for your project
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" and select "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials file and save it as `credentials.json`

4. Set up Google Drive authentication:
```bash
python -m gdrive_mcp_server.auth_setup --credentials /path/to/your/credentials.json --token /path/to/your/tokens.json
```

## Usage

Run the server:
```bash
# Standard mode
gdrive-mcp

# HTTP mode
gdrive-mcp --http
```

## Docker Usage

> **Quick Start:** See the [Quick Start with Docker Compose](#quick-start-with-docker-compose) section above for the fastest way to get started.

### Running with Docker Compose

1. Create a `.env` file (optional, for custom port):
```bash
HTTP_PORT=8000
```

2. Build and run the container:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the container:
```bash
docker-compose down
```

### Running with Docker

1. Build the image:
```bash
docker build -t gdrive-mcp-server .
```

2. Run the container:
```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/credentials.json:/app/data/credentials.json:ro \
  -v $(pwd)/tokens.json:/app/data/tokens.json \
  --name gdrive-mcp-server \
  gdrive-mcp-server
```

### Running in stdio mode

To run in stdio mode instead of HTTP mode, modify the command in `docker-compose.yml`:
```yaml
command: ["python", "-m", "gdrive_mcp_server.server", "--token", "/app/data/tokens.json"]
```

## Claude Desktop Integration

To integrate with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "google_drive": {
    "command": "/path/to/your/venv/bin/gdrive-mcp",
    "args": [
      "--token",
      "/path/to/your/tokens.json"
    ]
  }
}
```

Replace the paths with your actual paths:
- `command`: Path to the gdrive-mcp executable in your virtual environment
- `args[1]`: Path to your tokens.json file (generated during authentication setup)

## Development

The project uses:
- Python 3.11+
- Google Drive API
- MCP server framework
- FastMCP for HTTP transport
- Rich for terminal formatting

Development dependencies can be installed with:
```bash
pip install -e ".[dev]"
```

## Testing and Examples

### Quick Start
See [QUICK_START.md](QUICK_START.md) for a 5-minute guide to get started.

### Usage Documentation
See [MCP_USAGE.md](MCP_USAGE.md) for detailed documentation on:
- Connecting to the server
- Listing available tools
- Calling tools
- Example code in Python and curl

### Test Scripts

**Python test client:**
```bash
# Make sure server is running first
python test_mcp_client.py
```

**Bash examples:**
```bash
./examples.sh
```

## License

MIT License 