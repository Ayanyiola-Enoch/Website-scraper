import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to get page content
def fetch_page_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[{url}] Failed to fetch page: {response.status_code}")
            return None
    except Exception as e:
        print(f"[{url}] Error fetching page: {e}")
        return None

# Function to extract practice areas
def extract_practice_areas(soup):
    keywords = ["Practice Areas", "Expertise", "Services", "Industries", "Our Work"]
    practice_areas = []

    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.text.strip()
        if any(keyword.lower() in text.lower() for keyword in keywords):
            practice_areas.append(text)

    for link in soup.find_all("a", href=True):
        text = link.text.strip()
        if any(keyword.lower() in text.lower() for keyword in keywords):
            practice_areas.append(text)

    return list(set(practice_areas))  # Remove duplicates

# Function to extract emails using regex
def extract_emails(text):
    # Regex pattern for most emails
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    found_emails = re.findall(email_pattern, text)
    return list(set(found_emails))  # Remove duplicates

# Function to extract data
def extract_data(html, url):
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()

    # Extract title of the page
    title = soup.title.string.strip() if soup.title else "No Title Found"

    # Extract practice areas
    practice_areas = extract_practice_areas(soup)

    # Extract emails
    emails = extract_emails(text)

    return {
        "URL": url,
        "Title": title,
        "Practice Areas": ", ".join(practice_areas) if practice_areas else "None Found",
        "Emails": ", ".join(emails) if emails else "None Found"
    }

# Function to scrape multiple URLs and save to file
def scrape_multiple_urls(url_list, filename="multi_scrape_results.xlsx"):
    results = []

    for url in url_list:
        print(f"Scraping: {url}")
        if not url.startswith("http"):
            url = "https://" + url

        html = fetch_page_content(url)
        if html:
            data = extract_data(html, url)
            results.append(data)

    df = pd.DataFrame(results)
    df.to_excel(filename, index=False)
    print(f"\n✅ Scraping completed and saved to '{filename}'")

# Main function
def main():
    print("Enter the URLs you want to scrape (one per line). Type 'done' when finished:\n")
    urls = []
    while True:
        url = input("URL: ").strip()
        if url.lower() == 'done':
            break
        urls.append(url)

    if urls:
        scrape_multiple_urls(urls)
    else:
        print("No URLs provided. Exiting.")

if __name__ == "__main__":
    main()






















# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import os
# import datetime
# import time
# import urllib.parse
# import re

# # Function to fetch page content
# def fetch_page_content(url):
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             return response.text
#         else:
#             print(f"Failed to fetch page: {response.status_code} - {url}")
#             return None
#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# # Function to extract emails from HTML content
# def extract_emails(html):
#     # Pattern to match email addresses
#     email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
#     # Find all matches in the HTML
#     emails = re.findall(email_pattern, html)
    
#     # Clean up and deduplicate emails
#     unique_emails = []
#     for email in emails:
#         # Clean up trailing periods or commas
#         clean_email = email.rstrip('.,')
#         # Validate email has proper format
#         if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', clean_email):
#             if clean_email not in unique_emails:
#                 unique_emails.append(clean_email)
    
#     return unique_emails

# # Function to identify practice area links
# def identify_practice_areas(soup, base_url):
#     keywords = ["Practice Areas", "Expertise", "Services", "Industries", "Our Work", "Areas of Practice"]
#     practice_area_links = []
    
#     # Look for sections/divs that might contain practice areas
#     for keyword in keywords:
#         # Check headings that might indicate practice area sections
#         for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
#             if keyword.lower() in tag.text.lower():
#                 # Look for links in the next siblings or parent container
#                 container = tag.parent
#                 for link in container.find_all("a", href=True):
#                     # Make sure it's not a main navigation item
#                     if link.text.strip() and len(link.text.strip()) > 3:
#                         full_url = make_absolute_url(link["href"], base_url)
#                         practice_area_links.append({
#                             "name": link.text.strip(),
#                             "url": full_url
#                         })
    
#     # Also check for direct links that might be practice areas
#     for link in soup.find_all("a", href=True):
#         link_text = link.text.strip()
#         # Check if link text contains practice-related terms
#         practice_terms = ["litigation", "corporate", "tax", "intellectual property", "employment", 
#                          "real estate", "immigration", "bankruptcy", "family law", "criminal", 
#                          "personal injury", "estate planning", "patent", "trademark", "copyright"]
        
#         if any(term in link_text.lower() for term in practice_terms) and len(link_text) > 3:
#             full_url = make_absolute_url(link["href"], base_url)
#             # Avoid duplicates
#             if not any(pa["url"] == full_url for pa in practice_area_links):
#                 practice_area_links.append({
#                     "name": link_text,
#                     "url": full_url
#                 })
    
