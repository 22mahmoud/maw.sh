import { getPost } from '../../utils/posts.js';
import grayMatter from 'gray-matter';
import marked from 'marked';
import hljs from 'highlight.js';

export function get(req, res) {
  const { slug } = req.params;

  // retrive post md file text by provide his name
  const post = getPost(`${slug}/index.md`);

  // function that expose helpful callbacks
  // to manipulate the data before convert it into html
  const renderer = new marked.Renderer();

  // use hljs to highlight our blaock of codes
  renderer.code = (source, lang) => {
    const { value: highlighted } = hljs.highlight(lang, source);
    return `<pre class='language-javascriptreact'><code>${highlighted}</code></pre>`;
  };

  // convert md text into object and remove escaping characters
  // meta => header of md srounded by ======
  // content => modified content
  const { data: meta, content } = grayMatter(post);

  // finally convert the md to html and be ready to sent back to svelte
  const html = marked(content, { renderer });

  if (post) {
    res.writeHead(200, {
      'Content-Type': 'application/json',
    });

    res.end(JSON.stringify({ content: html, meta }));
  } else {
    res.writeHead(404, {
      'Content-Type': 'application/json',
    });

    res.end(
      JSON.stringify({
        message: `Not found`,
      })
    );
  }
}
