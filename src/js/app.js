import '../styles/base/fonts.css';
import '../styles/base/normalize.css';
import '../styles/base/typography.css';

import '../styles/utils/variables.css';

import '../styles/vendor/prismjs.css';

import '../styles/components/hero.css';
import '../styles/components/blogs.css';
import '../styles/components/header.css';
import '../styles/components/markdown.css';
import '../styles/components/container.css';

import Lazyload from 'vanilla-lazyload';

const lazyload = new Lazyload();

document.addEventListener('DOMContentLoaded', () => {
  lazyload.update();
});
