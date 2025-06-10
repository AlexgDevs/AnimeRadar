import json
from aiohttp import ClientSession
from faker import Faker
faq = Faker()


JIKAN_URL = "https://api.jikan.moe/v4"

async def search_anime(title: str) -> list[dict] | None:
    async with ClientSession() as session:

        param = {
            'q': title,
            'limit': 5,
            'min_score': 5,
                }

        header = {'User-Agent': faq.user_agent()}

        async with session.get(url=f'{JIKAN_URL}/anime', headers=header, params=param) as response:
            
            if response.status == 200:
                all_json = await response.json()
                # with open('anime_data.json', 'w', encoding='utf-8') as file:
                #     json.dump(all_json, file, indent=4, ensure_ascii=True)
                
                verified_list = []

                for items in all_json.get('data'):
                    
                    required_fields = {

                    'mal_id': None,
                    'title': None,
                    'episodes': None,
                    'synopsis': None,
                    'image': None       
                    }


                    required_fields['mal_id'] = items.get('mal_id', {})
                    required_fields['title'] = items.get('title_english') or items.get('title', {})
                    required_fields['episodes'] = items.get('episodes', {})
                    required_fields['synopsis'] = items.get('synopsis', {})
                    required_fields['image'] = items.get('images', {}).get('jpg', {}).get('large_image_url', {})

                    if all(required_fields.values()):
                        verified_list.append(required_fields)

    return verified_list if len(verified_list) != 0 else None