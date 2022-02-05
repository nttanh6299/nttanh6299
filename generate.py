import requests
import json
import random
import re
import math
from html2image import Html2Image

hti = Html2Image()

MAX_PROGRESS_VALUE = 300

pokeTypes = [
    {
        "name": 'normal',
        "color": '#A8A878',
    },
    {
        "name": 'fighting',
        "color": '#C03028',
    },
    {
        "name": 'flying',
        "color": '#A890F0',
    },
    {
        "name": 'poison',
        "color": '#A040A0',
    },
    {
        "name": 'ground',
        "color": '#E0C068',
    },
    {
        "name": 'rock',
        "color": '#B8A038',
    },
    {
        "name": 'bug',
        "color": '#A8B820',
    },
    {
        "name": 'ghost',
        "color": '#705898',
    },
    {
        "name": 'steel',
        "color": '#B8B8D0',
    },
    {
        "name": 'fire',
        "color": '#F08030',
    },
    {
        "name": 'water',
        "color": '#6890F0',
    },
    {
        "name": 'grass',
        "color": '#78C850',
    },
    {
        "name": 'electric',
        "color": '#F8D030',
    },
    {
        "name": 'psychic',
        "color": '#F85888',
    },
    {
        "name": 'ice',
        "color": '#98D8D8',
    },
    {
        "name": 'dragon',
        "color": '#7038F8',
    },
    {
        "name": 'dark',
        "color": '#705848',
    },
    {
        "name": 'fairy',
        "color": '#EE99AC',
    },
    {
        "name": 'unknown',
        "color": '#68A090',
    },
]


def formatName(name):
    result = ''
    for str in re.sub(r'[_-]', ' ', name.strip()).lower().split():
        result += str.capitalize() + ' '
    return result


def getBarColor(value):
    if (value >= 75):
        return '#72AA58'
    if (value >= 50):
        return '#F5CD3E'
    if (value >= 25):
        return '#F5A63A'
    return '#E15859'


def convertHgToPound(hg, round=1):
    return math.ceil(hg * 0.2204622622)


f = open("./README.md", "w")
pokemon_id = random.randint(1, 200)
res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
result = json.loads(res.text)

avatar = ''
if result['sprites'] and result['sprites']['other'] and result['sprites']['other']['official-artwork'] and result['sprites']['other']['official-artwork']['front_default']:
    avatar = result['sprites']['other']['official-artwork']['front_default']
else:
    avatar = 'https://www.freeiconspng.com/uploads/pokeball-transparent-png-2.png'

stats = ''
for stat in result['stats']:
    progress = (stat['base_stat'] / MAX_PROGRESS_VALUE) * 100
    stats += f'''<div class="stat">
        <div class="flex flex-items-center">
          <div class="label">{formatName(stat['stat']['name'])}</div>
          <div class="value">{stat['base_stat']}</div>
          <div class="flex-item">
            <div class="progress">
              <div class="bar" style="--value: {progress}%; --bg: {getBarColor(progress)};"></div>
            </div>
          </div>
        </div>
      </div>'''

types = ''
for type in result['types']:
    typeDot = ''
    variant = pokeTypes[len(pokeTypes) - 1]
    for pokeType in pokeTypes:
        if pokeType.get('name') == type['type']['name']:
            variant = pokeType
            break

    if result['types'].index(type) != len(result['types']) - 1:
        typeDot = '<div class="dot"> </div>'
    else:
        typeDot = ''

    types += f'''<div class="type-name" style="--color: {variant.get('color')}">
    {formatName(type['type']['name'])}
  </div>{typeDot}'''

