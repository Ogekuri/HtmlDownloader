#!/usr/bin/env python3
"""CLI tool for downloading HTML pages."""

import argparse
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def download_html(url: str, output_dir: Path) -> None:
    """
    Download HTML content from a URL and save it to a directory.
    
    Args:
        url: The URL to download from
        output_dir: The directory to save the HTML file
    """
    try:
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Download the HTML content
        print(f"Downloading from {url}...")
        with urlopen(url) as response:
            html_content = response.read()
        
        # Extract filename from URL or use default
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        path = parsed_url.path.rstrip('/')
        
        if path and path != '/':
            filename = path.split('/')[-1]
        else:
            filename = ""
        
        # If no filename or filename has no extension, use index.html
        if not filename:
            filename = "index.html"
        elif '.' not in filename:
            # Filename without extension, append .html
            filename = f"{filename}.html"
        elif not filename.endswith(('.html', '.htm')):
            # Has an extension but not .html/.htm, keep as is
            pass
        
        # Save to file
        output_path = output_dir / filename
        with open(output_path, 'wb') as f:
            f.write(html_content)
        
        print(f"Successfully saved to {output_path}")
        
    except HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Download HTML pages from a URL to a specified directory"
    )
    parser.add_argument(
        "--from-url",
        required=True,
        help="URL of the web page to download"
    )
    parser.add_argument(
        "--to-dir",
        required=True,
        help="Directory where the HTML file will be saved"
    )
    
    args = parser.parse_args()
    
    url = args.from_url
    output_dir = Path(args.to_dir)
    
    download_html(url, output_dir)


if __name__ == "__main__":
    main()
