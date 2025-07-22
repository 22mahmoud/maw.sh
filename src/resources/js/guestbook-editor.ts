import Alpine from 'alpinejs';

type Preset = {
  name: string;
  bg: string;
  text: string;
  font: string;
  radius: string;
  emoji: string;
};

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
      emoji: presets[0].emoji,
      url: '',
      bg: presets[0].bg,
      text: presets[0].text,
      font: presets[0].font,
      radius: presets[0].radius,
    },
    presets,
    applyPreset(index: number) {
      const preset = this.presets[index];
      this.form.bg = preset.bg;
      this.form.text = preset.text;
      this.form.font = preset.font;
      this.form.radius = preset.radius;
      this.form.emoji = preset.emoji;
    },
    randomize() {
      const i = Math.floor(Math.random() * this.presets.length);
      this.applyPreset(i);
    },
  };
});
