const mongoose = require('mongoose');

const eventoSchema = new mongoose.Schema({
  uuid: { type: String, required: true, unique: true },
  datos: { type: Object, required: true }
});

module.exports = mongoose.model('Evento', eventoSchema);
