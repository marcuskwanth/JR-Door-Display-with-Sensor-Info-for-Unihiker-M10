import requests
import datetime

url = 'https://graphql.anilist.co'

query = """
    query ($season: MediaSeason, $seasonYear: Int, $page: Int) {
    Page(page: $page, perPage: 25) {
        pageInfo { total currentPage lastPage hasNextPage }
        media(
        season: $season
        seasonYear: $seasonYear
        type: ANIME
        format_in: [TV]
        sort: POPULARITY_DESC
        ) {
            id
            title { romaji english native }
            format
            episodes
            status
            averageScore
            popularity
            genres
            siteUrl
            }
        }
    }
"""

def fetch_tv_seasonal_anime(season, year):
    all_anime = []
    page = 1
    has_next = True

    while has_next:
        variables = {'season': season, 'seasonYear': year, 'page': page}
        resp = requests.post(url, json={'query': query, 'variables': variables})
        if resp.status_code != 200:
            break
        data = resp.json()
        page_data = data.get('data', {}).get('Page', {})
        media = page_data.get('media', [])
        all_anime.extend(media)
        has_next = page_data.get('pageInfo', {}).get('hasNextPage', False)
        page += 1

    return all_anime

def get_current_season():
    month = datetime.datetime.now().month
    if 4 <= month <= 6:
        return "SPRING"
    elif 7 <= month <= 9:
        return "SUMMER"
    elif 10 <= month <= 12:
        return "FALL"
    else:
        return "WINTER"

def assign_performance_text(score):
    if score is None:
        return "No score available"
    elif score >= 90:
        return "Great"
    elif score >= 75:
        return "Good"
    elif score >= 50:
        return "Fine"
    elif score >= 40:
        return "Average"
    else:
        return "Poor"