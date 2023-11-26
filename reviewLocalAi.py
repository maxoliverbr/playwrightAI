"""
Playwright with Ollama API Server
Slower than ChatGPT 3.5 but free and open source
"""
import time
import asyncio
import requests
import json


from playwright.async_api import async_playwright

from config import URL_REVIEWS
from config import REVIEW_LOCATOR

model = 'llama2-uncensored'


def generate(p, context):
    """
    generate text completition function based on prompt p and context
    :param p: string
    :param context: list
    :return: context list
    """
    r = requests.post('http://localhost:11434/api/generate',
                      json={
                          "model": model,
                          "prompt": p,
                          "context": context,
                          "stream": False
                      },
                      stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        body = json.loads(line)
        response_part = body.get('response', '')
        # the response streams one token at a time, print that as we receive it
        print(response_part, end='', flush=True)

        if 'error' in body:
            raise Exception(body['error'])

        if body.get('done', False):
            return body['context']


async def reviewscrap():
    """
    Function to scrap reviews from Google.
    :return: list of reviews
    """
    async with async_playwright() as p:
        print("Playwright start...")
        width = 1024
        height = 5000
        browser = await p.chromium.launch(headless=True, slow_mo=500, timeout=90000)
        context = await browser.new_context()
        page = await context.new_page()
        await page.set_viewport_size({"width": width, "height": height})
        await page.goto(URL_REVIEWS, timeout=90000)
        time.sleep(10)
        await page.get_by_label("Avaliações de Tatu Bola Bar").click()
        time.sleep(10)
        for i in range(3):
            await page.mouse.wheel(0, 1000)
        await page.locator(REVIEW_LOCATOR).all()
        reviews_count = await page.locator(REVIEW_LOCATOR).count()
        reviews_text = []
        print(f"Collected {reviews_count} reviews...")
        for i in range(reviews_count):
            review = await page.locator(REVIEW_LOCATOR).nth(i).text_content()
            reviews_text.append(review)

        await browser.close()
        return reviews_text

if __name__ == '__main__':
    print("Scrap initialize...")
    scrap = asyncio.run(reviewscrap())

    prompt = "Com base nas avaliações abaixo, quais as 3 principais ações que devemos corrigir ? Responda em Português \n" + "".join((x+"\n") for x in scrap)

    # print(prompt)

    print("Start AI analysis...")
    generate(prompt, [])
