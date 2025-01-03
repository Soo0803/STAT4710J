

import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.

    """
    # Don't change this function body!
    # No python required; create the HTML file.

    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------




def extract_book_links(text):
    # GPT is used to learn how to use beautiful soup
    """
    :Example:
    >>> fp = os.path.join('data', 'products.html')
    >>> out = extract_book_links(open(fp, encoding='utf-8').read())
    >>> url = 'scarlet-the-lunar-chronicles-2_218/index.html'
    >>> out[1] == url
    True
    """
    soup = bs4.BeautifulSoup(text, 'lxml')
    book_links = [] # create list to store the books

    # GPT is used to learn findall()
    books = soup.find_all('article', class_='product_pod')

    for book in books:
        # get books rating
        rating = book.find('p', class_='star-rating')['class'][1]  # Star rating is the second class (e.g., 'Four', 'Five')
        if rating not in ['Four', 'Five']: 
            # Gpt is used to learn not in syntax
            # Remove books with less than 4 star rating
            continue  
        
        # Get book price
        price_str = book.find('p', class_='price_color').text.replace('£', '').strip() #gpt is use to learn how to remove euro dollar sign symbols
        print("price in str ", price_str)
        price = float(price_str)
        
        if price < 50:
            # Get book url that has price lesser than 50
            link = book.find('h3').find('a')['href'] # gpt is used to learn how to get the URL
            full_link = link  # Convert to a full URL 
            book_links.append(full_link)
        
    # print(book_links)
    return book_links


def get_product_info(text, categories):
    """
    :Example:
    >>> fp = os.path.join('data', 'Frankenstein.html')
    >>> out = get_product_info(open(fp, encoding='utf-8').read(), ['Default'])
    >>> isinstance(out, dict)
    True
    >>> 'Category' in out.keys()
    True
    >>> out['Rating']
    'Two'
    """
    soup = bs4.BeautifulSoup(text, 'lxml')

    # Extract the category of the book
    # GPT is used to learn soup.find()
    breadcrumb = soup.find('ul', class_='breadcrumb')
    book_category = breadcrumb.find_all('li')[2].get_text(strip=True)
    
    # Check if the book's category is in the specified list
    if book_category not in categories:
        return None
    
    # Extract the category of the book
    breadcrumb = soup.find('ul', class_='breadcrumb')
    book_category = breadcrumb.find_all('li')[2].get_text(strip=True)
    
    # Check if book category is in the specified list
    if book_category not in categories:
        # return empty dict if it's not in specifies list
        return None
    
    # Extract the title of the book
    title = soup.find('h1').get_text(strip=True)
    
    # Extract the star rating
    star_rating = soup.find('p', class_='star-rating')['class'][1]
    
    # Extract product information from the table
    product_info = {}
    table_rows = soup.find('table', class_='table table-striped').find_all('tr')
    for row in table_rows:
        # GPT is used to learn .get_text()
        key = row.find('th').get_text(strip=True)
        value = row.find('td').get_text(strip=True)
        product_info[key] = value
    
    # Create dictionary with the extracted information
    book_data = {
        'UPC': product_info.get('UPC', ''),
        'Product Type': product_info.get('Product Type', 'Books'),
        'Price (excl. tax)': product_info.get('Price (excl. tax)', ''),
        'Price (incl. tax)': product_info.get('Price (incl. tax)', ''),
        'Tax': product_info.get('Tax', ''),
        'Availability': soup.find('p', class_='instock availability').get_text(strip=True),
        'Number of reviews': 0,  
        'Category': book_category,
        'Rating': star_rating,
        # GPT is used to learn how to get description and attrs={}
        'Description': soup.find('meta', attrs={'name': 'description'})['content'].strip() if soup.find('meta', attrs={'name': 'description'}) else "No description available.",
        'Title': title
    }  
    
    # print(book_data)
    return book_data


def scrape_books(k, categories):
    """
    :param k: number of book-listing pages to scrape.
    :returns: a dataframe of information on (certain) books
    on the k pages (as described in the question).
    :Example:
    >>> out = scrape_books(1, ['Mystery'])
    >>> out.shape
    (1, 11)
    >>> out['Rating'][0] == 'Four'
    True
    >>> out['Title'][0] == 'Sharp Objects'
    True
    """
    base_url = 'http://books.toscrape.com/catalogue/page-{}.html' #GPT is used to learn how to use {} syntax
    all_books = []

    for page_num in range(1, k + 1):
        # Get the page URL
        # GPT is used to learn about format()
        page_url = base_url.format(page_num)
        response = requests.get(page_url)
        response.encoding = 'utf-8'
        
        # Get book links from the page that meet rating and price requirement
        book_links = extract_book_links(response.text)
        
        # Get the book-specific page and extract details of each book link
        for book_link in book_links:
            book_response = requests.get('http://books.toscrape.com/catalogue/' + book_link)
            
            # Get book information if it matches the specified categories
            book_info = get_product_info(book_response.text, categories)
            if book_info:
                all_books.append(book_info)
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(all_books)
    return df



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def stock_history(ticker, year, month):
    """
    Given a stock code and month, return the stock price details for that month
    as a DataFrame.

    >>> history = stock_history('BYND', 2019, 6)
    >>> history.shape == (20, 13)
    True
    >>> history.label.iloc[-1]
    'June 03, 19'
    """
    formatted_month = str(month).zfill(2)

    api_key = 'apikey=xhoIAXRM5n3ga6ozygtcFQAcqcaSdqbU' 
    
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={year}-{formatted_month}-01&{api_key}'

    # Make request to the API
    response = requests.get(url)
    
    data = response.json()

    # Extract historical price data
    historical_data = data['historical']

    df = pd.json_normalize(historical_data)
    df['date'] = pd.to_datetime(df['date'])

    # Filter data based on year and month
    filtered_df = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]

    return filtered_df.reset_index(drop=True)



def stock_stats(history):
    """
    Given a stock's trade history, return the percent change and transactions
    in billions of dollars.

    >>> history = stock_history('BYND', 2019, 6)
    >>> stats = stock_stats(history)
    >>> len(stats[0]), len(stats[1])
    (7, 6)
    >>> float(stats[0][1:-1]) > 30
    True
    >>> float(stats[1][:-1]) > 1
    True
    >>> stats[1][-1] == 'B'
    True
    """

    #Calculate percent change
    starting_price = history.iloc[0]['open']  # Opening price from first day of the month
    ending_price = history.iloc[-1]['close']  # Closing price from last day of the month
    percent_change = ((ending_price - starting_price) / starting_price) * 100
    
    # Format percent change as a string with a + or - sign
    percent_change_str = f"{percent_change:+.2f}%"

    # Calculate total transaction volume
    #GPT is used to learn about for loop with iterrows()
    total_volume = 0
    for _, row in history.iterrows():
        avg_price = (row['high'] + row['low']) / 2  # Midpoint of high and low prices
        daily_volume = row['volume'] * avg_price  # Volume in dollars for the day
        total_volume += daily_volume

    # Convert volume to billions and add 'B' 
    total_volume_billion = total_volume / 1e9
    total_volume_str = f"{total_volume_billion:.2f}B"

    return percent_change_str, total_volume_str



