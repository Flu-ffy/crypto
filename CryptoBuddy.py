import requests

def get_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        coin_info = {
            "name": data['name'],
            "symbol": data['symbol'],
            "price_usd": data['market_data']['current_price']['usd'],
            "price_change_24h": data['market_data']['price_change_percentage_24h'],
            "market_cap": data['market_data']['market_cap']['usd'],
            "market_cap_rank": data['market_cap_rank'],
            "energy_use": "low" if data['id'] in ['cardano', 'algorand'] else "high",  # estimated
            "sustainability_score": {
                "cardano": 8,
                "algorand": 7,
                "ethereum": 6,
                "bitcoin": 3
            }.get(data['id'], 5)  # fallback default
        }
        return coin_info
    else:
        return None
print("👋 Real-Time Crypto Advisor (via CoinGecko)")
print("Try: 'bitcoin', 'ethereum', 'cardano', 'solana'")
print("Type 'exit' to quit\n")

while True:
    user_query = input("You: ").lower()

    if user_query in ["exit", "quit", "bye"]:
        print("Bot: 👋 Goodbye!")
        break

    elif any(word in user_query for word in ["sustainable", "eco", "green"]):
        # Recommend from known sustainable coins
        best = max(["cardano", "algorand", "ethereum", "bitcoin"],
                   key=lambda x: get_coin_data(x)['sustainability_score'])
        best_data = get_coin_data(best)
        print(f"Bot: 🌱 {best_data['name']} is the most sustainable with a score of {best_data['sustainability_score']}/10.")

    elif any(word in user_query for word in ["trending", "rising"]):
        print("Bot: 📊 Checking trending coins...")
        top_coins = ['bitcoin', 'ethereum', 'cardano', 'solana']
        for coin in top_coins:
            data = get_coin_data(coin)
            if data and data['price_change_24h'] > 0:
                print(f"✅ {data['name']} is up {data['price_change_24h']:.2f}% in the last 24h.")

    elif any(c in user_query for c in ["bitcoin", "ethereum", "cardano", "solana"]):
        coin_id = next((c for c in ["bitcoin", "ethereum", "cardano", "solana"] if c in user_query), None)
        data = get_coin_data(coin_id)
        if data:
            print(f"🔎 {data['name']} ({data['symbol'].upper()})")
            print(f"💰 Price: ${data['price_usd']:.2f}")
            print(f"📈 24h Change: {data['price_change_24h']:.2f}%")
            print(f"🏷️ Market Cap Rank: #{data['market_cap_rank']}")
            print(f"⚡ Energy Use (est.): {data['energy_use']}")
            print(f"🌱 Sustainability Score: {data['sustainability_score']}/10")
        else:
            print("Bot: ❌ Couldn't fetch that coin's data. Try again later.")

    else:
        print("Bot: 🤔 I didn’t understand. Ask about trends, prices, or sustainability.")
