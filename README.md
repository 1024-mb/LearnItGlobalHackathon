# BusMapperSG 🚍
<a id="readme-top"></a>

[![Contributors](https://img.shields.io/github/contributors/1024-mb/LearnItGlobalHackathon)](https://github.com/1024-mb/LearnItGlobalHackathon/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/1024-mb/LearnItGlobalHackathon)](https://github.com/1024-mb/LearnItGlobalHackathon/network/members)
[![Stars](https://img.shields.io/github/stars/1024-mb/LearnItGlobalHackathon)](https://github.com/1024-mb/LearnItGlobalHackathon/stargazers)
[![Issues](https://img.shields.io/github/issues/1024-mb/LearnItGlobalHackathon)](https://github.com/1024-mb/LearnItGlobalHackathon/issues)

Welcome to BusMapperSG! A responsive Django web app that makes 
commuting easier by providing real-time bus and train locations, 
arrival times, crowding info, and station amenities. 

⚠️ **20-second demo:** [https://youtu.be/D_WVxfMUiTU  ](https://www.youtube.com/watch?v=D_WVxfMUiTU&list=PLnL6WpWjTSrJmPOEB30jLO2XghAlz9ZEn&index=2)

---

## Table of Contents
- Why This Project Matters  
- Technologies Used  
- Project Layout  
- Prequisites  
- Setup Instructions  


---

## Why this Project Matters

Navigating Singapore’s public transit can be stressful, especially for the elderly, disabled, or socially anxious commuters. Existing apps provide schedules, but real-time location, crowding, and accessibility information are often missing.

BusMapperSG solves this by:

- **🕰️ Saving time:** commuters can see live bus/train locations and arrivals.
- **♿️ Improving accessibility:** shows station amenities and disabled access. 
- **☺️ Reducing anxiety:** provides real-time crowding info so users can avoid crowded trains or buses. 
- **🧭 Simplifying navigation:** step-by-step directions for every station, removing guesswork. 
- In short, it makes daily commuting safer, faster, and more inclusive, which is a tangible impact for millions of transit users in Singapore.

---

## Technologies/Frameworks
- Python + Django 5
- PostgreSQL
- React.js
- SVG
- External transport APIs (LTA DataMall)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## Project Layout
- `LearnItGlobal/manage.py` Django entry point
- `LearnItGlobal/LearnItGlobal/settings.py` app settings
- `LearnItGlobal/LearnItGlobal/urls.py` routes
- `LearnItGlobal/LearnItGlobal/views.py`: page + API handlers
- `LearnItGlobal/LearnItGlobal/templates/base.html` base template
- `LearnItGlobal/LearnItGlobal/templates/main.html` main page template
- `LearnItGlobal/static/` CSS, JS, maps, images, React Elements

<p align="right">(<a href="#readme-top">back to top</a>)</p>


---
## Prerequisites
- Python 3.10+
- PostgreSQL running locally
- Django
- A virtual environment (optional)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---
## Setup
1. Go to the Django project root:
   ```bash
   cd LearnItGlobal
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install django psycopg2-binary requests
   ```
4. Configure database settings in `LearnItGlobal/settings.py` (`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`).
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the server:
   ```bash
   python manage.py runserver
   ```

Open: `http://127.0.0.1:8000/`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Routes
- `/` -> main map page
- `/admin/` -> Django admin
- `/api/busstops/` -> bus arrivals by stop code
- `/api/busroutes/` -> bus route data
- `/api/busstations/` -> station endpoint
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---


If you create new pages, place templates in `LearnItGlobal/LearnItGlobal/templates/` and extend `base.html` the same way.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
