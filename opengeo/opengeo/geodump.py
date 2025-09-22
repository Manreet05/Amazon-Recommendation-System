import sqlite3
import json
import codecs

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
for row in cur:
    data = row[1]  # assuming row[1] is in bytes or string format directly from the DB
    try:
        js = json.loads(data.decode() if isinstance(data, bytes) else data)
    except json.JSONDecodeError:
        print("JSON decode error, skipping row")
        continue

    if not js.get('features'):
        continue

    try:
        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        # Use display_name if available, otherwise try formatted, or default to 'Unknown location'
        where = js['features'][0]['properties'].get('display_name', js['features'][0]['properties'].get('formatted', 'Unknown location'))
        where = where.replace("'", "")
    except (IndexError, KeyError, TypeError) as e:
        print('Unexpected format:', e)
        print(js)
        continue

    try:
        print(where, lat, lng)
        count += 1
        if count > 1:
            fhand.write(",\n")
        output = f"[{lat},{lng}, '{where}']"
        fhand.write(output)
    except Exception as e:
        print("Error writing data:", e)
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")
