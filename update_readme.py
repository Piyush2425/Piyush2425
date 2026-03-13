#!/usr/bin/env python3

import os
import requests
import re

def get_repositories(username, token):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    params = {"type": "public", "sort": "updated", "per_page": 100}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    repos = response.json()
    return repos

def generate_mission_log(repos):
    # Filter out the profile repo itself
    repos = [repo for repo in repos if repo['name'] != 'Piyush2425']

    # Sort by updated date, most recent first
    repos.sort(key=lambda x: x['updated_at'], reverse=True)

    # Take top 10 or so
    repos = repos[:10]

    lines = []
    lines.append('<div align="center">\n\n| ⬡ CODENAME | 👾 ALIEN DEPLOYED | 🎯 MISSION BRIEF | STATUS |\n|:---:|:---:|:---|:---:|')

    alien_emojis = ['🔥', '🧠', '👁️', '⚡', '👻', '🌊', '🛡️', '🌐', '💎', '🚀']

    for i, repo in enumerate(repos):
        name = repo['name']
        url = repo['html_url']
        description = repo['description'] or "No description available"
        # Determine status based on if it's archived or has issues
        if repo['archived']:
            status = "🔵 ARCHIVED"
        elif repo['has_issues'] and not repo['private']:
            status = "🟢 LIVE"
        else:
            status = "🟡 WIP"

        # Cycle through aliens
        alien = alien_emojis[i % len(alien_emojis)]

        lines.append(f'| [{name}]({url}) | **{alien}** | {description} | {status} |')

    lines.append('\n</div>\n\n---')
    return '\n'.join(lines)

def update_readme():
    username = "Piyush2425"
    token = os.getenv("GITHUB_TOKEN")

    repos = get_repositories(username, token)
    mission_log = generate_mission_log(repos)

    # Read current README
    with open("README.md", "r") as f:
        content = f.read()

    # Replace the MISSION LOG section
    pattern = r'(## 📋 MISSION LOG — ACTIVE OPERATIONS\n\n).*?(\n\n## 📊 OMNITRIX POWER READINGS)'
    replacement = r'\1' + mission_log + r'\2'

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Write back
    with open("README.md", "w") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()