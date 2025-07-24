import Alpine from 'alpinejs';
import DOMPurify from 'dompurify';
import { marked } from 'marked';

type Preset = {
  id: string;
  name: string;
  emoji: string;
  radius: string;
  styles: string;
};

const allowedTags = [
  'p',
  'br',
  'strong',
  'em',
  'code',
  'pre',
  'ul',
  'ol',
  'li',
  'h1',
  'h2',
  'h3',
  'h4',
  'h5',
  'h6',
  'img',
];

const allowedImgDomains = ['.giphy.com', '.tenor.com', '.imgur.com'];
const allowedAttrs = ['src', 'alt', 'height', 'width'];

DOMPurify.addHook('uponSanitizeAttribute', (node, data) => {
  const tag = node.nodeName.toLowerCase();

  if (tag === 'img') {
    if (!allowedAttrs.includes(data.attrName)) {
      data.keepAttr = false;
      return;
    }

    if (data.attrName === 'src' && !isValidImgSrc(data.attrValue)) {
      data.keepAttr = false;
    }
  } else {
    data.keepAttr = false;
  }
});

function isValidImgSrc(value: string): boolean {
  try {
    const url = new URL(value, 'https://placeholder');
    const hostname = url.hostname;
    return !hostname || allowedImgDomains.some(d => hostname.endsWith(d));
  } catch {
    return false;
  }
}

Alpine.data('guestbookEditor', () => {
  const dataElm = document.getElementById('guestbook-editor-presets');
  const raw = dataElm?.textContent;

  let presets: Preset[];

  try {
    if (!raw) throw new Error('No preset data found');

    presets = JSON.parse(raw) as Preset[];

    if (!Array.isArray(presets)) {
      throw new Error('Invalid preset format');
    }
  } catch (err) {
    console.error('Failed to parse presets:', err);
    presets = [];
  }

  return {
    form: {
      name: '',
      message: '',
      url: '',
      radius: '',
      emoji: presets[0]?.emoji ?? '',
      style: presets[0]?.id ?? '',
    },
    isPreviewOpen: true,
    presets,
    get currentPreset() {
      return this.presets.find(p => p.id === this.form.style) ?? this.presets[0];
    },
    get classes() {
      return `${this.currentPreset.styles} ${this.form.radius}`;
    },
    async renderMarkdown(md: string = '') {
      const rawHtml = await marked.parse(md);

      const cleanHtml = DOMPurify.sanitize(rawHtml, {
        ALLOWED_TAGS: allowedTags,
        ALLOWED_ATTR: allowedAttrs,
      });

      return cleanHtml;
    },
  };
});
