from django.shortcuts import render
from .models import Property, Image, User, Otp
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
import boto3
import random
import datetime
from decouple import config

def index(request):

    apartments = Property.objects.all()
    all_properties = []
    for apartment in apartments:
        image = Image.objects.filter(property=apartment.id).first()
        flat_dict = {}

        flat_dict['id'] = apartment.__dict__['id']
        
        flat_dict['user_contact'] = User.objects.get(id=apartment.__dict__['user_id']).phone
        flat_dict['rent'] = apartment.__dict__['rent']
        flat_dict['prop_name'] = apartment.__dict__['prop_name']
        flat_dict['location'] = apartment.__dict__['location']
        flat_dict['address'] = apartment.__dict__['address']
        flat_dict['desc'] = apartment.__dict__['desc']
        flat_dict['furnishing'] = apartment.__dict__['furnishing']
        flat_dict['gender'] = apartment.__dict__['gender']
        try:
            flat_dict['image'] = image.image.url
        except:
            pass
        all_properties.append(flat_dict)

    return render(request, 'index.html', {'apartments' : all_properties})

def addproperty(request):
    return render(request, 'addprop.html')


def searchprop(request):

    location_search = request.POST['location_search']
    flat_category = request.POST['flat_category']
    no_flat = request.POST['no_flat']
    print("=====",location_search)
    print(flat_category)
    print(no_flat)
    
    if flat_category == "0":
        flat_category = ""
    if no_flat == "0":
        no_flat = ""

    props = Property.objects.all()


    if location_search != "":
        print("elif 33")

        props = props.filter(Q(location__icontains=location_search))

    if flat_category != "":
        print("elif 1")
        props = props.filter(Q(furnishing__icontains=flat_category))

    if no_flat != "":
        print("elif 2")

        props = props.filter(Q(prop_name__icontains=no_flat))
    
    
    # if location_search != "" and flat_category != "":
    #     print("elif 3")

    #     props = props.filter(Q(location__icontains=location_search) & Q(furnishing__icontains=flat_category))
    
    # if flat_category != "" and no_flat !="" :
    #     print("elif 4")

    #     props = props.filter(Q(furnishing__icontains=flat_category) & Q(prop_name__icontains=no_flat))

    # elif location_search != "" and no_flat !="" :
    #     print("elif 5")

    #     props = props.filter(Q(location__icontains=location_search) & Q(prop_name__icontains=no_flat))
    # if location_search == "":
    #     print("elif 6")

    #     location_search = "Ahmedabad"
    #     props = Property.objects.all()
        



    prop_id_lst = []
    for prop in props:
        flat_dict = {}
        image = Image.objects.filter(property=prop.id).first()

        flat_dict['id'] = prop.__dict__['id']
        
        flat_dict['user_id'] = prop.__dict__['user_id']
        flat_dict['rent'] = prop.__dict__['rent']
        flat_dict['prop_name'] = prop.__dict__['prop_name']
        flat_dict['location'] = prop.__dict__['location']
        flat_dict['address'] = prop.__dict__['address']
        flat_dict['desc'] = prop.__dict__['desc']
        flat_dict['furnishing'] = prop.__dict__['furnishing']
        try:
            flat_dict['image'] = image.image.url
        except:
            pass    
        prop_id_lst.append(flat_dict)
    
        
    return JsonResponse({"message":"Success", "properties":prop_id_lst,"location":location_search, "furnishing":flat_category, "no_flat":no_flat})

    

def propdetails(request, id):
    property = Property.objects.get(id=id)
    images = Image.objects.filter(property=property)

    flat_details = {}
    flat_details['rent'] = property.__dict__['rent']
    flat_details['prop_name'] = property.__dict__['prop_name']
    flat_details['location'] = property.__dict__['location']
    flat_details['amenities'] = [ amenity for amenity in property.__dict__['amenities'].split(',') ]
    flat_details['furnishing'] = property.__dict__['furnishing']
    flat_details['desc'] = property.__dict__['desc']


    flat_details['image'] = [image.image.url for image in images]

    flat_details['desc'] = property.__dict__['desc']
    flat_details['user_name'] = property.__dict__['desc']
    try:
        flat_details['user_contact'] = User.objects.get(id=property.__dict__['user_id']).phone
    except:
        pass

    print(flat_details['desc'])
    

    return render(request, 'propdetails.html', {'apartment':flat_details})

