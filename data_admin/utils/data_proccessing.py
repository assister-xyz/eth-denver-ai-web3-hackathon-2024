from bs4 import BeautifulSoup

def process_body(body):
    soup = BeautifulSoup(body, 'html.parser')
    for code_tag in soup.find_all('code'):
        code_tag.replace_with(f"```{code_tag.text}```")
    for li_tag in soup.find_all('li'):
        li_tag.replace_with(f"- {li_tag.text}")
    return soup.get_text(separator='\n')
