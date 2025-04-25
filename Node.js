require('dotenv').config();

const express = require('express');
const admin = require('firebase-admin');
const app = express();

admin.initializeApp({
  credential: admin.credential.cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
    privateKey: process.env.FIREBASE_PRIVATE_KEY.replace(/\\n/g, '\n'),
  }),
  databaseURL: process.env.FIREBASE_DB_URL,
});

// Test route
app.get('/test', async (req, res) => {
  try {
    const db = admin.database();
    const ref = db.ref('test');
    await ref.set({ message: 'Firebase is connected!' });
    res.send('Test successful');
  } catch (error) {
    res.status(500).send('Error: ' + error.message);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
