require('dotenv').config();
const express = require('express');
const connectDB = require('./db');
const Evento = require('./eventoModel');

const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST;

app.post('/eventos', async (req, res) => {
  const evento = req.body;
  const uuid = evento.uuid;

  if (!uuid) {
    return res.status(400).json({ error: 'UUID requerido' });
  }

  try {
    await Evento.create({ uuid, datos: evento });
    res.status(201).json({ status: 'Evento guardado' });
  } catch (err) {
    if (err.code === 11000) {
      res.status(200).json({ status: 'Evento duplicado (ignorado)' });
    } else {
      console.error("❌ Error al guardar:", err.message);
      res.status(500).json({ error: 'Error interno al guardar evento' });
    }
  }
});


app.get('/eventos', async (req, res) => {
  try {
    const filtro = {};

    if (req.query.type) {
      filtro['datos.type'] = req.query.type;
    }

    const eventos = await Evento.find(filtro).limit(1000);
    res.json(eventos);
  } catch (err) {
    res.status(500).json({ error: 'Error al obtener eventos' });
  }
});

app.get('/eventos/total', async (req, res) => {
  try {
    const totalEventos = await Evento.countDocuments();
    res.json({ total: totalEventos });
  } catch (err) {
    res.status(500).json({ error: 'Error al contar los eventos' });
  }
});

app.get('/eventos/por-tipo', async (req, res) => {
  try {
    const resultado = await Evento.aggregate([
      { $group: { _id: "$datos.type", total: { $sum: 1 } } }
    ]);
    res.json(resultado);
  } catch (err) {
    res.status(500).json({ error: 'Error al agrupar eventos por tipo' });
  }
});


//para testear
app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(PORT, async () => {
  await connectDB();
  console.log(`🚀 API escuchando en http://${HOST}:${PORT}`);
});
