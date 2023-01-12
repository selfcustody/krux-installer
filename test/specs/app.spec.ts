import App from '../pageobjects/app.page'
import Logo from '../pageobjects/logo.page'

describe('KruxInstaller', () => {

  it('should launch with correct title', async () => {
    expect(App.title).toHaveText('krux-installer')
  })
})


