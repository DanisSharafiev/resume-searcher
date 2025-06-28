# Resume Searcher Frontend

A simple frontend for a resume search service.

## Features

- 🔍 Search for candidates by keywords
- 📋 Display results as cards (name + position)
- 📄 Expanded resume view with LLM analysis
- 📱 Responsive design
- ⚡ Fast loading, no frameworks

## File structure

```
frontend/
├── index.html      # Main HTML page
├── styles.css      # Styles
├── script.js       # JavaScript logic
└── README.md       # This file
```

## How to run

### Option 1: Simple HTTP server (Python)

```bash
cd frontend
python -m http.server 8080
```

Open your browser and go to http://localhost:8080

### Option 2: Simple HTTP server (Node.js)

```bash
cd frontend
npx http-server -p 8080
```

### Option 3: Live Server (VS Code)

1. Install the "Live Server" extension in VS Code
2. Open `index.html`
3. Right-click → "Open with Live Server"

## API configuration

By default, the frontend expects the backend at `http://localhost:8000`.

To change the address, edit the `API_CONFIG.baseUrl` variable in `script.js`:

```javascript
const API_CONFIG = {
    baseUrl: 'http://your-backend-url',
    endpoints: {
        search: '/search',
        resume: '/resume'
    }
};
```

## API Endpoints

The frontend expects the following endpoints:

### POST /search
Search for candidates by query

**Request:**
```json
{
    "query": "keywords for search"
}
```

**Response:**
```json
[
    {
        "id": 123,
        "name": "Ivan Ivanov",
        "position": "Data Scientist"
    }
]
```

### GET /resume/{id}
Get detailed information about a candidate

**Response:**
```json
{
    "llm_response_markdown": "# Candidate analysis\n\n**Experience:** ...",
    "resume_plain": "Full resume text..."
}
```

## Technical details

- **Markdown rendering:** Uses `marked.js` to display LLM responses
- **No frameworks:** Pure HTML/CSS/JavaScript
- **Responsive:** Optimized for desktop, works on tablets
- **Error handling:** Shows clear error messages
- **UX:** Loading indicators, smooth animations, keyboard shortcuts

## Keyboard shortcuts

- **Enter** in the search field → start search
- **Escape** → close expanded resume

## Browser support

Works in all modern browsers:
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+
