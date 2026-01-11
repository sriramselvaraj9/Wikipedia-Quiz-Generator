import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re

def scrape_wikipedia(url: str) -> Optional[Dict]:
    """
    Scrape content from a Wikipedia article
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Dictionary containing scraped data or None if failed
    """
    try:
        # Validate URL
        if not url.startswith("https://en.wikipedia.org/wiki/"):
            return None
        
        # Send request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_element = soup.find('h1', {'id': 'firstHeading'})
        title = title_element.text.strip() if title_element else "Unknown Title"
        
        # Extract main content
        content_div = soup.find('div', {'id': 'mw-content-text'})
        if not content_div:
            return None
        
        # Remove unwanted elements
        for element in content_div.find_all(['table', 'sup', 'span', 'div'], 
                                           class_=['infobox', 'reference', 'reflist', 'navbox']):
            element.decompose()
        
        # Extract paragraphs
        paragraphs = content_div.find_all('p')
        content_text = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # Extract sections
        sections = []
        for heading in soup.find_all(['h2', 'h3']):
            headline = heading.find('span', {'class': 'mw-headline'})
            if headline:
                section_title = headline.get_text().strip()
                # Skip common metadata sections
                if section_title not in ['References', 'External links', 'See also', 'Notes', 'Bibliography']:
                    sections.append(section_title)
        
        # Extract first few paragraphs as summary
        summary_paragraphs = [p.get_text().strip() for p in paragraphs[:3] if p.get_text().strip()]
        summary = ' '.join(summary_paragraphs)[:500] + '...' if summary_paragraphs else ""
        
        # Clean content
        content_text = re.sub(r'\[\d+\]', '', content_text)  # Remove citation numbers
        content_text = re.sub(r'\s+', ' ', content_text)  # Normalize whitespace
        
        return {
            "title": title,
            "content": content_text[:15000],  # Limit content length for LLM
            "sections": sections[:15],  # Limit sections
            "summary": summary,
            "raw_html": str(soup)[:50000]  # Store limited raw HTML
        }
        
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
        return None

def validate_wikipedia_url(url: str) -> bool:
    """
    Validate if the URL is a valid Wikipedia article URL
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^https?://[a-z]{2,3}\.wikipedia\.org/wiki/.+$'
    return bool(re.match(pattern, url))

def extract_article_title_from_url(url: str) -> str:
    """
    Extract article title from Wikipedia URL
    
    Args:
        url: Wikipedia URL
        
    Returns:
        Article title
    """
    if validate_wikipedia_url(url):
        # Extract title from URL
        title = url.split('/wiki/')[-1]
        # Replace underscores with spaces and decode URL encoding
        title = title.replace('_', ' ')
        return title
    return ""