#     # If we still don't have practice areas, look for anything that might be a practice area
#     if not practice_area_links:
#         for link in soup.find_all("a", href=True):
#             link_text = link.text.strip()
#             if link_text and len(link_text) > 3 and not link_text.lower() in ["home", "about", "contact", "search"]:
#                 href = link["href"]
#                 # Skip links that are likely not practice areas
#                 if not (href.startswith("tel:") or href.startswith("mailto:") or "facebook.com" in href or "twitter.com" in href):
#                     full_url = make_absolute_url(href, base_url)
#                     # Avoid duplicates and external links
#                     if base_url in full_url and not any(pa["url"] == full_url for pa in practice_area_links):
#                         practice_area_links.append({
#                             "name": link_text,
#                             "url": full_url
#                         })
    
#     # Return unique practice areas
#     return practice_area_links

# # Helper function to convert relative URLs to absolute
# def make_absolute_url(href, base_url):
#     if href.startswith("http"):
#         return href
#     return urllib.parse.urljoin(base_url, href)

# # Function to extract details from a practice area page
# def extract_practice_area_details(url):
#     html = fetch_page_content(url)
#     if not html:
#         return {
#             "title": "Failed to load", 
#             "content": "Could not fetch page content",
#             "emails": []
#         }
    
#     # Extract emails from the page
#     emails = extract_emails(html)
    
#     soup = BeautifulSoup(html, "lxml")
    
#     # Extract title - try h1 first, then fall back to page title
#     title = None
#     h1_tags = soup.find_all("h1")
#     if h1_tags:
#         title = h1_tags[0].text.strip()
#     else:
#         title = soup.title.text.strip() if soup.title else "No Title Found"
    
#     # Extract main content
#     content = []
    
#     # Look for main content containers
#     main_content = soup.find("main") or soup.find(id=["content", "main-content"]) or soup.find(class_=["content", "main-content"])
    
#     if main_content:
#         # Extract paragraphs from main content
#         for p in main_content.find_all("p"):
#             text = p.text.strip()
#             if text and len(text) > 20:  # Skip very short paragraphs
#                 content.append(text)
#     else:
#         # Fall back to all paragraphs
#         for p in soup.find_all("p"):
#             text = p.text.strip()
#             if text and len(text) > 20:  # Skip very short paragraphs
#                 content.append(text)
    
#     # If still no content, try to find any text
#     if not content:
#         for tag in soup.find_all(["div", "section", "article"]):
#             text = tag.text.strip()
#             if text and len(text) > 100:  # Only substantial text blocks
#                 content.append(text)
#                 break
    
#     return {
#         "title": title,
#         "content": "\n\n".join(content) if content else "No content found",
#         "emails": emails
#     }

# # Function to extract title, practice areas, and emails
# def extract_data(html, url):
#     soup = BeautifulSoup(html, "lxml")
    
#     # Extract page title
#     title = soup.title.text.strip() if soup.title else "No Title Found"
    
#     # Extract emails from main page
#     main_page_emails = extract_emails(html)
#     print(f"Found {len(main_page_emails)} emails on the main page")
    
#     # Identify practice area links
#     practice_areas = identify_practice_areas(soup, url)
#     print(f"Found {len(practice_areas)} potential practice areas")
    
#     # Extract details for each practice area
#     detailed_practice_areas = []
#     all_emails = set(main_page_emails)  # Start with main page emails
    
#     for i, practice_area in enumerate(practice_areas):
#         print(f"Processing ({i+1}/{len(practice_areas)}): {practice_area['name']}")
#         details = extract_practice_area_details(practice_area["url"])
        
#         # Add emails to the overall set
#         for email in details["emails"]:
#             all_emails.add(email)
            
#         detailed_practice_areas.append({
#             "name": practice_area["name"],
#             "url": practice_area["url"],
#             "title": details["title"],
#             "content": details["content"],
#             "emails": details["emails"]
#         })
        
#         # Sleep to avoid overloading the server
#         time.sleep(1)
    
#     return {
#         "title": title,
#         "practice_areas": detailed_practice_areas,
#         "all_emails": list(all_emails)
#     }

# # Function to save data to Excel with error handling
# def save_to_excel(data, filename=None):
#     # Create a timestamped filename to avoid conflicts
#     if filename is None:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         filename = f"practice_areas_detailed_{timestamp}.xlsx"
    
#     try:
#         # Prepare site info dataframe
#         site_info = pd.DataFrame({
#             "Site Title": [data["title"]],
#             "Number of Practice Areas": [len(data["practice_areas"])],
#             "Total Unique Emails Found": [len(data["all_emails"])]
#         })
        
#         # Prepare emails dataframe
#         emails_df = pd.DataFrame({"Email": data["all_emails"]})
        
