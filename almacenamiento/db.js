require('dotenv').config();
const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      dbName: 'eventosdb'
    });
    console.log("✅ Conectado a MongoDB Atlas");
  } catch (err) {
    console.error("❌ Error conectando a MongoDB:", err.message);
    process.exit(1);
  }
};

module.exports = connectDB;
