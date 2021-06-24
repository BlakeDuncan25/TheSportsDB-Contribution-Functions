from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from PIL import Image
import pandas as pd
from IPython.display import display, HTML

browser = webdriver.Chrome(executable_path="/Users/blakeduncan/Documents/chromedriver")


def thesportsdb_login(username, password):
    browser.get("https://www.thesportsdb.com/")
    browser.find_element_by_xpath(
        "//*[@id='header']/nav/div/div[2]/ul/li[5]/a[1]"
    ).click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[1]/input"
    ).send_keys(username)
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[2]/input"
    ).send_keys(password)
    browser.find_element_by_xpath("//*[@id='rememberme']").click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[4]/input"
    ).click()


def add_event(league, date, starttime, season, hometeam, awayteam, week):
    for i in range(len(league)):
        browser.get(f"https://www.thesportsdb.com/edit_event_add.php?l={league[i]}")
        browser.find_element_by_xpath("//*[@id='datepicker']").send_keys(date[i])
        browser.find_element_by_xpath("//*[@id='starttime']").send_keys(starttime[i])
        browser.find_element_by_xpath("//*[@id='season']").send_keys(season[i])
        browser.find_element_by_xpath("//*[@id='hometeam']").send_keys(hometeam[i])
        browser.find_element_by_xpath("//*[@id='awayteam']").send_keys(awayteam[i])
        browser.find_element_by_xpath("//*[@id='round']").send_keys(week[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()


def add_score(
    league, date, starttime, season, hometeam, awayteam, homescore, awayscore, week
):
    for i in range(len(league)):
        browser.get(f"https://www.thesportsdb.com/edit_event_add.php?l={league[i]}")
        browser.find_element_by_xpath("//*[@id='datepicker']").send_keys(date[i])
        browser.find_element_by_xpath("//*[@id='starttime']").send_keys(starttime[i])
        browser.find_element_by_xpath("//*[@id='season']").send_keys(season[i])
        browser.find_element_by_xpath("//*[@id='hometeam']").send_keys(hometeam[i])
        browser.find_element_by_xpath("//*[@id='awayteam']").send_keys(awayteam[i])
        browser.find_element_by_xpath("//*[@id='homescore']").send_keys(homescore[i])
        browser.find_element_by_xpath("//*[@id='awayscore']").send_keys(awayscore[i])
        browser.find_element_by_xpath("//*[@id='round']").send_keys(week[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()


def add_player(
    path,
    team,
    player,
    dob,
    position,
    nationality,
    height,
    weight,
    team_name,
    image_url,
):
    for i in range(len(team)):
        browser.get(f"https://www.thesportsdb.com/edit_player_add.php?t={team[i]}")
        browser.find_element_by_xpath("//*[@id='fullname']").send_keys(player[i])
        browser.find_element_by_xpath("//*[@id='datepicker']").send_keys(dob[i])
        browser.find_element_by_xpath("//*[@id='position']").send_keys(position[i])
        browser.find_element_by_xpath("//*[@id='countries']").send_keys(nationality[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()
        browser.find_element_by_xpath("//*[@id='feature']/div/div/div[3]/a[1]").click()
        browser.find_element_by_xpath(
            "//*[@id='feature']/div/div/div[1]/a[4]/button"
        ).click()
        browser.find_element_by_xpath("//*[@id='height']").send_keys(Keys.COMMAND, "a")
        browser.find_element_by_xpath("//*[@id='height']").send_keys(height[i])
        browser.find_element_by_xpath("//*[@id='weight']").send_keys(Keys.COMMAND, "a")
        browser.find_element_by_xpath("//*[@id='weight']").send_keys(weight[i])
        browser.find_element_by_xpath("//*[@id='team']").send_keys(team_name[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()
        try:
            save_player_thumbnail(path, player[i], image_url[i])
            try:
                browser.find_element_by_xpath(
                    "//*[@id='feature']/div/div/div[1]/a[1]/img"
                ).click()
                try:
                    browser.find_element_by_xpath("/html/body/form/input").send_keys(
                        f"{path}/{player[i]}.jpg"
                    )
                    browser.find_element_by_xpath("/html/body/form/p[3]/input").click()
                except:
                    continue
            except:
                continue
        except:
            continue


def retrieve_image_jpg(path, image_name, image_url):
    urllib.request.urlretrieve(image_url, f"{path}/{image_name}.jpg")
    return Image.open(f"{path}/{image_name}.jpg").convert("RGB")


def retrieve_image_png(path, image_name, image_url):
    urllib.request.urlretrieve(image_url, f"{path}/{image_name}.png")
    return Image.open(f"{path}/{image_name}.png").convert("RGBA")


def crop_image(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    if img_height > img_width:
        coordinates = pil_img.crop((0, 0, img_width, crop_height))
    else:
        coordinates = pil_img.crop(
            (
                (img_width - crop_width) // 2,
                (img_height - crop_height) // 2,
                (img_width + crop_width) // 2,
                (img_height + crop_height) // 2,
            )
        )
    return coordinates


def crop_max_square(pil_img):
    return crop_image(pil_img, min(pil_img.size), min(pil_img.size))


def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def convert_transparent(path, image_name):
    img = Image.open(f"{path}/{image_name}.png")

    datas = img.getdata()

    newData = []

    for i in datas:
        if i[0] >= 240 and i[1] >= 240 and i[2] >= 240:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(i)

    img.putdata(newData)
    return img.save(f"{path}/{image_name}.png", "PNG")


def save_player_thumbnail(path, player, image_url):
    img = retrieve_image_jpg(path, player, image_url)
    im_thumb = crop_max_square(img).resize((700, 700), Image.LANCZOS)
    return im_thumb.save(f"{path}/{player}.jpg")


def upload_player_thumbnail(path, player, image_url):
    for i in range(len(player)):
        try:
            save_player_thumbnail(path, player[i], image_url[i])
            search = player[i].replace(" ", "+")
            browser.get(f"https://www.thesportsdb.com/search.php?s={search}")
            try:
                browser.find_element_by_xpath(
                    "//*[@id='feature']/div/div/div[3]/a/img"
                ).click()
                browser.find_element_by_xpath(
                    "//*[@id='feature']/div/div/div[1]/a[1]/img"
                ).click()
                try:
                    browser.find_element_by_xpath("/html/body/form/input").send_keys(
                        f"{path}/{player[i]}.jpg"
                    )
                    browser.find_element_by_xpath("/html/body/form/p[3]/input").click()
                except:
                    continue
            except:
                continue
        except:
            continue


def save_badge_png(path, team, image_url):
    img = retrieve_image_png(path, team, image_url)
    im_thumb = expand2square(img, (0, 0, 0, 0)).resize((512, 512), Image.LANCZOS)
    return im_thumb.save(f"{path}/{team}.png")


def save_jersey_png(path, team, image_url):
    img = retrieve_image_png(path, team, image_url)
    im_thumb = expand2square(img, (0, 0, 0, 0)).resize((500, 500), Image.LANCZOS)
    im_thumb.save(f"{path}/{team}.png")
    return convert_transparent(path, team)


def pad_png(pil_img, background_color, new_width, new_height):
    width, height = pil_img.size
    ratio = width / height
    print(ratio)
    new_ratio = new_width / new_height
    print(new_ratio)
    if ratio > new_ratio:
        print("wide")
        ratio_pixels = int((new_width / width) * height)
        print(ratio_pixels)
        pil_img = pil_img.resize((new_width, ratio_pixels), Image.LANCZOS)
        result = Image.new(pil_img.mode, (new_width, new_height), background_color)
        result.paste(pil_img, (0, (new_height - ratio_pixels) // 2))
        return result
    else:
        print("tall")
        ratio_pixels = int(ratio * new_height)
        print(ratio_pixels)
        pil_img = pil_img.resize((ratio_pixels, new_height), Image.LANCZOS)
        result = Image.new(pil_img.mode, (new_width, new_height), background_color)
        result.paste(pil_img, ((new_width - ratio_pixels) // 2, 0))
        return result


def save_channel_png(path, channel, image_url):
    img = retrieve_image_png(path, channel, image_url)
    im_thumb = pad_png(img, (0, 0, 0, 0), 800, 450)
    return im_thumb.save(f"{path}/{channel}.png")


def save_logo_png(path, logo, image_url):
    img = retrieve_image_png(path, logo, image_url)
    im_thumb = pad_png(img, (0, 0, 0, 0), 800, 310)
    return im_thumb.save(f"{path}/{logo}.png")


def crop_fan_art(pil_img, new_width, new_height):
    width, height = pil_img.size
    ratio_pixels = int((new_width / width) * height)
    pil_img = pil_img.resize((new_width, ratio_pixels), Image.LANCZOS)
    result = pil_img.crop((0, 0, new_width, new_height))
    return result


def save_fan_art(path, name, image_url):
    img = retrieve_image_jpg(path, name, image_url)
    im_thumb = crop_fan_art(img, 1280, 720)
    return im_thumb.save(f"{path}/{name}.jpg")


def upload_team_fan_art(path, team, fanart1, fanart2, fanart3, fanart4):
    for i in range(len(team)):
        for n in range(1, 5):
            try:
                name = str(team[i]) + f"{n}"
                if n == 1:
                    fanart = fanart1[i]
                elif n == 2:
                    fanart = fanart2[i]
                elif n == 3:
                    fanart = fanart3[i]
                else:
                    fanart = fanart4[i]
                save_fan_art(path, name, fanart)
                browser.get(
                    f"https://www.thesportsdb.com/uploadteamfanart{n}.php?t={team[i]}"
                )
                browser.find_element_by_xpath("/html/body/form/input").send_keys(
                    f"{path}/{team[i]}{n}.jpg"
                )
                browser.find_element_by_xpath("/html/body/form/p[3]/input").click()
                n = n + 1
            except:
                n = n + 1


def create_team(
    username,
    password,
    league,
    full_team_name,
    country,
    api_id,
    year_established,
    stadium,
    stadium_location,
    wiki_team,
):
    browser.get(f"https://thesportsdb.com/edit_team_add.php?l={league[0]}")
    browser.find_element_by_xpath(
        "//*[@id='header']/nav/div/div[2]/ul/li[5]/a[1]"
    ).click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[1]/input"
    ).send_keys(username)
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[2]/input"
    ).send_keys(password)
    browser.find_element_by_xpath("//*[@id='rememberme']").click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[4]/input"
    ).click()
    for i in range(len(league)):
        browser.get(f"https://thesportsdb.com/edit_team_add.php?l={league[i]}")
        browser.find_element_by_xpath("//*[@id='fullname']").send_keys(
            full_team_name[i]
        )
        browser.find_element_by_xpath("//*[@id='countries']").send_keys(country[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()
        browser.find_element_by_xpath("//*[@id='feature']/div/div/div[3]/a[1]").click()
        browser.find_element_by_xpath(
            "//*[@id='feature']/div/div/div[1]/p/a[2]/button"
        ).click()
        browser.find_element_by_xpath("//*[@id='formed']").send_keys(
            year_established[i]
        )
        browser.find_element_by_xpath("//*[@id='apifootball']").send_keys(api_id[i])
        browser.find_element_by_xpath("//*[@id='stadium']").send_keys(stadium[i])
        browser.find_element_by_xpath("//*[@id='stadiumlocation']").send_keys(
            stadium_location[i]
        )
        browser.find_element_by_xpath("//*[@id='descriptionEN']").send_keys(
            wiki_team[i]
        )
        browser.find_element_by_xpath("//*[@id='submit']").click()


def create_team_basic(
    username, password, league, full_team_name, country,
):
    browser.get(f"https://thesportsdb.com/edit_team_add.php?l={league[0]}")
    browser.find_element_by_xpath(
        "//*[@id='header']/nav/div/div[2]/ul/li[5]/a[1]"
    ).click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[1]/input"
    ).send_keys(username)
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[2]/input"
    ).send_keys(password)
    browser.find_element_by_xpath("//*[@id='rememberme']").click()
    browser.find_element_by_xpath(
        "//*[@id='feature']/div/div[3]/div/form/div[4]/input"
    ).click()
    for i in range(len(league)):
        browser.get(f"https://thesportsdb.com/edit_team_add.php?l={league[i]}")
        browser.find_element_by_xpath("//*[@id='fullname']").send_keys(
            full_team_name[i]
        )
        browser.find_element_by_xpath("//*[@id='countries']").send_keys(country[i])
        browser.find_element_by_xpath("//*[@id='submit']").click()


def get_hockey_roster_player_urls(path, roster_url):
    browser.get(roster_url)
    footer = (
        browser.find_element_by_xpath("//*[@id='roster']/div/div[3]/table/tfoot/tr/td")
        .text.split("|")[0]
        .replace("Position: G: ", "")
        .replace("D: ", "")
        .replace("F: ", "")
        .replace(" ", "")
    )
    guards = footer.split(",")[0]
    defenceman = footer.split(",")[1]
    forwards = footer.split(",")[2]
    number_of_players = int(guards) + int(defenceman) + int(forwards) + 7
    hockey_players = {
        "player_urls": [],
    }
    elems = browser.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if elem.get_attribute("href").startswith(
            "https://www.eliteprospects.com/player/"
        ):
            hockey_players["player_urls"].append(elem.get_attribute("href"))
        else:
            continue

    hockey_pd = pd.DataFrame.from_dict(hockey_players)
    hockey_pd = hockey_pd.loc[8:number_of_players]
    hockey_pd.to_csv(f"{path}/hockey_player_urls.csv")
    display(HTML(hockey_pd.to_html()))


def elite_prospects_scraper(path, team, player_urls):
    hockey_players = {
        "team": [],
        "player": [],
        "dob": [],
        "position": [],
        "nationality": [],
        "height": [],
        "weight": [],
        "image_url": [],
    }

    for i in range(len(player_urls)):
        browser.get(player_urls[i])
        player = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[1]/div/div/div[2]/div[1]/div[1]/div[1]"
        ).text
        dob = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[3]/div[3]/div[2]/div[3]/div[2]/div/div[1]/div[2]/a"
        ).text
        position = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[3]/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]"
        ).text
        nationality = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[3]/div[3]/div[2]/div[3]/div[2]/div/div[7]/div[2]/a"
        ).text
        height = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[3]/div[3]/div[2]/div[3]/div[2]/div/div[4]/div[2]"
        ).text
        weight = browser.find_element_by_xpath(
            "//*[@id='component-container']/div[3]/div[3]/div[2]/div[3]/div[2]/div/div[6]/div[2]"
        ).text
        image_url = (
            browser.find_element_by_xpath(
                "//*[@id='component-container']/div[1]/div/div/div[1]/div"
            )
            .get_attribute("style")
            .replace("background-image: url(", "https:")
            .replace('"', "")
            .replace(");", "")
        )
        hockey_players["team"].append(team[i])
        hockey_players["player"].append(player)
        hockey_players["dob"].append(dob)
        hockey_players["position"].append(position)
        hockey_players["nationality"].append(nationality)
        hockey_players["height"].append(height)
        hockey_players["weight"].append(weight)
        hockey_players["image_url"].append(image_url)

    hockey_pd = pd.DataFrame.from_dict(hockey_players)
    hockey_pd.to_csv(f"{path}/hockey_players.csv")
    display(HTML(hockey_pd.to_html()))
