const { spawn } = require('child_process');
const dependencies = {
  'darwin': [
    'dmg-builder@24.0.0-alpha.3',
    'dmg-license@1.011'
  ]
};

const platform = process.platform;

if (platform === 'darwin') {
  console.log(`  \x1b[34m\u2022\x1b[0m installing dependent platform dependencies for ${platform}`)

  const onData = function (chunk) {
    const data = chunk.toString();
    console.log(data);
  }

  const yarn = spawn('yarn', ['add', dependencies[platform].join(' ')]);

  yarn.stdout.on('data', onData)
  yarn.stderr.on('data', onData)
  yarn.on('close', function (code) {
    console.log(`  \x1b[34m\u2022\x1b[0m dependent platform dependencies for ${platform} exit code: ${code}`)
  });
} else {
  console.log(`  \x1b[34m\u2022\x1b[0m skipping dependent platform dependencies for ${platform}`)
}
