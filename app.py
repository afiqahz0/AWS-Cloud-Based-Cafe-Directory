from flask import Flask, render_template
import boto3

app = Flask(__name__)

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-southeast-2' 
)

table = dynamodb.Table('KLCoffeeExplorer')

def s3_to_https(s3_path):
    if s3_path.startswith("s3://"):
        parts = s3_path.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1]
        return f"https://{bucket}.s3.amazonaws.com/{key}"
    return s3_path

@app.route("/")
def index():
    response = table.scan()
    cafes = response.get('Items', [])

    for cafe in cafes:
        cafe['ImageURL'] = s3_to_https(cafe.get('ImageURL', ''))

    cafes = sorted(cafes, key=lambda x: x['CafeID'])

    return render_template("index.html", cafes=cafes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
