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
N_MOVIES = 20

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
opts.set_preference("browser.cache.disk.enable", value=True)
opts.set_preference("browser.cache.disk.capacity", 102400)
# opts.set_preference("browser.cache.disk.parent_directory", "/tmp/")
opts.add_argument("--")


# %%
driver = Firefox(options=opts)

# %%
# Stage 0 - Fetch de la lista completa de películas y algunos valores incluidos en ella
driver.get("https://www.imdb.com/search/title/?groups=top_1000&count=250&sort=user_rating,asc")

# %%
# Le damos click 3 veces para mostrar las 1000 peliculas
for i in range(3):
    sleep(5)
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
sleep(5)
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
    "rating_stars": [],
    "voters": [],
    "description": [],
}

for element in elements[:N_MOVIES]:
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
    data["rating_stars"] += [rating_star]
    data["voters"] += [votantes]
    data["description"] += [descripcion]


# %%
initial_df = pd.DataFrame(data)
print(initial_df.shape)
initial_df.to_parquet(utils.find_project_root() / "data" / "raw" / "stage0.parquet.gzip", compression="gzip")

# %%
# Stage 1 - Fetch de cada película por url
data.update(
    {
        "director": [],
        "writers": [],
        "stars": [],
        "storyline": [],
        "genres": [],  # Generos canon, espero. Ejemplo "Drama"
        "genres_ext": [],  # Con nombres complejos. Ejemplo "Showbiz Drama"
        "awards_and_nominations": [],
        "cast": [],
        "box_office": [],
        "aspect_ratio": [],
        "countries": [],
        "languages": [],
        "production_companies": [],
        "release_date": [],
        "comentarios_ia": [],
        "ai_summary": [],
    },
)


# %%
for idx, url in enumerate(data["url"]):
    if idx % 50 == 0 and idx != 0:
        print(f"Descanso de 50 en {idx}")
        sleep(10)

    url_sin_params = url.split("?", 1)[0]

    driver.get(url_sin_params)

    # %%
    listas = driver.find_elements(By.CLASS_NAME, "ipc-chip-list")

    try:
        lista_generos_ext = listas[0]

        generos_ext = lista_generos_ext.find_elements(By.CLASS_NAME, "ipc-chip__text")
        generos_ext = [genero.text for genero in generos_ext]
    except IndexError:
        generos_ext = []

    try:
        lista_comentarios = listas[1]

        comentarios_ia = lista_comentarios.find_elements(By.CLASS_NAME, "ipc-chip")
        comentarios_ia = [cmt.get_attribute("aria-label") for cmt in comentarios_ia]
    except IndexError:
        comentarios_ia = []

    data["genres_ext"] += [generos_ext]
    data["comentarios_ia"] += [comentarios_ia]

    # %%
    items_lista = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list__item")

    release_date = ""
    box_office = {}
    aspect_ratio = ""

    for item in items_lista:
        texto = item.text
        lines = texto.split("\n")

        if len(lines) > 1:
            label = lines[0].strip()

            if "Release date" in texto:
                release_date = lines[1]
            elif "Budget" in texto or "Gross" in texto or "Opening weekend" in texto:
                box_office[label] = lines[1] if len(lines) > 1 else ""
            elif "Aspect ratio" in texto:
                aspect_ratio = lines[1]

    data["release_date"] += [release_date]
    data["box_office"] += [box_office]
    data["aspect_ratio"] += [aspect_ratio]

    # %%
    directores = []
    escritores = []
    estrellas = []

    listas_origen = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="title-pc-principal-credit"]')

    for elemento in listas_origen:
        items = elemento.find_elements(By.CLASS_NAME, "ipc-inline-list__item")
        if "Stars" in elemento.text:
            estrellas = [a.text for a in items]
        if "Director" in elemento.text:
            directores = [a.text for a in items]
        if "Writer" in elemento.text:
            escritores = [a.text for a in items]

    data["director"] += [directores]
    data["writers"] += [escritores]
    data["stars"] += [estrellas]

    # %%
    paises_origen = []
    listas_origen = driver.find_elements(By.CSS_SELECTOR, 'li[data-testid="title-details-origin"]')

    for elemento in listas_origen:
        if "Conutries of" in elemento.text:
            continue

        paises = elemento.find_elements(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item")
        paises_origen = [pais.text for pais in paises]

        data["countries"] += [paises_origen]

    # %%
    idiomas = []
    listas_idiomas = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-details-languages"]')

    languages = listas_idiomas.find_elements(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item")
    idiomas = [idioma.text for idioma in languages]

    data["languages"] += [idiomas]

    # %%
    companias = []
    listas_companias = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="title-details-companies"]')

    companies = listas_companias.find_elements(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item")
    companias = [compania.text for compania in companies]

    data["production_companies"] += [companias]

    # %%
    generos = []

    storyline_element = driver.find_element(By.ID, "storyline")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", storyline_element)
    driver.execute_script("arguments[0].click();", storyline_element)
    sleep(2)

    try:
        lista_generos = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="storyline-genres"]')
        genres = lista_generos.find_elements(By.CLASS_NAME, "ipc-metadata-list-item__list-content-item")
        generos = [genero.text for genero in genres]

        data["genres"] += [generos]
    except NoSuchElementException:
        print(f"Sin generos para {url}.")
        data["genres"] += [[]]

    # %%
    ai_summary = ""
    try:
        storyline_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="ai-review-summary-text"]')
        ai_summary = storyline_element.text
    except NoSuchElementException:
        ai_summary = ""

    data["ai_summary"] += [ai_summary]

    # %%
    storyline = ""
    try:
        storyline_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="storyline-plot-summary"]')
        storyline = storyline_element.text
    except NoSuchElementException:
        storyline = ""

    data["storyline"] += [storyline]

    # %%
    cast = []
    try:
        cast_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="title-cast-item__actor"]')
        cast = [actor.text for actor in cast_elements]
    except NoSuchElementException:
        cast = []

    data["cast"] += [cast]

    # %%
    awards_and_nominations = ""
    try:
        award_li = driver.find_element(By.CSS_SELECTOR, 'li[data-testid="award_information"]')
        award_item = award_li.find_element(By.CLASS_NAME, "ipc-inline-list__item")
        awards_and_nominations = award_item.text
    except NoSuchElementException:
        awards_and_nominations = ""

    data["awards_and_nominations"] += [awards_and_nominations]

    print(url)

# %%
stage1_df = pd.DataFrame(data)
print(stage1_df.shape)
stage1_df.to_parquet(utils.find_project_root() / "data" / "raw" / "stage1.parquet")


# %%
driver.quit()
