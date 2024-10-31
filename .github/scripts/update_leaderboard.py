import os
from github import Github
from collections import defaultdict

# Points mapping based on label names
points_map = {
    "level1": 10,
    "level2": 25,
    "level3": 45
}

# Function to fetch closed pull requests from GitHub using the github library
def get_closed_prs(repo):
    prs = repo.get_pulls(state='closed')
    return prs

# Function to generate the leaderboard in markdown format
def generate_leaderboard_md(leaderboard):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["points"], reverse=True)
    md_content = "# Leaderboard\n\n"
    md_content += "| Avatar | Username | Points |\n"
    md_content += "|--------|----------|--------|\n"
    
    for user, data in sorted_leaderboard:
        points = data["points"]
        avatar_url = data["avatar_url"]
        md_content += f'| <img src="{avatar_url}" width="50" height="50"> | {user} | {points} |\n'
    
    return md_content

# Main function to fetch PRs, calculate leaderboard points, and save to file
def main():
    gh_token = os.getenv("GH_TOKEN")
    gh_repo = os.getenv("GITHUB_REPOSITORY")

    if not gh_token or not gh_repo:
        print("Environment variables GH_TOKEN and GITHUB_REPOSITORY must be set.")
        return

    # Authenticate and access repository
    g = Github(gh_token)
    repo = g.get_repo(gh_repo)
    
    prs = get_closed_prs(repo)
    leaderboard = defaultdict(lambda: {"points": 0, "avatar_url": ""})

    # Process each PR and calculate points based on labels
    for pr in prs:
        user = pr.user.login
        avatar_url = pr.user.avatar_url
        labels = pr.labels
        
        for label in labels:
            label_name = label.name
            if label_name in points_map:
                leaderboard[user]["points"] += points_map[label_name]
                leaderboard[user]["avatar_url"] = avatar_url

    # Generate markdown content for the leaderboard
    leaderboard_md = generate_leaderboard_md(leaderboard)

    # Save the leaderboard to leaderboard.md
    try:
        with open('leaderboard.md', 'w') as f:
            f.write(leaderboard_md)
        print("Leaderboard updated successfully!")
    except IOError as e:
        print(f"Error writing to leaderboard.md: {e}")

if __name__ == "__main__":
    main()
