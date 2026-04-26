
const loginButton = document.querySelector("[data-loginBiometricsBtn]")
const usernameInput = document.querySelector("[data-username]")
const userFeedBack = document.querySelector("[data-userFeedBack]")

const { startAuthentication } = SimpleWebAuthnBrowser;

loginButton.addEventListener("click", biometric_login)

async function biometric_login() {

  const username = usernameInput.value

  // 1. Get challenge from server
  const initResponse = await fetch(`${SERVER_URL}/init-auth?user=${username}`, {credentials: "include",})
  const options = await initResponse.json()
  if (!initResponse.ok) {showModalText(options.error)}

  // 2. Get passkey
  const authJSON = await startAuthentication({ optionsJSON: options, })

  // 3. Verify passkey with DB
  const verifyResponse = await fetch(
    `${SERVER_URL}/verify-auth`,
    {
      credentials: "include",
      method: "POST",
      headers: { "Content-Type": "application/json", },
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

function showModalText(text) {
  modal.querySelector("[data-content]").innerText = text
  modal.showModal()
}