import fs from 'fs';
import { Request, Response, NextFunction } from 'express';

interface Manifet {
  'app.css'?: string;
  'vendor.css'?: string;
  'app.js'?: string;
  'vendor.js'?: string;
}

let manifest: Manifet;

function loadManifest(path: string): Manifet {
  // if (manifest) return manifest;

  try {
    const file = fs.readFileSync(path, 'utf8');
    return JSON.parse(file);
  } catch (err) {
    throw new Error('Asset Manifest could not be loaded.');
  }
}

function lookup(path: string, source: keyof Manifet): string | undefined {
  manifest = loadManifest(path);

  if (manifest[source]) {
    return manifest[source];
  }

  return '';
}

const assetPath = (path: string) => (
  source: keyof Manifet
): string | undefined => {
  return lookup(path, source);
};

const manifestHelper = (path: string) => (
  _req: Request,
  res: Response,
  next: NextFunction
): void => {
  res.locals.assetPath = assetPath(path);
  next();
};

export { manifestHelper };
