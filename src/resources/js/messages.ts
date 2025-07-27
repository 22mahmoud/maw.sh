import Alpine from 'alpinejs';

Alpine.data('messages', () => ({
  visible: false,
  timeout: null,

  init() {
    this.$nextTick(() => {
      const i = Number(this.$el.getAttribute('data-counter') ?? 0);
      const delay = 150 * Math.sqrt(i);
      setTimeout(() => {
        this.visible = true;
        this.timeout = setTimeout(() => {
          this.visible = false;
        }, 4000);
      }, delay);
    });
  },

  stop() {
    clearTimeout(this.timeout);
  },

  play() {
    this.timeout = setTimeout(() => {
      this.visible = false;
    }, 4000);
  },

  get opened() {
    return this.visible;
  },

  get closed() {
    return !this.visible;
  },

  close() {
    this.visible = false;
  },
}));
