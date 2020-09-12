const { spawn } = require('child_process');

function generateSW() {
  return spawn(`yarn`, ['sw'], {
    shell: true,
    stdio: 'inherit',
  });
}

module.exports = {
  generateSW,
};
