# imports

import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

# Initialize and constants

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')  
MODEL = 'gpt-4o-mini'
openai = OpenAI()

# A class to represent a Webpage

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    A utility class to represent a Website with links
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

link_system_prompt = "You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about a fund, \
such as links to Cover/Title, Fund Overview, Investment Strategy, Performance, Portfolio Holdings, \
Fees & Expenses, Risk Metrics, Additional Info, Disclosures/Contact.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt += """
{
    "links": [
        {"type": "Fund Overview page", "url": "https://full.url/goes/here/overview"},
        {"type": "Performance page": "url": "https://another.full.url/performance"}
    ]
}
"""

#print(link_system_prompt)

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the fund, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

#print(get_links_user_prompt(ed))

def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
      ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)

# fidelity = Website("https://fundresearch.fidelity.com/mutual-funds/summary/494613805")
# fidelity.links
# get_links("https://fundresearch.fidelity.com/mutual-funds/summary/494613805")


def get_all_details(url):
    result = "Landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    #print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a investment website \
and creates a short brochure about the fund for overview, investment strategy, risk apetite, asset allocation, growth prediction and performance. Respond in markdown.\
Include details of fund composition, fees and expected return if you have the information."

def get_brochure_user_prompt(fund_name, url):
    user_prompt = f"You are looking at a brochure of a fund named: {fund_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

#get_brochure_user_prompt("Kinetics Global No Load Class", "https://fundresearch.fidelity.com/mutual-funds/summary/494613805")

##### non-stream - get all and then display
# def create_brochure(fund_name, url):
#     response = openai.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": get_brochure_user_prompt(fund_name, url)}
#           ],
#     )
#     result = response.choices[0].message.content
#     display(Markdown(result))

#### Alternate streaming content
def stream_brochure(fund_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(fund_name, url)}
          ],
        stream=True
    )
    
    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```","").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)
        
stream_brochure("Kinetics Global No Load Class", "https://fundresearch.fidelity.com/mutual-funds/summary/494613805")
#create_brochure("Thornburg Investment Income Builder Fund Class I", "https://fundresearch.fidelity.com/mutual-funds/summary/885215467")
#stream_brochure("Fidelity Family Funds", "https://fundresearch.fidelity.com/fund-screener/results/table/overview/averageAnnualReturnsYear3/desc/1?assetClass=BAL&category=AL%2CCA%2CCV%2CGA%2CGC%2CGM%2CGQ%2CGX%2CMA%2CRI%2CTA%2CTD%2CTE%2CTG%2CTH%2CTI%2CTJ%2CTK%2CTL%2CTN%2CTU%2CTV%2CXA%2CXM%2CXQ%2CXY&fidelityFundOnly=F&fundFamily=&gad_campaignid=1490091060&gad_source=1&gbraid=0AAAAAD7OUhJSGftTlObWhsemuR9kPw8Xv&gclid=Cj0KCQjw8vvABhCcARIsAOCfwwpqABgVD3t3_Gc_bbOxm1blr8ncQkt4KMmNuXi-y_EA3frdaLbZpYUaAkP0EALw_wcB&gclsrc=aw.ds&imm_eid=ep35275476312&imm_pid=58700004243390943&immid=100726_SEA&order=assetClass%2Ccategory%2CfidelityFundOnly%2CfundFamily&utm_account_id=700000001009773&utm_campaign=MUT&utm_campaign_id=100726&utm_content=58700004243390943&utm_id=71700000038714008&utm_medium=paid_search&utm_source=GOOGLE&utm_term=fidelity%20mutual%20fund%20search")