# Postman Testing Guide

## 🚀 API Server is Running

**Base URL:** `http://127.0.0.1:8001`

---

## 📋 Postman Collection

### 1. Health Check

**Method:** `GET`  
**URL:** `http://127.0.0.1:8001/health`

**Headers:** None required

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "message": "Service is running and ready to translate"
}
```

---

### 2. Translate English to Hinglish

**Method:** `POST`  
**URL:** `http://127.0.0.1:8001/translate`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "text": "hello how are you"
}
```

**Expected Response (Success):**
```json
{
  "original_text": "hello how are you",
  "hinglish_text": "namaste Apa kaise ho",
  "success": true,
  "error": null
}
```

**Expected Response (Error - if SSL issue):**
```json
{
  "original_text": "hello how are you",
  "hinglish_text": "",
  "success": false,
  "error": "Translation error: ..."
}
```

---

## 📝 Test Cases for Postman

### Test Case 1: Simple Greeting
```json
{
  "text": "hello"
}
```

### Test Case 2: Question
```json
{
  "text": "what are you doing"
}
```

### Test Case 3: Common Phrase
```json
{
  "text": "good morning"
}
```

### Test Case 4: Longer Sentence
```json
{
  "text": "I am going to the market"
}
```

### Test Case 5: Gratitude
```json
{
  "text": "thank you very much"
}
```

### Test Case 6: Empty Text (Should Fail)
```json
{
  "text": ""
}
```

**Expected:** 422 Unprocessable Entity

### Test Case 7: Very Long Text (Should Fail)
```json
{
  "text": "a very long text with more than 1000 characters..."
}
```

**Expected:** 422 Unprocessable Entity

---

## 🔧 How to Import in Postman

### Option 1: Manual Setup

1. Open Postman
2. Create a new Collection named "English to Hinglish API"
3. Add requests as described above

### Option 2: Quick Setup Steps

1. **Create Collection**
   - Click "New" → "Collection"
   - Name: "English to Hinglish API"

2. **Add Health Check Request**
   - Click "Add Request"
   - Name: "Health Check"
   - Method: GET
   - URL: `http://127.0.0.1:8001/health`
   - Click "Save"

3. **Add Translation Request**
   - Click "Add Request"
   - Name: "Translate"
   - Method: POST
   - URL: `http://127.0.0.1:8001/translate`
   - Go to "Headers" tab:
     - Key: `Content-Type`
     - Value: `application/json`
   - Go to "Body" tab:
     - Select "raw"
     - Select "JSON" from dropdown
     - Paste:
       ```json
       {
         "text": "hello how are you"
       }
       ```
   - Click "Save"

---

## 🎯 Quick Test in Postman

1. Open Postman
2. Create a new request
3. Set method to **POST**
4. Set URL to: `http://127.0.0.1:8001/translate`
5. Go to **Headers** tab and add:
   - `Content-Type: application/json`
6. Go to **Body** tab:
   - Select **raw**
   - Select **JSON** from dropdown
7. Paste this payload:
   ```json
   {
     "text": "hello how are you"
   }
   ```
8. Click **Send**

---

## 📊 Alternative: Using Swagger UI

You can also test the API using the built-in Swagger UI:

**URL:** `http://127.0.0.1:8001/docs`

1. Open this URL in your browser
2. Click on the endpoint you want to test
3. Click "Try it out"
4. Enter your data
5. Click "Execute"

---

## 🛑 Stop the Server

To stop the API server, press `CTRL+C` in the terminal where it's running.

---

## 💡 Note

If you see SSL certificate errors in the response, refer to `SSL_TROUBLESHOOTING.md` for solutions. The API structure works correctly; the error is only in the translation service connection.
