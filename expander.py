#!/usr/bin/env python3
#-------------------------------------------------------------------------------------------------------------------------------------------#
#IMPORTS
from requests import head as http
from argparse import ArgumentParser
from sys import stdin
from re import compile as recompile,findall,IGNORECASE
from csv import writer as csvwriter

#-------------------------------------------------------------------------------------------------------------------------------------------#
# Parse Args
if stdin.isatty():
  parser = ArgumentParser()
  parser.add_argument("-u", "--url", type=str, required=False, help="URL or URLs to expand")
  args = parser.parse_args()
  if args.url and ',' in args.url:
    content = '\n'.join(str(v) for v in args.urls.split(','))
  else:
    content = args.url
else:
  content = stdin.read()

#-------------------------------------------------------------------------------------------------------------------------------------------#
#FUNCTIONS
def parse_urls(content):
  """Regex for URLs in content"""
  if not content:
    return
  regex=recompile(r'(?P<url>(?:http|ftp)s?://'  # scheme
                         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                         r'localhost|'  # localhost...
                         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
                         r'(?::\d+)?'  # optional port
                         r'\/?.+)', IGNORECASE)
  return findall(regex, content)

def expand_url(short_url):
  """Expand a shortened URL using requests module"""
  try:
    # Send a HEAD request to the short URL to get the Location header
    response = http(short_url, allow_redirects=False)
    return response.headers['Location'] if 'Location' in response.headers else ''
  except Exception as e:
    print("Error expanding URL: ", e)
    return ''

def write_to_csv(my_dict):
    """Write dict to csv"""
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csvwriter(csvfile)
        writer.writerow(my_dict.keys())
        writer.writerows(zip(*my_dict.values()))
def main(URLS):
  results = [{u:expand_url(u)} for u in URLS]
  if len(results) >= 10:
    output = {'short':[], 'long':[]}
    for d in results:
        for key, value in d.items():
            output['short'].append(key)
            output['long'].append(value)
    write_to_csv(output)
    print("[*] Output saved to output.csv")
  else:
     for d in results:
        print(','.join(f'{x},{y}' for x,y in d.items()))



#-------------------------------------------------------------------------------------------------------------------------------------------#
#EXECUTE
URLS=parse_urls(content)
if URLS:
  main(URLS)
else:
  print("[!] Nothing to do...")
  exit()

