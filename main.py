import openai

with open("hidden.txt") as file:
    openai.api_key = file.read()

def get_api_response(prompt: str) -> str | None:
    text: str | None = None
    
    try:
        response: dict = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.2,
            stop=["Human:", "AI:"]
        )
        print(response['choices'][0]['message']['content'])
        choices:dict = response.get('choices')[0]
        text = choices.get('text')


    except Exception as e:
        print("Error:", e)
    return text

def update_list(message: str, pl:list[str]):
    pl.append(message)

def create_prompt(message:str, pl:list[str])-> str:
    p_message:str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt:str = ''.join(pl)
    return prompt

def get_response(message:str, pl:list[str])-> str:
    prompt:str = create_prompt(message, pl)
    bot_response:str = get_api_response(prompt)

    if bot_response:
        update_list(bot_response, pl)
        pos:int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos+5:]
    else:
        bot_response = "Sorry, Something went wrong. Please try again."

    return bot_response


def main():
    prompt_list:list[str] = ["You are an human assistant that helps people with info only about Blood Donation and nothing else. You are based in India and hence know only of things that go in Indian hospitals. You are not a doctor but you know a lot about blood donation. You are a very helpful assistant.",
    "\nHuman: Hello, I am looking for information about blood donation.",
    "\nAI: Hello, how can I help you today?",
    "\nHuman: I would like to know more about blood donation.",
    "\nAI: Sure, what would you like to know?",
    "\nHuman: What is blood donation?",
    "\nAI: Blood donation is the process of giving blood to people who need it.",
    "\nHuman: Thank You",
    "\nAI: You're welcome.",
    ]

    try:
        while True:
            user_input:str = input("You: ")
            response: str = get_response(user_input, prompt_list)
            print("Bot:", {response})
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()