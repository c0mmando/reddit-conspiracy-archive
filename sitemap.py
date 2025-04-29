#!/usr/bin/env python3
import os
import re
import sys
import argparse
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom

# Regular expression to extract creationDate value from an HTML comment (if needed)
# Example comment: 'creationDate' => '2014-06-19 19:20:00'
creation_date_regex = re.compile(r"'creationDate'\s*=>\s*'([^']+)'", re.IGNORECASE)

# Regular expression to extract a date from the HTML content.
# For example, in HTML: ... 1061 2017-06-12 by ... we look for the YYYY-MM-DD format.
content_date_regex = re.compile(r"(\d{4}-\d{2}-\d{2})\s+by", re.IGNORECASE)

# Maximum URLs per sitemap file.
MAX_URLS_PER_SITEMAP = 1000

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate SEO optimized sitemap(s) and sitemap index for an offline HTML site."
    )
    parser.add_argument("directory", help="Root directory to scan for HTML files")
    parser.add_argument("domain", help="Root domain URL (e.g., https://example.com)")
    parser.add_argument("--max-url", type=int, default=MAX_URLS_PER_SITEMAP,
                        help="Maximum number of URLs per sitemap file (default: 1000)")
    parser.add_argument("--output", default="sitemaps",
                        help="Output directory for sitemap files (default: sitemaps)")
    args = parser.parse_args()
    return args

def prettify_xml(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def extract_creation_date(file_path):
    """
    Look for an HTML comment that includes a "creationDate" value.
    If found, returns it as an ISO timestamp (without microseconds).
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            match = creation_date_regex.search(content)
            if match:
                date_str = match.group(1)
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    return dt.replace(microsecond=0).isoformat()
                except ValueError:
                    return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def extract_date_from_content(file_path):
    """
    Parse the file content and try to extract a date in the form YYYY-MM-DD
    (for example, found in text like "1061 2017-06-12 by").
    If found, returns the date as an ISO timestamp (with time set to 00:00:00).
    Otherwise, returns None.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            match = content_date_regex.search(content)
            if match:
                date_str = match.group(1)
                try:
                    dt = datetime.strptime(date_str, "%Y-%m-%d")
                    return dt.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
                except ValueError:
                    return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return None

def get_file_last_modified(file_path):
    """Return file modified time in ISO format without microseconds."""
    t = os.path.getmtime(file_path)
    dt = datetime.fromtimestamp(t)
    return dt.replace(microsecond=0).isoformat()

def generate_url(root_directory, file_path, domain):
    """Generates the URL for a given file by preserving its relative posix path."""
    rel_path = os.path.relpath(file_path, root_directory)
    # Convert Windows backslashes to URL forward slashes.
    rel_url = rel_path.replace(os.sep, '/')
    # Ensure domain does not end with a slash.
    if domain.endswith('/'):
        domain = domain[:-1]
    return f"{domain}/{rel_url}"

def generate_sitemap(url_entries, filename):
    """
    Generates a sitemap XML file with the given url_entries.
    Each entry is a dictionary with keys: loc and lastmod.
    """
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for entry in url_entries:
        url_elem = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = entry["loc"]
        if entry.get("lastmod"):
            lastmod = ET.SubElement(url_elem, "lastmod")
            lastmod.text = entry["lastmod"]
    xml_str = prettify_xml(urlset)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_str)

def generate_sitemap_index(sitemap_filenames, domain, output_dir):
    """
    Generates a sitemap index XML file listing all sitemap filenames.
    """
    sitemapindex = ET.Element("sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for sitemap in sitemap_filenames:
        sm_elem = ET.SubElement(sitemapindex, "sitemap")
        loc = ET.SubElement(sm_elem, "loc")
        loc.text = f"{domain.rstrip('/')}/{output_dir.rstrip('/')}/{sitemap}"
        lastmod = ET.SubElement(sm_elem, "lastmod")
        lastmod.text = datetime.now().replace(microsecond=0).isoformat()
    xml_str = prettify_xml(sitemapindex)
    index_file = os.path.join(output_dir, "sitemap_index.xml")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(xml_str)
    return index_file

def main():
    args = parse_args()
    root_directory = args.directory
    domain = args.domain
    max_url = args.max_url
    output_dir = args.output

    os.makedirs(output_dir, exist_ok=True)

    url_entries = []
    total_files = 0

    # Walk the directory and scan for .html files.
    for subdir, dirs, files in os.walk(root_directory):
        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(subdir, file)
                url = generate_url(root_directory, file_path, domain)
                # Check if the url contains "/user/" (case-insensitive).
                if "/user/" in url.lower():
                    continue

                # File passes, so process it.
                total_files += 1
                entry = {"loc": url}
                file_lower = file.lower()

                # If the file name starts with "index", use current timestamp.
                if file_lower.startswith("index"):
                    entry["lastmod"] = datetime.now().replace(microsecond=0).isoformat()
                else:
                    # First try to extract the date from the content.
                    content_date = extract_date_from_content(file_path)
                    if content_date:
                        entry["lastmod"] = content_date
                    else:
                        # Then try to extract a creationDate comment.
                        creation = extract_creation_date(file_path)
                        if creation:
                            entry["lastmod"] = creation
                        else:
                            # Fallback to file's last modified time.
                            entry["lastmod"] = get_file_last_modified(file_path)
                url_entries.append(entry)

    # Write out sitemap files.
    sitemap_filenames = []
    total_urls = len(url_entries)
    num_sitemaps = (total_urls // max_url) + (1 if total_urls % max_url != 0 else 0)

    for i in range(num_sitemaps):
        start = i * max_url
        end = start + max_url
        sitemap_entries = url_entries[start:end]
        sitemap_filename = f"sitemap_{i+1}.xml"
        sitemap_full_path = os.path.join(output_dir, sitemap_filename)
        generate_sitemap(sitemap_entries, sitemap_full_path)
        sitemap_filenames.append(sitemap_filename)

    # Generate sitemap index file.
    sitemap_index_file = generate_sitemap_index(sitemap_filenames, domain, output_dir)

    # Summary report.
    print("Sitemap Generation Summary:")
    print(f"Total HTML files scanned (after filtering): {total_files}")
    print(f"Total URLs added to sitemaps: {total_urls}")
    print(f"Number of sitemap files generated: {num_sitemaps}")
    print(f"Sitemap index file created at: {sitemap_index_file}")

if __name__ == "__main__":
    main()
