# playwright Generative AI

#### This repo is based on https://github.com/kying18/palm-api-projects/tree/main from @kying18 but uses Playwright instead.

### Using Playwright with Python and Ollama & Google Generative AI for recommendation 

This is an example of how to Playwright to scrap a website, collect reviews from users and process them using
Google Generative PaLM AI. 

A prompt is created with a question and appended with the reviews. 

The trained model is selected and passed to `completition` function that generates a `result`.

This example has some challenges:
- Async functions to scrap text from URL
- Setup of Generative AI

Required tools:
- Google PaLM Generative AI
- PlayWright
- Python
- Ollama AI Model & API server

Problems found:
- Google model does not work with Brazilian Portuguese so we had to stick with English reviews.
- URL needed to add `hl=en` so reviews are not translated by default causing async issues.
- Some reviews trigger Google safety blocks and return `None` as the result of completition. 

Todo:
- [ ] Implement error handling for SAFETY feedback from API 
- [ ] Implement translation API for reviews that are not in English

More information:
[PaLM API: Text Quickstart with Python
](https://developers.generativeai.google/tutorials/text_quickstart?authuser=3)
