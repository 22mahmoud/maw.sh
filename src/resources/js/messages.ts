import Alpine from 'alpinejs';

Alpine.data('messages', () => ({
  visible: false,
  timeout: null as number | null,

  init() {
    this.$nextTick(() => {
      const index = Number(this.$el?.dataset.counter ?? 0);
      const delay = 150 * Math.sqrt(index);

      setTimeout(() => {
        this.show();
      }, delay);
    });
  },

  show() {
    this.visible = true;
    this.timeout = window.setTimeout(this.close.bind(this), 4000);
  },

  stop() {
    if (this.timeout !== null) {
      clearTimeout(this.timeout);
      this.timeout = null;
    }
  },

  play() {
    this.timeout = window.setTimeout(this.close.bind(this), 4000);
  },

  get opened() {
    return this.visible;
  },

  get closed() {
    return !this.visible;
  },

  close() {
    this.visible = false;
    this.timeout = null;
  },
}));
