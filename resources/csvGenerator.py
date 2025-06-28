import requests
import json
import sys
import os
import csv
from urllib.parse import quote, unquote, urlparse  # for url decoding (unquote) and encoding (quote)

def extract_tag(url):
    
    path_segments = urlparse(url).path.split('/')   
    encoded_tag = path_segments[-1]                 # takes last element of path_segments array
    decoded_tag = unquote(encoded_tag)              # decodes the url encoding, like "%20" becomes " "
    return decoded_tag

def extract_arabic_latin(id):
    
    url = "https://www.arwords.com/words/view/" + id

    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }

    response = requests.get(url, headers = headers)

    html_data = response.text
    
    # with open('html_data.txt', 'w', encoding='utf-8') as file:
    #     file.write(html_data) 
        
    # with open('html_data.txt', 'r', encoding='utf-8') as file:
    #     content = file.read()
    #     print(content)
    
    start_tag = '<span class="chat_view">'
    end_tag = "</span>"    

    try:
        return html_data.split(start_tag)[1].split(end_tag)[0].strip()
    except IndexError:
        return "None"

def demand_input_tag(tag):
    encoded_tag = quote(tag.lower().strip())
    return encoded_tag

def check_tag(tag):
    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    csv_path = os.path.join(script_dir, "data.csv")
    with open(csv_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file) 
        for row in csv_reader:
            if unquote(tag) == row.get('tag'):
                return 1             
                
def csvGenerator(temp_tag):

    input_tag = demand_input_tag(temp_tag)

    check = check_tag(input_tag)

    if check == 1:
        print("Tag already added to .csv file.")
        input("Press Enter to exit...")
        sys.exit(0)

    url = "https://www.arwords.com/words/ajax_tags/" + input_tag

    headers = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }

    params = {
        "jtStartIndex" : "0",
        "jtPageSize" : "3000"
    }

    try:
        response = requests.get(url, headers = headers, params = params)
        if response.ok:
            data = response.json()  
        else:
            sys.exit(1)   
    except Exception:
        sys.exit(1)  

    # print(json.dumps(data, indent=2, ensure_ascii=False))

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    # input("Press Enter to exit...")

    new_data = []

    if data.get("Records"):
        for item in data.get("Records"):
            new_item = {
                "word_id" : item.get("word_id"),
                "english" : item.get("def"),
                "arabic" : item.get("word"),
                "word_type" : item.get("ps"),
                "dia_codes" : item.get("dia_codes"),
                "arabic_latin" : extract_arabic_latin(item.get("word_id")),
                "tag" : extract_tag(url)
            }
            print(new_item)
            new_data.append(new_item)

    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(new_data, file, ensure_ascii=False, indent=2)  
        

    script_dir = os.path.dirname(os.path.abspath(__file__)) 
    csv_path = os.path.join(script_dir, "data.csv")

    fieldnames = ["tag", "word_type", "arabic", "english", "arabic_latin", "word_id"]

    with open(csv_path, 'a', encoding='utf-8', newline='') as file: # newline to remove skipped lines
        csv_writer = csv.DictWriter(file, fieldnames = fieldnames)  # fieldnames is an argument in DictWriter that specifies the csv columns
        for item in new_data:
            if "1" in item.get("dia_codes"):
                csv_writer.writerow({
                    "tag" : item.get("tag"),
                    "word_type" : item.get("word_type"),
                    "arabic" : item.get("arabic"),
                    "english" : item.get("english"),
                    "arabic_latin" : item.get("arabic_latin")    
                })



# csvGenerator("color")
# csvGenerator("new testament")
# csvGenerator("finances")
# csvGenerator("life")
# csvGenerator("war")
# csvGenerator("power")
# csvGenerator("eating")
# csvGenerator("military")
# csvGenerator("weather")
# csvGenerator("feelings")
# csvGenerator("history")
# csvGenerator("middle east")
# csvGenerator("work")
# csvGenerator("children")
# csvGenerator("personality")
# csvGenerator("law")
# csvGenerator("family")
# csvGenerator("cars")
# csvGenerator("nature")
# csvGenerator("home")
# csvGenerator("speech")
# csvGenerator("motion")
# csvGenerator("society")
# csvGenerator("health")
# csvGenerator("money")
# csvGenerator("government")
# csvGenerator("time")
# csvGenerator("people")
# csvGenerator("relationships")
# csvGenerator("communication")
# csvGenerator("business")
# csvGenerator("religion")
# csvGenerator("politics")
# csvGenerator("1: most frequent")
# csvGenerator("2: very frequent")
# csvGenerator("3: frequent")
# csvGenerator("4: infrequent")
# csvGenerator("5: rare")
# csvGenerator("a: most frequent")
# csvGenerator("arabic bible svd")
# csvGenerator("c: frequent")



#3 things to do:
#change name of test.py // DONE
#remove items that are not in Lebanese dialect (look through data.json generated by test.py, there is a key that checks the dialects for a particular word) // DONE
#add a button in trnaslator to change the arabic_latin of the csv if I dont like it // DONE
