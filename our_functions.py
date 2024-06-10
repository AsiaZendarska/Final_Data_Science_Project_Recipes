import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
import time


# Ustawiamy nagłówek dla wszystkich pobrań
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def start_time_meter():
  # Uruchomienie stopera
  print("Rozpoczęcie pomiaru czasu wykonania fragmentu kodu.")
  return time.time()


def stop_time_meter(start_time):
  # Zatrzymanie stopera
  end_time = time.time()

  # Obliczenie czasu wykonania
  execution_time = end_time - start_time

  # Wyświetlenie czasu wykonania
  return print(f"Czas wykonania: {execution_time:.2f} sekundy")


# Pobieramy url na podstawie kategorii i numeru strony
def get_recipe_page_kwestiasmaku(base_url, category, page_number, include_przepisy_html=True):
    if page_number == 1:
        url = f'{base_url}/{category}' + ('/przepisy.html' if include_przepisy_html else '')
    else:
        url = f'{base_url}/{category}' + ('/przepisy.html' if include_przepisy_html else '') + f'?page={page_number}'
    print(f'Pobieranie URL: {url}')  # Dodano dla debugowania
    content = requests.get(url).text
    return BeautifulSoup(content, 'html.parser')


def get_recipe_details_kwestiasmaku(recipe_url, category):
    response = requests.get(recipe_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # znajdowanie tytułu
    title_element = soup.find('h1', {'class': 'przepis page-header'})
    recipe_title = title_element.get_text(strip=True) if title_element else 'Brak tytułu'
    # znajdowanie składników
    ingredients_list = soup.find('div', {'class' : 'field field-name-field-skladniki field-type-text-long field-label-hidden'})
    ingredients = [li.get_text(strip=True) for li in ingredients_list.find_all('li')] if ingredients_list else []
    # znajdowanie oceny
    rating_element = soup.find('span', {'itemprop': 'ratingValue'})
    rating = rating_element.get_text(strip=True) if rating_element else 'Brak oceny'
    # znajdowanie liczby opinii
    opinions = soup.find('span', {'itemprop': 'reviewCount'})
    opinions_count = opinions.get_text(strip=True) if opinions else 'Brak opinii'
    # znajdowanie sposobu przygotowania
    preparation_method_container = soup.find('div', {'class' : 'field field-name-field-przygotowanie field-type-text-long field-label-above'})
    preparation_method = preparation_method_container.get_text(strip=True) if preparation_method_container else 'Brak sposobu przygotowania'

    return {'category': category, 'recipe_title': recipe_title, 'ingredients': ';'.join(ingredients), 'preparation_method': preparation_method, 'rating': rating, 'opinions_count': opinions_count}


# Znajdujemy strony z przepisami i wszystkim potrzebnymi rzeczami
def get_recipes_data_kwestiasmaku(category, number_of_pages, base_url, include_przepisy_html=True):
    all_recipes = []
    for page_number in range(1, number_of_pages + 1):
        soup = get_recipe_page_kwestiasmaku(base_url, category, page_number, include_przepisy_html)
        recipes = soup.find_all('div', {'class': 'col col-lg-3'})
        for recipe in recipes:
            link_element = recipe.find('a', href=True)
            if link_element:
                recipe_link = 'https://www.kwestiasmaku.com' + link_element['href']
                print(recipe_link)
                details = get_recipe_details_kwestiasmaku(recipe_link, category)
                if details:  # Dodajemy tylko, jeśli udało się pobrać szczegóły
                    all_recipes.append(details)
        print(f'Downloaded data from page {page_number}')
    return all_recipes


def get_recipe_page_przepisy(category, page_number):
  url = f'https://www.przepisy.pl/przepisy/posilek/{category}?page={page_number}'
  response = requests.get(url, headers=headers)
  # sleep(2)  # Dodanie opóźnienia, aby nie obciążać serwera
  return BeautifulSoup(response.content, 'html.parser')


def get_recipe_details_przepisy(recipe_url, category):
  response = requests.get(recipe_url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  # znajdowanie tytułu
  title_element = soup.find('h1', {'class': 'title'})
  recipe_title = title_element.get_text(strip=True) if title_element else 'Brak tytułu'
  # znajdowanie składników
  ingredients_list = soup.find_all('span', {'class': 'text-bg-white'})
  ingredients = '; '.join([ingredient.get_text(strip=True) for ingredient in ingredients_list])
  # znajdowanie sposobu przygotowania
  preparation_method_element = soup.find('div', {'class': 'steps-list-wrapper ng-star-inserted'})
  preparation_method = preparation_method_element.get_text(
    strip=True) if preparation_method_element else 'Brak sposobu przygotowania'
  # znajdowanie oceny
  rating_elements_full = soup.find_all('app-asset-ico-rating', class_='ico-rating ng-star-inserted')
  rating_elements_half = soup.find_all('app-asset-ico-rating', class_='ico-rating last ng-star-inserted')
  rating = len(rating_elements_full) + len(rating_elements_half) * 0.5
  # znajdowanie liczby opinii
  opinions_count_element = soup.find('div', {'class': 'comments-list-container ng-star-inserted'})
  opinions_count_p = opinions_count_element.find('p',
                                                 class_='average-count rating-total') if opinions_count_element else None
  opinions_count = opinions_count_p.get_text(strip=True) if opinions_count_p else 'Brak opinii'
  # znajdowanie czasu przygotowania
  preparation_time_element = soup.find('div', {'class': 'time-count'})
  preparation_time = preparation_time_element.get_text(strip=True) if preparation_time_element else 'Brak informacji'
  # sprawdzanie czy danie jest wegetariańskie
  vegetarian_element = soup.find('a', href="/przepisy/wege")
  vegetarian = bool(vegetarian_element and 'Wege' in vegetarian_element.text)

  return {'category': category, 'recipe_title': recipe_title, 'ingredients': ingredients,
          'preparation_method': preparation_method, 'rating': rating, 'opinions_count': opinions_count,
          'preparation_time': preparation_time, 'vegetarian': vegetarian, }


def get_recipes_data_przepisy(categories, number_of_pages):
  all_recipes = []
  for category in categories:
    for page_number in range(1, number_of_pages + 1):
      soup = get_recipe_page_przepisy(category, page_number)
      if not soup:
        continue
      links = soup.find_all('a', class_='recipe-box__title')
      for link in links:
        recipe_url = 'https://www.przepisy.pl' + link['href']
        recipe_data = get_recipe_details_przepisy(recipe_url, category)
        if recipe_data:
          all_recipes.append(recipe_data)
  return all_recipes


def get_page_aniastramach(url):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:  # Sprawdzenie, czy strona nie istnieje
      return None
    return BeautifulSoup(response.text, 'html.parser')


def get_recipes_names_urls_for_page_aniastramach(page_url):
  soup = get_page_aniastramach(page_url)
  if soup is None:  # Jeśli strona nie istnieje, zwróć puste listy
    return [], [], True
  recipes_names, recipes_urls = [], []
  recipes = soup.find_all('div', class_='recipe')
  for recipe in recipes:
    title = recipe.get('data-title')
    recipe_url = recipe.find('a', class_='overlay')['href']
    recipes_names.append(title)
    recipes_urls.append(recipe_url)
  return recipes_names, recipes_urls, False


def get_receipes_details_aniastramach(recipes_urls, category):
  recipes_data = []
  for url in recipes_urls:
    soup = get_page_aniastramach(url)
    if soup is None:
      continue

    # Pobieranie i czyszczenie nazwy potrawy
    recipe_title = soup.find('div', class_='recipe').get('data-title', 'Brak tytułu')
    recipe_title = recipe_title.replace('\n', '').replace(';', '=')

    # Pobieranie i czyszczenie składników
    items = soup.find('div', class_='recipe-what-to-buy')
    ingredients_descriptions = []
    if items:
      items = items.find_all('li')
    for item in items:
      quantity = item.find('span', class_='quantity')
      quantity = quantity.text.strip() if quantity else 'do smaku'
      ingredient_name = item.text.strip().replace(quantity, '', 1).strip()
      description = f"{quantity} {ingredient_name}" if quantity != 'do smaku' else ingredient_name
      ingredients_descriptions.append(description)
    ingredients = '; '.join(ingredients_descriptions)
    ingredients = ingredients.replace('\n', '').replace(';', '=')

    # Pobieranie i czyszczenie sposobu przygotowania
    steps_section = soup.find('div', class_='recipe-steps')
    preparation = "Brak informacji"
    if steps_section:
      steps = steps_section.find_all('li')
      preparation_steps = []
      for step in steps:
        p = step.find('p')
        step_text = p.text.strip() if p else step.text.strip()
        preparation_steps.append(step_text)
      preparation = "\n\n".join(preparation_steps)
    preparation = preparation.replace('\n', '').replace(';', '=')

    # Pozostałe elementy
    time_section = soup.find('div', class_='recipe-icon icon-timer')
    preparation_time = time_section.span.text.strip() + " min" if time_section and time_section.span else "Brak informacji"

    vegetarian_icon = soup.find('div', class_='recipe-icon icon-vegetarian')
    is_vegetarian = bool(vegetarian_icon)

    recipes_data.append({
      'category': category,
      'recipe_title': recipe_title,
      'ingredients': ingredients,
      'preparation_method': preparation,
      'preparation_time': preparation_time,
      'vegetarian': is_vegetarian,
    })

  return recipes_data

