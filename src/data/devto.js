const fetch = require('node-fetch');

function makeRelativeUrl(url) {
  const urlObj = new URL(url);
  return urlObj.pathname;
}

module.exports = async () => {
  const res = await fetch('https://dev.to/api/articles?username=22mahmoud');
  const data = await res.json();

  return data.reduce(
    (acc, curr) => ({ ...acc, [makeRelativeUrl(curr.canonical_url)]: curr }),
    {}
  );
};
