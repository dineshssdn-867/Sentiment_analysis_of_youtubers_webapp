<div align="center">
  
<img src="https://youtuberssentiment.herokuapp.com/static/assets/img/hero/YouTuber_Sentiment.png">
  
</div>

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->

[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)

<!-- ALL-CONTRIBUTORS-BADGE:END -->

# Youtubers Sentiment✨

Personal Project - Youtubers Sentiment

## Demo💻

[Demo](https://youtuberssentiment.herokuapp.com/)

## Environment Variables⚙

To run this project, you will need to add the following environment variables to a .env file at the root of the project


- `AWS_KEY` : Your aws key for S3

- `AWS_SECRET_KEY` : Your secret aws key for S3

- `AWS_CDN_URL` : Your static cdn url

- `CACHE_USERNAME` : Operator of cache username

- `CACHE_PASSWORD` : Password of cache service password

## Run Locally🚀

Clone the project

```bash
  git clone https://github.com/dineshssdn-867/Sentiment_analysis_of_youtubers_webapp.git
```

Go to the project directory

```bash
  cd Sentiment_analysis_of_youtubers
```

Create Environement and install dependencies

```bash
python m venv env
env\Scripts\activate
pip install -r requirements.txt
```

Make migrations and start the server

```bash
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver
```

## Features🧾

You can register as a user(youtuber)
<details>
  <summary>For Yotubers Channel Video's</summary>

  - Get to know the info of emotions of channel videos in the time interval.
  - Get to know the info of intents of channel videos in the time interval.
  - Visualize results of emotions
  - Get to know how this works
</details>

<details>
  <summary>For Yotubers Video</summary>
  - Get to know the info of emotions of individual videos.
  - Get to know the info of intents of individual videos.
  - Visualize results of emotions
  - Get to know how this works
</details>

<details>
  <summary>For Yotubers Video Comments</summary>
  - Get to know the info of emotions of individual video comments.
  - Get to know the info of intents of individual videos comments.
  - Visualize results of emotions
  - Get to know how this works
</details>

## Tech Stack👨‍💻

**Frontend:** HTML, CSS, JS, Bootstrap

**Backend:** Django, Firebase, Nginx, Caching Services, AWS Cloudfront

[emoji key](https://allcontributors.org/docs/en/emoji-key)

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/dineshssdn-867"><img src="https://avatars.githubusercontent.com/u/66898317?v=4" width="100px;" alt=""/><br /><sub><b>Dinesh Nariani</b></sub></a><br /><a href="https://github.com/dineshssdn-867/DIM/commits?author=dineshssdn-867" title="Code">💻</a> <a href="https://github.com/dineshssdn-867/DIM/commits?author=dineshssdn-867" title="Documentation">📖</a> <a href="#design-dineshssdn-867" title="Design">🎨</a> <a href="#maintenance-dineshssdn-867" title="Maintenance">🚧</a> <a href="#projectManagement-dineshssdn-867" title="Project Management">📆</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
