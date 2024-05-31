from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random
import time
from .models import RoomMember
import json

from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def getToken(request):
    appId = "0012ffe2f9e64d45b0198de9f7cbfba8"
    appCertificate = "161e05bed5d44eb18695e4cf87596ea3"
    channelName = request.GET.get("channel")
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs
    )
    return JsonResponse({"token": token, "uid": uid}, safe=False)


def lobby(request):
    return render(request, "base/lobby.html")


def room(request):
    return render(request, "base/room.html")


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    return JsonResponse({"name": data["name"]}, safe=False)

def getMember(request):
    uid = request.GET.get("UID")
    room_name = request.GET.get("room_name")
    member = RoomMember.objects.get(uid=uid, room_name=room_name)
    name = member.name
    return JsonResponse({"name": name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    print("data: ",data)
    member = RoomMember.objects.get(
        name=data["name"], uid=data["UID"], room_name=data["room_name"]
    )
    if member:
        print("member: ",member)
        member.delete()
    return JsonResponse("Member was deleted!", safe=False)