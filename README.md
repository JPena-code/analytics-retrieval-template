<div align="center">
    <h1 style="font-size: 64px">FastAnalytics</h1>
    <p style="font-style: italic">
        <strong>Fast</strong>, easy and ready to go API to handle and capture analytics for your end API
    </p>
    <img src="https://img.shields.io/github/actions/workflow/status/JPena-code/analytics-retrieval-template/ci.yml?branch=main" alt="Build Status">
    <img src="https://img.shields.io/github/license/JPena-code/analytics-retrieval-template" alt="License">
    <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python Version">
    <img src="https://img.shields.io/badge/docker-supported-blue" alt="Docker">
    <img src="https://img.shields.io/codecov/c/github/JPena-code/analytics-retrieval-template" alt="Coverage">
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen" alt="Contributions">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="Pre-commit">
</div>

---

## Table of Contents

<details>
<summary>Click to expand</summary>

- [Table of Contents](#table-of-contents)
- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Base URL](#base-url)
  - [Example Endpoints](#example-endpoints)
    - [Retrieve Events](#retrieve-events)
    - [Add Event](#add-event)
- [Examples](#examples)
  - [Python Client Example](#python-client-example)
- [Future Tasks](#future-tasks)
- [Contributing](#contributing)
- [License](#license)

</details>

---

## Overview

The `FasAnalytics` project is a robust Analytics API designed for efficient information retrieval. Built with FastAPI, it leverages TimescaleDB for managing time-series data. The modular architecture ensures scalability and maintainability.

This project was inspired by the concepts and techniques demonstrated in [this video](https://www.youtube.com/watch?v=tiBeLLv5GJo&t=9420s) by **jmitchel3**. The video provided valuable insights into building scalable and efficient APIs, which greatly influenced the design and implementation of this project. Full credit goes to the author for their excellent content and inspiration.

---

## Features

- **FastAPI Backend**: High-performance Python web framework.
- **TimescaleDB Integration**: Optimized for time-series data.
- **Modular Design**: Easy to extend and maintain.
- **Pre-commit Hooks**: Ensures code quality and consistency.

---

## Getting Started

### Prerequisites

- Docker
- Python 3.10+
- TimescaleDB

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/JPena-code/analytics-retrieval-template.git
   cd analytics-retrieval-template
   ```

2. Build the Docker container:

   ```bash
   docker build -t analytics-retrieval .
   ```

3. Run the setup script:

   ```bash
   ./scripts/setup.sh
   ```

4. Start the application:

   ```bash
   ./scripts/entrypoint.sh
   ```

---

## API Endpoints

### Base URL

```text
http://localhost:8000/api/{version}/events
```

### Example Endpoints

#### Retrieve Events

- **GET** `/events`
  - Description: Fetch a list of events.
  - Response:

    ```json
    {
      "data": [
        {
          "id": 1,
          "path": "/dummy/path",
          "agent": "dummy-agent",
          "ip_address": "127.0.0.1",
          "session_id": "dummy-session"
        },
        {
          "id": 2,
          "path": "/dummy/path/2",
          "agent": "dummy-agent-2",
          "ip_address": "172.0.0.1",
          "session_id": "dummy-session-2"
        }
      ]
    }
    ```

#### Add Event

- **POST** `/events`
  - Description: Add a new event.
  - Request Body:

    ```json
    {
      "path": "/new/path",
      "agent": "new-agent",
      "ip_address": "192.168.0.1",
      "session_id": "new-session"
    }
    ```

  - Response:

    ```json
    {
      "data": {
        "id": 3,
        "path": "/new/path",
        "agent": "new-agent",
        "ip_address": "192.168.0.1",
        "session_id": "new-session"
      }
    }
    ```

---

## Examples

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000/api/{version}"

# Fetch events
response = requests.get(f"{BASE_URL}/events")
print(response.json())

# Add an event
data = {
    "path": "/new/path",
    "agent": "new-agent",
    "ip_address": "192.168.0.1",
    "session_id": "new-session"
}
response = requests.post(f"{BASE_URL}/events", json=data)
print(response.json())
```

---

## Future Tasks

- **Authentication**: Implement OAuth2 for secure access.
- **Pagination**: Add pagination for large datasets.
- **GraphQL Support**: Explore GraphQL for flexible queries.
- **CI/CD Integration**: Automate testing and deployment.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your message here"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
