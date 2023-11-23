import time
import asyncio
import os

import google.generativeai as palm
from playwright.async_api import async_playwright

from config import API_KEY
from config import URL_REVIEWS
from config import REVIEW_LOCATOR


async def reviewscrap():
    async with async_playwright() as p:
        width = 1024
        height = 3000
        browser = await p.chromium.launch(headless=True, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(URL_REVIEWS)
        await page.set_viewport_size({"width": width, "height": height})
        time.sleep(10)
        await page.locator(REVIEW_LOCATOR).all()
        reviews_count = await page.locator(REVIEW_LOCATOR).count()
        reviews_text = []
        # print(reviews_count)
        for i in range(reviews_count):
            review = await page.locator(REVIEW_LOCATOR).nth(i).text_content()
            reviews_text.append(review)

        await browser.close()
        return reviews_text


def reviewai(reviews, m):
    prompt = "I'm a manager of a sports bar and collected the reviews below from clients. \
              Can you summarize the action items to better serve the clients?"

    for review in reviews:
        prompt += "\n" + review

    # print(prompt)

    completion = palm.generate_text(
        model=m,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )

    print("\nRecommendation:\n", completion.result)
    # print("\nSafety Feedback:\n", completion.safety_feedback)
    # print(completion.candidates)
    # print(completion.filters)


if __name__ == '__main__':

    print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

    palm.configure(api_key=API_KEY)

    model = palm.get_model('models/text-bison-001')

    scrap = asyncio.run(reviewscrap())

    # print(scrap)

    reviewai(scrap, model)
