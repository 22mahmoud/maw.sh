import Alpine from 'alpinejs';

Alpine.data('guestbookEditor', () => {
  const presets = [
    {
      name: 'Sunset Vibes',
      bg: 'bg-sunset',
      text: 'text-white',
      font: 'font-serif',
      radius: 'rounded-xl',
      emoji: '🌅',
    },
    {
      name: 'Retro Wave',
      bg: 'bg-darker',
      text: 'text-accent',
      font: 'font-mono',
      radius: 'rounded-md',
      emoji: '🕹️',
    },
    {
      name: 'Bright Pop',
      bg: 'bg-accent',
      text: 'text-black',
      font: 'font-sans',
      radius: 'rounded-3xl',
      emoji: '🎉',
    },
    {
      name: 'Minimal',
      bg: 'bg-dark',
      text: 'text-white',
      font: 'font-sans',
      radius: 'rounded-lg',
      emoji: '🖤',
    },
    {
      name: 'Calm Forest',
      bg: 'bg-gradient-1',
      text: 'text-white',
      font: 'font-serif',
      radius: 'rounded-xl',
      emoji: '🌲',
    },
    {
      name: 'Golden Hour',
      bg: 'bg-gradient-2',
      text: 'text-black',
      font: 'font-sans',
      radius: 'rounded-lg',
      emoji: '🌞',
    },
    {
      name: 'Night Neon',
      bg: 'bg-darker',
      text: 'text-accent',
      font: 'font-mono',
      radius: 'rounded-xl',
      emoji: '🌌',
    },
  ];

  return {
    form: {
      name: '',
      message: '',
      emoji: '',
      url: '',
      bg: 'bg-white',
      text: 'text-black',
      font: 'font-sans',
      radius: 'rounded-lg',
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
