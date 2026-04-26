const signupButton = document.querySelector("[data-signup]")
const loginButton = document.querySelector("[data-loginBiometricsBtn]")
const usernameInput = document.querySelector("[data-username]")
const modal = document.querySelector("[data-modal]")
const closeButton = document.querySelector("[data-close]")
const userFeedBack = document.querySelector("[data-userFeedBack]")

const { startRegistration } = SimpleWebAuthnBrowser;

signupButton.addEventListener("click", signup)
loginButton.addEventListener("click", biometric_login)
closeButton.addEventListener("click", () => modal.close())


async function signup() {
  
  // 1.GET OPTIONS - challenge from server. 
  const initResponse = await fetch(`${SERVER_URL}${REGISTER_INIT_URL}`, {credentials: "include"})
  const options = await initResponse.json()
  console.log(options)
  userFeedBack.innerHTML = "RECEIVED OPTIONS " + JSON.stringify(options)
  if (!initResponse.ok) {showModalText(options.error)}

  // 2. Create passkey(especific to current device)
  console.log("creating passkey")
  userFeedBack.innerHTML += " CREATING PASSKEY. "
  const registrationJSON = await startRegistration(options)


  // 3. SEND PASSKEY TO SERVER(VERIFY AND SAVE)
  console.log("sending passkey to server")
  userFeedBack.innerHTML += " SENDING PASSKEY: " + JSON.stringify(registrationJSON)
  const verifyResponse = await fetch(
    `${SERVER_URL}${REGISTER_VERIFY_URL}`,
    {
      credentials: "include",
      method: "POST",
      headers: { "Content-Type": "application/json", },
      body: JSON.stringify(registrationJSON),
    }
  )

  //feedback to user
  const verifyData = await verifyResponse.json()
  userFeedBack.innerHTML += " SERVER VERIFICATION RESPONSE: " + JSON.stringify(verifyData)
  if (verifyData.verified) {
    showModalText(`Successfully registered `)
  } else {
    showModalText(`Failed to register`)
  }
}

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