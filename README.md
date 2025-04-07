# Material Icons Python

A Flask-based API service for serving Material Design icons as SVG files. This project provides a simple interface to search and retrieve Material Design icons in various styles.

## Features

- Search for Material Design icons by name
- Filter icons by style (baseline, outlined, rounded, sharp, twotone)
- Serve SVG files directly
- RESTful API endpoints
- Cross-Origin Resource Sharing (CORS) support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/devatrii/material-icons-python.git
cd material-icons-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the Flask application:

```bash
python main.py
```

The server will start on `http://0.0.0.0:2005`.

### API Endpoints

#### Search Icons

```
GET /search/<query>?style=<style>
```

Parameters:
- `query`: The name of the icon to search for
- `style` (optional): Filter by style (baseline, outlined, rounded, sharp, twotone)

Example:
```
GET /search/account_circle?style=outlined
```

Response:
```json
{
  "status": true,
  "message": "",
  "data": [
    {
      "name": "account_circle",
      "varients": ["twotone", "baseline", "round", "outline", "sharp"]
    }
  ]
}
```

#### Get Icon SVG

```
GET /icon/<icon_name>?style=<style>
```

Parameters:
- `icon_name`: The name of the icon to retrieve
- `style` (optional): The style of the icon (defaults to "baseline")

Example:
```
GET /icon/account_circle?style=outlined
```

Response: SVG file content

## Project Structure

- `main.py`: Flask application setup and configuration
- `api_routes.py`: API endpoint definitions
- `converter.ipynb`: Jupyter notebook for data conversion (if applicable)
- `icons_db.json`: Database of available icons and their variants
- `svg/`: Directory containing SVG files

## Development

### Adding New Icons

1. Add the SVG files to the appropriate directories in the `svg/` folder
2. Update the `icons_db.json` file with the new icon information

### Extending the API

To add new endpoints, modify the `api_routes.py` file and add new route handlers.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 