#         # Prepare practice areas dataframe
#         practice_areas_data = []
#         for pa in data["practice_areas"]:
#             practice_areas_data.append({
#                 "Practice Area Name": pa["name"],
#                 "Practice Area URL": pa["url"],
#                 "Page Title": pa["title"],
#                 "Content": pa["content"],
#                 "Emails": ", ".join(pa["emails"]) if pa["emails"] else "None found"
#             })
        
#         df_practice_areas = pd.DataFrame(practice_areas_data)
        
#         # First attempt - try current directory
#         try:
#             with pd.ExcelWriter(filename) as writer:
#                 site_info.to_excel(writer, sheet_name="Site Info", index=False)
#                 emails_df.to_excel(writer, sheet_name="All Emails", index=False)
#                 df_practice_areas.to_excel(writer, sheet_name="Practice Areas", index=False)
#             print(f"Data saved to {filename}")
#             return True
#         except PermissionError:
#             print(f"Permission denied for {filename}. Trying documents folder...")
            
#             # Second attempt - try user's documents folder
#             documents_path = os.path.join(os.path.expanduser("~"), "Documents")
#             new_filename = os.path.join(documents_path, filename)
            
#             with pd.ExcelWriter(new_filename) as writer:
#                 site_info.to_excel(writer, sheet_name="Site Info", index=False)
#                 emails_df.to_excel(writer, sheet_name="All Emails", index=False)
#                 df_practice_areas.to_excel(writer, sheet_name="Practice Areas", index=False)
#             print(f"Data saved to {new_filename}")
#             return True
            
#     except Exception as e:
#         print(f"Error saving data: {e}")
        
#         # Fallback to CSV if Excel fails
#         try:
#             base_name = os.path.splitext(filename)[0]
            
#             # Save practice areas as CSV
#             practice_areas_csv = f"{base_name}_practice_areas.csv"
#             df_practice_areas = pd.DataFrame(practice_areas_data)
#             df_practice_areas.to_csv(practice_areas_csv, index=False)
            
#             # Save emails as CSV
#             emails_csv = f"{base_name}_emails.csv"
#             emails_df = pd.DataFrame({"Email": data["all_emails"]})
#             emails_df.to_csv(emails_csv, index=False)
            
#             print(f"Data saved to {practice_areas_csv} and {emails_csv} due to Excel error")
#             return True
#         except Exception as csv_err:
#             print(f"Failed to save even as CSV: {csv_err}")
#             return False

# # Function to also scrape the "Contact" page for additional emails
# def scrape_contact_page(base_url):
#     common_contact_paths = [
#         "/contact", "/contact-us", "/about/contact", "/contactus", 
#         "/contact-us.html", "/about/contact-us", "/contact.html",
#         "/firm/contact", "/firm/contact-us"
#     ]
    
#     emails = []
    
#     for path in common_contact_paths:
#         contact_url = make_absolute_url(path, base_url)
#         print(f"Trying to find contact page at: {contact_url}")
        
#         html = fetch_page_content(contact_url)
#         if html:
#             print(f"Contact page found at {contact_url}")
#             contact_emails = extract_emails(html)
#             emails.extend(contact_emails)
#             break  # Stop after finding a working contact page
    
#     return list(set(emails))  # Return deduplicated emails

# # Main function
# def main():
#     url = input("Enter the website URL to scrape: ").strip()
    
#     if not url.startswith("http"):
#         url = "https://" + url  # Ensure proper format
    
#     print(f"Fetching main page: {url}")
#     html = fetch_page_content(url)
    
#     if html:
#         # Try to find and scrape contact page for emails too
#         contact_emails = scrape_contact_page(url)
#         if contact_emails:
#             print(f"Found {len(contact_emails)} emails on contact page")
        
#         print("Extracting practice areas and details...")
#         data = extract_data(html, url)
        
#         # Add contact page emails to the overall email list
#         data["all_emails"] = list(set(data["all_emails"] + contact_emails))
        
#         if data["practice_areas"]:
#             if save_to_excel(data):
#                 print(f"Scraping completed successfully!")
#                 print(f"Found {len(data['practice_areas'])} practice areas")
#                 print(f"Found {len(data['all_emails'])} unique email addresses")
#             else:
#                 print("Scraping completed but there were issues saving the data.")
#         else:
#             print("No practice areas found on this website.")
            
#             # Save just the emails even if no practice areas found
#             if data["all_emails"]:
#                 emails_df = pd.DataFrame({"Email": data["all_emails"]})
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 emails_df.to_csv(f"emails_{timestamp}.csv", index=False)
#                 print(f"Found {len(data['all_emails'])} emails saved to emails_{timestamp}.csv")
#     else:
#         print("Failed to fetch the website. Please check the URL and try again.")

# if __name__ == "__main__":
#     main()