import aiohttp
from typing import Any, Dict, Optional
import asyncio
from faker import Faker
import pprint
from aiogram.types import message, Message
from aiogram import F

fake = Faker()

header = {'User-Agent': fake.user_agent()}

import aiohttp
import asyncio
from typing import Optional, Dict, Any

JIKAN_URL = "https://api.jikan.moe/v4"


async def search_anime_title(title: str) -> dict:
    async with aiohttp.ClientSession() as session:

        param = {
                'q': title,
                'limit': 5,
                'order_by': 'members',
                'sort': 'desc',
                'type': 'tv',          
                'min_score': 3
            }

        async with session.get(f'{JIKAN_URL}/anime', params=param, timeout=5) as response:

                result = await response.json()
                
                if response.status != 200:
                    print(f"API Error: Status {response.status}")
                    return []
                
                result = await response.json()
                
                if not result.get('data'):
                    print("No data found in response")
                    return []
                
                valid_anime_list = [] 
                
                # pprint.pprint(result)

                for anime_data in result['data']:
                    try:
                        
                        required_fields = {
                            'title': anime_data.get('title_english') or anime_data.get('title'),
                            'image_url': anime_data['images']['jpg']['large_image_url'],
                            'mal_id': anime_data['mal_id'],
                            'episodes': anime_data['episodes'],
                            'synopsis': anime_data['synopsis']
                        }
                        
                        if all(required_fields.values()):
                            valid_anime_list.append({
                                'title': required_fields['title'],
                                'image_url': required_fields['image_url'],
                                'mal_id': required_fields['mal_id'],
                                'episodes': required_fields['episodes'],
                                'synopsis': required_fields['synopsis']
                            })
                            
                    except KeyError or TypeError as e:
                        print(f"Error processing anime data: {e}")
                        continue
                
                return valid_anime_list

# asyncio.run(search_anime_title('Naruto'))
