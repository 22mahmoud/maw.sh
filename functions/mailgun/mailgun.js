const fetch = require('node-fetch');
const Mailgun = require('mailgun-js');

const API_KEY = process.env.MAILGUN_API_KEY;
const DOMAIN = process.env.MAILGUN_DOMAIN;

const sendThankyouEmail = async ({ email }) => {
  return new Promise((resolve, reject) => {
    console.log('Sending the email');
    const mailgun = Mailgun({
      apiKey: API_KEY,
      domain: DOMAIN,
    });

    const mailData = {
      from: 'Mahmoud Ashraf <hello@mahmoudashraf.dev>',
      to: email,
      subject: `Thank You! 🎆`,
      text: 'Thanks you for subscribing to my newsletter!',
    };

    mailgun.messages().send(mailData, err => {
      if (err) return reject(err);

      resolve();
    });
  });
};

const addToMailingList = async ({ name, email: address, listName }) => {
  return new Promise((resolve, reject) => {
    console.log('Adding to the mailing list');
    const mailgun = Mailgun({
      apiKey: API_KEY,
      domain: DOMAIN,
    });

    const list = mailgun.lists(listName);
    list.members().create({ name, address }, err => {
      if (err) {
        if (err.message.includes('Address already exists')) {
          resolve();
        } else {
          return reject(err);
        }
      }
      resolve();
    });
  });
};

exports.handler = async function(event) {
  try {
    if (event.httpMethod !== 'POST' || !event.body) {
      return {
        statusCode: 400,
        body: `${event.httpMethod} http medthod is not allowed!`,
      };
    }
    const body = JSON.parse(event.body);
    const { email, name } = body;

    await addToMailingList({
      email,
      name,
      listName: 'hello@mahmoudashraf.dev',
    });
    await sendThankyouEmail({ email });
    return {
      statusCode: 200,
      body: JSON.stringify({
        message: 'thank you',
      }),
    };
  } catch (error) {
    console.error(error);
    return {
      statusCode: 500,
      body: error.message,
    };
  }
};
