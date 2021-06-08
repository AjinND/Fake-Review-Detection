#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
 
#headers = {
#  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
#}
#url = 'https://www.amazon.in/Samsung-Galaxy-Storage-Additional-Exchange/product-reviews/B08VB2KYDB/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
def get_data(url,headers):
  response = requests.get(url,headers=headers)
  print(response)
  soup = bs(response.content,'lxml')
  return soup

def get_reviwer_id(soup):
  profile_id=[]
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  profiles = reviews_section.find_all('div',{'data-hook':"genome-widget"})
  for profile in range(len(profiles)):
    profile_id.append(profiles[profile].find('a')['href'])
  profile_id[:] = [id.lstrip('/gp/profile/amzn1.account.') for id in profile_id]
  profile_id[:] = [id.rstrip('/ref=cm_cr_arp_d_gw_btm?ie=UTF8') for id in profile_id]
  return profile_id

def get_names(soup):
  cust_names = []
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  names = reviews_section.find_all('span',class_='a-profile-name')
  for i in range(len(names)):
    cust_names.append(names[i].get_text())
  return cust_names

def get_titles(soup):
  review_title = []
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  title = reviews_section.find_all('a',class_='review-title-content')
  for i in range(len(title)):
    review_title.append(title[i].get_text())
  review_title[:] = [titles.lstrip('\n') for titles in review_title]
  review_title[:] = [titles.rstrip('\n') for titles in review_title]
  return review_title
 
def get_ratings(soup):
  review_rating = []
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  rating = reviews_section.find_all('i',{"data-hook":'review-star-rating'})
  for i in range(len(rating)):
    review_rating.append(rating[i].get_text())
  review_rating[:] = [values.rstrip(' out of 5 stars') for values in review_rating]
  return review_rating

def get_review_body(soup):
  review_content = []
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  review = reviews_section.find_all("span",{"data-hook":"review-body"})
  for i in range(len(review)):
      review_content.append(review[i].get_text())
  review_content[:] = [reviews.lstrip('\n') for reviews in review_content]
  review_content[:] = [reviews.lstrip(' ') for reviews in review_content]
  review_content[:] = [reviews.rstrip('\n') for reviews in review_content]
  return review_content

def get_review_date(soup):
  review_date=[]
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  date = reviews_section.find_all("span",{'data-hook':"review-date"})
  for i in range(len(date)):
    review_date.append(date[i].get_text())
  review_date[:] = [texts.lstrip('Reviewed in India on ') for texts in review_date]
  return review_date

def get_verified_purchase(soup):
  verified_purchase=[]
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  purchase = reviews_section.find_all('div',class_='a-row a-spacing-mini review-data review-format-strip')
  for i in range(len(purchase)):
    status = purchase[i].find("span",{'data-hook':'avp-badge'})
    if(status):
      verified_purchase.append('1')
    else:
      verified_purchase.append('0')
  return verified_purchase

def get_review_helpful(soup):
  helpful_votes=[]
  reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
  #print(reviews_section)
  helpful = reviews_section.find_all('div',class_='a-row a-expander-container a-expander-inline-container cr-vote-action-bar') 
  #print(len(helpful))
  for i in range(len(helpful)):
    value = helpful[i].find('span',{'data-hook':"helpful-vote-statement"})
    if(value):
      helpful_votes.append(value.get_text())
    else:
      helpful_votes.append('0')
  helpful_votes[:] = [values.rstrip(' people found this helpful') for values in helpful_votes]
  return helpful_votes

def get_next_page(soup):
  page = soup.find('ul',class_='a-pagination')
  #print(page.find('li',class_='a-disabled a-last'))
  #print(page.find('li',class_='a-last'))
  if not page.find('li',class_='a-disabled a-last'):
    url = 'https://www.amazon.in' + str(page.find('li',class_='a-last').find('a')['href'])
    return url
  else:
    return

def collection(url, headers):
    reviewer_profile_list = []
    review_names_list = [] 
    review_title_list = []
    review_ratings_list = []
    review_body_list = []
    review_date_list = []
    review_verified_list = []
    review_helpful_list = []

    while(True):

      soup = get_data(url,headers)
      #reviews_section = soup.find('div',class_='a-section a-spacing-none reviews-content a-size-base')
      print(url)

      ids = get_reviwer_id(soup)
      for profile_id in ids:
        reviewer_profile_list.append(profile_id) 

      names = get_names(soup)
      #print(names)
      for name in names:
        review_names_list.append(name)

      titles = get_titles(soup)
      for title in titles:
        review_title_list.append(title)

      ratings = get_ratings(soup)
      for rating in ratings:
        review_ratings_list.append(rating)

      contents = get_review_body(soup)
      for content in contents:
        review_body_list.append(content)

      dates = get_review_date(soup)
      for date in dates:
        review_date_list.append(date)

      verified_purchase = get_verified_purchase(soup)
      for purchase in verified_purchase:
        review_verified_list.append(purchase)

      helpful = get_review_helpful(soup)
      for votes in helpful:
        review_helpful_list.append(votes)

      url = get_next_page(soup)

      if not url:
        break

    product = soup.find('div',class_="a-row product-title")
    product_name = product.get_text()


    df=pd.DataFrame()
    df['Customer ID'] = reviewer_profile_list
    df['Product Name'] = product_name
    df['Customer Name'] = review_names_list
    df['Review Titles'] = review_title_list
    df['Ratings'] = review_ratings_list
    df['Review Body'] = review_body_list
    df['Review Date'] = review_date_list
    df['Purchase Status'] = review_verified_list
    df['Helpful Votes'] = review_helpful_list

    '''
    print("========================")
    print(" If any Values are Null")
    print("========================")
    print(df.isnull().values.any())

    print("====================================")
    print(" Count of Values in Purchase Status")
    print("=====================================")
    print(df['Purchase Status'].value_counts())

    '''

    df['Ratings'] = df['Ratings'].astype(float).astype(int)
    df['Purchase Status'] = df['Purchase Status'].astype(str).astype(int)
    df['Review Body'] = df['Review Body'].astype(str)

    #df.to_csv('Collected_Reviews.csv', index=False)
    
    return df

if __name__ == "__main__":
    collection(url,headers)
    #print(data_collected)

