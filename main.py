from fastapi import FastAPI, Form, Request
from starlette.responses import HTMLResponse
import pickle
import warnings

with open('car_price_prediction_model', 'rb') as f:
    model = pickle.load(f)

warnings.filterwarnings("ignore")

def get_price(price):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Car Price</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }}
            .car-price {{
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 20px;
                max-width: 300px;
                margin: 0 auto;
                text-align: center;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .car-price h2 {{
                color: #333333;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            .car-price .price {{
                font-size: 36px;
                font-family: Arial, sans-serif;
                color: #007bff;
                margin-bottom: 20px;
            }}
            .car-price p {{
                color: #666666;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="car-price">
            <h2>Car Price</h2>
            <div class="price">$ {price}</div>
            <p>This is the price of the car you are interested in.</p>
        </div>
    </body>
    </html>

    """

    return html_content


app = FastAPI()

encoded_val = {'make': {'alfa-romero': 1,
                        'audi': 2,
                        'bmw': 3,
                        'chevrolet': 4,
                        'dodge': 5,
                        'honda': 6,
                        'isuzu': 7,
                        'mazda': 8,
                        'mercedes-benz': 9,
                        'mercury': 10,
                        'mitsubishi': 11,
                        'nissan': 12,
                        'peugot': 13,
                        'plymouth': 14,
                        'porsche': 15,
                        'saab': 16,
                        'subaru': 17,
                        'toyota': 18,
                        'volkswagen': 19,
                        'volvo': 20},
                        'fuel-type': {'gas': 1, 'diesel': 2},
                        'aspiration': {'std': 1, 'turbo': 2},
                        'body-style': {'convertible': 1,
                        'hatchback': 2,
                        'sedan': 3,
                        'wagon': 4,
                        'hardtop': 5},
                        'drive-wheels': {'rwd': 1, 'fwd': 2, '4wd': 3},
                        'engine-location': {'front': 1, 'rear': 2},
                        'fuel-system': {'mpfi': 1,
                        '2bbl': 2,
                        'mfi': 3,
                        '1bbl': 4,
                        'spfi': 5,
                        'idi': 6,
                        'spdi': 7},
                        'engine-type': {'dohc': 1, 'ohcv': 2, 'ohc': 3, 'l': 4, 'ohcf': 5}}


@app.post("/submit-form/", response_class=HTMLResponse)
async def submit_form(make: str = Form(...), fuel_type: str = Form(...), num_cylinders: int = Form(...), horsepower: int = Form(...), engine_size: float = Form(...)):
    collected = {
        "make": make.lower(),
        "fuel_type": fuel_type.lower(),
        "num_cylinders": num_cylinders,
        "engine_size": engine_size,
        "horsepower": horsepower
    }

    make = encoded_val['make'][collected['make']]
    fuel_type = encoded_val['fuel-type'][collected['fuel_type']]
    num_cyl = collected['num_cylinders']
    engine_size = collected['engine_size']
    wheel_base = 98.74
    length = 174.13
    width = 65.82
    curb = 2536.31
    city = 21
    high = 26
    horsepower = collected['horsepower']

    arr = [[make, fuel_type, 2, wheel_base, length, width, curb, engine_size, num_cyl, horsepower, city, high]]

    res = model.predict(arr)


    
    return get_price(res[0])



