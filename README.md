# Baby API Script

## Overview
The Baby API script is a Python-based tool designed to simplify interactions with APIs. It allows you to perform GET, POST, PUT, and DELETE requests, manage API endpoints, and include custom headers and JSON payloads easily.

---

## Features
- Add and manage endpoints interactively.
- Support for headers such as `Authorization`, `Content-Type`, etc.
- Easily send JSON data with POST/PUT requests.
- Switch between base URLs seamlessly.

---

## Requirements
- **Python 3**: Ensure Python 3 is installed and accessible on your system.

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/0xmuka/baby-api.git
   ```
2. Navigate to the project directory:
   ```bash
   cd baby-api
   ```
3. Make the script executable:
   ```bash
   chmod +x baby-api.py
   ```
4. Move it to a directory in your system's PATH for global access:
   ```bash
   sudo mv baby-api.py /usr/local/bin/baby-api
   ```

---

## Usage
Run the script directly from your terminal:
```bash
baby-api
```

### Interactive Features:
1. **Set Base URL**: Start by specifying the base URL for your API.
2. **Add Endpoints**: Define API endpoints interactively with their respective methods.
3. **Send Requests**: Choose the HTTP method (GET/POST/PUT/DELETE) and include headers or JSON payloads as needed.

---

## Example
1. Start the script:
   ```bash
   baby-api
   ```
2. Enter the base URL:
   ```
   Enter the base URL [http://localhost:8000]:
   ```
3. Define an API endpoint:
   ```
   Enter endpoint: /api/v1/resource
   Select method [GET/POST/PUT/DELETE]: POST
   ```
4. Include headers and payload if required, and send the request.

---

## File Management
The script automatically handles required files:
- **`endpoints.json`**: Stores your defined API endpoints.
- **`README.md`**: Describes the script's functionality and usage.

If these files are missing, the script will create them during the initial run.

---

## Notes
- Ensure your `endpoints.json` file is located in the same directory as the script, or the script will create a new one.
- To update or customize the base URL, you can enter a new URL interactively at runtime.
- For troubleshooting or contributions, refer to the repository.

---

## Contributing
Feel free to fork the repository, make changes, and submit pull requests! Contributions to improve the script or add new features are always welcome.


