# Meeting Notes to Google Docs Converter

A Python tool that converts Markdown meeting notes into formatted Google Docs using the Google Docs API. Designed to run in Google Colab.

## Features

*   **Smart Formatting**: Converts Markdown headers (#, ##, ###) to Google Docs Heading styles.
*   **Lists**: Handles bullet points and nested indentation.
*   **Checkboxes**: Converts `- [ ]` task lists into Google Docs checkboxes.
*   **Rich Text**: Detects and styles user mentions (`@name`) with bold/color.
*   **Metadata**: Special styling for footer information (Recorder, Duration).

## Setup Instructions

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/product-team-sync-converter
    cd product-team-sync-converter
    ```

2.  **Open in Google Colab**:
    *   Upload the `meeting_converter.ipynb` notebook to Google Colab.
    *   Or open the notebook directly from GitHub if you push it there.

3.  **Upload Meeting Notes**:
    *   Ensure `meeting_notes.md` is in the Colab file system (upload it to the content folder).

## Required Dependencies

*   `google-auth`
*   `google-auth-oauthlib`
*   `google-api-python-client`

(These are installed automatically by the notebook).

## How to Run

1.  Open `meeting_converter.ipynb` in Google Colab.
2.  Run the first cell to install dependencies.
3.  Run the subsequent cells.
4.  When prompted, authenticate with your Google account to allow the script to create documents.
5.  The script will read `meeting_notes.md`, create a new Google Doc, and print the link.