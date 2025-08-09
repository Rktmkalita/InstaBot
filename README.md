# Download posts from reddit and post to instagram
# 🤖 Instagram Reddit Bot

An automated bot that fetches memes/images from a chosen subreddit and posts them to Instagram at random intervals.  
It runs as a Flask API with a built-in scheduler so you can start, stop, and control it remotely.

---

## 🚀 Features
- Pulls images from any subreddit.
- Automatically uploads them to Instagram.
- Configurable posting intervals and sleep times.
- Remote control via simple REST API.
- Prevents reposting the same Reddit post.
- Runs locally or on cloud platforms like **Koyeb**, **Render**, **Fly** **Railway**.

---

The creds need to be added to .env file
  * INSTA_USERNAME=
  * INSTA_PASSWORD=
  * REDDIT_CLIENT_ID=
  * REDDIT_CLIENT_SECRET=
  * REDDIT_USER_AGENT=

---


## 📡 API Endpoints
Run app.py and hit the endpoints there -

### **1. Start Scheduler**
`POST /start`  
Starts the background scheduler to begin posting automatically.

---

### **2. Stop Scheduler**
`POST /stop`  
Stops the background scheduler.

---

### **3. Run Bot Immediately**
`POST /run-now`  
Runs the bot instantly, ignoring the regular schedule and sleep hours.

---

### **4. Get Config**
`GET /config`  
Returns the current bot configuration.

---

### **5. Update Config**
`POST /config`  
Updates bot configuration.  
**Example Request Body:**
```json
{
  "category": "funny",
  "max_posts": 5,
  "timezone": "Asia/Kolkata",
  "sleep_hours": ["00:00", "08:00"],
  "upload_interval": [60, 180]
}
```

---

### **6. Get Scheduler Status**
`GET /status`
Returns whether the scheduler is running and the next run time.

---

### **7. Get Logs**
`GET /logs`
Returns the last 100 log entries from the bot.

---

⚠ Disclaimer: 
This bot is for educational purposes only.
Using automation on Instagram may violate Instagram's Terms of Service.
Use responsibly and at your own risk.
