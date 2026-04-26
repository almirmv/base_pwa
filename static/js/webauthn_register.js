const { startAuthentication } = SimpleWebAuthnBrowser;

const add_device_btn = document.getElementById("add-device").addEventListener("click", biometric_login);

async function biometric_login() {
  
  const deviceName = document.getElementById("device-name");
  const name = deviceName.value
  if(name == ''){
    console.log("username vazio")
    return
  }
   // 1. Get challenge from server - options
  const initResponse = await fetch(`${SERVER_URL}/accounts/webauthn/registration`, {credentials: "include",})
  const options = await initResponse.json()
  if (!initResponse.ok) {showModalText(options.error)}

  // 2. Get passkey from device based on options
  const authJSON = await startAuthentication({ optionsJSON: options, })

  // 3. Send passkey to server for verification
  const verifyResponse = await fetch(
    `${SERVER_URL}/accounts/webauthn/registration`,
    {
      credentials: "include",
      method: "POST",
      headers: { "Content-Type": "application/json", 'X-CSRFToken': CSRF_TOKEN },
      body: JSON.stringify(authJSON),
    }
  )

  const verifyData = await verifyResponse.json()
  if (!verifyResponse.ok) {
    showModalText(verifyData.error)
  }
  if (verifyData.verified) {
    showModalText(`Successfully logged in ${email}`)
  } else {
    showModalText(`Failed to log in`)
  }
}
