import App from '../pageobjects/app.page'

// eslint-disable-next-line no-undef
describe('KruxInstaller', () => {

  // eslint-disable-next-line no-undef
  it('should launch with correct title', async () => {
    
    // eslint-disable-next-line no-undef
    expect(App.title).toHaveText('krux-installer')
  })
})


