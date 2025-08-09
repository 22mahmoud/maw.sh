import Alpine from 'alpinejs';

Alpine.data('headerNav', () => ({
  open: false,

  init() {
    window.addEventListener('scroll', () => {
      this.$el.classList.toggle('shadow-xl', window.scrollY > 10);
    });
  },

  get openStr() {
    return this.open ? 'true' : 'false';
  },

  get opened() {
    return this.open;
  },

  get closed() {
    return !this.open;
  },

  toggle() {
    this.open = !this.open;
  },

  close() {
    this.open = false;
  },
}));
