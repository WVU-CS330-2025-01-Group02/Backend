
# Backend

This repository contains the backend source code for a basic API that parses a CSV file of the walkability index and runs on a local Node.js server.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) installed on your machine.

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/WVU-CS330-2025-01-Group02/Backend.git
   cd Backend
   ```

2. Install the dependencies:

   ```sh
   npm install
   ```

### Running the Server

To start the server, run:

```sh
node server.js
```

The server will start on `http://localhost:5000`.

Simply drag and drop the downloaded index.html file on your browser and watch as it takes forever to load just the first 10 rows of Walkability index!!!

![Screenshot](https://github.com/WVU-CS330-2025-01-Group02/Backend/blob/chuck-practice-apibackend/Screenshot%202025-03-05%20144220.png)

### API Endpoints

- **GET /walkability**: Parses the CSV file and returns the walkability index data.

