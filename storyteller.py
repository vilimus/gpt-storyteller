import os
import requests

class GPT3():
  def __init__(self, api_key):
    self.api_key = api_key

  def generate(self, prompt, model="text-davinci-003", **kwargs):
    headers = {"Authorization": f"Bearer {self.api_key}"}
    response = requests.post(
      "https://api.openai.com/v1/completions",
      headers=headers,
      json={"model": model, "prompt": prompt, **kwargs},
    )
    r = response.json()
    try:
      return r["choices"][0]["text"]
    except:
      print(r)

gpt3 = GPT3(api_key=os.getenv("OPENAI_API_KEY"))

def generate_actions(story):
  prompt = f"The following text is from an exciting text-based adventure game:\n\"{story}\"\nPresent the user with 3 possible actions:\n1."
  output = gpt3.generate(prompt, temperature=1.3, max_tokens=128, frequency_penalty=1.0,)
  opt1, opt2, opt3 = output.split("\n")
  opt1 = opt1.strip()
  opt2 = opt2[2:].strip()
  opt3 = opt3[2:].strip()
  return [opt1, opt2, opt3]

def action_to_line(action):
  return "You " + action[0].lower() + action[1:] + ("" if action.endswith(".") else ".")
  
def add_action_and_generate(story, action):
  prompt = f"The following text is from an exciting text-based adventure game:\n\"{story}\"\nThe user decided to \"{action}\"\nBased on this, generate the next sentence in the story:"
  output = gpt3.generate(prompt, temperature=1.3, max_tokens=128, frequency_penalty=1.0,)
  return output
  
if __name__ == "__main__":
  prompt = "Generate a short paragraph which serves as the introduction to a text based adventure game\nYou"
  story = gpt3.generate(prompt, temperature=1.3, max_tokens=256, frequency_penalty=1.0,)
  story = "You" + story
  story = story.strip()

  os.system("cls")
  print(story)
  input("\nPress Enter to being...")
  os.system("cls")
  print("Generating story...")

  done = False
  while not done:
    actions = generate_actions(story)
    os.system("cls")
    print(story)
    print()
    for i in range(3):
      print(f"{i+1}: {actions[i]}")
    x = input("\n>")
    action = actions[int(x)-1] if x in ["1", "2", "3"] else x
    action_line = action_to_line(action)
    story_line = add_action_and_generate(story, action)  
    action_line = action_line.strip()
    story_line = story_line.strip()
    story += "\n\n>" + action_line + "\n\n" + story_line + "\n"
    story = story.strip()
