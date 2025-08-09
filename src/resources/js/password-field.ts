import Alpine from 'alpinejs';

Alpine.data('passwordField', () => ({
  show: false,

  toggle() {
    this.show = !this.show;
  },

  get inputType() {
    return this.show ? 'text' : 'password';
  },

  get isVisible() {
    return this.show;
  },

  get isHidden() {
    return !this.show;
  },

  get toggleLabel() {
    return this.show ? 'Hide password' : 'Show password';
  },
}));
