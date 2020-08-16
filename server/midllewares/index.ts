import express, { Express } from 'express';
import morgan from 'morgan';
import cookieParser from 'cookie-parser';

import lightTheme from 'highlight.js/styles/atom-one-light.css';
import darkTheme from 'highlight.js/styles/atom-one-dark.css';

import { manifestHelper } from './manifestHelper';
import { paths } from '../../config/paths';
// import { webpackDevServer } from './webpackDevServer';

const isDev = process.env.NODE_ENV === 'development';

export const middlewares = async (app: Express) => {
  // log requests basic info
  app.use(morgan('dev'));

  // body parser
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  app.use(cookieParser());

  // handle static files via nginx server.
  if (isDev) {
    app.use(express.static(paths.buildWeb));
  }

  // help to read and parse manifest file to get assets paths.
  app.use(manifestHelper(paths.manifest));

  app.use((req, res, next) => {
    res.locals.meta = {
      defaultTitle: 'Mahmoud Ashraf',
      defaultDescription: "Mahmoud Ashraf's sapce on the internet.",
    };

    const { assetPath } = res.locals;

    const codeTheme = [
      { href: `/${darkTheme}`, name: 'dark-theme' },
      { href: `/${lightTheme}`, name: 'light-theme' },
    ];

    const styles = [{ href: assetPath('app.css'), name: 'app' }];
    const scripts = [assetPath('app.js'), assetPath('vendor.js')];

    res.locals.styles = styles.filter(Boolean);
    res.locals.scripts = scripts.filter(Boolean);
    res.locals.codeTheme = codeTheme.filter(Boolean);

    res.locals.url = req.url;

    res.locals.cookies = req.cookies;

    next();
  });
};
