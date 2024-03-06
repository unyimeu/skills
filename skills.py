import openai
import pandas as pd
import os
import sample_data as data
import asyncio
import aiohttp
import ssl
import certifi
import warnings
#make sure to install requirements
#RUN THIS FILE

warnings.simplefilter(action='ignore', category=FutureWarning)

def GPT_calls(prompts,api_key):
    # Settings
    MODEL = "gpt-3.5-turbo"
    OPENAI_SECRET_KEY = api_key

    # Call ChatGPT with the given prompt, asynchronously.
    async def call_chatgpt_async(session, prompt: str):
        payload = {
            'model': MODEL,
            'messages': [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            async with session.post(
                url='https://api.openai.com/v1/chat/completions',
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_SECRET_KEY}"},
                json=payload,
                ssl=ssl.create_default_context(cafile=certifi.where())
            ) as response:
                response = await response.json()
            if "error" in response:
                print(f"OpenAI request failed with error {response['error']}")
            return response['choices'][0]['message']['content']
        except:
            print("Request failed.")

    # Call chatGPT for all the given prompts in parallel.
    async def call_chatgpt_bulk(prompts):
        async with aiohttp.ClientSession() as session, asyncio.TaskGroup() as tg:
            responses = [tg.create_task(call_chatgpt_async(session, prompt)) for prompt in prompts]
        return responses
    
    results = asyncio.run(call_chatgpt_bulk(prompts))

    return results
    

def prompt_creation(data):
    prompts = []
    for index, row in data.iterrows():
        name = row['Title']
        descp = 'Course Prereqs:{}'.format(row['Prereqs']) + '\n'+ row['Description']
        prompts.append(f"""You are a domain expert of numerous MIT fields/course subjects. I will be providing you with the name of a course and
                       an extremely detailed description of the course. Your job is to read the course descriptions and give 3 - 10 
                       skills that will likely be learned from the course. Ensure that the course skills are very specific to the
                       course itself and the data that is in the course.
                       
                       Now, the name of the course is {name} and here is the course description: {descp}\n Please only provide the skills
                       as asked for. An example response could look like this for one hypothetical class:\nPython,Dynamic Programming, Compiler Implementation, Software.
                       Do not say anythign extra. Just provide the skills no extra words. 
                        """)
    
    return prompts

def get_skills(responses):
    skills = []
    for response in responses:
        skills.append(response.result())
    return skills

def populate_df(df,skills):

    for i in range(len(df['skills'])):
        if df['skills'][i] ==None:  
            if not skills: break  
            df['skills'][i] = skills[0]
            print('-----------------------------------')
            print(f"Course Name: {df['Title'][i]} ; Extracted Skills: {skills[0]}")
            print('-----------------------------------')
            skills= skills[1:]
    df.to_csv('classes.csv')
    return df



def bacth_requests(df,prompts,api_key,batch=2):
    rest = prompts
    while rest:
        first_two = rest[:batch]
        rest = rest[batch:]
        print('Calling gpt======================>')
        gpt = GPT_calls(first_two,api_key)
        skills = get_skills(gpt)
        print('Updating the df ================>')
        df = populate_df(df,skills)


def main():
    api_key=os.getenv("OPENAI_API_KEY")
    api_key = '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'

    courses = pd.read_csv('classes.csv')
    courses['skills'] = None #create an empty skills column

    print('creating prompts')
    prompts = prompt_creation(courses)

    print('starting to batch requests')
    bacth_requests(courses,prompts,api_key)
    

if __name__ == '__main__':
    main()
    