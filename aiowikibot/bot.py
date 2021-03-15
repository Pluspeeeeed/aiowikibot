import httpx
import asyncio
import ujson as json


class Bot:
    def __init__(self, username, password, api_url):
        self.username = username
        self.password = password
        self.api_url = api_url
        self.client = httpx.AsyncClient()
        
    async def close(self):
        await self.client.aclose()
    
    async def ask(self, ask_args):
        client = self.client
        
        post_data = {'format': 'json', 'action': 'ask', 'query': ask_args, 'api_version': '3'}
        
        r = await client.post(self.api_url, data=post_data)
        
        return r.json()["query"]
    
    async def write_wiki(self, title, text, summary, **others):
        client = self.client
        
        token = await self.fetch_token()
        post_data = {'format': 'json', 'action': 'edit', 'assert': 'user', 'text': text, 'summary': summary, 'title': title, 'token': token, 'minor': 1}
        for k in others:
            post_data[k] = others[k]
            
        r = await client.post(self.api_url, data=post_data)
        
        print(r.text)
        
    async def read_wiki(self, title):
        client = self.client
        
        res = await client.post(self.api_url, data={'format': 'json', 'action': 'query', 'assert': 'user', 'titles': title, 'prop': 'revisions', 'rvprop': 'content'})
        
        ret = res.json()['query']['pages']
        for k in ret:
            ret = ret[k]
            break
        
        return ret["revisions"][0]["*"] 
        
    async def fetch_token(self):
        client = self.client
        
        token = await client.get(self.api_url, params={'format': 'json', 'action': 'query', 'meta': 'tokens'})
        token.raise_for_status()
        
        csrf = token.json()['query']['tokens']['csrftoken']
        return csrf
        
    async def login_wiki(self):
        client = self.client
        
        lgtoken = await client.get(self.api_url, params={'format': 'json', 'action': 'query', 'meta': 'tokens', 'type': 'login'})
        lgtoken.raise_for_status()
        
        res = await client.post(self.api_url, data={'format': 'json', 'action': 'login', 'lgname': self.username, 'lgpassword': self.password, 'lgtoken': lgtoken.json()['query']['tokens']['logintoken']})
        
        if res.json()['login']['result'] != 'Success':
            raise RuntimeError(res.json()['login']['reason'])
        
        return