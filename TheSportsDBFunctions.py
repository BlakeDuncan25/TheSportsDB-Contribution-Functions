from selenium import webdriver
import urllib.request
from PIL import Image
import pandas as pd

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
    path, team, player, dob, position, nationality, height, weight, number, image_url
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
        browser.find_element_by_xpath("//*[@id='height']").send_keys(height[i])
        browser.find_element_by_xpath("//*[@id='weight']").send_keys(weight[i])
        browser.find_element_by_xpath("//*[@id='number']").send_keys(number[i])
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
    new_ratio = new_width / new_height
    if ratio > new_ratio:
        ratio_pixels = int(ratio * height)
        pil_img = pil_img.resize((new_width, ratio_pixels), Image.LANCZOS)
        result = Image.new(pil_img.mode, (new_width, new_height), background_color)
        result.paste(pil_img, (0, (new_height - ratio_pixels) // 2))
        return result
    else:
        ratio_pixels = int(ratio * new_height)
        pil_img = pil_img.resize((ratio_pixels, new_height), Image.LANCZOS)
        result = Image.new(pil_img.mode, (new_width, new_height), background_color)
        result.paste(pil_img, ((new_width - ratio_pixels) // 2, 0))
        return result


def save_channel_png(path, channel, image_url):
    img = retrieve_image_png(path, channel, image_url)
    im_thumb = pad_png(img, (0, 0, 0, 0), 800, 450)
    return im_thumb.save(f"{path}/{channel}.png")