def submitprop(request):
    data = request.POST
    flat_name = request.POST['flat_name']
    location = request.POST['location']
    amenities = request.POST['amenities']
    contact_name = request.POST['contact_name']
    contact_no = request.POST['contact_no']
    rent = request.POST['rent']
    furnishing = request.POST['furnishing']
    desc = request.POST['desc']
    gender = request.POST['gender']
    otp = request.POST['otp']


    print("=====================",desc)

    files = request.FILES.getlist('flat_pics')

    # if checkotp(otp, contact_no):

    try:

        user = User.objects.create(username=contact_name, phone=contact_no)

        prop = Property.objects.create(user=user,rent=rent,prop_name=flat_name,location=location,address="Ahmedabad", amenities=amenities, furnishing=furnishing, desc=desc, gender=gender)
        prop.save()

        for file in files:

            print("prop saved")
            image_save = Image.objects.create(image=file, property=prop)
            image_save.save()

        return JsonResponse({"message":"Success"})

    except:
        return JsonResponse({"message":"Failure"})
    # else:
    #     return JsonResponse({"message":"Invalid OTP or OTP expired"})


    

    # flat_name = request.POST['flat_name']
    # location = request.POST['location']
    # amenities = request.POST['amenities']
    # contact_name = request.POST['contact_name']
    # contact_no = request.POST['contact_no']

    # flat_pics = request.POST['flat_pics']


    # # flat_pics = request.FILES.get('flat_pics')
    # print("====================",type(flat_pics))
    # for pic in flat_pics:

    #     print("============",flat_pics)

    # prop = Property.objects.create(prop_name=flat_name,location=location,address=address,desc=amenities)
    # image_save = Image.objects.create(image=flat_pics, property=prop)
    # print(image_save)

def checkotp(otp, phone):
    otp_obj = Otp.objects.get(phone=phone)
    user_otp = otp_obj.otp
    timestamp_otp = str(otp_obj.timestamp)
    current_time = datetime.datetime.utcnow()

    new_ts_otp = datetime.datetime.strptime(timestamp_otp[:-6], '%Y-%m-%d %H:%M:%S.%f')

    print("time new stamp",new_ts_otp)
    print("sasaaaaaaaaa",current_time)


    print(otp)
    if user_otp == otp:
        if (new_ts_otp - current_time).total_seconds() < 600 :
            return True
        else:
            return False
    else:
        return False
    
def about(request):
    return render(request, 'about.html')

client = boto3.client('sns', region_name='ap-northeast-1', aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
         aws_secret_access_key= config('AWS_SECRET_ACCESS_KEY'))



def donate(request):
    return render(request, 'donate.html')

def working(request):
    return render(request, 'working.html')


def sendotp(request):

    contact_no = "+91"+request.POST['contact_no']
    print("contact dw", contact_no)
    otp = random.randrange(1000, 9999)
    try:
        otp_obj = Otp.objects.get(phone=request.POST['contact_no'])
        otp_obj.otp = otp
        otp_obj.timestamp = datetime.datetime.utcnow()
        otp_obj.save()

        message = "Hello your otp to add your flat is " + str(otp) + " - flatesmate.com"
        
        try:
            response = client.publish(
            PhoneNumber=contact_no,
            Message=message,
            Subject='OTP',
            MessageStructure='string3',
        
            MessageDeduplicationId='string7',
            MessageGroupId='string8'
            )
            
            return JsonResponse({"message":"Success"})
        except Exception as e:
            print(str("-=================",str(e)))
            return JsonResponse({"message":"failed"})
    except:
        otp = Otp.objects.create(phone=request.POST['contact_no'], otp=otp, timestamp = datetime.datetime.utcnow())
        otp.save()
        return JsonResponse({"message":"Success"})







# def sendmessage():
#     response = client.publish(
#     PhoneNumber='+918856911982',
#     Message='string1',
#     Subject='string2',
#     MessageStructure='string3',
   
#     MessageDeduplicationId='string7',
#     MessageGroupId='string8'
# )
    
    # return JsonResponse({"message":"success"})