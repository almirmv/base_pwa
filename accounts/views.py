import json
from http import HTTPStatus
from secrets import token_hex
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from accounts.models import WebAuthDevice
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from webauthn import (
    generate_registration_options,
    verify_registration_response,
    generate_authentication_options,
    options_to_json,
    base64url_to_bytes,
)
from webauthn.helpers.structs import (
    AttestationConveyancePreference,
    AuthenticatorAttachment,
    AuthenticatorSelectionCriteria,
    PublicKeyCredentialDescriptor,
    PublicKeyCredentialHint,
    ResidentKeyRequirement,
    UserVerificationRequirement,
    RegistrationCredential,

)
from django.contrib.auth import get_user_model
User = get_user_model()


#@login_required(login_url='login')
def signup(request):    
    return render(request, 'signup.html')

def register(request):    
    return render(request, 'register.html')


class DeviceListView(ListView, LoginRequiredMixin):
    model = WebAuthDevice
    template_name = 'device_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class DeleteDevice(DeleteView, LoginRequiredMixin):
    model = WebAuthDevice
    success_url = reverse_lazy("accounts:device_delete")

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class DeviceRegistration(LoginRequiredMixin, View):

    # GET - Generates the options for the registration
    def get(self, request, *args, **kwargs):
        display_name = request.user.get_full_name() or request.user.username
        challenge = token_hex() # gera numero randomico
        request.session["webauth_challenge"] = challenge
        
              
        options = generate_registration_options(    
            rp_name="armarioTec", # human readable name of your server intended only for display
            rp_id=settings.URL_CLOUD_SYSTEM, # the hostname (minus scheme and port) of the server running your Django app
            user_id=bytes(f'user:{request.user.id}','utf-8'),
            user_name=request.user.username,
            challenge=bytes(challenge,'utf-8'),
            # Require the user to verify their identity to the authenticator
            authenticator_selection=AuthenticatorSelectionCriteria(
                user_verification=UserVerificationRequirement.REQUIRED,
            ),
        )
  
        options_json = options_to_json(options)
        print(f"OPTIONS: {options_json}")
        return HttpResponse(options_json)
        '''
        return JsonResponse(
            {
                "publicKey": {
                    "rp": {
                        "id": settings.WEBAUTH_RP_ID,
                        "name": settings.WEBAUTH_RP_NAME,
                    },
                    "user": {
                        "id": hex_id,
                        "name": request.user.email,
                        "displayName": display_name,
                    },
                    "pubKeyCredParams": [
                        {
                            "type": "public-key",
                            "alg": -7,
                        },
                    ],
                    "attestation": "direct",
                    "timeout": 60000,
                    "challenge": challenge,
                },
            }
        )
        '''
    def post(self, request, *args, **kwargs):
        print(f'[POST]=============================================')
        challenge = bytes.fromhex(request.session.pop("webauth_challenge"))

        data = json.loads(request.body)
        name = data.get("name")
        pub_key_credential = json.dumps(data.get("pubKeyCredential"))

        verification = verify_registration_response(
            credential=RegistrationCredential.parse_raw(pub_key_credential),
            expected_challenge=challenge,
            expected_origin=settings.WEBAUTH_ORIGIN,
            expected_rp_id=settings.WEBAUTH_RP_ID,
            require_user_verification=False,
        )
        WebAuthDevice.objects.create(
            user=request.user,
            name=name,
            credential_id=verification.credential_id,
            public_key=verification.credential_public_key,
            format=verification.fmt,
            type=verification.credential_type,
            sign_count=verification.sign_count,
        )
        return HttpResponse(status=HTTPStatus.CREATED)





@login_required()
def register_init(request):
    print(f'[register_init]=============================================')
    logged_in_user_id = request.user.id
    options = generate_registration_options(    
        rp_name="armarioTec", # human readable name of your server intended only for display
        rp_id=settings.URL_CLOUD_SYSTEM, # the hostname (minus scheme and port) of the server running your Django app
        
        # An assigned random identifier
        # never anything user-identifying like an email address
        user_id=bytes([1, 2, 3, 3]),
        
        # A user-visible hint of which account this credential belongs to
        # An email address is fine here
        user_name=request.user.username,
        
        # Require the user to verify their identity to the authenticator
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.REQUIRED,
        ),
    )
  
    options_json = options_to_json(options) # return json.dumps
    # Remember the challenge for later, you'll need it in the next step
    request.session['options_reg_info'] = options_json

    #print(f"[OPTIONS_JSON]{options_json}")   
    return HttpResponse(options_json)


@csrf_exempt
def register_verify(request):
    '''Verify the registration data'''
    print(f'[register VERIFY]=============================================')
    if request.method != 'POST':
        print('[ERROR] Method not allowed')
        return HttpResponse(status=405)
    
    post_data_str = request.body.decode('utf-8')
    post_data = json.loads(post_data_str)
    print(f'POST DATA: {post_data}')
    # pegar de volta dados de registro para esse user
    reg_info =  json.loads(request.session['options_reg_info'])
    
    try:
        verification = verify_registration_response(
            credential=post_data,        
            expected_challenge=base64url_to_bytes(reg_info['challenge']),
            expected_origin=f"https://{settings.URL_CLOUD_SYSTEM}",
            expected_rp_id=settings.URL_CLOUD_SYSTEM,
        )
    except Exception as e:
        print(f'[ERROR]{e}')
        return HttpResponse(status=400, content={"verified": False, "msg": str(e), "status": 400})
    
    print(f'[REGISTRATION VERIFICATION]{verification}')
    if verification.user_verified:
        print("Deu certo! Dados verificados!")
        print(f'DADOS:\n {verification} ')
        #salvar novo tipo de acesso do usuario
        new_user_device = WebAuthDevice.objects.create(
            user = request.user,
            credential_id = verification.credential_id,
            public_key = verification.credential_public_key,
            sign_count = verification.sign_count,
            transport = post_data['response']['transports'],
            device_type = verification.credential_device_type,
            backed_up = verification.credential_backed_up,
        )
        new_user_device.save()
        return JsonResponse({ "verified": verification.user_verified})
    else:
        return HttpResponse(status=400, content={"verified": False, "msg": "Verification Failed!", "status": 400})


def auth_init(request):
    print(f'[AUTH INIT. GENERATE OPTIONS]====================================')
    if not request.GET.get('user'):
        print("cade o user??")
        return HttpResponse(status=400, content={"error": "Usuario requerido"})
    
    try:
        user = User.objects.get(username=request.GET.get('user'))
        print(f'[USER]{user.first_name}')
        credential = WebAuthDevice.objects.get(user=user.pk)
        print(f'[CREDENTIAL ID]{credential.credential_id}')
        
        # temos um user buscar credencial dele
        options = generate_authentication_options(
            rp_id = settings.URL_CLOUD_SYSTEM,
            allow_credentials = [
                {
                "id": credential.credential_id,
                "type": "public-key",
                "transports": credential.transport,
                },
            ]   
        )
    except Exception as e:
        return HttpResponse(status=400, content={f"error: {e}", "msg: usuario e/ou Biometria incorretos. Ja tem biometria?", "status: 400"} )
    
  
    options_json = options_to_json(options) # return json.dumps
    print(options_json)
    # Remember the challenge for later, you'll need it in the next step
    #request.session['options_reg_info'] = options_json

    #print(f"[OPTIONS_JSON]{options_json}")   
    return HttpResponse(options)


def auth_verify(request):
    return render(request, 'init_register.html')