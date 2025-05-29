import json


schedule = {
    "company": "Tech Solutions",
    "events": [
        {
            "name": "Project Kickoff",
            "date": {
                "year": 2025,
                "month": 6,
                "day": 15,
                "time": {
                    "hour": 10,
                    "minute": 30
                }
            },
            "location": "Conference Room A"
        },
        {
            "name": "Sprint Review",
            "date": {
                "year": 2025,
                "month": 6,
                "day": 22,
                "time": {
                    "hour": 14,
                    "minute": 0
                }
            },
            "location": "Zoom"
        },
        {
            "name": "Team Building",
            "date": {
                "year": 2025,
                "month": 7,
                "day": 5,
                "time": {
                    "hour": 9,
                    "minute": 0
                }
            },
            "location": "Outdoor Park"
        }
    ]
}

with open('jsons.json', 'w', encoding='utf-8') as file:
    json.dump(schedule, file,  ensure_ascii=False, indent=4)


ls = []
print(schedule['company'], '\n')
for comp in schedule['events']:
    date_name = comp['name']

    date = comp['date']

    year = date['year']
    month = date['month']
    day = date['day']

    time = date['time']
    hour = time['hour']
    minute = time['minute']
    
    location = comp['location']

    caption = f'''
Name: {date_name}
year: {year}
month: {month}
day: {day}
time: {hour}:{minute}
'''
    ls.append(caption)

for i in ls:
    print(i)