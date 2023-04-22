from django.shortcuts import render
from .models import Property, Image, User
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
def index(request):
    apartments = Property.objects.all()
    for apartment in apartments:
        image = Image.objects.filter(property=apartment.id).first()
        apartment_data = apartment.__dict__

        apartment_data['image'] = image
    return render(request, 'index.html', {'apartments' : apartments})

def addproperty(request):
    return render(request, 'addprop.html')

# def search_results(request):

#     print("saaaaaaaaaaaaaa", numbers_json)
#     prop_list = []
#     for query in numbers_json:
#         print("thsisasssssssssssssssssssssss is", query)
#         if query != ',':
#             prop = Property.objects.get(id=query)
#             flat_dict = {}
#             image = Image.objects.filter(property=prop.id).first()


            # flat_dict['user_id'] = prop.__dict__['user_id']
            # flat_dict['rent'] = prop.__dict__['rent']
            # flat_dict['prop_name'] = prop.__dict__['prop_name']
            # flat_dict['location'] = prop.__dict__['location']
            # flat_dict['address'] = prop.__dict__['address']
            # flat_dict['desc'] = prop.__dict__['desc']
            # flat_dict['furnishing'] = prop.__dict__['furnishing']
            # flat_dict['image'] = image
            



#             prop_list.append(flat_dict)

#     print(prop_list)



def searchprop(request):
    # location_search = request.GET.get('location')
    # flat_category = request.GET.get('furnishing')
    # no_flat = request.GET.get('type')

    location_search = request.POST['location_search']
    flat_category = request.POST['flat_category']
    no_flat = request.POST['no_flat']

    if location_search == "":
        location_search = "Ahmedabad"
        props = Property.objects.all()
    else:
        props = Property.objects.filter(Q(location__icontains=location_search) & Q(furnishing__icontains=flat_category) & Q(prop_name__icontains=no_flat))
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
        flat_dict['image'] = image.image.url


        flat_dict['id'] = prop.__dict__['id']
        
        prop_id_lst.append(flat_dict)
    
        
    return JsonResponse({"message":"Success", "properties":prop_id_lst,"location":location_search, "furnishing":flat_category, "no_flat":no_flat})

    

def propdetails(request, id):
    property = Property.objects.get(id=id)
    images = Image.objects.filter(property=property)

    flat_details = {}
    flat_details['rent'] = property.__dict__['rent']
    flat_details['prop_name'] = property.__dict__['prop_name']
    flat_details['location'] = property.__dict__['location']
    flat_details['desc'] = [ amenity for amenity in property.__dict__['desc'].split(',') ]
    flat_details['furnishing'] = property.__dict__['furnishing']
    flat_details['image'] = [image.image.url for image in images]
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



    files = request.FILES.getlist('flat_pics')
    # currentTime = 

    try:

        user = User.objects.create(username=contact_name, phone=contact_no)

        prop = Property.objects.create(user=user,rent=rent,prop_name=flat_name,location=location,address="Ahmedabad", desc=amenities, furnishing=furnishing)
        prop.save()

        for file in files:
 
            print("prop saved")
            image_save = Image.objects.create(image=file, property=prop)
            image_save.save()

        return JsonResponse({"message":"Success"})

    except:
        return JsonResponse({"message":"Failure"})

    

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

    
