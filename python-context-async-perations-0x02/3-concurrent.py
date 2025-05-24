import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: List of all user records.
    """
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: List of user records where age > 40.
    """
    async with aiosqlite.connect('users.db') as conn:
        cursor = await conn.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        await cursor.close()
        return results

async def fetch_concurrently():
    """
    Run both fetch queries concurrently using asyncio.gather.
    
    Returns:
        tuple: Results of both queries (all users, older users).
    """
    try:
        all_users, older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )
        return all_users, older_users
    except Exception as e:
        print(f"Error during concurrent fetch: {e}")
        return [], []


if __name__ == "__main__":
    results = asyncio.run(fetch_concurrently())
    all_users, older_users = results
    print("All users:", all_users)
    print("Users older than 40:", older_users)