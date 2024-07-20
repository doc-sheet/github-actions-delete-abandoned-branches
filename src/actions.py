from src.github import Github
import asyncio
from src.io import Options


async def run_action(options: Options) -> list:
    print(f"Starting github action to cleanup old branches. Input: {options}")

    github = Github(
        repo=options.github_repo,
        token=options.github_token,
        base_url=options.github_base_url,
    )

    tasks = []
    branches = []
    async for branch in github.get_deletable_branches(
        last_commit_age_days=options.last_commit_age_days,
        ignore_branches=options.ignore_branches,
        allowed_prefixes=options.allowed_prefixes,
    ):
        branches.append(branch)
        if options.dry_run:
            print(f"This is a dry run, skipping deletion of branch {branch}")
        else:
            print(f"This is NOT a dry run, deleting branch {branch}")
            tasks.append(asyncio.create_task(github.delete_branches(branches=[branch])))
            await asyncio.sleep(0.1)

    print(f"Branches queued for deletion: {branches}")
    try:
        await asyncio.gather(*tasks)
    except Exception:
        raise

    return branches
