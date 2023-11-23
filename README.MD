# playwright Generative AI

### Using Playwright with Python and Google Generative AI for recommendation 

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
- Github Actions

Github Actions Workflow is activated only if a push is made to the tests folder. 

After each run artifacts are uploaded and retained for 30 days. 

Todo:
- [ ] Implement error handling for SAFETY feedback from API 
- [ ] Implement translation API for reviews that are not in English
