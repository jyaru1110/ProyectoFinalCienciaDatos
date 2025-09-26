# %%
from time import sleep

import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from common import utils

# %%
MAX_MOVIES = 1000

# %%
opts = FirefoxOptions()
opts.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0 (Educational Web Scraping)",
)
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.set_preference("dom.webdriver.enabled", value=False)
opts.set_preference("useAutomationExtension", value=False)
opts.add_argument("--")

# %%
driver = Firefox(options=opts)

# %%
driver.get("https://www.imdb.com/search/title/?groups=top_1000&count=250&sort=user_rating,asc")

# %%
# Le damos click 3 veces para mostrar las 1000 peliculas
for i in range(3):
    sleep(10)
    see_more_btn = WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located((By.CLASS_NAME, "ipc-see-more__button")),
    )

    see_more_btn = WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.CLASS_NAME, "ipc-see-more__button")),
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", see_more_btn)
    driver.execute_script("arguments[0].click();", see_more_btn)
    # see_more_btn.click()

    print(f"Done {i}")

# %%
sleep(10)
elements = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")
assert len(elements) == MAX_MOVIES, f"Expected {MAX_MOVIES} movies but found {len(elements)}"
# %%
data = {
    "title": [],
    "url": [],
    "metacritic_score": [],
    "rating": [],
    "year": [],
    "duration": [],
    "stars": [],
    "voters": [],
    "description": [],
}

for element in elements:
    title_element = element.find_element(By.CLASS_NAME, "ipc-title-link-wrapper")
    title = title_element.text
    url = title_element.get_attribute("href")

    metadata_container = element.find_element(By.CLASS_NAME, "dli-title-metadata")
    metadata = metadata_container.find_elements(By.CLASS_NAME, "dli-title-metadata-item")
    anio = metadata[0].text
    duracion = metadata[1].text
    try:
        rating = metadata[2].text
    except IndexError:
        rating = "Not Rated"

    try:
        metascore = element.find_element(By.CLASS_NAME, "metacritic-score-box").text
    except NoSuchElementException:
        metascore = "No Score"

    rating_star = element.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text
    votantes = element.find_element(By.CLASS_NAME, "ipc-rating-star--voteCount").text
    descripcion = element.find_element(By.CLASS_NAME, "ipc-html-content-inner-div").text

    data["title"] += [title]
    data["url"] += [url]
    data["year"] += [anio]
    data["duration"] += [duracion]
    data["metacritic_score"] += [metascore]
    data["rating"] += [rating]
    data["stars"] += [rating_star]
    data["voters"] += [votantes]
    data["description"] += [descripcion]


# %%
initial_df = pd.DataFrame(data)
print(initial_df.shape)

# %%
initial_df.to_parquet(utils.find_project_root() / "data" / "raw" / "stage0.parquet.gzip", compression="gzip")
