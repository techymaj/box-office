# Raspberry Pi Media Library Application

This Flask application serves a media library where users can browse, stream, and download video files. The application dynamically builds a library of video files using hashes and provides a web interface to access them.

## Features

1. **Dynamic Media Crawling**:
   - Automatically generates a file tree and hashes filenames when the application starts if `tree.json` doesn't exist.

2. **Library View**:
   - Displays a list of available media files with links to play them.

3. **Media Playback**:
   - Streams video files via the browser and provides an option to download them.

4. **Error Handling**:
   - Returns a 404 error if a requested file or hash doesn't exist.

## Folder Structure

```
.
├── app.py                 # Main Flask application
├── crawler.py             # Contains the `crawl()` function to generate file tree and hashes
├── templates/             # HTML templates
│   ├── index.html         # Displays the media library
│   └── play.html          # Plays a selected media file
├── tree.json              # Stores the media file tree and hashes
└── static/                # Static files (if any)
```

## Prerequisites

- Python 3.x
- Flask

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/techymaj/box-office.git
   cd box-office
   ```

2. Install dependencies:
   ```bash
   pip install flask
   ```

3. Ensure the `tree.json` file exists or will be generated dynamically by the app.

4. (Optional) Place your media files in the root directory or update the `MEDIA_FOLDER` configuration.

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Access the application in your browser:
   ```
   http://localhost:8080
   ```

3. For remote access, replace `localhost` with your server's IP.

## Endpoints

### 1. `/` or `/home`
Redirects to the library view.

### 2. `/library`
Displays a list of available media files with links to play them.

### 3. `/library/<hash>`
Streams the selected media file and provides its size and download link.

### 4. `/<path:filename>`
Serves media files directly for streaming or downloading.

## Example HTML

### `index.html`
Displays the media library:
```html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Box Office</title>
</head>
<body>
	{% for hash, filename in content.items() %}
	<a href="/library/{{hash}}">{{filename}}</a>
	{% endfor %}
</body>
</html>
```

### `play.html`
Streams and provides details for a selected media file:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Box Office | Now Playing</title>
</head>
<body>
    <h1>Now Playing</h1>
    <p>{{file_path}}</p>
    <p>Size: {{file_size}} bytes</p>
    <video controls width="1200">
        <source src="{{file_path}}" type="video/x-matroska" />
        <source src="{{file_path}}" type="video/mp4" />
        Download here:
        <a href="{{file_path}}">Click to download</a>
    </video>
</body>
</html>
```

## Configuration

### Media Folder
By default, the app assumes media files are in the root directory. Update the `MEDIA_FOLDER` configuration in `app.py` if your files are stored elsewhere:

```python
app.config['MEDIA_FOLDER'] = '/path/to/your/media/files'
```

### Supported Media Types
Update the HTML `<source>` tags in `play.html` to include additional video formats as needed.

## Error Handling

### Missing `tree.json`
If `tree.json` is missing, the app automatically calls `crawl()` to generate the file structure.

### File or Hash Not Found
- If a hash is not found, the app responds with `"No such hash found"` and a 404 status.
- If a file path is invalid, the app responds with a 404 error.

## Security Considerations
- **File Access**: Ensure `MEDIA_FOLDER` is restricted to trusted directories to avoid serving sensitive files.
- **Remote Access**: If exposing the app to the internet, consider using HTTPS and securing the server.

## Future Improvements
- Add authentication to restrict access to the library.
- Implement a search functionality for movies and series.
- Enhance error messages for better user experience.
- Use a database to store metadata and improve scalability.

---

This application provides a foundation for serving a media library and can be extended with additional features as needed.

Please, feel free to contribute.