card = f'''<div class="card">
 <div class="back-face">
  <h2>#{result['id']}</h2>
 </div>
 <div class="content">
  <div class="flex flex-column flex-content-center flex-items-center">
    <div>
     <div class="image-wrapper">
        <img alt="{result['name']}" src="{avatar}" class="image" />
      </div>
    </div>
    <div>
      <h3 class="name">{formatName(result['name'])}</h3>
    </div>
    <div>
      <div class="flex flex-items-center">
        <p style="color: #87847E; font-size: 14px; margin: 0;">W: {convertHgToPound(result['weight'])}lbs</p>
        <div class="dot"> </div>
        <p style="color: #87847E; font-size: 14px; margin: 0;">H: {result['height'] / 10}m</p>
      </div>
    </div>
    <div>
      <div class="flex flex-items-center">
        {types}
      </div>
    </div>
  </div>
 </div>
</div>'''


classes = '''* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
  .container {
		font-family:
			system-ui,
			-apple-system,
			'Segoe UI',
			Roboto,
			Helvetica,
			Arial,
			sans-serif,
			'Apple Color Emoji',
			'Segoe UI Emoji';
	}
  .flex {
    display: flex;
  }
  .flex-column {
    flex-direction: column;
  }
  .flex-item {
    flex: 1;
  }
  .flex-content-center {
    -webkit-box-pack: center;
    justify-content: center;
  }
  .flex-items-center {
   -webkit-box-align: center;
    align-items: center;
  }
  .dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: #ccc;
    border-radius: 50%;
    margin-left: 6px;
    margin-right: 6px;
  }
  .stat {
    width: 600px;
    margin-top: 16px;
  }
  .stat .label {
    flex: 0 0 150px;
    font-weight: 500;
    font-size: 1.15rem;
    color: #bbb;
    text-align: right;
  }
  .stat .value {
    flex: 0 0 80px;
    display: inline-block;
    font-size: 1.15rem;
    font-weight: 400;
    color: #555;
    text-align: center;
  }
  .stat .progress {
    position: relative;
    border-radius: 6px;
    background-color: #f8f8f8;
    overflow: hidden;
    height: 15px;
    width: 80%;
  }
  .stat .bar {
    position: absolute;
    top: 0;
    left: 0;
    width: var(--value, 0);
    height: 100%;
    background-color: var(--bg, #ccc);
    transition: width 0.25s,
    background-color 0.25s;
  }
  .card {
    width: 450px;
    margin-bottom: 20px;
    position: relative;
    background-color: #fff;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 5px 10px;
    border-radius: 16px;
    padding: 10px;
  }
  .card .back-face {
    position: absolute;
    right: 5%;
    top: 5%;
    font-size: 1.8rem;
    font-weight: 600;
  }
  .card .back-face h2 {
    color: #ebebeb;
    margin-top: 0;
    margin-bottom: 0;
  }
  .card .content {
    z-index: 1;
    cursor: pointer;
    padding-bottom: 4px;
  }
  .card .image-wrapper {
    background-color: transparent;
    width: 180px;
    height: 180px;
    margin-top: 6px;
  }
  .card .image {
    display: inline-block;
    width: 100%;
    height: auto;
    -webkit-filter: drop-shadow(0px 2px 4px #888);
    filter: drop-shadow(0px 2px 4px #888);
  }
  .card .name {
    margin-top: 0;
    margin-bottom: 0;
    font-weight: 600;
    font-size: 26px;
    color: #615E58;
  }
  .card .type-name {
    margin-top: 0;
    margin-bottom: 0;
    font-weight: 600;
    font-size: 19px;
    color: var(--color, #ccc);
  }'''

html = f'''<div class="container">
        <div class="flex flex-column">
          <div class="flex-item flex flex-items-center flex-content-center">
            {card}
          </div>
          <div class="flex-item flex flex-column flex-items-center flex-content-center">
            {stats}
          </div>
        </div>
      </div>'''

hti.screenshot(html_str=html, css_str=classes,
               save_as='pokemon.png', size=(700, 600))

f.write(f'''<h4 style="margin-top: 0; margin-bottom: 0;">It's nice to meet you!</h4>
  <p>Look. Is this your favorite pokemon?</p>
  <a href="https://poke-client.vercel.app/pokemon/{result['name']}" target="_blank">
    <img src="pokemon.png" alt="pokemon">
  </a>''')
f.close()
