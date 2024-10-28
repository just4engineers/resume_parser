import json
import yaml
import requests

# Load API key from the config.yaml file
CONFIG_PATH = r"config.yaml"

def load_google_api_key():
    with open(CONFIG_PATH) as file:
        data = yaml.safe_load(file)
        google_api_key = data['GOOGLE_API_KEY']
        return google_api_key

def ats_extractor(resume_data):
    # Load the API key from config.yaml
    api_key = load_google_api_key()

    # Define the Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    # Define the prompt to extract resume information
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes, give tips, mistakes and rate the resume out of 100 give a score in an integer. You are given a resume, and your job is to extract the following information:
    1. Full name
    2. Email address
    3. GitHub portfolio
    4. LinkedIn profile
    5. Employment details
    6. Technical skills
    7. Soft skills
    8. Rating out of 100
    9. Mistakes
    10. Tips

    Provide the extracted information only in JSON format.
    '''

    # Prepare the request payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{prompt}\n\n{resume_data}"
                    }
                ]
            }
        ]
    }

    # Make a POST request to the Gemini API
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    # Print the response status code and raw text for debugging
    print("Response Status Code:", response.status_code)
    print("Response Text:", response.text)  # Debugging output

    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()  # Attempt to parse the JSON
            # Check if 'candidates' is in the parsed data
            if 'candidates' in data and len(data['candidates']) > 0:
                generated_content = data['candidates'][0]['content']['parts'][0]['text']

                # Remove the code block formatting and parse the JSON
                json_data_str = generated_content.strip('```json\n').strip('```')
                extracted_info = json.loads(json_data_str)

                return extracted_info
            else:
                print("Key 'candidates' not found in response.")
                return None
        except ValueError as e:
            print("Error parsing JSON:", e)
            return None
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None