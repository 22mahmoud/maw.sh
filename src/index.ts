import express from 'express';

const app = express();

const port = process.env.PORT || 8000;

app.get('/', (_req, res) => {
  res.send('Hello, World');
});

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`App is running at http://localhost:${port}`);
});
