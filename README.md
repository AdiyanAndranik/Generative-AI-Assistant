# Generative-AI-Assistant

This project provides a FastAPI application for managing and analyzing venture capital (VC) firms data.

## Features

- **Add VC Data**: Add a VC firm's data to the application by providing its URL.
- **Extract Information**: Extract key information from a VC firm's website, such as the firm name, contacts, investment industries, and investment rounds.
- **Find Similar Firms**: Find the top three most similar VC firms to a given firm based on semantic similarity analysis.

## API Endpoints

- **POST `/add_vc/`**: Add a VC firm's data to the application by providing a JSON payload with the key `url`. Example:

    ```json
    {
        "url": "http://www.example.com/"
    }
    ```

- **GET `/extract_info/`**: Extract key information from a VC firm's website by providing its URL as a query parameter. Example:

    ```
    GET /extract_info/?url=http://www.example.com/
    ```

- **GET `/find_similar/`**: Find the top three most similar VC firms to a given firm by providing its URL as a query parameter. Example:

    ```
    GET /find_similar/?url=http://www.example.com/
    ```

The examples provided for each endpoint demonstrate how to interact with the API using the specified URL and parameters.
